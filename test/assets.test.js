import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { verifyAssets } from '../src/assets.js';

test('asset verification rejects missing and modified resources', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-assets-'));
  try {
    await assert.rejects(verifyAssets(dir), /asset|manifest/i);
    await writeFile(join(dir, 'manifest.json'), JSON.stringify({ files: [{ path: 'model', sha256: '0'.repeat(64) }] }));
    await writeFile(join(dir, 'model'), 'tampered');
    await assert.rejects(verifyAssets(dir), /checksum|resource/i);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('prepared asset inventory includes model and every selected core build', async () => {
  const r = await verifyAssets();
  assert.ok(r.files.some((f) => f.path === 'eng.traineddata.gz'));
  assert.ok(r.files.some((f) => f.path === 'core/tesseract-core-simd-lstm.wasm'));
  assert.ok(r.files.some((f) => f.path === 'core/tesseract-core-relaxedsimd-lstm.wasm.js'));
  const manifest = JSON.parse(await readFile(new URL('../assets/manifest.json', import.meta.url), 'utf8'));
  assert.equal(manifest.versions.tesseract, '7.0.0'); assert.equal(manifest.versions.core, '7.0.0');
});
