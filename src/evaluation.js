// Ground truth is intentionally confined to this module and metrics.js.
import { readFile, writeFile, mkdir, realpath, stat, mkdtemp, rename, rm } from 'node:fs/promises';
import { resolve, dirname, join } from 'node:path';
import { createRequire } from 'node:module';
import sharp from 'sharp';
import { sha256, verifyAssets } from './assets.js';
import { OCR_CONFIG } from './config.js';
import { OcrSupervisor, runBatch } from './supervisor.js';
import { evaluateMetrics, levenshtein } from './metrics.js';
import { readImageBytes } from './input.js';
import { serializeError } from './result.js';

export async function loadDataset(manifestPath, { signal } = {}) {
  const manifestFile = resolve(manifestPath);
  const entries = JSON.parse(await readFile(manifestFile, 'utf8'));
  if (!Array.isArray(entries) || !entries.length) throw new Error('Dataset must be a nonempty array');
  const seen = new Set();
  const rows = [];
  for (const entry of entries) {
    if (typeof entry.file !== 'string' || !entry.file || typeof entry.expected !== 'string' || !entry.expected.length) throw new Error('Every label requires file and nonempty expected text');
    const file = resolve(dirname(manifestFile), entry.file);
    if (seen.has(file)) throw new Error(`Duplicate dataset file: ${file}`);
    seen.add(file);
    let checksum = null;
    let inputError = null;
    try { checksum = sha256(await readImageBytes(file, { signal })); }
    catch (error) {
      if (signal?.aborted) throw Object.assign(new Error('Interrupted during dataset verification'), { code: 'ABORTED' });
      inputError = serializeError(error, 'INPUT_ERROR');
    }
    if (checksum && entry.sha256 && checksum !== entry.sha256) throw new Error(`Dataset checksum mismatch: ${entry.file}`);
    rows.push({ id: entry.id ?? String(rows.length + 1), file, expected: entry.expected, sha256: checksum,
      checksumVerified: Boolean(checksum && entry.sha256), inputError });
  }
  return rows;
}

async function protectReportOutput(target, inputs) {
  const canonicalTarget = join(await realpath(dirname(target)), 'analysis.json');
  let targetInfo;
  try { targetInfo = await stat(target); } catch (error) { if (error.code !== 'ENOENT') throw error; }
  for (const input of inputs) {
    let canonicalInput, info;
    try { canonicalInput = await realpath(input); info = await stat(input); }
    catch (error) { if (!['ENOENT', 'EACCES', 'ENOTDIR', 'ELOOP'].includes(error.code)) throw error; }
    if (resolve(input) === resolve(target) || canonicalInput === canonicalTarget
      || (info && targetInfo && info.dev === targetInfo.dev && info.ino === targetInfo.ino)) {
      throw new Error(`Report output collides with an input: ${input}`);
    }
  }
}

function experimentRuns(experiment) {
  if (experiment === 'none') return [{ id: 'default', config: {} }];
  if (experiment === 'raw') return [{ id: 'raw', config: { variants: ['V0'] } }];
  if (experiment === 'border') return [0, 1, 2].map((borderPx) => ({ id: `border-${borderPx}`, config: { variants: ['V2'], borderPx } }));
  if (experiment === 'psm') return [7, 8, 13].flatMap((psm) => ['V1', 'V2', 'V3'].map((variant) => ({ id: `psm-${psm}-${variant}`, config: { variants: [variant], psm } })));
  if (experiment === 'scale') return [3, 4, 5].map((scale) => ({ id: `scale-${scale}`, config: { variants: ['V2'], scale } }));
  if (experiment === 'otsu') return [{ id: 'otsu', config: { variants: ['V3'], threshold: 'otsu' } }];
  if (experiment === 'lines') return [{ id: 'lines', config: { variants: ['V2'], removeLines: true } }];
  throw new Error(`Unknown experiment: ${experiment}`);
}

function perVariantMetrics(rows, initMs) {
  const ids = [...new Set(rows.flatMap((r) => r.result.candidates.map((c) => c.variant)))];
  const metrics = {};
  for (const variant of ids) {
    metrics[variant] = evaluateMetrics(rows.map((row) => {
      const candidate = row.result.candidates.find((c) => c.variant === variant);
      return { expected: row.expected, result: { text: candidate?.text ?? '',
        status: candidate?.error || !candidate ? 'error' : 'needs_review', durationMs: candidate?.durationMs ?? 0 } };
    }), initMs);
  }
  const baseline = metrics.V0?.exactMatchOverall;
  for (const value of Object.values(metrics)) value.exactMatchDeltaVsV0 = baseline === undefined ? null : value.exactMatchOverall - baseline;
  return metrics;
}

export async function evaluateDataset(manifest, { outputDir, experiment = 'none', debugDir, signal } = {}) {
  const dataset = await loadDataset(manifest, { signal });
  await mkdir(outputDir, { recursive: true });
  const target = join(outputDir, 'analysis.json');
  const inputs = [manifest, ...dataset.map((entry) => entry.file)];
  await protectReportOutput(target, inputs);
  const assets = await verifyAssets();
  const require = createRequire(import.meta.url);
  const runs = [];
  for (const run of experimentRuns(experiment)) {
    const supervisor = new OcrSupervisor();
    // Labels, expected text and checksums never cross the recognition boundary.
    const results = await runBatch(dataset.map((entry) => entry.file), {
      supervisor, config: run.config, signal,
      debugDir: debugDir ? join(debugDir, run.id) : undefined,
    });
    const rows = dataset.map((entry, i) => ({ ...entry, result: results[i],
      exactMatch: results[i].status !== 'error' && results[i].text === entry.expected,
      editDistance: levenshtein(entry.expected, results[i].status === 'error' ? '' : results[i].text) }));
    const initMs = supervisor.initTimings.reduce((sum, item) => sum + item.workerInitMs, 0);
    runs.push({ id: run.id, config: { ...OCR_CONFIG, ...run.config },
      initializations: supervisor.initTimings, rows,
      metrics: evaluateMetrics(rows, initMs), perVariant: perVariantMetrics(rows, initMs) });
  }
  const report = { schemaVersion: 4, createdAt: new Date().toISOString(), experiment,
    environment: { node: process.version, platform: process.platform, arch: process.arch,
      tesseract: require('tesseract.js/package.json').version, core: require('tesseract.js-core/package.json').version,
      sharp: sharp.versions.sharp, vips: sharp.versions.vips },
    resources: assets, limitations: ['Three original samples are a feasibility set, not generalization evidence.',
      'Confidence and agreement are not calibrated probabilities.'],
    runs, ...(runs.length === 1 ? { rows: runs[0].rows, metrics: runs[0].metrics, perVariant: runs[0].perVariant } : {}) };
  await protectReportOutput(target, inputs);
  // Atomic replacement avoids following an existing symlink or truncating a report.
  const temporary = await mkdtemp(join(outputDir, '.ocr-tb-report-'));
  try {
    await writeFile(join(temporary, 'analysis.json'), JSON.stringify(report, null, 2) + '\n', { flag: 'wx' });
    await rename(join(temporary, 'analysis.json'), target);
  } finally { await rm(temporary, { recursive: true, force: true }); }
  return report;
}
