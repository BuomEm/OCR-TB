"""Test cho OCR-TB. Chạy: pytest tools/ocr-tb/tests -q

Các test không cần mạng: ddddocr đi kèm trong package pip, model PP-OCR được
bỏ qua nếu chưa tải về cache.
"""

from __future__ import annotations

import base64
import io
import json
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

SAMPLES_DIR = Path(__file__).resolve().parents[1] / "samples"

from ocr_tb.config import REMOTE_MODELS, ensure_dirs  # noqa: E402
from ocr_tb.download import cache_status, is_cached  # noqa: E402
from ocr_tb.preprocess import VARIANTS, apply_variant  # noqa: E402
from ocr_tb.registry import build_registry, normalize  # noqa: E402
from ocr_tb.util import char_similarity, levenshtein, percentile, stats  # noqa: E402


def make_captcha_png(text: str = "abcd") -> bytes:
    """Sinh ảnh captcha giả (chữ đen trên nền trắng) để test không cần dữ liệu thật."""
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (200, 50), "white")
    draw = ImageDraw.Draw(image)
    draw.text((40, 12), text, fill="black")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


# --------------------------------------------------------------------- normalize
@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Ab3D", "ab3d"),
        (" e7k7 ", "e7k7"),
        ("| >cate—", "cate"),
        ("x3dkb", "x3dkb"),
        ("", ""),
        (None, ""),
    ],
)
def test_normalize(raw, expected):
    assert normalize(raw) == expected


# --------------------------------------------------------------------- util
def test_levenshtein_and_similarity():
    assert levenshtein("abc", "abc") == 0
    assert levenshtein("abc", "abd") == 1
    assert levenshtein("", "abcd") == 4
    assert char_similarity("abcd", "abcd") == 1.0
    assert 0 < char_similarity("abcd", "abxd") < 1.0


def test_percentile_and_stats():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert percentile(data, 0.5) == pytest.approx(5.5)
    summary = stats(data)
    assert summary["count"] == 10
    assert summary["mean"] == 5.5
    assert summary["max"] == 10
    assert stats([])["count"] == 0


# --------------------------------------------------------------------- preprocess
def test_all_variants_return_png():
    png = make_captcha_png("3b6a")
    for name in VARIANTS:
        out = apply_variant(png, name)
        assert out[:8] == b"\x89PNG\r\n\x1a\n", f"{name} không trả về PNG"
        assert len(out) > 0


def test_variant_empty_and_unknown():
    png = make_captcha_png()
    assert apply_variant(png, "none") == png
    assert apply_variant(png, "") == png
    with pytest.raises(KeyError):
        apply_variant(png, "khong-ton-tai")


# --------------------------------------------------------------------- download/cache
def test_cache_status_reports_all_remote_models():
    ensure_dirs()
    rows = cache_status()
    assert {row["model_id"] for row in rows} == set(REMOTE_MODELS)
    for row in rows:
        assert isinstance(row["cached"], bool)


def test_is_cached_false_when_empty(tmp_path, monkeypatch):
    monkeypatch.setattr("ocr_tb.download.model_dir", lambda model_id: tmp_path / model_id)
    assert is_cached("ppocr_v6_small") is False


# --------------------------------------------------------------------- registry
def test_registry_contains_expected_models():
    ids = {model.id for model in build_registry()}
    assert {"ddddocr", "ppocr_v5_en", "ppocr_v6_small", "tesseract5"} <= ids


def test_ddddocr_runs_offline():
    """Chỉ kiểm tra pipeline chạy được offline (ảnh giả không bảo đảm OCR đúng)."""
    from ocr_tb.solver import Solver

    solver = Solver()
    result = solver.solve(make_captcha_png("3b6a"))
    assert result.model_id == "ddddocr"
    assert isinstance(result.normalized, str)
    assert result.elapsed_ms >= 0


def test_ddddocr_reads_real_captcha():
    """Nếu trỏ OCR_TB_IMAGES tới ảnh thật thì kiểm tra độ dài đầu ra."""
    import os

    raw_dir = os.environ.get("OCR_TB_IMAGES")
    if not raw_dir:
        pytest.skip("Chưa đặt OCR_TB_IMAGES")
    image_dir = Path(raw_dir).expanduser()
    if not image_dir.exists():
        pytest.skip("OCR_TB_IMAGES không tồn tại")
    images = sorted(image_dir.glob("*.png"))[:5]
    if not images:
        pytest.skip("Thư mục ảnh không có file png")

    from ocr_tb.solver import Solver

    solver = Solver()
    lengths = [len(solver.solve(path.read_bytes(), expect_length=4).normalized) for path in images]
    # Benchmark thật đo 98% ảnh ra đúng 4 ký tự; để ngưỡng 80% cho test ổn định.
    ok = sum(1 for length in lengths if length == 4)
    assert ok >= 0.8 * len(lengths), f"ddddocr trả sai độ dài quá nhiều: {lengths}"


def test_solver_fallback_uses_second_model():
    """Nếu bước đầu lỗi thì chain phải thử bước sau và vẫn trả kết quả."""
    from ocr_tb.solver import Solver

    solver = Solver()
    chain = [
        {"model": "khong-ton-tai", "config": "default", "variant": "raw"},
        {"model": "ddddocr", "config": "default", "variant": "raw"},
    ]
    result = solver.solve(make_captcha_png("a1b2"), chain=chain)
    assert result.model_id == "ddddocr"
    assert any("error" in attempt for attempt in result.attempts)


def test_solver_unknown_model_raises():
    from ocr_tb.solver import Solver

    with pytest.raises(RuntimeError):
        Solver().solve(make_captcha_png(), chain=[{"model": "no-such-model", "config": "default", "variant": "raw"}])


def test_solver_picks_model_default_config():
    """Bỏ --config thì solver phải tự chọn config hợp lệ của model đó."""
    from ocr_tb.solver import Solver

    result = Solver().solve(make_captcha_png("a1b2"), chain=[{"model": "ddddocr", "variant": "raw"}])
    assert result.config_id in Solver().registry[0].configs


# --------------------------------------------------------------------- HTTP server
@pytest.fixture()
def client():
    fastapi_testclient = pytest.importorskip("fastapi.testclient")
    from ocr_tb.server import create_app

    return fastapi_testclient.TestClient(create_app())


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app"] == "ocr-tb"


def test_models_endpoint(client):
    body = client.get("/models").json()
    assert "models" in body and "default_chain" in body


def test_solve_json(client):
    payload = {"image_base64": base64.b64encode(make_captcha_png("3b6a")).decode(), "model": "ddddocr"}
    response = client.post("/solve", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "ddddocr"
    assert isinstance(body["normalized"], str)


def test_solve_upload(client):
    response = client.post(
        "/solve/upload", files={"file": ("c.png", make_captcha_png("a1b2"), "image/png")}, data={"model": "ddddocr"}
    )
    assert response.status_code == 200
    assert response.json()["model"] == "ddddocr"


def test_solve_batch(client):
    encoded = base64.b64encode(make_captcha_png("3b6a")).decode()
    body = client.post("/solve/batch", json={"images_base64": [encoded, encoded]}).json()
    assert body["count"] == 2
    assert len(body["results"]) == 2


def test_solve_invalid_base64(client):
    response = client.post("/solve", json={"image_base64": "!!!khong-hop-le!!!"})
    assert response.status_code in (400, 500)


def test_normalize_endpoint(client):
    assert client.post("/normalize", json={"text": "A7-b"}).json()["normalized"] == "a7b"


# --------------------------------------------------------------------- version / update
def test_current_version_matches_package_metadata():
    """version trong pyproject.toml và code phải khớp (workflow release kiểm tra việc này)."""
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as dist_version

    from ocr_tb.config import VERSION
    from ocr_tb.update import current_version

    try:
        installed = dist_version("ocr-tb")
    except PackageNotFoundError:
        pytest.skip("ocr-tb chưa được cài dưới dạng package")

    assert current_version() == installed
    assert VERSION == installed, "pyproject.toml và ocr_tb.config.VERSION đang lệch nhau"


@pytest.mark.parametrize(
    ("candidate", "current", "expected"),
    [
        ("1.0.1", "1.0.0", True),
        ("1.0.0", "1.0.0", False),
        ("v2.0.0", "1.9.9", True),
        ("0.9.9", "1.0.0", False),
        ("1.10.0", "1.9.0", True),
    ],
)
def test_is_newer(candidate, current, expected):
    from ocr_tb.update import is_newer

    assert is_newer(candidate, current) is expected


def test_install_meta_roundtrip(tmp_path, monkeypatch):
    from ocr_tb import update as update_module

    (tmp_path / "data").mkdir(parents=True)
    monkeypatch.setattr(update_module, "DATA_DIR", tmp_path / "data")

    update_module.write_install_meta({"method": "script", "repo_dir": "/tmp/ocr-tb"})
    meta = update_module.read_install_meta()
    assert meta["method"] == "script"
    assert meta["repo_dir"] == "/tmp/ocr-tb"


def test_check_status_handles_offline(monkeypatch):
    from ocr_tb import update as update_module

    monkeypatch.setattr(update_module, "fetch_latest_release", lambda *a, **k: None)
    status = update_module.check_status()
    assert status["update_available"] is None
    assert status["current"]


def test_update_dry_run_does_not_touch_system(monkeypatch):
    from ocr_tb import update as update_module

    monkeypatch.setattr(update_module, "read_install_meta", lambda: {"method": "pypi"})
    code, output = update_module._pip_upgrade(dry_run=True)
    assert code == 0
    assert "[dry-run]" in output


def test_update_notice_disabled_by_env(monkeypatch):
    from ocr_tb import update as update_module

    monkeypatch.setenv("OCR_TB_CHECK_UPDATE", "0")
    assert update_module.update_notice() is None


# --------------------------------------------------------------------- samples
def _sample_labels() -> list[dict]:
    if not (SAMPLES_DIR / "labels.json").exists():
        pytest.skip("Không có samples/labels.json")
    return json.loads((SAMPLES_DIR / "labels.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("sample", _sample_labels(), ids=lambda item: item["id"])
def test_solves_bundled_samples(sample):
    """Ảnh mẫu đi kèm repo: ddddocr/default phải đọc đúng."""
    image = SAMPLES_DIR / sample["file"]
    if not image.exists():
        pytest.skip("Thiếu ảnh mẫu")

    from ocr_tb.solver import Solver

    result = Solver().solve(image.read_bytes())
    assert result.model_id == "ddddocr"
    assert result.normalized == sample["expected"], (
        f"{sample['file']}: mong đợi {sample['expected']}, nhận {result.normalized}"
    )


def test_samples_files_are_present():
    labels = _sample_labels()
    assert len(labels) >= 3
    for sample in labels:
        assert (SAMPLES_DIR / sample["file"]).exists()