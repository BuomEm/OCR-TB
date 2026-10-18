"""Tiện ích dùng chung cho benchmark: thư mục run, chuẩn hoá, thống kê, Levenshtein."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Iterable

from .config import DATA_DIR, VERSION, ensure_dirs
from .registry import normalize  # noqa: F401  (re-export để benchmark dùng chung)

RUNS_DIR = DATA_DIR / "runs"
REPORT_DIR = DATA_DIR / "report"
LABELS_CSV = DATA_DIR / "labels.csv"
LABELING_HTML = DATA_DIR / "labeling.html"

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def workdir() -> Path:
    """Thư mục chứa ảnh captcha (mặc định DATA_DIR/captcha)."""
    import os

    return Path(os.environ.get("OCR_TB_IMAGES", DATA_DIR / "captcha")).expanduser()


def list_images(image_dir: Path | None = None) -> list[Path]:
    image_dir = image_dir or workdir()
    if not image_dir.exists():
        return []
    return sorted(p for p in image_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)


def ensure_bench_dirs() -> None:
    ensure_dirs()
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (ca != cb)))
        previous = current
    return previous[-1]


def char_similarity(pred: str, truth: str) -> float:
    longest = max(len(pred), len(truth))
    if longest == 0:
        return 1.0
    return 1.0 - levenshtein(pred, truth) / longest


def percentile(values: Iterable[float], q: float) -> float:
    data = sorted(values)
    if not data:
        return 0.0
    if len(data) == 1:
        return data[0]
    pos = (len(data) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(data) - 1)
    frac = pos - lo
    return data[lo] * (1 - frac) + data[hi] * frac


def stats(values: Iterable[float]) -> dict[str, float]:
    data = list(values)
    if not data:
        return {"count": 0, "mean": 0.0, "p50": 0.0, "p95": 0.0, "min": 0.0, "max": 0.0, "total": 0.0}
    return {
        "count": len(data),
        "mean": round(sum(data) / len(data), 2),
        "p50": round(percentile(data, 0.5), 2),
        "p95": round(percentile(data, 0.95), 2),
        "min": round(min(data), 2),
        "max": round(max(data), 2),
        "total": round(sum(data), 2),
    }


def load_labels(labels_csv: Path | None = None) -> dict[str, str]:
    import csv

    path = labels_csv or LABELS_CSV
    if not path.exists():
        return {}
    labels: dict[str, str] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            filename = (row.get("filename") or "").strip()
            label = normalize((row.get("label") or "").strip())
            if filename and label:
                labels[filename] = label
    return labels


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def utc_run_id() -> str:
    return time.strftime("%Y%m%d-%H%M%S", time.localtime())


def latest_run_dir() -> Path | None:
    if not RUNS_DIR.exists():
        return None
    candidates = [p for p in RUNS_DIR.iterdir() if p.is_dir()]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def image_meta(data: bytes) -> dict[str, Any]:
    """Kích thước + chỉ số độ khó (mực chữ, cạnh, số nét) để phân tích sau."""
    import io

    import cv2
    import numpy as np
    from PIL import Image

    array = np.array(Image.open(io.BytesIO(data)).convert("L"))
    height, width = array.shape
    dark = (array < 128).astype(np.uint8)
    return {
        "width": width,
        "height": height,
        "bytes": len(data),
        "ink_ratio": round(float(dark.mean()), 4),
        "edge_density": round(float((cv2.Canny(array, 80, 180) > 0).mean()), 4),
        "components": int(cv2.connectedComponents(dark, connectivity=8)[0] - 1),
    }


def library_versions() -> dict[str, str]:
    from importlib.metadata import PackageNotFoundError, version

    out: dict[str, str] = {"ocr-tb": VERSION}
    for dist, module in (
        ("ddddocr", "ddddocr"),
        ("onnxruntime", "onnxruntime"),
        ("rapidocr-onnxruntime", "rapidocr_onnxruntime"),
        ("pytesseract", "pytesseract"),
        ("opencv-python-headless", "cv2"),
        ("numpy", "numpy"),
        ("pillow", "PIL"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
    ):
        try:
            out[module] = version(dist)
        except PackageNotFoundError:
            out[module] = "not installed"
    try:
        from .registry import TesseractModel

        out["tesseract"] = TesseractModel.version() or "not available"
    except Exception:  # noqa: BLE001
        out["tesseract"] = "not available"
    return out


def platform_info() -> dict[str, Any]:
    import os
    import platform

    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
    }