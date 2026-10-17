import { createRequire } from 'node:module';
import { join } from 'node:path';
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import Tesseract from 'tesseract.js';
import { ASSET_DIR, OCR_CONFIG } from './config.js';
import { verifyAssets } from './assets.js';
import { prepareImage, renderVariant } from './preprocess.js';
import { selectCandidates } from './selection.js';
import { serializeError, errorResult } from './result.js';

export async function createEngine() {
  const started = performance.now();
  await verifyAssets();
  sharp.concurrency(1);
  // Forces native decoder loading as part of doctor/initialization.
  await sharp({ create: { width: 1, height: 1, channels: 3, background: '#fff' } }).png().toBuffer();
  const require = createRequire(import.meta.url);
  const worker = await Tesseract.createWorker('eng', Tesseract.OEM.LSTM_ONLY, {
    workerPath: require.resolve('tesseract.js/src/worker-script/node/index.js'),
    corePath: join(ASSET_DIR, 'core'), langPath: ASSET_DIR,
    gzip: true, cacheMethod: 'none', logger: () => {},
    errorHandler: () => {},
  }, OCR_CONFIG.init);
  try {
    await worker.setParameters({ tessedit_char_whitelist: OCR_CONFIG.whitelist,
      tessedit_pageseg_mode: '7', user_defined_dpi: '300' });
  } catch (error) { await worker.terminate(); throw error; }
  return {
    initMs: performance.now() - started,
    async recognize(input, config = {}, debugDir) {
      const file = input instanceof URL ? fileURLToPath(input) : input;
      const start = performance.now();
      try {
        const image = await prepareImage(file);
        const variants = config.variants ?? OCR_CONFIG.variants;
        if (!variants.length || variants.some((v) => !OCR_CONFIG.variants.includes(v))) throw new Error('Invalid OCR variants');
        const psm = config.psm ?? OCR_CONFIG.psm;
        if (![7, 8, 13].includes(psm)) throw new Error('Supported PSM: 7, 8, 13');
        await worker.setParameters({ tessedit_pageseg_mode: String(psm) });
        if (debugDir) {
          await mkdir(debugDir, { recursive: true });
          await writeFile(join(debugDir, 'normalized.png'), image.buffer, { flag: 'wx' });
        }
        const candidates = [];
        for (const variant of variants) {
          const variantStart = performance.now();
          try {
            const buffer = await renderVariant(image, { ...config, variant });
            if (debugDir) await writeFile(join(debugDir, `${variant}.png`), buffer, { flag: 'wx' });
            const { data } = await worker.recognize(buffer);
            candidates.push({ variant, text: data.text, confidence: data.confidence,
              durationMs: performance.now() - variantStart, error: null });
          } catch (error) {
            candidates.push({ variant, text: '', confidence: null,
              durationMs: performance.now() - variantStart, error: serializeError(error, 'VARIANT_ERROR') });
          }
        }
        const result = { file, ...selectCandidates(candidates),
          preprocessing: { ...image.preprocessing,
            borderRemovedPx: image.preprocessing.borderDetected
              ? config.borderPx ?? (variants.every((v) => v === 'V0') ? 0 : image.preprocessing.borderRemovedPx) : 0 },
          durationMs: performance.now() - start };
        if (debugDir) await writeFile(join(debugDir, 'result.json'), JSON.stringify(result, null, 2) + '\n', { flag: 'wx' });
        return result;
      } catch (error) { return errorResult(file, error, performance.now() - start); }
    },
    close: () => worker.terminate(),
  };
}
