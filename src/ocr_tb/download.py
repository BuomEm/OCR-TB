"""Tải model ONNX về cache, sinh character dict từ inference.yml.

Cache vĩnh viễn trong `OCR_TB_CACHE` (mặc định ~/.cache/ocr-tb/models),
nên chạy nhiều lần/container restart không tải lại.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable

from .config import HF_ENDPOINT, REMOTE_MODELS, ensure_dirs, model_dir


def is_cached(model_id: str) -> bool:
    spec = REMOTE_MODELS.get(model_id)
    if not spec:
        return True
    target = model_dir(model_id)
    return all((target / filename).exists() and (target / filename).stat().st_size > 0 for filename in spec["files"])


def missing_models() -> list[str]:
    return [model_id for model_id in REMOTE_MODELS if not is_cached(model_id)]


def _download(repo: str, filename: str, dest: Path, force: bool, log: Callable[[str], None]) -> str:
    if dest.exists() and dest.stat().st_size > 0 and not force:
        return f"bỏ qua {filename} (đã có {dest.stat().st_size // 1024} KB)"

    import requests

    url = f"{HF_ENDPOINT}/{repo}/resolve/main/{filename}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    started = time.perf_counter()
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with tmp.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1 << 20):
                fh.write(chunk)
    tmp.replace(dest)
    took = time.perf_counter() - started
    return f"tải {filename} ({dest.stat().st_size // 1024} KB, {took:.1f}s)"


def _build_keys(yml_path: Path, out_path: Path) -> str:
    """Lấy PostProcess.character_dict trong inference.yml -> file txt 1 ký tự/dòng."""
    if not yml_path.exists():
        return "bỏ qua ppocr_keys.txt (không có inference.yml)"
    if out_path.exists() and out_path.stat().st_size > 0:
        return f"bỏ qua ppocr_keys.txt (đã có {out_path.stat().st_size // 1024} KB)"

    import yaml

    data = yaml.safe_load(yml_path.read_text(encoding="utf-8"))
    characters = ((data or {}).get("PostProcess") or {}).get("character_dict")
    if not characters:
        return "bỏ qua ppocr_keys.txt (không tìm thấy character_dict)"
    out_path.write_text("\n".join(str(item) for item in characters) + "\n", encoding="utf-8")
    return f"tạo ppocr_keys.txt ({len(characters)} ký tự)"


def pull_model(model_id: str, force: bool = False, log: Callable[[str], None] = print) -> dict[str, Any]:
    spec = REMOTE_MODELS.get(model_id)
    if not spec:
        raise KeyError(f"Không có model tải về tên '{model_id}'. Có: {', '.join(REMOTE_MODELS)}")

    target = model_dir(model_id)
    target.mkdir(parents=True, exist_ok=True)
    log(f"[{model_id}] {spec['label']} <- huggingface.co/{spec['repo']}")
    for filename in spec["files"]:
        log("  " + _download(spec["repo"], filename, target / filename, force, log))
    log("  " + _build_keys(target / "inference.yml", target / "ppocr_keys.txt"))
    return {"model_id": model_id, "path": str(target)}


def pull_all(force: bool = False, log: Callable[[str], None] = print, only_missing: bool = True) -> list[dict[str, Any]]:
    ensure_dirs()
    targets = missing_models() if only_missing else list(REMOTE_MODELS)
    if not targets:
        log("Tất cả model đã có trong cache.")
        return []
    return [pull_model(model_id, force=force, log=log) for model_id in targets]


def cache_status() -> list[dict[str, Any]]:
    rows = []
    for model_id, spec in REMOTE_MODELS.items():
        target = model_dir(model_id)
        size = sum(p.stat().st_size for p in target.glob("*") if p.is_file()) if target.exists() else 0
        rows.append(
            {
                "model_id": model_id,
                "label": spec["label"],
                "path": str(target),
                "cached": is_cached(model_id),
                "size_mb": round(size / (1024 * 1024), 1),
            }
        )
    return rows