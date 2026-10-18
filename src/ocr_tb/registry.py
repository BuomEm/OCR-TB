"""Registry các mô hình OCR dùng trong OCR-TB.

Mỗi model có nhiều "config" (tổ hợp tham số). Việc nạp model là lazy và chỉ
xảy ra một lần cho mỗi engine, phục vụ cả CLI lẫn HTTP server.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import model_dir

# --------------------------------------------------------------------------------------
# Chuẩn hoá kết quả
# --------------------------------------------------------------------------------------


def normalize(text: str | None) -> str:
    """Giữ đúng charset captcha: lowercase, bỏ ký tự ngoài [0-9a-z]."""
    import re

    return re.sub(r"[^0-9a-z]", "", (text or "").lower())


@dataclass
class Prediction:
    text: str
    confidence: float | None = None
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunSpec:
    model_id: str
    model_label: str
    config_id: str
    params: dict[str, Any]


# --------------------------------------------------------------------------------------
# Lớp nền
# --------------------------------------------------------------------------------------
class OcrModel:
    id: str = ""
    label: str = ""
    vendor: str = ""
    source: str = ""
    #: True nếu model nằm trong package cài đặt, không cần tải thêm.
    builtin: bool = True
    configs: dict[str, dict[str, Any]] = {}

    def __init__(self) -> None:
        self.loaded = False
        self.load_error: str | None = None
        self.load_ms: float = 0.0

    def load(self) -> None:
        raise NotImplementedError

    def predict(self, img_bytes: bytes, params: dict[str, Any]) -> Prediction:
        raise NotImplementedError

    def close(self) -> None:
        return None

    def ensure_loaded(self) -> None:
        if self.loaded:
            return
        started = time.perf_counter()
        try:
            self.load()
            self.loaded = True
        except Exception as error:  # noqa: BLE001 - ghi lý do rồi báo ra ngoài
            self.load_error = f"{type(error).__name__}: {error}"
            raise
        finally:
            self.load_ms = round((time.perf_counter() - started) * 1000, 2)

    def describe(self) -> dict[str, Any]:
        return {
            "model_id": self.id,
            "label": self.label,
            "vendor": self.vendor,
            "source": self.source,
            "builtin": self.builtin,
            "configs": self.configs,
            "loaded": self.loaded,
            "load_ms": self.load_ms,
            "load_error": self.load_error,
        }


# --------------------------------------------------------------------------------------
# ddddocr
# --------------------------------------------------------------------------------------
class DdddOcrModel(OcrModel):
    id = "ddddocr"
    label = "ddddocr (ONNX, không detection)"
    vendor = "sml2h3/ddddocr"
    source = "pip ddddocr (common.onnx / common_old.onnx)"

    configs = {
        "default": {"old": False, "charset_range": None},
        "old": {"old": True, "charset_range": None},
        "alnum": {"old": False, "charset_range": list("0123456789abcdefghijklmnopqrstuvwxyz")},
    }

    def __init__(self) -> None:
        super().__init__()
        self._engines: dict[bool, Any] = {}

    def load(self) -> None:
        import ddddocr

        self._ddddocr = ddddocr

    def _engine(self, old: bool):
        if old not in self._engines:
            self._engines[old] = self._ddddocr.DdddOcr(show_ad=False, old=old)
        return self._engines[old]

    def predict(self, img_bytes: bytes, params: dict[str, Any]) -> Prediction:
        engine = self._engine(bool(params.get("old")))
        charset_range = params.get("charset_range")
        if charset_range:
            engine.set_ranges(list(charset_range))
        text = engine.classification(img_bytes)
        return Prediction(text=text, confidence=None, detail={"charset_range": "alnum" if charset_range else "full"})


# --------------------------------------------------------------------------------------
# PP-OCR qua RapidOCR (rec-only)
# --------------------------------------------------------------------------------------
class RapidOcrModel(OcrModel):
    """RapidOCR chạy model rec-only (tắt detection) cho ảnh captcha 1 dòng."""

    def __init__(
        self,
        id: str,
        label: str,
        remote_id: str,
        source: str,
    ) -> None:
        super().__init__()
        self.id = id
        self.label = label
        self.vendor = "PaddlePaddle (ONNX export)"
        self.source = source
        self.remote_id = remote_id
        self.builtin = False
        self.configs = {"rec_only": {}}

    @property
    def model_path(self) -> Path:
        return model_dir(self.remote_id)

    def load(self) -> None:
        from rapidocr_onnxruntime import RapidOCR, rapid_ocr_api

        rec_path = self.model_path / "inference.onnx"
        keys_path = self.model_path / "ppocr_keys.txt"
        if not rec_path.exists() or not keys_path.exists():
            raise FileNotFoundError(
                f"Thiếu model {self.id}. Chạy `ocr-tb models pull {self.remote_id}`."
            )

        # RapidOCR 1.2.3 chỉ đọc character dict qua config key "keys_path", mà kwargs
        # phẳng không map được key đó -> dựng config.yaml riêng rồi trỏ root_dir tạm.
        import yaml
        from rapidocr_onnxruntime import utils as rapid_utils

        cfg_dir = self.model_path / "_rapidocr_cfg"
        cfg_dir.mkdir(parents=True, exist_ok=True)
        base_cfg = yaml.safe_load((Path(rapid_utils.root_dir) / "config.yaml").read_text(encoding="utf-8"))
        base_cfg["Global"].update(
            {
                "use_text_det": False,
                "use_angle_cls": False,
                "print_verbose": False,
                "text_score": 0.0,
                "min_height": 48,
            }
        )
        base_cfg["Rec"].update(
            {
                "model_path": str(rec_path),
                "keys_path": str(keys_path),
                "rec_img_shape": [3, 48, 320],
                "rec_batch_num": 6,
            }
        )
        (cfg_dir / "config.yaml").write_text(yaml.safe_dump(base_cfg, allow_unicode=True), encoding="utf-8")

        original_root = rapid_ocr_api.root_dir
        rapid_ocr_api.root_dir = cfg_dir
        try:
            self._engine = RapidOCR()
        finally:
            rapid_ocr_api.root_dir = original_root

    def predict(self, img_bytes: bytes, params: dict[str, Any]) -> Prediction:
        result, _elapse = self._engine(img_bytes)
        if not result:
            return Prediction(text="", confidence=None, detail={"boxes": 0})

        entries: list[tuple[str, float | None]] = []
        for item in result:
            if isinstance(item, (list, tuple)) and len(item) >= 3:
                entries.append((str(item[1]), float(item[2]) if item[2] is not None else None))
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                entries.append((str(item[0]), float(item[1]) if item[1] is not None else None))
            else:
                entries.append((str(item), None))

        text = "".join(value for value, _ in entries)
        scores = [score for _, score in entries if score is not None]
        return Prediction(
            text=text,
            confidence=round(sum(scores) / len(scores), 6) if scores else None,
            detail={"boxes": len(entries)},
        )


# --------------------------------------------------------------------------------------
# Tesseract
# --------------------------------------------------------------------------------------
class TesseractModel(OcrModel):
    id = "tesseract5"
    label = "Tesseract 5 (CPU, --psm)"
    vendor = "tesseract-ocr"
    source = "apt install tesseract-ocr (hoặc binary trong PATH)"

    configs = {
        "psm8_whitelist": {"config": "--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789"},
        "psm13_raw": {"config": "--psm 13"},
        "psm7_whitelist": {
            "config": "--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789"
        },
        "psm7_raw": {"config": "--psm 7"},
        "psm6_whitelist": {
            "config": "--psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789"
        },
    }

    def load(self) -> None:
        import pytesseract

        exe = self.find_tesseract()
        if exe:
            pytesseract.pytesseract.tesseract_cmd = str(exe)
        self._pytesseract = pytesseract
        if not self.version():
            raise RuntimeError("Không tìm thấy tesseract binary. Cài `apt install tesseract-ocr`.")

    @staticmethod
    def find_tesseract() -> Path | None:
        candidates = [
            os.environ.get("TESSERACT_CMD"),
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract",
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        ]
        for candidate in candidates:
            if candidate and Path(candidate).exists():
                return Path(candidate)
        found = shutil.which("tesseract")
        return Path(found) if found else None

    @staticmethod
    def version() -> str:
        exe = TesseractModel.find_tesseract()
        if not exe:
            return ""
        try:
            result = subprocess.run([str(exe), "--version"], capture_output=True, text=True, timeout=20)
            return result.stdout.strip().splitlines()[0] if result.stdout else ""
        except Exception:  # noqa: BLE001
            return ""

    def predict(self, img_bytes: bytes, params: dict[str, Any]) -> Prediction:
        import io

        from PIL import Image

        image = Image.open(io.BytesIO(img_bytes))
        text = self._pytesseract.image_to_string(
            image, config=params.get("config", "--psm 8"), lang=params.get("lang", "eng")
        )
        return Prediction(text=text.strip(), confidence=None, detail={"psm": params.get("config", "--psm 8")})


# --------------------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------------------
def build_registry() -> list[OcrModel]:
    return [
        DdddOcrModel(),
        RapidOcrModel(
            id="ppocr_v5_en",
            label="PP-OCRv5 English mobile rec (ONNX)",
            remote_id="ppocr_v5_en",
            source="huggingface.co/PaddlePaddle/en_PP-OCRv5_mobile_rec_onnx",
        ),
        RapidOcrModel(
            id="ppocr_v6_small",
            label="PP-OCRv6 small rec (ONNX)",
            remote_id="ppocr_v6_small",
            source="huggingface.co/PaddlePaddle/PP-OCRv6_small_rec_onnx",
        ),
        TesseractModel(),
    ]


def expand_runs(
    registry: list[OcrModel],
    model_ids: list[str] | None = None,
    configs: dict[str, list[str]] | None = None,
) -> list[RunSpec]:
    configs = configs or {}
    runs: list[RunSpec] = []
    for model in registry:
        if model_ids and model.id not in model_ids:
            continue
        for config_id, params in model.configs.items():
            wanted = configs.get(model.id)
            if wanted and config_id not in wanted:
                continue
            runs.append(RunSpec(model.id, model.label, config_id, params))
    return runs


def get_model(registry: list[OcrModel], model_id: str) -> OcrModel:
    for model in registry:
        if model.id == model_id:
            return model
    raise KeyError(f"Không có model '{model_id}'. Có: {', '.join(m.id for m in registry)}")