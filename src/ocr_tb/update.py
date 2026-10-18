"""Kiểm tra và cập nhật OCR-TB từ GitHub Releases.

Ba kịch bản cài đặt được hỗ trợ, phân biệt qua `install-meta.json`:

    {"method": "pypi",    "version": "1.0.0"}
    {"method": "script",  "repo_dir": "/opt/ocr-tb-src"}
    {"method": "source",  "repo_dir": "/home/me/OCR-TB"}

    ocr-tb update --check    # chỉ báo có bản mới không (không thay đổi gì)
    ocr-tb update            # cập nhật theo đúng cách cài đặt đang dùng
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .config import APP_NAME, CACHE_DIR, DATA_DIR

REPO = os.environ.get("OCR_TB_REPO", "BuomEm/OCR-TB")
GITHUB_API = "https://api.github.com"
CHECK_TIMEOUT_S = float(os.environ.get("OCR_TB_CHECK_TIMEOUT", "5"))
CACHE_FILE = CACHE_DIR / "update-check.json"
CACHE_TTL_S = 24 * 3600

INSTALL_META = {  # tên file đọc/ghi ở thư mục gốc OCR_TB_HOME
    "pypi": "install-meta.json",
}


# --------------------------------------------------------------------------- version
def current_version() -> str:
    """Phiên bản đang chạy: ưu tiên metadata của package, fallback về config."""
    try:
        from importlib.metadata import PackageNotFoundError, version

        return version(APP_NAME)
    except Exception:  # noqa: BLE001
        from .config import VERSION

        return VERSION


def _parse(version_text: str) -> tuple[int, ...]:
    cleaned = (version_text or "").strip().lstrip("vV")
    parts = []
    for chunk in cleaned.split("."):
        digits = "".join(c for c in chunk if c.isdigit())
        parts.append(int(digits) if digits else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def is_newer(candidate: str, current: str) -> bool:
    return _parse(candidate) > _parse(current)


# --------------------------------------------------------------------------- install meta
def meta_path() -> Path:
    return DATA_DIR.parent / "install-meta.json"


def read_install_meta() -> dict[str, Any]:
    path = meta_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def write_install_meta(meta: dict[str, Any]) -> Path:
    path = meta_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def detect_method() -> dict[str, Any]:
    """Suy ra cách cài đặt khi thiếu install-meta.json."""
    meta = read_install_meta()
    if meta.get("method"):
        return meta

    package_dir = Path(__file__).resolve().parent
    if str(package_dir).endswith("site-packages/ocr_tb") or "site-packages" in str(package_dir):
        # pip từ PyPI hoặc từ thư mục cục bộ đã build
        return {"method": "pypi", "detected": True}
    for parent in package_dir.parents:
        if (parent / "pyproject.toml").exists():
            return {"method": "source", "repo_dir": str(parent), "detected": True}
    return {"method": "unknown", "detected": True}


# --------------------------------------------------------------------------- GitHub
def fetch_latest_release(use_cache: bool = False, force: bool = False) -> dict[str, Any] | None:
    """Lấy release mới nhất từ GitHub API (có cache 24h để không gọi nhiều)."""
    if use_cache and not force and CACHE_FILE.exists():
        try:
            cached = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            if time.time() - float(cached.get("checked_at", 0)) < CACHE_TTL_S:
                return cached.get("release")
        except Exception:  # noqa: BLE001
            pass

    import requests

    try:
        response = requests.get(
            f"{GITHUB_API}/repos/{REPO}/releases/latest",
            timeout=CHECK_TIMEOUT_S,
            headers={"Accept": "application/vnd.github+json"},
        )
        if response.status_code != 200:
            return None
        data = response.json()
    except Exception:  # noqa: BLE001 - lỗi mạng không được làm hỏng luồng chính
        return None

    release = {
        "version": str(data.get("tag_name", "")).lstrip("vV"),
        "name": data.get("name") or "",
        "url": data.get("html_url", ""),
        "published_at": data.get("published_at", ""),
        "notes": (data.get("body") or "")[:2000],
    }
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(
            json.dumps({"checked_at": time.time(), "release": release}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:  # noqa: BLE001
        pass
    return release


def check_status() -> dict[str, Any]:
    current = current_version()
    latest = fetch_latest_release()
    if not latest or not latest.get("version"):
        return {
            "current": current,
            "latest": None,
            "update_available": None,
            "message": "Chưa có release nào trên GitHub, hoặc không kết nối được mạng",
        }
    newer = is_newer(latest["version"], current)
    return {
        "current": current,
        "latest": latest,
        "update_available": newer,
        "message": (
            f"Có bản mới: {current} -> {latest['version']}" if newer else f"Đang mới nhất ({current})"
        ),
    }


def update_notice() -> str | None:
    """Thông báo ngắn cho server log, dùng cache, không chặn, không log khi CI."""
    if os.environ.get("OCR_TB_CHECK_UPDATE", "").lower() in {"0", "false", "off"}:
        return None
    if os.environ.get("GITHUB_ACTIONS") or os.environ.get("CI"):
        return None
    status = check_status()
    if status.get("update_available"):
        return f"{APP_NAME}: có bản mới {status['latest']['version']} (đang chạy {status['current']}) — chạy `ocr-tb update`"
    return None


# --------------------------------------------------------------------------- update
def _run(command: list[str], dry_run: bool = False) -> tuple[int, str]:
    printable = " ".join(command)
    if dry_run:
        return 0, f"[dry-run] {printable}"
    print(f"$ {printable}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=1800)
    except FileNotFoundError as error:
        return 1, str(error)
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output.strip()


def _pip_upgrade(package: str = APP_NAME, dry_run: bool = False) -> tuple[int, str]:
    return _run([sys.executable, "-m", "pip", "install", "--upgrade", package], dry_run)


def apply_update(assume_yes: bool = False, dry_run: bool = False) -> int:
    """Cập nhật theo đúng cách cài đặt đang dùng. Trả về exit code."""
    meta = detect_method()
    method = meta.get("method", "unknown")
    repo_dir = meta.get("repo_dir") or str(Path(__file__).resolve().parents[2])

    if method == "script":
        repo_dir = repo_dir if Path(repo_dir).exists() else str(Path(__file__).resolve().parents[2])
        code, output = _run(["git", "-C", repo_dir, "pull", "--ff-only"], dry_run)
        if code != 0 and not dry_run:
            print(f"Không `git pull` được ({output}). Cài lại bằng install.sh/install.ps1.", file=sys.stderr)
            return code
        script = Path(repo_dir) / ("install.ps1" if os.name == "nt" else "install.sh")
        if not script.exists():
            print(f"Không tìm thấy {script}. Hãy chạy lại script cài đặt.", file=sys.stderr)
            return 1
        command = (
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), "-Force"]
            if os.name == "nt"
            else ["bash", str(script), "--force"]
        )
        code, output = _run(command, dry_run)
        if output and not dry_run:
            print(output[-2000:])
        return code

    if method == "source":
        code, output = _run(["git", "-C", repo_dir, "pull", "--ff-only"], dry_run)
        if code != 0:
            if not dry_run:
                print(output, file=sys.stderr)
            return code
        return _run([sys.executable, "-m", "pip", "install", "-e", repo_dir], dry_run)

    if method == "pypi":
        return _pip_upgrade(dry_run=dry_run)[0] if dry_run else _pip_upgrade()[0]

    if not assume_yes:
        print(
            "Không xác định được cách cài đặt.\n"
            f"  - nếu cài bằng pip từ PyPI:  {sys.executable} -m pip install --upgrade {APP_NAME}\n"
            f"  - nếu cài bằng script:        chạy lại install.sh / install.ps1\n"
            f"  - nếu cài từ mã nguồn:       git pull trong thư mục đã clone rồi pip install -e .",
            file=sys.stderr,
        )
        return 2

    code, _ = _pip_upgrade()
    return code


def record_install(method: str, repo_dir: str | None = None, extra: dict[str, Any] | None = None) -> Path:
    """Dùng bởi install.sh / install.ps1 để ghi lại cách cài đặt."""
    meta = {
        "method": method,
        "repo_dir": repo_dir,
        "version": current_version(),
        "installed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "python": sys.executable,
        "platform": os.name,
    }
    if extra:
        meta.update(extra)
    return write_install_meta(meta)


def _executable(name: str) -> bool:
    return shutil.which(name) is not None