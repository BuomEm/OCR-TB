"""HTTP server cho OCR-TB (FastAPI + uvicorn).

    ocr-tb serve --host 0.0.0.0 --port 8080

Endpoint
    GET  /health              trạng thái, phiên bản, model đã nạp
    GET  /models              danh sách model + config + trạng thái cache
    POST /models/pull         tải model còn thiếu về cache
    POST /solve               1 ảnh, JSON base64
    POST /solve/upload        1 ảnh, multipart upload
    POST /solve/batch         nhiều ảnh, JSON base64
    POST /normalize           chuẩn hoá chuỗi về charset captcha

Lưu ý kỹ thuật: file này dùng `from __future__ import annotations`, nên FastAPI
phải resolve được tên kiểu ở module scope. Vì vậy import FastAPI/Pydantic và
khai báo request model đều nằm ở cấp module, không import trong hàm.
"""

from __future__ import annotations

import asyncio
import base64
import binascii
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, Any

from .config import APP_NAME, VERSION, describe_paths
from .download import cache_status, missing_models, pull_all
from .registry import normalize
from .solver import DEFAULT_CHAIN, Solver

try:
    from fastapi import FastAPI, File, Form, HTTPException, UploadFile
    from pydantic import BaseModel

    SERVER_AVAILABLE = True
    SERVER_IMPORT_ERROR = ""
except ImportError as error:  # pragma: no cover
    SERVER_AVAILABLE = False
    SERVER_IMPORT_ERROR = str(error)
    FastAPI = Any  # type: ignore[assignment,misc]
    BaseModel = object  # type: ignore[assignment,misc]


class SolveRequest(BaseModel if SERVER_AVAILABLE else object):  # type: ignore[misc]
    image_base64: str
    model: str | None = None
    config: str | None = None
    variant: str | None = None
    expect_length: int | None = None


class BatchRequest(BaseModel if SERVER_AVAILABLE else object):  # type: ignore[misc]
    images_base64: list[str]
    model: str | None = None
    config: str | None = None
    variant: str | None = None
    expect_length: int | None = None


def _require_server() -> None:
    if not SERVER_AVAILABLE:  # pragma: no cover
        raise SystemExit(
            "Thiếu FastAPI/uvicorn. Cài phần server: pip install 'ocr-tb[server]' "
            f"({SERVER_IMPORT_ERROR})"
        )


def create_app(solver: Solver | None = None, max_workers: int = 4) -> Any:
    _require_server()

    solver = solver or Solver()
    pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="ocr")
    app = FastAPI(title=f"{APP_NAME} HTTP API", version=VERSION, docs_url="/docs")
    app.state.solver = solver

    def build_chain(model: str | None, config: str | None, variant: str | None) -> list[dict[str, str]] | None:
        if not model:
            return None
        return [{"model": model, "config": config or "default", "variant": variant or "raw"}]

    def decode_base64(payload: str) -> bytes:
        raw = payload.split(",", 1)[1] if payload.startswith("data:") else payload
        try:
            return base64.b64decode(raw, validate=False)
        except (binascii.Error, ValueError) as error:
            raise HTTPException(status_code=400, detail=f"base64 không hợp lệ: {error}") from error

    async def run_solve(data: bytes, chain, expect_length: int | None):
        loop = asyncio.get_running_loop()
        try:
            return await loop.run_in_executor(pool, lambda: solver.solve(data, chain, expect_length))
        except HTTPException:
            raise
        except Exception as error:  # noqa: BLE001
            raise HTTPException(status_code=500, detail=f"{type(error).__name__}: {error}") from error

    # ------------------------------------------------------------------ endpoints
    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "app": APP_NAME,
            "version": VERSION,
            "paths": describe_paths(),
            "models": [model.describe() for model in solver.registry],
            "missing_downloads": missing_models(),
        }

    @app.get("/models")
    async def models() -> dict[str, Any]:
        return {
            "models": solver.describe_models(),
            "cache": cache_status(),
            "default_chain": DEFAULT_CHAIN,
        }

    @app.post("/models/pull")
    async def models_pull() -> dict[str, Any]:
        loop = asyncio.get_running_loop()
        pulled = await loop.run_in_executor(pool, pull_all)
        return {"pulled": pulled, "cache": cache_status()}

    @app.post("/solve")
    async def solve_json(request: SolveRequest) -> dict[str, Any]:
        data = decode_base64(request.image_base64)
        chain = build_chain(request.model, request.config, request.variant)
        result = await run_solve(data, chain, request.expect_length)
        return result.to_dict()

    @app.post("/solve/upload")
    async def solve_upload(
        file: Annotated[UploadFile, File(description="Ảnh captcha")],
        model: Annotated[str | None, Form()] = None,
        config: Annotated[str | None, Form()] = None,
        variant: Annotated[str | None, Form()] = None,
        expect_length: Annotated[int | None, Form()] = None,
    ) -> dict[str, Any]:
        data = await file.read()
        if not data:
            raise HTTPException(status_code=400, detail="file rỗng")
        chain = build_chain(model, config, variant)
        result = await run_solve(data, chain, expect_length)
        return result.to_dict()

    @app.post("/solve/batch")
    async def solve_batch(request: BatchRequest) -> dict[str, Any]:
        if not request.images_base64:
            raise HTTPException(status_code=400, detail="images_base64 rỗng")
        chain = build_chain(request.model, request.config, request.variant)
        results = []
        for payload in request.images_base64:
            data = decode_base64(payload)
            results.append((await run_solve(data, chain, request.expect_length)).to_dict())
        return {"count": len(results), "results": results}

    @app.post("/normalize")
    async def only_normalize(payload: dict[str, str]) -> dict[str, str]:
        return {"normalized": normalize(payload.get("text", ""))}

    return app


def run(host: str, port: int, workers_threads: int = 4) -> None:  # pragma: no cover
    _require_server()
    import uvicorn

    uvicorn.run(create_app(max_workers=workers_threads), host=host, port=port, log_level="info")