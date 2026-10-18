"""Cấu hình đường dẫn, biến môi trường và hằng số của OCR-TB.

Mọi đường dẫn đều có thể ghi đè bằng biến môi trường, nhờ vậy chạy Docker,
WSL, systemd hay CI đều dùng chung một bộ code.
"""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "ocr-tb"
VERSION = "1.0.0"

#: Đặt OCR_TB_HOME để dùng chung cache giữa nhiều user/container.
HOME = Path(os.environ.get("OCR_TB_HOME") or Path.home() / ".cache" / APP_NAME).expanduser()
CACHE_DIR = Path(os.environ.get("OCR_TB_CACHE", HOME / "models")).expanduser()
DATA_DIR = Path(os.environ.get("OCR_TB_DATA", HOME / "data")).expanduser()

DEFAULT_MODEL = os.environ.get("OCR_TB_MODEL", "ddddocr")
DEFAULT_CONFIG = os.environ.get("OCR_TB_CONFIG", "")
DEFAULT_VARIANT = os.environ.get("OCR_TB_VARIANT", "raw")

#: Thời gian tối đa cho 1 lượt giải (giây).
SOLVE_TIMEOUT_S = float(os.environ.get("OCR_TB_TIMEOUT", "15"))

SERVER_HOST = os.environ.get("OCR_TB_HOST", "0.0.0.0")
SERVER_PORT = int(os.environ.get("OCR_TB_PORT", "2424"))

ALLOWED_LABEL_CHARS = set("0123456789abcdefghijklmnopqrstuvwxyz")

#: Bộ captcha ViettelPost dùng 4 ký tự; chỉ dùng để gợi ý khi gán nhãn tay.
DEFAULT_CAPTCHA_LENGTH = 4

#: Model tải về lần đầu, dung lượng ~37 MB (ddddocr đã nằm trong package pip).
REMOTE_MODELS: dict[str, dict] = {
    "ppocr_v5_en": {
        "dir": "en_ppocrv5_mobile_rec_onnx",
        "repo": "PaddlePaddle/en_PP-OCRv5_mobile_rec_onnx",
        "files": ["inference.onnx", "inference.yml"],
        "label": "PP-OCRv5 English mobile rec (ONNX)",
        "approx_mb": 7.5,
    },
    "ppocr_v6_small": {
        "dir": "ppocr_v6_small_rec_onnx",
        "repo": "PaddlePaddle/PP-OCRv6_small_rec_onnx",
        "files": ["inference.onnx", "inference.yml"],
        "label": "PP-OCRv6 small rec (ONNX)",
        "approx_mb": 20.2,
    },
    "ppocr_v6_small_det": {
        "dir": "ppocr_v6_small_det_onnx",
        "repo": "PaddlePaddle/PP-OCRv6_small_det_onnx",
        "files": ["inference.onnx"],
        "label": "PP-OCRv6 small det (ONNX, dự phòng)",
        "approx_mb": 9.4,
    },
}

HF_ENDPOINT = os.environ.get("HF_ENDPOINT", "https://huggingface.co")


def model_dir(model_id: str) -> Path:
    return CACHE_DIR / REMOTE_MODELS[model_id]["dir"]


def ensure_dirs() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def describe_paths() -> dict[str, str]:
    return {
        "OCR_TB_HOME": str(HOME),
        "cache_models": str(CACHE_DIR),
        "data": str(DATA_DIR),
    }


def enable_utf8_console() -> None:
    """Console Windows mặc định cp1252 nên không in được tiếng Việt."""
    import sys

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:  # pragma: no cover
            pass