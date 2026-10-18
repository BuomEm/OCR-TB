"""Các biến thể tiền xử lý ảnh captcha.

Biến thể dùng cho `solver` (chọn 1 theo config) và cho benchmark
(so sánh tác động của từng cách xử lý với từng model).
"""

from __future__ import annotations

import io
from typing import Callable

VARIANTS: dict[str, Callable[[bytes], bytes]] = {}

try:  # Pillow là bắt buộc, nhưng để import registry không chết khi thiếu
    import numpy as np
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover
    Image = None  # type: ignore[assignment]


def _to_image(img_bytes: bytes):
    image = Image.open(io.BytesIO(img_bytes))
    return image.convert("RGB") if image.mode not in {"RGB", "L"} else image


def _save(image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _raw(img_bytes: bytes) -> bytes:
    return img_bytes


def _gray(img_bytes: bytes) -> bytes:
    return _save(ImageOps.autocontrast(_to_image(img_bytes).convert("L")))


def _otsu(img_bytes: bytes) -> bytes:
    import cv2

    gray = np.array(ImageOps.autocontrast(_to_image(img_bytes).convert("L")))
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return _save(Image.fromarray(binary))


def _upscale2x_otsu(img_bytes: bytes) -> bytes:
    import cv2

    gray = np.array(ImageOps.autocontrast(_to_image(img_bytes).convert("L")))
    scaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, binary = cv2.threshold(scaled, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return _save(Image.fromarray(binary))


VARIANTS.update(
    {
        "raw": _raw,
        "gray": _gray,
        "otsu": _otsu,
        "upscale2x_otsu": _upscale2x_otsu,
    }
)


def apply_variant(img_bytes: bytes, variant: str) -> bytes:
    if variant in (None, "", "none"):
        return img_bytes
    if variant not in VARIANTS:
        raise KeyError(f"Tiền xử lý không hỗ trợ: {variant}. Hợp lệ: {', '.join(VARIANTS)}")
    return VARIANTS[variant](img_bytes)