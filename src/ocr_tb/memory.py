"""Đo RAM và dung lượng đĩa khi nạp/chạy model (dùng psutil)."""

from __future__ import annotations

import gc
import os
import subprocess
import time
from pathlib import Path
from typing import Callable

from .config import CACHE_DIR
from .registry import build_registry

try:
    import psutil

    PROC = psutil.Process(os.getpid())
except Exception:  # pragma: no cover
    psutil = None  # type: ignore[assignment]
    PROC = None  # type: ignore[assignment]


def _rss_mb() -> float:
    return (PROC.memory_info().rss / (1024 * 1024)) if PROC else 0.0


def _dir_size(path: Path) -> float:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file()) / (1024 * 1024)


def model_disk_usage() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    import ddddocr

    package_dir = Path(ddddocr.__file__).parent
    for file in sorted(package_dir.glob("*.onnx")):
        rows.append(
            {
                "component": f"ddddocr/{file.name}",
                "size_mb": round(file.stat().st_size / (1024 * 1024), 1),
                "path": str(file),
            }
        )

    if CACHE_DIR.exists():
        for path in sorted(CACHE_DIR.rglob("*.onnx")):
            rows.append(
                {
                    "component": f"cache/{path.relative_to(CACHE_DIR)}",
                    "size_mb": round(path.stat().st_size / (1024 * 1024), 1),
                    "path": str(path),
                }
            )
    return rows


def tesseract_process_mb(image: Path) -> float:
    """RAM tiến trình con Tesseract khi dự đoán 1 ảnh."""
    from .registry import TesseractModel

    exe = TesseractModel.find_tesseract()
    if not exe or psutil is None:
        return 0.0
    peak = 0.0
    process = subprocess.Popen(
        [str(exe), str(image), "stdout", "--psm", "8"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        handle = psutil.Process(process.pid)
        while process.poll() is None:
            try:
                peak = max(peak, handle.memory_info().rss / (1024 * 1024))
            except Exception:  # noqa: BLE001
                break
            time.sleep(0.005)
    finally:
        process.wait()
    return round(peak, 1)


def measure(image_dir: Path | None = None, log: Callable[[str], None] = print) -> dict[str, object]:
    from .util import list_images

    images = list_images(image_dir)[:100]
    sample = images[0].read_bytes() if images else b""
    if not sample:
        raise SystemExit("Không có ảnh để đo. Trỏ OCR_TB_IMAGES tới thư mục ảnh captcha.")

    payload: dict[str, object] = {"steps": []}
    steps: list[dict[str, object]] = payload["steps"]  # type: ignore[assignment]
    steps.append({"step": "python interpreter", "rss_mb": round(_rss_mb(), 1)})

    for model in build_registry():
        if not model.builtin:
            continue
        before = _rss_mb()
        config_id, params = next(iter(model.configs.items()))
        try:
            model.ensure_loaded()
        except Exception as error:  # noqa: BLE001
            steps.append({"step": f"load {model.id}", "error": f"{type(error).__name__}: {error}"})
            continue

        after_load = _rss_mb()
        started = time.perf_counter()
        try:
            model.predict(sample, params)
        except Exception as error:  # noqa: BLE001
            log(f"  (bỏ qua dự đoán {model.id}: {type(error).__name__}: {error})")
        after_run = _rss_mb()
        steps.append(
            {
                "step": f"{model.id}/{config_id}",
                "rss_after_load_mb": round(after_load, 1),
                "load_delta_mb": round(after_load - before, 1),
                "rss_after_run_mb": round(after_run, 1),
                "first_call_ms": round((time.perf_counter() - started) * 1000, 1),
            }
        )
        gc.collect()

    payload["disk"] = model_disk_usage()
    payload["disk_total_mb"] = round(sum(float(row["size_mb"]) for row in payload["disk"]), 1)  # type: ignore[union-attr]
    try:
        payload["venv_mb"] = round(_dir_size(Path(os.sys.prefix)), 1)
    except Exception:  # noqa: BLE001
        pass
    if images:
        payload["tesseract_process_mb"] = tesseract_process_mb(images[0])
    payload["psutil"] = bool(psutil)
    return payload


def format_report(payload: dict[str, object]) -> str:
    lines = ["=== RAM (RSS) ==="]
    for step in payload["steps"]:  # type: ignore[union-attr]
        if "error" in step:
            lines.append(f"  {step['step']}: LỖI {step['error']}")
            continue
        if "rss_after_load_mb" not in step:
            lines.append(f"  {step['step']:34} {step['rss_mb']} MB")
            continue
        lines.append(
            f"  {step['step']:34} nạp {step['rss_after_load_mb']} MB (+{step['load_delta_mb']}) "
            f"| sau lượt đầu {step['rss_after_run_mb']} MB | {step['first_call_ms']} ms"
        )
    if payload.get("tesseract_process_mb"):
        lines.append(f"  tesseract (tiến trình con)          {payload['tesseract_process_mb']} MB")
    lines.append("")
    lines.append("=== Dung lượng đĩa model ===")
    for row in payload["disk"]:  # type: ignore[union-attr]
        lines.append(f"  {row['component']:44} {row['size_mb']} MB")
    lines.append(f"  {'tổng model':44} {payload['disk_total_mb']} MB")
    if payload.get("venv_mb"):
        lines.append(f"  {'môi trường python (venv)':44} {payload['venv_mb']} MB")
    return "\n".join(lines)