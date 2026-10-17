import { fileURLToPath } from 'node:url';
import { join } from 'node:path';
import { evaluateDataset } from '../src/evaluation.js';
import { ROOT } from '../src/config.js';

const manifest = fileURLToPath(new URL('../samples/labels.json', import.meta.url));
let errors = false;
for (const [experiment, directory] of [['raw', 'baseline-a'], ['none', 'default'], ['border', 'border'],
  ['psm', 'psm'], ['scale', 'scale'], ['otsu', 'otsu'], ['lines', 'lines']]) {
  const report = await evaluateDataset(manifest, { experiment, outputDir: join(ROOT, 'reports', directory) });
  for (const run of report.runs) {
    console.log(`${directory}/${run.id}: exact=${run.metrics.exactMatchOverall}, CER=${run.metrics.cerOverall}`);
    if (run.rows.some((row) => row.result.status === 'error')) errors = true;
  }
}
// A benchmark records recognition misses; an operational failure fails the run.
process.exitCode = errors ? 1 : 0;
