#!/usr/bin/env bash
# Cài OCR-TB trên Ubuntu 22.04 / 24.04 (cũng chạy được trên WSL Ubuntu).
#
#   sudo bash install.sh              # cài vào /opt/ocr-tb, tạo user ocr-tb
#   bash install.sh --user-only       # cài cho user hiện tại, không cần sudo
#   bash install.sh --no-server       # bỏ FastAPI/uvicorn (chỉ CLI)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="${OCR_TB_PREFIX:-/opt/ocr-tb}"
WITH_SERVER=1
USER_ONLY=0

for arg in "$@"; do
  case "$arg" in
    --no-server) WITH_SERVER=0 ;;
    --user-only) USER_ONLY=1 ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "Tham số lạ: $arg"; exit 1 ;;
  esac
done

PY="${PYTHON:-python3}"
MIN_MINOR=10
MAX_MINOR=13

echo "==> Kiểm tra phiên bản Python"
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "Không tìm thấy python3. Cài bằng: sudo apt install -y python3 python3-venv" >&2
  exit 1
fi
if ! "$PY" -c "import sys; raise SystemExit(0 if ($MIN_MINOR <= sys.version_info.minor <= $MAX_MINOR) else 1)"; then
  echo "Cần Python 3.${MIN_MINOR} - 3.${MAX_MINOR}, hiện tại: $($PY --version)" >&2
  exit 1
fi
"$PY" --version

if [ "$USER_ONLY" -eq 1 ]; then
  PREFIX="$HOME/.local/share/ocr-tb"
  mkdir -p "$PREFIX"
fi

echo "==> Tạo virtualenv tại $PREFIX/venv"
"$PY" -m venv "$PREFIX/venv"
VENV_PY="$PREFIX/venv/bin/python"

echo "==> Nâng pip và cài OCR-TB"
"$VENV_PY" -m pip install --upgrade pip setuptools wheel >/dev/null
if [ "$WITH_SERVER" -eq 1 ]; then
  "$VENV_PY" -m pip install "$SCRIPT_DIR[server]"
else
  "$VENV_PY" -m pip install "$SCRIPT_DIR"
fi

echo "==> Kiểm tra Tesseract (tuỳ chọn, chỉ cần cho benchmark)"
if command -v tesseract >/dev/null 2>&1; then
  tesseract --version | head -n 1
else
  echo "  Chưa có. Cài bằng: sudo apt install -y tesseract-ocr"
fi

echo "==> Kiểm tra thư viện hệ thống cho OpenCV"
if ! "$VENV_PY" -c "import cv2" >/dev/null 2>&1; then
  echo "  OpenCV không import được. Cài thư viện hệ thống rồi chạy lại:"
  echo "    sudo apt install -y libgl1 libglib2.0-0"
else
  echo "  OK"
fi

export OCR_TB_HOME="$PREFIX"
export OCR_TB_CACHE="$PREFIX/models"

echo "==> Tải model ONNX vào cache"
"$VENV_PY" -m ocr_tb models pull

BIN_DIR="/usr/local/bin"
if [ "$USER_ONLY" -eq 1 ]; then
  BIN_DIR="$HOME/.local/bin"
  mkdir -p "$BIN_DIR"
fi

# Wrapper script thay cho symlink trực tiếp tới binary python:
# symlink tới python sẽ mở REPL thay vì chạy CLI.
WRAPPER="$BIN_DIR/ocr-tb"
cat > "$WRAPPER" <<EOF
#!/usr/bin/env bash
exec "$VENV_PY" -m ocr_tb "\$@"
EOF
chmod +x "$WRAPPER"
echo "==> Đã tạo lệnh: $WRAPPER"

cat <<EOF

Cài xong. Kiểm tra nhanh:
  ocr-tb info
  ocr-tb solve /duong/dan/anh-captcha.png
  ocr-tb serve --host 0.0.0.0 --port 8080

Cache model: $OCR_TB_CACHE
Dữ liệu (benchmark/labels): ${OCR_TB_HOME:-$PREFIX}/data
EOF