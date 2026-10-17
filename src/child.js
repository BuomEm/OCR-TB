import { createEngine } from './engine.js';
import { serializeError } from './result.js';

let engine;
let busy = false;
let stopping = false;
const send = (message) => { if (process.connected) process.send(message); };
async function shutdown() {
  if (stopping) return;
  stopping = true;
  try { await engine?.close(); } finally { process.exit(0); }
}
process.on('SIGTERM', shutdown);
process.on('disconnect', shutdown);
process.on('message', async (message) => {
  if (!message || typeof message !== 'object') return;
  if (message.type === 'shutdown') { await shutdown(); return; }
  if (busy || stopping) return;
  busy = true;
  try {
    if (message.type === 'init') {
      if (engine) throw new Error('Worker already initialized');
      engine = await createEngine();
      send({ type: 'ready', id: message.id, initMs: engine.initMs });
    } else if (message.type === 'recognize') {
      if (!engine || typeof message.file !== 'string') throw new Error('Invalid recognition request');
      const result = await engine.recognize(message.file, message.config, message.debugDir);
      send({ type: 'result', id: message.id, result });
    }
  } catch (error) {
    send({ type: 'fatal', id: message.id, error: serializeError(error, 'CHILD_FATAL') });
    await shutdown();
  } finally { busy = false; }
});
