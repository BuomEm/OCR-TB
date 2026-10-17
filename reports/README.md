# Phase 1 — three-image feasibility benchmark

Ground truth was supplied by the user. SHA-256 mapping was verified against the
original JPG files; no reconstructed PNG or label-informed correction was used.

Environment: Node.js 24.19.0, Linux x64, Sharp 0.35.5/libvips 8.18.7,
Tesseract.js/core 7.0.0, local English data package 1.0.0 (`4.0.0`).
Exact resource hashes and timings are in each `analysis.json`.

## Baselines A and B

`∅` means no characters returned. These are measured outputs, not expected text:

| Image | Ground truth | V0 raw | V1 | V2 | V3 | Default selection |
|---|---|---|---|---|---|---|
| 01.jpg | `3h8a` | ∅ | ∅ | ∅ | `3h8a` | `3h8a` |
| 02.jpg | `3akp` | ∅ | `A3akp` | `A3akp` | `A3akp` | `A3akp` |
| 03.jpg | `ehxe` | `Retxe` | ∅ | ∅ | `ehxe` | `ehxe` |

| Configuration | Exact match | CER valid | CER overall | Operational errors |
|---|---:|---:|---:|---:|
| V0 raw | 0/3 | 83.33% | 83.33% | 0/3 |
| V1 | 0/3 | 75% | 75% | 0/3 |
| V2 | 0/3 | 75% | 75% | 0/3 |
| V3 | 2/3 | 8.33% | 8.33% | 0/3 |
| Default vote selection | 2/3 | 8.33% | 8.33% | 0/3 |

All default predictions are `needs_review`. Confidences are 0, 0 and 8;
auto-accept coverage is 0%, and auto-accept accuracy is `null`. Even the three
agreeing variants on image 02 return an incorrect extra `A`. No automatic prefix
deletion or four-character truncation is applied.

Evidence: [raw baseline](baseline-a/analysis.json), [default and each variant](default/analysis.json).

## Controlled experiments C and D

V2 border ablation at 0/1/2 px gave 0/3 exact matches and 75% CER for each
condition. This experiment does not establish that border removal improves OCR.

PSM 7 with V3 reproduced 2/3 exact matches, 8.33% CER. PSM 8 and 13 with
V1/V2/V3 each returned `3n8a`, `p3akp`, `Hehxe`: 0/3 exact matches, 25% CER.
PSM alternatives are not automatically promoted.

Evidence: [border ablation](border/analysis.json), [PSM comparison](psm/analysis.json).

## Additional opt-in experiments

| Experiment | Exact match | CER overall |
|---|---:|---:|
| V2 scale 3× | 1/3 | 41.67% |
| V2 scale 4× | 0/3 | 75% |
| V2 scale 5× | 1/3 | 66.67% |
| Otsu | 0/3 | 100% |
| Thin-line removal | 0/3 | 75% |

Evidence: [scale](scale/analysis.json), [Otsu](otsu/analysis.json), [lines](lines/analysis.json).

## Interpretation and reproduction

The default pipeline improved this feasibility set from 0/3 to 2/3. The remaining
error is an extra character on image 02; automatic acceptance is not supported by
these measured confidences. More labeled images held apart from tuning are
required before claiming general accuracy or changing production defaults.

Latency percentiles are `null` because there are fewer than 20 samples. Worker
initialization and per-image/variant timings are recorded separately in JSON.
Timing depends on host load and is not a performance guarantee.

```bash
npm run benchmark:all
```

That command reruns A → B → C → D → additional experiments and replaces their
JSON reports. It returns failure for operational errors, while preserving OCR
misses as benchmark results. Each report retains all candidates, labels, hashes,
configurations and errors for inspection.
