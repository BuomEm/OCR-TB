import { parseArgs } from 'node:util';
import { stat, readdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { OcrSupervisor, runBatch } from './supervisor.js';
import { evaluateDataset } from './evaluation.js';
import { verifyAssets } from './assets.js';
import { exitCode, serializeError } from './result.js';

export const HELP = `OCR-TB — offline short-text OCR
Usage:
  ocr-tb doctor [--format json|text]
  ocr-tb recognize <image|directory> [--format json|text] [--debug-dir path]
  ocr-tb evaluate <labels.json> [--output-dir path] [--format json|text]
                  [--experiment raw|border|psm|scale|otsu|lines] [--debug-dir path]
Exit: 0 all ok; 2 review/unrecognized or evaluation mismatch; 1 operational error.
`;

export function parseArguments(args) {
  const parsed = parseArgs({ args, allowPositionals: true, options: {
    format: { type: 'string' }, 'debug-dir': { type: 'string' }, 'output-dir': { type: 'string' },
    experiment: { type: 'string' }, help: { type: 'boolean', short: 'h' },
  }, tokens: true });
  if (parsed.values.help || !args.length) return { help: true };
  const counts = new Set();
  for (const token of parsed.tokens.filter((t) => t.kind === 'option')) {
    if (counts.has(token.name)) throw new Error(`Duplicate option --${token.name}`);
    counts.add(token.name);
  }
  const [command, input] = parsed.positionals;
  if (!['doctor', 'recognize', 'evaluate'].includes(command)) throw new Error('Expected doctor, recognize or evaluate command');
  if (parsed.positionals.length !== (command === 'doctor' ? 1 : 2)) throw new Error('Incorrect number of input paths');
  const format = parsed.values.format ?? 'text';
  if (!['text', 'json'].includes(format)) throw new Error('Format must be text or json');
  if (command !== 'evaluate' && (parsed.values['output-dir'] || parsed.values.experiment)) throw new Error('Output directory and experiment require evaluate command');
  if (command === 'doctor' && parsed.values['debug-dir']) throw new Error('Doctor does not create debug images');
  const experiment = parsed.values.experiment ?? 'none';
  if (!['none', 'raw', 'border', 'psm', 'scale', 'otsu', 'lines'].includes(experiment)) throw new Error('Unknown experiment');
  return { command, input, format, experiment, debugDir: parsed.values['debug-dir'] ? resolve(parsed.values['debug-dir']) : undefined,
    outputDir: resolve(parsed.values['output-dir'] ?? 'reports/latest') };
}

export async function discoverFiles(input) {
  const path = resolve(input);
  const info = await stat(path);
  if (info.isFile()) {
    if (!/\.(jpe?g|png|webp)$/i.test(path)) throw new Error('Supported image extensions: JPG, PNG, WebP');
    return [path];
  }
  if (!info.isDirectory()) throw new Error('Input must be a file or directory');
  const files = (await readdir(path, { withFileTypes: true })).filter((entry) => entry.isFile() && /\.(jpe?g|png|webp)$/i.test(entry.name))
    .map((entry) => resolve(path, entry.name)).sort();
  if (!files.length) throw new Error('No supported images found in directory');
  return files;
}

export async function runCli(args) {
  let options;
  try {
    options = parseArguments(args);
    if (options.help) { process.stdout.write(HELP); return 0; }
    const controller = new AbortController();
    const interrupt = () => controller.abort();
    process.once('SIGINT', interrupt);
    process.once('SIGTERM', interrupt);
    try {
      if (options.command === 'doctor') {
        const resources = await verifyAssets();
        const supervisor = new OcrSupervisor();
        const cancel = () => supervisor.cancel();
        controller.signal.addEventListener('abort', cancel, { once: true });
        try {
          await supervisor.start();
          const result = { status: 'ok', offline: true, versions: resources.versions,
            resourcesVerified: resources.files.length, initializations: supervisor.initTimings };
          process.stdout.write(options.format === 'json' ? JSON.stringify(result, null, 2) + '\n' : `OK: local model, JS/WASM, Sharp and worker (${resources.files.length} resources verified)\n`);
        } finally { controller.signal.removeEventListener('abort', cancel); await supervisor.close(); }
        return controller.signal.aborted ? 130 : 0;
      }
      if (options.command === 'recognize') {
        const files = await discoverFiles(options.input);
        const results = await runBatch(files, { debugDir: options.debugDir, signal: controller.signal });
        process.stdout.write(options.format === 'json' ? JSON.stringify(results, null, 2) + '\n'
          : results.map((r) => files.length === 1 ? r.text : `${r.file}\t${r.text}`).join('\n') + '\n');
        for (const r of results) if (r.status !== 'ok') process.stderr.write(`${r.file}: ${r.status}${r.error ? ` (${r.error.code}: ${r.error.message})` : ` (${r.reviewReasons.join(', ')})`}\n`);
        return controller.signal.aborted ? 130 : exitCode(results);
      }
      const report = await evaluateDataset(options.input, { ...options, signal: controller.signal });
      process.stdout.write(options.format === 'json' ? JSON.stringify(report, null, 2) + '\n' : report.runs.map((run) =>
        `${run.id}: exact=${run.metrics.exactMatchOverall}, CER valid=${run.metrics.cerValidOnly}, CER overall=${run.metrics.cerOverall}`).join('\n') + `\nReport: ${options.outputDir}/analysis.json\n`);
      const results = report.runs.flatMap((run) => run.rows.map((r) => r.result));
      if (controller.signal.aborted) return 130;
      if (results.some((r) => r.status === 'error')) return 1;
      if (report.runs.some((run) => run.rows.some((r) => !r.exactMatch))) return 2;
      return exitCode(results);
    } finally { process.removeListener('SIGINT', interrupt); process.removeListener('SIGTERM', interrupt); }
  } catch (error) {
    if (options?.format === 'json') process.stdout.write(JSON.stringify({ status: 'error', error: serializeError(error) }, null, 2) + '\n');
    process.stderr.write(`ocr-tb: ${error.message}\n`);
    return error.code === 'ABORTED' ? 130 : 1;
  }
}
