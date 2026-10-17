import { createRequire } from 'node:module';
import { mkdir, copyFile, readFile, readdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { ASSET_DIR } from '../src/config.js';
import { sha256 } from '../src/assets.js';
import sharp from 'sharp';

// Setup only: copy installed npm resources; this script never downloads anything.
const require = createRequire(import.meta.url);
const coreDir = dirname(require.resolve('tesseract.js-core/package.json'));
const model = require('@tesseract.js-data/eng');
await mkdir(join(ASSET_DIR, 'core'), { recursive: true });
const files = [];
async function copy(source, destination) {
  await copyFile(source, join(ASSET_DIR, destination));
  files.push({ path: destination, sha256: sha256(await readFile(join(ASSET_DIR, destination))) });
}
await copy(join(model.langPath, 'eng.traineddata.gz'), 'eng.traineddata.gz');
for (const name of (await readdir(coreDir)).sort()) {
  if (/^tesseract-core.*\.(?:js|wasm)$/.test(name)) await copy(join(coreDir, name), `core/${name}`);
}
await copy(join(coreDir, 'LICENSE'), 'core/LICENSE');
const versions = { tesseract: require('tesseract.js/package.json').version,
  core: require('tesseract.js-core/package.json').version, model: require('@tesseract.js-data/eng/package.json').version,
  sharp: sharp.versions.sharp };
await writeFile(join(ASSET_DIR, 'manifest.json'), JSON.stringify({ versions, files }, null, 2) + '\n');
console.log(`Prepared ${files.length} local resources in ${ASSET_DIR}`);
