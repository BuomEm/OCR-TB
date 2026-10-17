# OCR-TB CLI v4

Offline JavaScript CLI for short alphanumeric images. Node.js 24+, Sharp,
Tesseract.js/core 7.0.0. No API keys, runtime model downloads or Internet fallback.

## Install and run

The installation step needs npm access; asset preparation only copies installed
resources and requires no additional download:

```bash
npm ci
npm run prepare:assets
node bin/ocr-tb.js doctor
node bin/ocr-tb.js recognize samples/01.jpg
node bin/ocr-tb.js recognize samples --format json
node bin/ocr-tb.js recognize samples/01.jpg --debug-dir debug/one
```

After preparation, keep the project with `node_modules` and `assets` together.
Paths to model/core/worker resources resolve from the package, so commands also
work from another current directory. Native dependencies must match the target
OS/architecture; install them on that platform before going offline.

`doctor` verifies model/core checksums, the pinned core version, native Sharp and
initialization of a real OCR worker. Upstream Tesseract's Node adapter resolves
core from `node_modules` rather than `corePath`; both copies are checked.

## Commands and output

```bash
node bin/ocr-tb.js --help
node bin/ocr-tb.js doctor --format json
node bin/ocr-tb.js evaluate samples/labels.json --output-dir reports/default
node bin/ocr-tb.js evaluate samples/labels.json --experiment border --output-dir reports/border
npm run benchmark:all
```

`recognize` accepts one JPG/PNG/WebP or a directory (one level, filename order).
Limits: 10 MiB and 20 million input pixels, 3,000 px longest output edge and
10 million output pixels including padding. Animated/multipage input is rejected.
Original files are never modified. Debug output is opt-in and contains normalized
images, each variant and JSON; each batch uses a fresh `run-*` directory with
numbered job subdirectories and exclusive file creation.

JSON recognition output is always an array, including for a single image. Every
discovered image has a result, even when decoding or OCR fails. Result fields:
`file`, `text`, `status`, `confidence`, `votes`, `candidates`, `reviewReasons`,
`preprocessing`, `durationMs`, `error`. Confidence may be `null`; error is either
`null` or `{code,message}`. Fatal command errors after parsing use one JSON error
object. Known limitation: argument parsing errors are stderr-only, even when
`--format json` was requested.
Text output prints one recognized string, or `path<TAB>text` for a batch.
Progress/warnings/errors go to stderr; stdout contains only results.

Exit codes: `0` all results accepted; `2` review required/unrecognized (or an
evaluation mismatch); `1` operational/argument error; `130` interrupted. A code
`2` with valid JSON is expected on these difficult images.

## Recognition policy

EXIF orientation is applied and transparency flattened onto white. The outer
frame is detected using grayscale ≤32, ≥98% dark pixels on each edge, dark
corners, and a minimum 8×8 image. Exactly one pixel is removed for V1–V3 when
detected. V0 retains the original frame. No unconditional trim or repeated crop.

| Variant | Processing before 16 px white padding |
|---|---|
| V0 | Normalized original, no upscale |
| V1 | Remove detected frame, upscale 4× |
| V2 | As V1, grayscale + normalize before resize |
| V3 | As V2, threshold 160 after resize |

Upscaling is reduced when needed to honor output limits. PSM 7, LSTM-only,
English model; whitelist A–Z/a–z/0–9. Word/frequency DAWGs are disabled at init.
Only whitespace is removed from returned text. There is no forced length,
case conversion, label-informed correction or default line removal.

Exact text groups rank by votes, highest confidence, then V2 → V3 → V1 → V0.
Ties, one-vote winners, missing confidence, confidence below 80 or any failed
variant require review. Confidence and agreement are **not probabilities**.

## Evaluation and experiments

`samples/labels.json` records user-supplied ground truth and SHA-256 checksums
for the untouched original JPG bytes. A custom manifest is a nonempty array:

```json
[{ "file": "image.jpg", "expected": "3h8a", "sha256": "optional SHA-256" }]
```

Paths resolve relative to the manifest. Supplied checksums must match before
benchmarking. Checksum reads are bounded to 10 MiB, only open regular files and
support cancellation. Invalid/missing images remain operational errors in the evaluation.
Reports refuse to overwrite input images or the manifest, including link aliases.
Labels are only read by evaluation and never sent to recognition or selection.

`analysis.json` includes per-image/candidate outputs, resource checksums,
runtime versions, worker initialization timings and metrics. CER valid excludes
operational errors; CER overall treats operational errors as empty predictions.
Unrecognized images remain in both metrics. CER can exceed 100%. Undefined
denominators are `null`; p50/p95 require at least 20 samples. Auto-accept coverage
uses all images as denominator; auto-accept accuracy uses only `status=ok` images.

Experiments are isolated from default votes:

| `--experiment` | Controlled comparison |
|---|---|
| `raw` | V0 baseline A |
| `border` | V2 with frame crop 0/1/2 px (only if frame detected) |
| `psm` | V1/V2/V3 individually with PSM 7/8/13 |
| `scale` | V2 at scale 3×/4×/5× |
| `otsu` | V3 with Otsu threshold instead of 160 |
| `lines` | V2 with experimental long thin line removal |

The line experiment searches slopes −0.4…0.4 with ≥60% support and preserves
thick vertical intersections. It can remove glyph strokes and is not a default.
`benchmark:all` runs baseline A, default B, border C, then PSM D and remaining
experiments in order. No winning configuration is promoted automatically.

## Reliability and verification

The main process schedules one job at a time in a child process. IPC carries
JSON paths/config/results, never image Buffers. One Tesseract worker is reused.
Initialization has a 60s deadline; each image has 30s. On timeout/fatal error,
request graceful shutdown, wait 2s, force termination, then wait up to 5s for
actual process exit before replacement. Unconfirmed exit halts the batch.
Ctrl+C stops new jobs and returns an error result for unfinished images.

```bash
npm test
npm run lint
npm run check
python3 scripts/offline-linux.py node bin/ocr-tb.js doctor
python3 scripts/offline-linux.py node bin/ocr-tb.js recognize samples --format json
```

The optional offline verification helper requires Linux, Python 3 and libseccomp;
it denies IPv4/IPv6 socket creation for the command and descendants, verifies
denial, and leaves host networking unchanged. Linux integration tests include it.
Windows recovery behavior has not been tested; do not infer OS-wide resource
release merely from a successful signal send.

See [benchmark report](reports/README.md) for the measured three-sample results.
The tool's operational stability and recognition accuracy are separate outcomes.
