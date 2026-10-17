# Verification — 2026-10-17

- `npm test`: 36 passed, 0 failed, 0 skipped.
- `npm run lint`: passed.
- `npm run check`: 26 JavaScript files passed syntax checking.
- Python offline helper syntax parsed successfully.
- `npm audit --audit-level=high`: 0 vulnerabilities.
- `python3 scripts/offline-linux.py node bin/ocr-tb.js doctor --format json`:
  exit 0; model, native Sharp, worker and 20 resources verified.
- `python3 scripts/offline-linux.py node scripts/benchmark.js`: exit 0;
  full A/B/C/D and opt-in experiments completed with IPv4/IPv6 socket creation
  denied for the process and descendants. Recognition outputs/metrics reproduced.
- Original sample SHA-256 values match `samples/labels.json`.

The suite includes real worker reuse; child hang/crash/init timeout and confirmed
exit recovery; abort; clean JSON from another working directory; invalid image
results; FIFO and oversized evaluation inputs; debug/report collision protection,
including manifest symlink/hardlink aliases; input bounds/alpha/EXIF; selection
ties; and CER with operational errors or rates above 100%.

Independent review found two Important issues. Both were reproduced by failing
regressions, fixed, and verified by the full suite: output could overwrite input;
evaluation preflight could hang/read unbounded or discard invalid image rows.

Remaining minor limitations: parse-time argument errors are stderr-only despite
`--format json`; no dedicated test for OS refusal to confirm child exit or for a
missing inventory entry. Missing/corrupt assets and ordinary forced exit are tested.
Windows runtime recovery and host-wide resource release were not verified.

Accuracy conclusions are limited to the three original images. See
[measured outputs and metrics](README.md).
