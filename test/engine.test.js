import test from 'node:test';
import assert from 'node:assert/strict';
import { createEngine } from '../src/engine.js';

test('real local OCR initializes and reuses worker without ground truth', { timeout: 60000 }, async () => {
  const engine = await createEngine();
  try {
    const config = { variants: ['V0'] };
    const result = await engine.recognize(new URL('../samples/01.jpg', import.meta.url), config);
    assert.equal(result.candidates.length, 1);
    assert.equal(result.candidates[0].variant, 'V0');
    assert.equal(typeof result.candidates[0].text, 'string');
    const second = await engine.recognize(new URL('../samples/02.jpg', import.meta.url), config);
    assert.notEqual(second.status, 'error');
    assert.ok(engine.initMs > 0);
  } finally { await engine.close(); }
});
