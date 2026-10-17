import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { spawnSync } from 'node:child_process';
import { mkdtemp, mkdir, writeFile, readFile, copyFile, rm, open, link, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';
import { discoverFiles, parseArguments } from '../src/cli.js';
import { loadDataset } from '../src/evaluation.js';

const cli = fileURLToPath(new URL('../bin/ocr-tb.js', import.meta.url));
async function run(args, options = {}) {
  // File descriptors also work in sandbox hosts that cannot relay child pipes.
  const dir = await mkdtemp(join(tmpdir(), 'ocr-cli-output-'));
  const stdout = await open(join(dir, 'stdout'), 'w');
  const stderr = await open(join(dir, 'stderr'), 'w');
  try {
    const { launch = [process.execPath, cli], deadlineMs = 55000, ...spawnOptions } = options;
    const code = await new Promise((resolve, reject) => {
      const child = spawn(launch[0], [...launch.slice(1), ...args], { ...spawnOptions, stdio: ['ignore', stdout.fd, stderr.fd] });
      const timer = setTimeout(() => child.kill('SIGKILL'), deadlineMs);
      child.on('error', reject); child.on('close', (code) => { clearTimeout(timer); resolve(code); });
    });
    return { code, stdout: await readFile(join(dir, 'stdout'), 'utf8'), stderr: await readFile(join(dir, 'stderr'), 'utf8') };
  } finally { await stdout.close(); await stderr.close(); await rm(dir, { recursive: true, force: true }); }
}
test('CLI validates unknown flags and duplicate options', () => {
  assert.throws(() => parseArguments(['recognize', 'x', '--unknown']));
  assert.throws(() => parseArguments(['recognize', 'x', '--format', 'csv']));
  assert.throws(() => parseArguments(['recognize', 'x', '--format', 'json', '--format', 'text']));
  assert.equal(parseArguments(['recognize', 'x', '--format', 'json']).format, 'json');
});
test('discovery is sorted, one level, with explicit empty-directory error', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-discover-'));
  try {
    await assert.rejects(discoverFiles(dir), /no.*image/i);
    for (const f of ['b.PNG', 'a.jpg', 'skip.txt']) await writeFile(join(dir, f), 'x');
    await mkdir(join(dir, 'nested')); await writeFile(join(dir, 'nested', 'c.jpg'), 'x');
    assert.deepEqual((await discoverFiles(dir)).map((f) => f.slice(dir.length + 1)), ['a.jpg', 'b.PNG']);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('evaluation rejects tampered sample mapping before OCR', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-labels-'));
  try {
    await writeFile(join(dir, 'a.png'), 'changed');
    await writeFile(join(dir, 'labels.json'), JSON.stringify([{ file: 'a.png', expected: 'ab', sha256: '0'.repeat(64) }]));
    await assert.rejects(loadDataset(join(dir, 'labels.json')), /checksum/i);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('doctor runs from another working directory with clean JSON', { timeout: 60000 }, async () => {
  const r = await run(['doctor', '--format', 'json'], { cwd: tmpdir() });
  assert.equal(r.code, 0, r.stderr); assert.equal(JSON.parse(r.stdout).status, 'ok');
});
test('real batch keeps corrupt image result and handles Vietnamese spaced path', { timeout: 60000 }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr ảnh mẫu '));
  try {
    await copyFile(new URL('../samples/01.jpg', import.meta.url), join(dir, '01 ảnh.jpg'));
    await writeFile(join(dir, '02 broken.png'), 'broken');
    const r = await run(['recognize', dir, '--format', 'json']);
    assert.equal(r.code, 1, r.stderr);
    const results = JSON.parse(r.stdout); assert.equal(results.length, 2);
    assert.notEqual(results[0].status, 'error'); assert.equal(results[1].status, 'error');
    assert.equal(results[0].candidates.length, 4);
    assert.ok(!r.stdout.includes('loading'));
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('evaluation produces analysis with all rows and CER metrics', { timeout: 60000 }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-analysis-'));
  try {
    const manifest = fileURLToPath(new URL('../samples/labels.json', import.meta.url));
    const r = await run(['evaluate', manifest, '--output-dir', dir, '--format', 'json']);
    assert.ok([0, 2].includes(r.code), r.stderr);
    const analysis = JSON.parse(await readFile(join(dir, 'analysis.json'), 'utf8'));
    assert.equal(analysis.rows.length, 3); assert.equal(typeof analysis.metrics.cerOverall, 'number');
    assert.equal(analysis.rows[0].expected, '3h8a'); assert.ok(analysis.perVariant.V0);
    assert.equal(analysis.metrics.latencyP95Ms, null);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('real recognize works with kernel-denied Internet sockets', { timeout: 60000, skip: process.platform !== 'linux' }, async () => {
  const launcher = fileURLToPath(new URL('../scripts/offline-linux.py', import.meta.url));
  const sample = fileURLToPath(new URL('../samples/01.jpg', import.meta.url));
  const r = await run(['recognize', sample, '--format', 'json'], { launch: ['python3', launcher, process.execPath, cli], cwd: tmpdir() });
  assert.ok([0, 2].includes(r.code), r.stderr);
  assert.ok(r.stderr.includes('Verified AF_INET/AF_INET6 denied'));
  assert.equal(JSON.parse(r.stdout)[0].candidates.length, 4);
});
test('debug output cannot overwrite an input matching a debug filename', { timeout: 60000 }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-debug-collision-'));
  try {
    await mkdir(join(dir, '0001'));
    const source = join(dir, '0001', 'V0.png');
    await copyFile(new URL('../samples/01.jpg', import.meta.url), source);
    const before = await readFile(source);
    const r = await run(['recognize', source, '--debug-dir', dir, '--format', 'json']);
    assert.ok(before.equals(await readFile(source)), 'debug must preserve the original bytes');
    assert.notEqual(JSON.parse(r.stdout)[0].status, 'error');
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('invalid dataset images remain per-image operational errors in analysis', { timeout: 60000 }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-invalid-eval-'));
  try {
    await mkdir(join(dir, 'directory.png'));
    await writeFile(join(dir, 'labels.json'), JSON.stringify([
      { file: 'directory.png', expected: 'abcd' }, { file: 'missing.jpg', expected: 'abcd' }
    ]));
    const r = await run(['evaluate', join(dir, 'labels.json'), '--output-dir', join(dir, 'report')]);
    assert.equal(r.code, 1);
    const report = JSON.parse(await readFile(join(dir, 'report', 'analysis.json'), 'utf8'));
    assert.equal(report.rows.length, 2); assert.ok(report.rows.every((r) => r.result.status === 'error'));
    assert.equal(report.metrics.cerValidOnly, null); assert.equal(report.metrics.cerOverall, 1);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('evaluation never opens a FIFO image before the child input validation', { timeout: 10000, skip: process.platform !== 'linux' }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-fifo-'));
  try {
    assert.equal(spawnSync('mkfifo', [join(dir, 'fifo.png')]).status, 0);
    await writeFile(join(dir, 'labels.json'), JSON.stringify([{ file: 'fifo.png', expected: 'abcd' }]));
    const moduleUrl = new URL('../src/evaluation.js', import.meta.url).href;
    const r = await run([join(dir, 'labels.json')], { deadlineMs: 4000,
      launch: [process.execPath, '--input-type=module', '-e',
        `import {loadDataset} from ${JSON.stringify(moduleUrl)}; console.log(JSON.stringify(await loadDataset(process.argv[1])));`] });
    assert.equal(r.code, 0, 'FIFO verification should finish without waiting for an OCR worker or being killed');
    assert.equal(JSON.parse(r.stdout)[0].inputError.code, 'INVALID_INPUT');
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('evaluation refuses to overwrite a manifest named analysis.json', { timeout: 60000 }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-report-collision-'));
  try {
    await copyFile(new URL('../samples/01.jpg', import.meta.url), join(dir, 'image.jpg'));
    const manifest = join(dir, 'analysis.json');
    const labels = JSON.stringify([{ file: 'image.jpg', expected: '3h8a' }]);
    await writeFile(manifest, labels);
    const r = await run(['evaluate', manifest, '--output-dir', dir]);
    assert.equal(await readFile(manifest, 'utf8'), labels, 'manifest must remain unchanged');
    assert.equal(r.code, 1);
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('oversized images are not read for checksum and remain evaluation errors', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-large-'));
  try {
    const file = await open(join(dir, 'large.png'), 'w');
    await file.truncate(11 * 1024 * 1024); await file.close();
    await writeFile(join(dir, 'labels.json'), JSON.stringify([{ file: 'large.png', expected: 'abcd' }]));
    const rows = await loadDataset(join(dir, 'labels.json'));
    assert.equal(rows[0].sha256, null); assert.equal(rows[0].inputError.code, 'INPUT_TOO_LARGE');
  } finally { await rm(dir, { recursive: true, force: true }); }
});
test('report collision protection follows symlinks and hardlinks to the manifest', { timeout: 60000, skip: process.platform === 'win32' }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'ocr-linked-report-'));
  try {
    await copyFile(new URL('../samples/01.jpg', import.meta.url), join(dir, 'image.jpg'));
    const manifest = join(dir, 'labels.json');
    const content = JSON.stringify([{ file: 'image.jpg', expected: '3h8a' }]);
    await writeFile(manifest, content);
    for (const create of [link, symlink]) {
      const out = await mkdtemp(join(dir, 'out-'));
      await create(manifest, join(out, 'analysis.json'));
      const r = await run(['evaluate', manifest, '--output-dir', out]);
      assert.equal(r.code, 1); assert.equal(await readFile(manifest, 'utf8'), content);
    }
  } finally { await rm(dir, { recursive: true, force: true }); }
});
