"""Solver: nạp model một lần, giải ảnh captcha, hỗ trợ chuỗi fallback.

Dùng chung cho CLI và HTTP server. Mặc định chain:
    ddddocr/default -> ppocr_v6_small/rec_only(otsu)
Vì theo benchmark trên bộ 100 ảnh thự nghiệm:
    ddddocr/default  98% đúng, 22 ms/ảnh
    ppocr_v6_small   93% đúng (bắt buộc dùng biến thể otsu)
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .config import DEFAULT_CONFIG, DEFAULT_MODEL, DEFAULT_VARIANT
from .preprocess import apply_variant
from .registry import Prediction, build_registry, get_model, normalize

DEFAULT_CHAIN: list[dict[str, str]] = [
    {"model": "ddddocr", "config": "default", "variant": "raw"},
    {"model": "ppocr_v6_small", "config": "rec_only", "variant": "otsu"},
]


@dataclass
class SolveResult:
    text: str
    normalized: str
    model_id: str
    config_id: str
    variant: str
    elapsed_ms: float
    confidence: float | None
    raw_text: str
    attempts: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "normalized": self.normalized,
            "raw_text": self.raw_text,
            "model": self.model_id,
            "config": self.config_id,
            "variant": self.variant,
            "confidence": self.confidence,
            "elapsed_ms": self.elapsed_ms,
            "attempts": self.attempts,
        }


class Solver:
    """Giữ registry + cache engine; thread-safe nhờ khoá khi nạp model."""

    def __init__(self, registry: list | None = None) -> None:
        self.registry = registry if registry is not None else build_registry()
        self._lock = threading.Lock()
        self._engines_loaded: set[str] = set()

    # ---------------------------------------------------------------- model handling
    def _model(self, model_id: str):
        model = get_model(self.registry, model_id)
        if model.id not in self._engines_loaded:
            with self._lock:
                if model.id not in self._engines_loaded:
                    model.ensure_loaded()
                    self._engines_loaded.add(model.id)
        return model

    def warmup(self, model_id: str) -> None:
        self._model(model_id)

    def describe_models(self) -> list[dict[str, Any]]:
        return [model.describe() for model in self.registry]

    def _run_once(self, model_id: str, config_id: str, variant: str, img_bytes: bytes) -> tuple[Prediction, float, str]:
        model = self._model(model_id)
        if not config_id or config_id not in model.configs:
            # Không bắt người dùng phải nhớ config của từng model (PP-OCR chỉ có rec_only).
            config_id = next(iter(model.configs))
        params = model.configs[config_id]
        prepared = apply_variant(img_bytes, variant)
        started = time.perf_counter()
        prediction = model.predict(prepared, params)
        return prediction, (time.perf_counter() - started) * 1000, config_id

    # ---------------------------------------------------------------- public API
    def solve(
        self,
        image: bytes | str | Path,
        chain: Iterable[dict[str, str]] | None = None,
        expect_length: int | None = None,
    ) -> SolveResult:
        img_bytes = _read(image)
        steps = list(chain) if chain is not None else _default_chain()

        attempts: list[dict[str, Any]] = []
        last: SolveResult | None = None

        for step in steps:
            try:
                prediction, elapsed, used_config = self._run_once(
                    step["model"], step.get("config", ""), step.get("variant", "raw"), img_bytes
                )
            except Exception as error:  # noqa: BLE001 - thử bước tiếp theo
                attempts.append(
                    {"model": step["model"], "config": step["config"], "error": f"{type(error).__name__}: {error}"}
                )
                continue

            normalized = normalize(prediction.text)
            attempts.append(
                {
                    "model": step["model"],
                    "config": used_config,
                    "variant": step.get("variant", "raw"),
                    "text": normalized,
                    "raw_text": prediction.text,
                    "confidence": prediction.confidence,
                    "elapsed_ms": round(elapsed, 2),
                }
            )
            last = SolveResult(
                text=prediction.text,
                normalized=normalized,
                model_id=step["model"],
                config_id=used_config,
                variant=step.get("variant", "raw"),
                elapsed_ms=round(elapsed, 2),
                confidence=prediction.confidence,
                raw_text=prediction.text,
                attempts=attempts,
            )

            # Hợp lệ khi đủ độ dài mong muốn (nếu có yêu cầu) -> dừng chain
            if expect_length is None or len(normalized) == expect_length:
                return last

        if last is None:
            raise RuntimeError(f"Không model nào chạy được: {attempts}")
        return last

    def solve_batch(
        self,
        images: Iterable[bytes | str | Path],
        chain: Iterable[dict[str, str]] | None = None,
        expect_length: int | None = None,
    ) -> list[SolveResult]:
        return [self.solve(image, chain=chain, expect_length=expect_length) for image in images]


def _read(image: bytes | str | Path) -> bytes:
    if isinstance(image, (bytes, bytearray)):
        return bytes(image)
    return Path(image).read_bytes()


def _default_chain() -> list[dict[str, str]]:
    if not DEFAULT_MODEL:
        return DEFAULT_CHAIN
    return [{"model": DEFAULT_MODEL, "config": DEFAULT_CONFIG or "default", "variant": DEFAULT_VARIANT}]