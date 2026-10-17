import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { dirname, join, resolve, sep } from 'node:path';
import { ASSET_DIR } from './config.js';

export const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
export async function verifyAssets(directory = ASSET_DIR) {
  let manifest;
  try { manifest = JSON.parse(await readFile(join(directory, 'manifest.json'), 'utf8')); }
  catch (cause) { throw new Error('Local asset manifest missing/invalid. Run npm run prepare:assets.', { cause }); }
  if (!Array.isArray(manifest.files) || !manifest.files.length) throw new Error('Invalid asset inventory');
  for (const entry of manifest.files) {
    const path = resolve(directory, entry.path);
    if (!path.startsWith(resolve(directory) + sep)) throw new Error('Invalid resource path');
    let bytes;
    try { bytes = await readFile(path); }
    catch (cause) { throw new Error(`Missing local resource: ${entry.path}`, { cause }); }
    if (sha256(bytes) !== entry.sha256) throw new Error(`Resource checksum mismatch: ${entry.path}`);
  }
  const required = ['eng.traineddata.gz'];
  for (const build of ['tesseract-core', 'tesseract-core-lstm', 'tesseract-core-simd', 'tesseract-core-simd-lstm', 'tesseract-core-relaxedsimd', 'tesseract-core-relaxedsimd-lstm']) {
    required.push(`core/${build}.wasm`, `core/${build}.wasm.js`);
  }
  for (const file of required) if (!manifest.files.some((entry) => entry.path === file)) throw new Error(`Missing asset inventory entry: ${file}`);
  const require = createRequire(import.meta.url);
  const tesseract = require('tesseract.js/package.json').version;
  const core = require('tesseract.js-core/package.json').version;
  if (tesseract !== '7.0.0' || core !== '7.0.0' || manifest.versions?.tesseract !== tesseract || manifest.versions?.core !== core) {
    throw new Error('Tesseract.js/core assets must match pinned version 7.0.0');
  }
  // Node's upstream adapter resolves core from node_modules, ignoring corePath.
  const coreDirectory = dirname(require.resolve('tesseract.js-core/package.json'));
  for (const entry of manifest.files.filter((f) => f.path.startsWith('core/'))) {
    if (sha256(await readFile(join(coreDirectory, entry.path.slice(5)))) !== entry.sha256) {
      throw new Error(`Installed core checksum mismatch: ${entry.path}`);
    }
  }
  return manifest;
}
