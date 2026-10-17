import test from 'node:test';
import assert from 'node:assert/strict';
import sharp from 'sharp';
import { otsuThreshold, removeThinLine } from '../src/experiments.js';
import { prepareImage, renderVariant } from '../src/preprocess.js';

test('Otsu separates two distinct grayscale classes without erasing dark pixels', () => {
  const t = otsuThreshold(Buffer.from([0, 0, 0, 255, 255]));
  assert.equal(t, 1);
  assert.ok(0 < t && 255 >= t);
});
test('experimental line removal preserves thick intersections and leaves source intact', () => {
  const w = 80, h = 30;
  const source = Buffer.alloc(w * h, 255);
  for (let x = 0; x < w; x++) source[15 * w + x] = 0;
  for (let y = 7; y < 24; y++) for (let x = 35; x < 41; x++) source[y * w + x] = 0;
  const r = removeThinLine(source, w, h);
  assert.equal(r.detected, true); assert.equal(r.pixels[15 * w + 3], 255);
  assert.equal(r.pixels[15 * w + 37], 0); assert.equal(source[15 * w + 3], 0);
  assert.equal(removeThinLine(Buffer.alloc(w * h, 255), w, h).detected, false);
});
test('Otsu and line experiments produce bounded images without modifying default', async () => {
  const image = await prepareImage(new URL('../samples/01.jpg', import.meta.url));
  const original = Buffer.from(image.buffer);
  for (const config of [{ variant: 'V3', threshold: 'otsu' }, { variant: 'V2', removeLines: true }]) {
    const output = await renderVariant(image, config);
    const meta = await sharp(output).metadata();
    assert.equal(meta.width, 824); assert.equal(meta.height, 224);
  }
  assert.ok(image.buffer.equals(original));
});
