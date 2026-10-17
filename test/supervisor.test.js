import test from 'node:test';
import assert from 'node:assert/strict';
import { OcrSupervisor, runBatch } from '../src/supervisor.js';

const options = { childPath: new URL('./fixtures/child.js', import.meta.url), jobTimeoutMs: 120,
  initTimeoutMs: 2000, gracefulMs: 50, forceMs: 1000 };
test('reuses one child and confirms its exit on close', async () => {
  const supervisor = new OcrSupervisor(options);
  const first = await supervisor.recognize('first');
  const second = await supervisor.recognize('second');
  assert.equal(first.pid, second.pid);
  await supervisor.close();
  assert.throws(() => process.kill(first.pid, 0), { code: 'ESRCH' });
});
test('timeout kills stuck child before next image gets a new process', async () => {
  const supervisor = new OcrSupervisor(options);
  try {
    const first = await supervisor.recognize('first');
    await assert.rejects(supervisor.recognize('hang'), { code: 'IMAGE_TIMEOUT' });
    assert.throws(() => process.kill(first.pid, 0), { code: 'ESRCH' });
    const next = await supervisor.recognize('next');
    assert.notEqual(first.pid, next.pid);
  } finally { await supervisor.close(); }
});
test('batch retains one result per image across crash and recovery', async () => {
  const supervisor = new OcrSupervisor(options);
  const results = await runBatch(['first', 'crash', 'last'], { supervisor });
  assert.deepEqual(results.map((r) => r.status), ['ok', 'error', 'ok']);
  assert.equal(results[1].file, 'crash');
  assert.notEqual(results[0].pid, results[2].pid);
});
test('initialization deadline terminates child and leaves no process behind', async () => {
  const supervisor = new OcrSupervisor({ ...options, childArgs: ['hang-init'], initTimeoutMs: 120 });
  await assert.rejects(supervisor.start(), { code: 'INIT_TIMEOUT' });
  assert.equal(supervisor.child, null);
  await supervisor.close();
});
test('abort stops current job and marks unscheduled jobs without hanging', async () => {
  const supervisor = new OcrSupervisor(options);
  await supervisor.start();
  const controller = new AbortController();
  setTimeout(() => controller.abort(), 30);
  const results = await runBatch(['hang', 'later'], { supervisor, signal: controller.signal });
  assert.equal(results.length, 2); assert.ok(results.every((r) => r.status === 'error'));
  assert.equal(results[1].error.code, 'ABORTED');
  assert.equal(supervisor.child, null);
});
