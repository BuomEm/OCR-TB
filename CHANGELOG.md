# Changelog

Mọi thay đổi đáng chú ý của OCR-TB được ghi lại tại đây.
Cấu trúc dựa theo [Keep a Changelog](https://keepachangelog.com/v1.1.0/) và
[Semantic Versioning](https://semver.org/lang/vi/).

## [1.0.0] - 2026-10-18

### Bản phát hành đầu tiên

#### Thêm
- `ocr-tb solve`: giải 1 hoặc nhiều ảnh captcha, hỗ trợ thư mục, `--json`.
- Chuỗi fallback: `ddddocr/default/raw` → `ppocr_v6_small/rec_only/otsu`,
  dừng sớm khi đạt `--expect-length`.
- HTTP server FastAPI: `GET /health`, `GET /models`, `POST /models/pull`,
  `POST /solve`, `POST /solve/upload`, `POST /solve/batch`, `POST /normalize`.
- Bộ benchmark: chạy nhiều model × config × biến thể tiền xử lý, ghi `rows.jsonl`,
  xuất báo cáo Markdown + CSV + JSON.
- Gán nhãn thủ công: `ocr-tb label make` sinh `labeling.html` (lưu localStorage, xuất CSV).
- Registry 4 model: `ddddocr`, `ppocr_v5_en`, `ppocr_v6_small`, `tesseract5`.
- Tiền xử lý ảnh: `raw`, `gray`, `otsu`, `upscale2x_otsu`.
- `ocr-tb memory`: đo RSS và dung lượng đĩa thực tế.
- Tải model ONNX về cache vĩnh viễn (`ocr-tb models pull`), hỗ trợ `HF_ENDPOINT`.
- Cài đặt: `install.sh` (Linux/macOS), `install.ps1` (Windows), `install-service.sh`
  (systemd), `Dockerfile` (python:3.12-slim, user không phải root).
- CI: test trên ubuntu/windows/macos × Python 3.11/3.12 + build và smoke test Docker.
- 3 ảnh captcha mẫu kèm nhãn trong `samples/`, dùng làm test hồi quy.

#### Kết quả đo (100 ảnh captcha ViettelPost, CPU)
- `ddddocr/alnum`: 99% chính xác, 59 ms/ảnh.
- `ddddocr/default`: 98% chính xác, 22 ms/ảnh — khuyến nghị.
- `ppocr_v6_small` + `otsu`: 93% chính xác, 25 ms/ảnh.
- `tesseract5 --psm 8`: 17% chính xác — không khả dụng cho captcha nhiễu nặng.

[1.0.0]: https://github.com/BuomEm/OCR-TB/releases/tag/v1.0.0