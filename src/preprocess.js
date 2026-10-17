import sharp from 'sharp';
import { LIMITS } from './config.js';
import { otsuThreshold, removeThinLine } from './experiments.js';
import { readImageBytes } from './input.js';

export function detectBorder(gray, width, height) {
  let detected = false;
  if (width >= 8 && height >= 8) {
    const dark = (x, y) => gray[y * width + x] <= 32;
    let top = 0, bottom = 0, left = 0, right = 0;
    for (let x = 0; x < width; x++) { top += dark(x, 0); bottom += dark(x, height - 1); }
    for (let y = 0; y < height; y++) { left += dark(0, y); right += dark(width - 1, y); }
    detected = top / width >= .98 && bottom / width >= .98 && left / height >= .98 && right / height >= .98
      && dark(0, 0) && dark(width - 1, 0) && dark(0, height - 1) && dark(width - 1, height - 1);
  }
  return { borderDetected: detected, borderRemovedPx: detected ? 1 : 0, borderDetectionMethod: 'dark-edge-ratio' };
}

export function outputSize(width, height, scale) {
  const available = LIMITS.longEdge - LIMITS.padding * 2;
  const factor = Math.min(scale, available / Math.max(width, height));
  let w = Math.max(1, Math.floor(width * factor));
  let h = Math.max(1, Math.floor(height * factor));
  while ((w + 32) * (h + 32) > LIMITS.outputPixels) { w--; h--; }
  return { width: w, height: h };
}

export async function prepareImage(file) {
  const source = await readImageBytes(file);
  const decoder = sharp(source, { limitInputPixels: LIMITS.inputPixels, animated: false, failOn: 'warning' });
  const metadata = await decoder.metadata();
  if (!['jpeg', 'png', 'webp'].includes(metadata.format)) throw new Error('Supported input formats: JPG, PNG, WebP');
  if ((metadata.pages ?? 1) > 1) throw new Error('Animated/multipage input is unsupported');
  const { data: buffer, info: normalized } = await decoder.rotate().flatten({ background: '#fff' }).removeAlpha().png().toBuffer({ resolveWithObject: true });
  const gray = await sharp(buffer).greyscale().raw().toBuffer();
  return { buffer, width: normalized.width, height: normalized.height,
    preprocessing: detectBorder(gray, normalized.width, normalized.height) };
}

export async function renderVariant(image, options = {}) {
  const { variant = 'V2', borderPx, scale, threshold } = options;
  const crop = borderPx === undefined ? (variant === 'V0' ? 0 : image.preprocessing.borderRemovedPx)
    : image.preprocessing.borderDetected ? borderPx : 0;
  if (![0, 1, 2].includes(crop) || image.width - crop * 2 < 4 || image.height - crop * 2 < 4) throw new Error('Unsafe border crop');
  let pipeline = sharp(image.buffer);
  if (crop) pipeline = pipeline.extract({ left: crop, top: crop, width: image.width - crop * 2, height: image.height - crop * 2 });
  if (variant === 'V2' || variant === 'V3') pipeline = pipeline.greyscale().normalise();
  const size = outputSize(image.width - crop * 2, image.height - crop * 2, scale ?? (variant === 'V0' ? 1 : 4));
  // Separate stages keep grayscale/normalise before resizing, threshold after it.
  let buffer = await pipeline.png().toBuffer();
  if (options.removeLines) {
    const { data, info } = await sharp(buffer).greyscale().raw().toBuffer({ resolveWithObject: true });
    const processed = removeThinLine(data, info.width, info.height);
    buffer = await sharp(processed.pixels, { raw: { width: info.width, height: info.height, channels: 1 } }).png().toBuffer();
  }
  pipeline = sharp(buffer).resize(size.width, size.height);
  buffer = await pipeline.png().toBuffer();
  if (variant === 'V3') {
    const value = threshold === 'otsu' ? otsuThreshold(await sharp(buffer).greyscale().raw().toBuffer()) : threshold ?? 160;
    buffer = await sharp(buffer).threshold(value).png().toBuffer();
  }
  return sharp(buffer).extend({ top: 16, bottom: 16, left: 16, right: 16, background: '#fff' }).png().toBuffer();
}
