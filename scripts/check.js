import { readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT } from '../src/config.js';

let count = 0;
for (const directory of ['src', 'bin', 'scripts', 'test', 'test/fixtures']) {
  for (const name of await readdir(join(ROOT, directory))) {
    if (!name.endsWith('.js')) continue;
    const checked = spawnSync(process.execPath, ['--check', join(ROOT, directory, name)], { stdio: 'inherit' });
    if (checked.error || checked.status !== 0) process.exit(1);
    count++;
  }
}
console.log(`Syntax checked ${count} JavaScript files`);
