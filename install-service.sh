#!/usr/bin/env bash
# Cài OCR-TB dạng systemd service (chạy sau install.sh với quyền sudo).
#
#   sudo bash install-service.sh
set -euo pipefail

PREFIX="${OCR_TB_PREFIX:-/opt/ocr-tb}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_USER="${SERVICE_USER:-ocr-tb}"

if [ ! -x "$PREFIX/venv/bin/ocr-tb" ]; then
  echo "Chưa cài OCR-TB tại $PREFIX. Chạy install.sh trước." >&2
  exit 1
fi

if ! id -u "$SERVICE_USER" >/dev/null 2>&1; then
  echo "Tạo user hệ thống $SERVICE_USER"
  useradd --system --home-dir "$PREFIX" --shell /usr/sbin/nologin "$SERVICE_USER"
fi
chown -R "$SERVICE_USER:$SERVICE_USER" "$PREFIX"

install -m 0644 "$SCRIPT_DIR/ocr-tb.service" /etc/systemd/system/ocr-tb.service
systemctl daemon-reload
systemctl enable --now ocr-tb
systemctl --no-pager status ocr-tb || true

cat <<EOF

Đã bật service. Kiểm tra:
  curl -s http://127.0.0.1:8080/health
  journalctl -u ocr-tb -f
EOF