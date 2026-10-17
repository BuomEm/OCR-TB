import { fork } from 'node:child_process';
import { mkdir, mkdtemp } from 'node:fs/promises';
import { join } from 'node:path';
import { errorResult } from './result.js';

const failure = (code, message) => Object.assign(new Error(message), { code });

export class OcrSupervisor {
  constructor(options = {}) {
    this.options = { childPath: new URL('./child.js', import.meta.url), childArgs: [],
      initTimeoutMs: 60000, jobTimeoutMs: 30000, gracefulMs: 2000, forceMs: 5000, ...options };
    this.child = null;
    this.pending = null;
    this.sequence = 0;
    this.initTimings = [];
    this.closed = false;
    this.aborted = false;
    this.blocked = null;
  }

  request(type, payload, timeoutMs, timeoutCode) {
    if (this.pending) throw failure('BUSY', 'Only one OCR request can run at a time');
    const child = this.child;
    return new Promise((resolve, reject) => {
      const id = String(++this.sequence);
      const finish = (error, result) => {
        if (this.pending?.id !== id) return;
        clearTimeout(timer);
        this.pending = null;
        if (error) reject(error); else resolve(result);
      };
      const timer = setTimeout(() => finish(failure(timeoutCode, `${type} exceeded ${timeoutMs} ms`)), timeoutMs);
      this.pending = { id, type, finish };
      try { child.send({ type, id, ...payload }, (error) => { if (error) finish(error); }); }
      catch (error) { finish(error); }
    });
  }

  async start() {
    if (this.blocked) throw this.blocked;
    if (this.closed || this.aborted) throw failure('ABORTED', 'OCR supervisor stopped');
    if (this.child) return;
    // Never inherit test runner/eval flags; preserve explicit preloads for offline tests.
    const child = fork(this.options.childPath, this.options.childArgs, {
      shell: false, serialization: 'json', stdio: ['ignore', 'ignore', 'pipe', 'ipc'],
      execArgv: this.options.execArgv ?? [],
    });
    this.child = child;
    child.stderr?.on('data', (data) => process.stderr.write(data));
    this.exitPromise = new Promise((resolve) => {
      child.once('exit', (code, signal) => {
        if (this.child === child) this.child = null;
        this.pending?.finish(failure('CHILD_EXIT', `OCR child exited (code ${code}, signal ${signal})`));
        resolve();
      });
      child.on('error', (error) => {
        this.pending?.finish(error);
        if (!child.pid) { if (this.child === child) this.child = null; resolve(); }
      });
    });
    child.on('message', (message) => {
      const pending = this.pending;
      if (!pending || !message || message.id !== pending.id) return;
      if (message.type === 'fatal') pending.finish(failure(message.error?.code ?? 'CHILD_FATAL', message.error?.message ?? 'OCR child failed'));
      else if (pending.type === 'init' && message.type === 'ready') pending.finish(null, message);
      else if (pending.type === 'recognize' && message.type === 'result') pending.finish(null, message.result);
    });
    try {
      const start = performance.now();
      const ready = await this.request('init', {}, this.options.initTimeoutMs, 'INIT_TIMEOUT');
      this.initTimings.push({ durationMs: performance.now() - start, workerInitMs: ready.initMs });
    } catch (error) { await this.terminate(); throw error; }
  }

  async recognize(file, config = {}, debugDir) {
    await this.start();
    const started = performance.now();
    try {
      const result = await this.request('recognize', { file: String(file), config, debugDir }, this.options.jobTimeoutMs, 'IMAGE_TIMEOUT');
      if (!result || !['ok', 'needs_review', 'unrecognized', 'error'].includes(result.status)) throw failure('INVALID_IPC', 'Invalid OCR result');
      return { ...result, file: String(file), durationMs: performance.now() - started };
    } catch (error) { await this.terminate(); throw error; }
  }

  cancel() {
    this.aborted = true;
    this.pending?.finish(failure('ABORTED', 'Interrupted by user'));
  }

  async terminate() {
    if (this.stopping) return this.stopping;
    const child = this.child;
    if (!child) return;
    const exited = this.exitPromise;
    const waitForExit = async (ms) => {
      let timer;
      const stopped = await Promise.race([exited.then(() => true), new Promise((resolve) => { timer = setTimeout(() => resolve(false), ms); })]);
      clearTimeout(timer);
      return stopped;
    };
    this.stopping = (async () => {
      if (child.connected) { try { child.send({ type: 'shutdown' }, () => {}); } catch { /* escalate below */ } }
      if (await waitForExit(this.options.gracefulMs)) return;
      try { child.kill('SIGKILL'); } catch { /* require actual exit, not a signal return value */ }
      if (!await waitForExit(this.options.forceMs)) {
        this.blocked = failure('CHILD_NOT_REAPED', 'Unable to confirm OCR child exit; batch halted');
        // A blocked OS process must not keep the main process alive indefinitely.
        child.disconnect?.(); child.stderr?.destroy(); child.unref();
        throw this.blocked;
      }
    })();
    try { await this.stopping; } finally { this.stopping = null; }
  }

  async close() {
    this.closed = true;
    this.pending?.finish(failure('ABORTED', 'OCR supervisor closed'));
    await this.terminate();
  }
}

export async function runBatch(files, { supervisor = new OcrSupervisor(), config = {}, debugDir, signal, onResult } = {}) {
  const results = [];
  let debugRunDir;
  const cancel = () => supervisor.cancel();
  signal?.addEventListener('abort', cancel, { once: true });
  if (signal?.aborted) cancel();
  try {
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const start = performance.now();
      let result;
      try {
        if (signal?.aborted) throw failure('ABORTED', 'Not scheduled: interrupted by user');
        if (debugDir && !debugRunDir) {
          await mkdir(debugDir, { recursive: true });
          debugRunDir = await mkdtemp(join(debugDir, 'run-'));
        }
        result = await supervisor.recognize(file, config, debugRunDir ? join(debugRunDir, String(i + 1).padStart(4, '0')) : undefined);
      } catch (error) { result = errorResult(file, error, performance.now() - start); }
      results.push(result);
      onResult?.(result, i);
    }
  } finally {
    signal?.removeEventListener('abort', cancel);
    await supervisor.close();
  }
  return results;
}
