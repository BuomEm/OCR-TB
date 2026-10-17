import test from 'node:test';
import assert from 'node:assert/strict';
import sharp from 'sharp';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { prepareImage, renderVariant, detectBorder, outputSize } from '../src/preprocess.js';

test('border detector requires all four connected outer edges and a safe image size', () => {
  const w = 30, h = 20, pixels = Buffer.alloc(w * h, 255);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (!x || !y || x === w - 1 || y === h - 1) pixels[y * w + x] = 0;
  }
  assert.equal(detectBorder(pixels, w, h).borderDetected, true);
  pixels[0] = 255;
  assert.equal(detectBorder(pixels, w, h).borderDetected, false);
  assert.equal(detectBorder(Buffer.alloc(9), 3, 3).borderDetected, false);
  assert.equal(detectBorder(Buffer.alloc(600, 255), w, h).borderDetected, false);
});
test('output dimensions include padding and constrain large inputs', () => {
  assert.deepEqual(outputSize(198, 48, 4), { width: 792, height: 192 });
  const r = outputSize(5000, 4000, 4);
  assert.ok(r.width + 32 <= 3000); assert.ok((r.width + 32) * (r.height + 32) <= 10_000_000);
});
test('sample border is detected; V0 preserves it and V1 removes exactly one pixel', async () => {
  const image = await prepareImage(new URL('../samples/01.jpg', import.meta.url));
  assert.equal(image.width, 200); assert.equal(image.height, 50);
  assert.equal(image.preprocessing.borderDetected, true);
  assert.equal(image.preprocessing.borderRemovedPx, 1);
  const v0 = await renderVariant(image, { variant: 'V0' });
  const v1 = await renderVariant(image, { variant: 'V1' });
  assert.equal((await sharp(v0).metadata()).width, 232);
  assert.equal((await sharp(v1).metadata()).width, 824);
  assert.equal((await sharp(v1).metadata()).height, 224);
});
test('transparent pixels flatten to white and EXIF orientation applies before dimensions', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-preprocess-'));
  try {
    const transparent = join(dir, 'alpha.png');
    await sharp({ create: { width: 30, height: 20, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } } }).png().toFile(transparent);
    const image = await prepareImage(transparent);
    assert.equal(image.preprocessing.borderDetected, false);
    const pixels = await sharp(image.buffer).raw().toBuffer();
    assert.ok(pixels.every((p) => p === 255));
    const oriented = join(dir, 'rotate.jpg');
    await sharp({ create: { width: 30, height: 20, channels: 3, background: 'white' } }).withMetadata({ orientation: 6 }).jpeg().toFile(oriented);
    const rotated = await prepareImage(oriented);
    assert.equal(rotated.width, 20); assert.equal(rotated.height, 30);
    const corrupt = join(dir, 'broken.png'); await writeFile(corrupt, 'invalid');
    await assert.rejects(prepareImage(corrupt));
  } finally { await rm(dir, { recursive: true, force: true }); }
});
