// Opt-in experiments only. Never used by the default voting pipeline.
export function otsuThreshold(pixels) {
  const histogram = new Uint32Array(256);
  for (const p of pixels) histogram[p]++;
  let total = 0;
  for (let i = 0; i < 256; i++) total += i * histogram[i];
  let count = 0, sum = 0, best = -1, threshold = 128;
  for (let i = 0; i < 255; i++) {
    count += histogram[i]; sum += i * histogram[i];
    const other = pixels.length - count;
    if (!count || !other) continue;
    const difference = sum / count - (total - sum) / other;
    const variance = count * other * difference * difference;
    if (variance > best) { best = variance; threshold = i + 1; }
  }
  return threshold;
}

export function removeThinLine(source, width, height) {
  const pixels = Buffer.from(source);
  let best = { count: 0, slope: 0, intercept: 0 };
  // Bounded slope search for long near-horizontal interference, not glyph strokes.
  for (let step = -4; step <= 4; step++) {
    const slope = step / 10;
    const offset = Math.ceil(Math.abs(slope) * width);
    const votes = new Uint32Array(height + offset * 2 + 2);
    for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
      if (source[y * width + x] <= 64) votes[Math.round(y - slope * x) + offset]++;
    }
    for (let i = 0; i < votes.length; i++) {
      const intercept = i - offset, end = intercept + slope * (width - 1);
      if (intercept < 0 || intercept >= height || end < 0 || end >= height) continue;
      if (votes[i] > best.count) best = { count: votes[i], slope, intercept };
    }
  }
  if (best.count / width < .6) return { pixels, detected: false };
  for (let x = 0; x < width; x++) {
    const center = Math.round(best.intercept + best.slope * x);
    for (let y = Math.max(0, center - 1); y <= Math.min(height - 1, center + 1); y++) {
      if (source[y * width + x] > 64) continue;
      let verticalDark = 0;
      for (let dy = -2; dy <= 2; dy++) if (y + dy >= 0 && y + dy < height && source[(y + dy) * width + x] <= 64) verticalDark++;
      if (verticalDark < 3) pixels[y * width + x] = 255;
    }
  }
  return { pixels, detected: true, slope: best.slope, intercept: best.intercept, support: best.count / width };
}
