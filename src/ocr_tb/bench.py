"""Benchmark OCR: chạy model trên bộ ảnh, chấm điểm theo nhãn tay, xuất báo cáo."""

from __future__ import annotations

import csv
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

from .config import DEFAULT_CAPTCHA_LENGTH, ensure_dirs
from .preprocess import VARIANTS, apply_variant
from .registry import build_registry, expand_runs, normalize
from .util import (
    LABELS_CSV,
    LABELING_HTML,
    REPORT_DIR,
    RUNS_DIR,
    char_similarity,
    ensure_bench_dirs,
    image_meta,
    latest_run_dir,
    levenshtein,
    library_versions,
    list_images,
    load_labels,
    platform_info,
    read_json,
    read_jsonl,
    stats,
    utc_run_id,
    write_json,
    workdir,
)


# --------------------------------------------------------------------------- labeling
CSV_FIELDS = ["filename", "label", "note"]


def write_labels_template() -> Path:
    existing = load_labels()
    images = list_images()
    ensure_bench_dirs()
    with LABELS_CSV.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for image in images:
            writer.writerow({"filename": image.name, "label": existing.get(image.name, ""), "note": ""})
    return LABELS_CSV


def write_labeling_html(expected_length: int = DEFAULT_CAPTCHA_LENGTH) -> Path:
    """Bảng gán nhãn tay: ảnh + ô nhập, lưu localStorage, xuất CSV."""
    import html as html_lib

    images = list_images()
    rows = []
    for index, image in enumerate(images, start=1):
        name = html_lib.escape(image.name)
        rows.append(
            f"""    <tr>
      <td class="idx">{index}</td>
      <td><img src="{name}" alt="{name}" loading="lazy"></td>
      <td class="file">{name}</td>
      <td><input class="answer" data-file="{name}" maxlength="12" autocomplete="off" spellcheck="false"></td>
      <td class="state">-</td>
    </tr>"""
        )

    doc = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gán nhãn captcha - OCR-TB</title>
<script>const EXPECTED = {expected_length};</script>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 16px; background: #111; color: #eee; }}
  h1 {{ font-size: 18px; }}
  .bar {{ position: sticky; top: 0; background: #1b1b1b; padding: 8px 12px; border-radius: 6px;
          display: flex; gap: 12px; align-items: center; flex-wrap: wrap; z-index: 2; }}
  button {{ padding: 6px 12px; cursor: pointer; border-radius: 4px; border: 0; }}
  table {{ border-collapse: collapse; width: 100%; }}
  td, th {{ border-bottom: 1px solid #333; padding: 6px; text-align: left; vertical-align: middle; }}
  img {{ width: 200px; height: 50px; background: #fff; image-rendering: pixelated; display: block; }}
  .idx {{ width: 40px; color: #888; }}
  .file {{ font-family: ui-monospace, monospace; font-size: 11px; color: #999; width: 320px; }}
  input.answer {{ width: 140px; font-size: 18px; padding: 4px 8px; text-transform: lowercase;
                 background: #222; color: #7CFC00; border: 1px solid #444; border-radius: 4px; }}
  input.answer.ok {{ border-color: #2b6; }}
  input.answer.bad {{ border-color: #a33; }}
  .state {{ font-size: 12px; color: #888; width: 90px; }}
  tr.done {{ opacity: 0.55; }}
</style>
</head>
<body>
<h1>Gán nhãn thủ công - captcha ({expected_length} ký tự, a-z 0-9)</h1>
<div class="bar">
  <button id="export">Xuất CSV</button>
  <button id="copy">Copy CSV</button>
  <button id="reset">Xoá hết</button>
  <span id="progress">0 / {len(images)}</span>
  <span style="color:#888">Lưu tự động trong localStorage</span>
</div>
<table>
  <thead><tr><th>#</th><th>Ảnh</th><th>File</th><th>Đáp án</th><th>Trạng thái</th></tr></thead>
  <tbody>
{chr(10).join(rows)}
  </tbody>
</table>
<script>
const KEY = 'ocr-tb-labels-v1';
const CHARS = '0123456789abcdefghijklmnopqrstuvwxyz';
let store = JSON.parse(localStorage.getItem(KEY) || '{{}}');
const inputs = [...document.querySelectorAll('input.answer')];

function validate(value) {{
  return value.length === EXPECTED && [...value].every(c => CHARS.includes(c));
}}

function refresh() {{
  let done = 0;
  for (const input of inputs) {{
    const value = (input.value || '').trim().toLowerCase();
    input.value = value;
    const state = input.closest('tr').querySelector('.state');
    if (value) {{ store[input.dataset.file] = value; done += 1; }}
    else {{ delete store[input.dataset.file]; }}
    if (!value) {{ input.className = 'answer'; state.textContent = '-'; input.closest('tr').classList.remove('done'); }}
    else if (validate(value)) {{ input.className = 'answer ok'; state.textContent = 'ok'; input.closest('tr').classList.add('done'); }}
    else {{ input.className = 'answer bad'; state.textContent = 'sai định dạng'; input.closest('tr').classList.remove('done'); }}
  }}
  localStorage.setItem(KEY, JSON.stringify(store));
  document.getElementById('progress').textContent = done + ' / ' + inputs.length;
}}

function csvText() {{
  const lines = ['filename,label,note'];
  for (const input of inputs) lines.push(input.dataset.file + ',' + (input.value || '') + ',');
  return lines.join('\\n');
}}

for (const input of inputs) {{
  input.value = store[input.dataset.file] || '';
  input.addEventListener('input', refresh);
  input.addEventListener('keydown', (e) => {{
    if (e.key === 'Enter') {{
      const next = inputs[inputs.indexOf(input) + 1];
      if (next) next.focus();
      e.preventDefault();
    }}
  }});
}}

document.getElementById('export').onclick = () => {{
  const blob = new Blob(['\\ufeff' + csvText()], {{ type: 'text/csv;charset=utf-8' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = 'labels.csv'; a.click();
  URL.revokeObjectURL(a.href);
}};
document.getElementById('copy').onclick = async () => {{
  try {{ await navigator.clipboard.writeText(csvText()); alert('Đã copy CSV'); }}
  catch (error) {{ alert('Không copy được: ' + error); }}
}};
document.getElementById('reset').onclick = () => {{
  if (!confirm('Xoá toàn bộ nhãn đã nhập?')) return;
  store = {{}};
  for (const input of inputs) input.value = '';
  refresh();
}};
refresh();
</script>
</body>
</html>
"""
    LABELING_HTML.write_text(doc, encoding="utf-8")
    return LABELING_HTML


def label_progress() -> dict[str, Any]:
    images = list_images()
    labels = load_labels()
    missing = [image.name for image in images if image.name not in labels]
    return {"total": len(images), "labeled": len(labels), "missing": len(missing), "missing_sample": missing[:10]}


# --------------------------------------------------------------------------- run
def _parse_pairs(value: str | None) -> dict[str, list[str]]:
    if not value:
        return {}
    pairs: dict[str, list[str]] = {}
    for chunk in value.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        model_id, _, config_ids = chunk.partition(":")
        pairs[model_id] = [c for c in config_ids.split("|") if c]
    return pairs


def run_benchmark(
    models: list[str] | None = None,
    configs: str | None = None,
    variants: list[str] | None = None,
    limit: int = 0,
    repeat: int = 1,
    warmup: int = 3,
    run_id: str = "",
) -> Path:
    variants = variants or ["raw"]
    unknown = [v for v in variants if v not in VARIANTS]
    if unknown:
        raise ValueError(f"Tiền xử lý không hợp lệ: {unknown}. Hợp lệ: {list(VARIANTS)}")

    images = list_images()
    if limit > 0:
        images = images[:limit]
    if not images:
        raise SystemExit(f"Không có ảnh trong {workdir()}. Trỏ OCR_TB_IMAGES hoặc copy ảnh vào đó.")

    ensure_bench_dirs()
    registry = build_registry()
    runs = expand_runs(registry, models, _parse_pairs(configs))

    run_id = run_id or utc_run_id()
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    rows_path = run_dir / "rows.jsonl"
    rows_path.write_text("", encoding="utf-8")
    write_json(
        run_dir / "env.json",
        {
            "run_id": run_id,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "images": len(images),
            "variants": variants,
            "repeat": repeat,
            "warmup": warmup,
            "platform": platform_info(),
            "libraries": library_versions(),
        },
    )

    payloads = [(image.name, image.read_bytes(), image_meta(image.read_bytes())) for image in images]
    preprocessed = {
        variant: {name: apply_variant(data, variant) for name, data, _ in payloads} for variant in variants
    }

    print(f"Run {run_id}: {len(images)} ảnh x {len(runs)} cấu hình x {len(variants)} biến thể")
    summaries: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    rows_written = 0

    with rows_path.open("a", encoding="utf-8") as rows_file:
        for run in runs:
            model = next((m for m in registry if m.id == run.model_id), None)
            if model is None:
                continue
            try:
                model.ensure_loaded()
            except Exception as error:  # noqa: BLE001
                reason = f"{type(error).__name__}: {error}"
                print(f"[BỎ QUA] {run.model_id}/{run.config_id}: {reason}")
                skipped.append({"model_id": run.model_id, "config_id": run.config_id, "reason": reason})
                continue

            for name, _data, _meta in payloads[: max(warmup, 0)]:
                for variant in variants:
                    try:
                        model.predict(preprocessed[variant][name], run.params)
                    except Exception:  # noqa: BLE001
                        pass

            for variant in variants:
                timings: list[float] = []
                errors = 0
                empty = 0
                started_all = time.perf_counter()

                for name, _data, meta in payloads:
                    img_bytes = preprocessed[variant][name]
                    raw_text, confidence, detail, error = "", None, {}, ""

                    for _attempt in range(repeat):
                        started = time.perf_counter()
                        try:
                            prediction = model.predict(img_bytes, run.params)
                            elapsed = (time.perf_counter() - started) * 1000
                            timings.append(elapsed)
                            raw_text = prediction.text
                            confidence = prediction.confidence
                            detail = prediction.detail
                            error = ""
                        except Exception as exc:  # noqa: BLE001
                            elapsed = (time.perf_counter() - started) * 1000
                            timings.append(elapsed)
                            errors += 1
                            raw_text, confidence, detail = "", None, {}
                            error = f"{type(exc).__name__}: {exc}"

                    text = normalize(raw_text)
                    if not text:
                        empty += 1
                    rows_file.write(
                        json.dumps(
                            {
                                "run_id": run_id,
                                "model_id": run.model_id,
                                "model_label": model.label,
                                "config_id": run.config_id,
                                "variant": variant,
                                "filename": name,
                                "image": meta,
                                "raw_text": raw_text,
                                "text": text,
                                "length": len(text),
                                "confidence": confidence,
                                "elapsed_ms": round(elapsed, 2),
                                "detail": detail,
                                "error": error,
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                    rows_written += 1
                rows_file.flush()

                wall = (time.perf_counter() - started_all) * 1000
                summary = {
                    "model_id": run.model_id,
                    "model_label": model.label,
                    "config_id": run.config_id,
                    "variant": variant,
                    "images": len(payloads),
                    "timing": stats(timings),
                    "wall_ms": round(wall, 2),
                    "errors": errors,
                    "empty_outputs": empty,
                }
                summaries.append(summary)
                timing = summary["timing"]
                print(
                    f"[{run.model_id}/{run.config_id}/{variant}] mean {timing['mean']} ms | "
                    f"p95 {timing['p95']} ms | lỗi {errors} | rỗng {empty}"
                )

    write_json(run_dir / "summary.json", {"run_id": run_id, "rows": rows_written, "skipped": skipped, "summaries": summaries})
    print(f"\nXong: {rows_written} dòng -> {rows_path}")
    return run_dir


# --------------------------------------------------------------------------- score
def _group(rows: list[dict]) -> dict[tuple[str, str, str], list[dict]]:
    grouped: dict[tuple[str, str, str], list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["model_id"], row["config_id"], row.get("variant", "raw")), []).append(row)
    return grouped


def _score_group(group: list[dict], labels: dict[str, str]) -> dict[str, Any]:
    scored = [row for row in group if row["filename"] in labels]
    total = len(scored)
    exact = sum(1 for row in scored if row["text"] == labels[row["filename"]])
    length_ok = sum(1 for row in scored if len(row["text"]) == len(labels[row["filename"]]))
    similarity = [char_similarity(row["text"], labels[row["filename"]]) for row in scored]
    confidences = [row["confidence"] for row in scored if row.get("confidence") is not None]

    confusion: Counter[str] = Counter()
    for row in scored:
        truth, pred = labels[row["filename"]], row["text"]
        if pred == truth:
            continue
        for index in range(max(len(truth), len(pred))):
            want = truth[index] if index < len(truth) else "∅"
            got = pred[index] if index < len(pred) else "∅"
            if want != got:
                confusion[f"{want}->{got}"] += 1

    return {
        "total_images": len(group),
        "labeled": total,
        "exact": exact,
        "exact_accuracy": round(exact / total * 100, 2) if total else None,
        "length_match_rate": round(length_ok / total * 100, 2) if total else None,
        "char_accuracy": round(sum(similarity) / total * 100, 2) if total else None,
        "avg_edit_distance": round(sum(levenshtein(r["text"], labels[r["filename"]]) for r in scored) / total, 3)
        if total
        else None,
        "empty_outputs": sum(1 for row in group if not row["text"]),
        "errors": sum(1 for row in group if row.get("error")),
        "confidence_mean": round(sum(confidences) / len(confidences), 4) if confidences else None,
        "timing": stats([row["elapsed_ms"] for row in group]),
        "top_confusions": confusion.most_common(12),
    }


def _agreement(rows: list[dict], keys: list[tuple[str, str, str]]) -> dict[str, Any]:
    index: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        index.setdefault((row["model_id"], row["config_id"], row.get("variant", "raw")), {})[row["filename"]] = row["text"]
    labels = load_labels()
    pairs = []
    for key_a in keys:
        for key_b in keys:
            if key_a >= key_b:
                continue
            common = set(labels) & set(index.get(key_a, {})) & set(index.get(key_b, {}))
            if not common:
                continue
            same = sum(1 for name in common if index[key_a][name] == index[key_b][name])
            pairs.append(
                {
                    "a": "/".join(key_a),
                    "b": "/".join(key_b),
                    "images": len(common),
                    "same_output": same,
                    "same_rate": round(same / len(common) * 100, 2),
                }
            )
    return {"pairs": pairs}


def score_run(run_id: str = "") -> dict[str, Any]:
    run_dir = RUNS_DIR / run_id if run_id else latest_run_dir()
    if run_dir is None or not run_dir.exists():
        raise SystemExit("Chưa có run nào. Chạy `ocr-tb bench run` trước.")

    run_id = run_dir.name
    rows = read_jsonl(run_dir / "rows.jsonl")
    if not rows:
        raise SystemExit(f"Run {run_id} không có dữ liệu.")

    labels = load_labels()
    images = list_images()
    missing = [image.name for image in images if image.name not in labels]

    ranked = []
    for (model_id, config_id, variant), group in sorted(_group(rows).items()):
        ranked.append(
            {
                "name": f"{model_id}/{config_id}/{variant}",
                "model_id": model_id,
                "config_id": config_id,
                "variant": variant,
                "model_label": group[0]["model_label"],
                "score": _score_group(group, labels),
            }
        )
    ranked.sort(
        key=lambda item: (
            -(item["score"]["exact_accuracy"] if item["score"]["exact_accuracy"] is not None else -1),
            -(item["score"]["char_accuracy"] if item["score"]["char_accuracy"] is not None else -1),
            item["score"]["timing"]["mean"],
        )
    )

    payload = {
        "run_id": run_id,
        "total_images": len(images),
        "labeled_images": len(labels),
        "missing_labels": missing,
        "ranked": ranked,
        "agreement": _agreement(rows, sorted(_group(rows))),
    }
    ensure_bench_dirs()
    write_json(REPORT_DIR / f"score-{run_id}.json", payload)
    _write_csvs(run_id, ranked, rows, labels)
    _write_report(run_id, run_dir, ranked, labels, payload)
    return payload


def _write_csvs(run_id: str, ranked: list[dict], rows: list[dict], labels: dict[str, str]) -> None:
    with (REPORT_DIR / f"score-{run_id}.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "config", "model_label", "images", "labeled", "exact", "exact_accuracy_pct", "char_accuracy_pct",
                "length_match_pct", "avg_edit_distance", "empty_outputs", "errors", "mean_ms", "p50_ms", "p95_ms",
                "max_ms", "total_s",
            ]
        )
        for item in ranked:
            score, timing = item["score"], item["score"]["timing"]
            writer.writerow(
                [
                    item["name"], item["model_label"], score["total_images"], score["labeled"], score["exact"],
                    score["exact_accuracy"], score["char_accuracy"], score["length_match_rate"],
                    score["avg_edit_distance"], score["empty_outputs"], score["errors"], timing["mean"], timing["p50"],
                    timing["p95"], timing["max"], round(timing["total"] / 1000, 2),
                ]
            )

    with (REPORT_DIR / f"details-{run_id}.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "filename", "label", "config", "raw_text", "normalized", "correct", "edit_distance", "similarity",
                "confidence", "elapsed_ms", "ink_ratio", "edge_density", "components", "error",
            ]
        )
        for row in sorted(rows, key=lambda r: (r["filename"], r["model_id"], r["config_id"])):
            truth = labels.get(row["filename"], "")
            meta = row.get("image", {})
            writer.writerow(
                [
                    row["filename"], truth, f"{row['model_id']}/{row['config_id']}/{row.get('variant', 'raw')}",
                    row["raw_text"], row["text"], int(bool(truth) and row["text"] == truth),
                    levenshtein(row["text"], truth) if truth else "",
                    round(char_similarity(row["text"], truth), 4) if truth else "",
                    row.get("confidence") if row.get("confidence") is not None else "",
                    row["elapsed_ms"], meta.get("ink_ratio"), meta.get("edge_density"), meta.get("components"),
                    row.get("error", ""),
                ]
            )


def _write_report(run_id: str, run_dir: Path, ranked: list[dict], labels: dict[str, str], payload: dict[str, Any]) -> Path:
    env = read_json(run_dir / "env.json") if (run_dir / "env.json").exists() else {}
    lines = [f"# Benchmark OCR captcha — run `{run_id}`\n"]
    lines.append(f"- Thời điểm: {env.get('created_at')}")
    lines.append(f"- Ảnh: {payload['total_images']} | đã có nhãn: {len(labels)}")
    lines.append(f"- Máy: {env.get('platform', {}).get('platform')} ({env.get('platform', {}).get('cpu_count')} luồng)")
    lines.append("- Thư viện: " + ", ".join(f"{k}={v}" for k, v in env.get("libraries", {}).items()))
    lines.append("")

    usable = [item for item in ranked if item["score"]["exact_accuracy"] is not None]
    lines.append("## Kết luận\n")
    if usable:
        best = usable[0]
        lines.append(f"**Khuyến nghị: `{best['name']}`** — chính xác {best['score']['exact_accuracy']}%, "
                     f"{best['score']['timing']['mean']} ms/ảnh.")
        fastest = min(usable, key=lambda i: i["score"]["timing"]["mean"])
        if fastest["name"] != best["name"]:
            lines.append(f"Nhanh nhất: `{fastest['name']}` ({fastest['score']['timing']['mean']} ms/ảnh, "
                         f"{fastest['score']['exact_accuracy']}%).")
    else:
        lines.append("Chưa có nhãn. Chạy `ocr-tb label make` rồi gán tay trong labeling.html.")
    lines.append("")

    lines.append("## Bảng xếp hạng\n")
    lines.append("| # | Cấu hình | Chính xác | Char acc | Đúng độ dài nhãn | Rỗng | Lỗi | mean ms | p95 ms |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for index, item in enumerate(ranked, start=1):
        score, timing = item["score"], item["score"]["timing"]
        accuracy = f"{score['exact_accuracy']}%" if score["exact_accuracy"] is not None else "chưa chấm"
        char_acc = f"{score['char_accuracy']}%" if score["char_accuracy"] is not None else "-"
        length_rate = f"{score['length_match_rate']}%" if score["length_match_rate"] is not None else "-"
        lines.append(
            f"| {index} | `{item['name']}` | **{accuracy}** | {char_acc} | {length_rate} | "
            f"{score['empty_outputs']} | {score['errors']} | {timing['mean']} | {timing['p95']} |"
        )
    lines.append("")

    lines.append("## Chi tiết\n")
    for item in ranked:
        score = item["score"]
        timing = score["timing"]
        lines.append(f"### `{item['name']}`\n")
        lines.append(f"- {item['model_label']}")
        lines.append(
            f"- Ảnh: {score['total_images']} | đã chấm: {score['labeled']} | chính xác: {score['exact_accuracy']}% | "
            f"char acc: {score['char_accuracy']}%"
        )
        lines.append(f"- Rỗng: {score['empty_outputs']} | exception: {score['errors']}")
        lines.append(
            f"- Thời gian: mean {timing['mean']} ms | p50 {timing['p50']} ms | p95 {timing['p95']} ms | "
            f"max {timing['max']} ms"
        )
        if score["top_confusions"]:
            lines.append("- Nhầm ký tự: " + ", ".join(f"`{p}`×{c}" for p, c in score["top_confusions"][:10]))
        lines.append("")

    pairs = payload.get("agreement", {}).get("pairs", [])
    if pairs:
        lines.append("## Mức độ giống nhau giữa các cấu hình\n")
        lines.append("| A | B | Ảnh | Giống nhau | Tỉ lệ |")
        lines.append("|---|---|---|---|---|")
        for item in pairs:
            lines.append(f"| `{item['a']}` | `{item['b']}` | {item['images']} | {item['same_output']} | {item['same_rate']}% |")
        lines.append("")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"report-{run_id}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


__all__ = [
    "label_progress",
    "run_benchmark",
    "score_run",
    "write_labeling_html",
    "write_labels_template",
    "ensure_dirs",
]