import { constants } from 'node:fs';
import { open, stat } from 'node:fs/promises';
import { LIMITS } from './config.js';

function validate(info) {
  if (!info.isFile()) throw Object.assign(new Error('Input must be a regular file'), { code: 'INVALID_INPUT' });
  if (info.size > LIMITS.bytes) throw Object.assign(new Error('Input exceeds 10 MiB'), { code: 'INPUT_TOO_LARGE' });
}

export async function readImageBytes(file, { signal } = {}) {
  // Check before opening (FIFO), then again on the actual descriptor (path race).
  validate(await stat(file));
  const handle = await open(file, constants.O_RDONLY | (constants.O_NONBLOCK ?? 0));
  try {
    validate(await handle.stat());
    const deadline = AbortSignal.timeout(30000);
    const stream = handle.createReadStream({ start: 0, end: LIMITS.bytes, autoClose: false,
      signal: signal ? AbortSignal.any([signal, deadline]) : deadline });
    const chunks = [];
    let length = 0;
    for await (const chunk of stream) {
      length += chunk.length;
      if (length > LIMITS.bytes) throw Object.assign(new Error('Input exceeds 10 MiB'), { code: 'INPUT_TOO_LARGE' });
      chunks.push(chunk);
    }
    return Buffer.concat(chunks, length);
  } finally { await handle.close(); }
}
