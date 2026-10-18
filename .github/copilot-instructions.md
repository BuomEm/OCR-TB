# Hướng dẫn cho bot review tự động (GitHub Copilot code review) và cho AI assistant.

## Dự án là gì

OCR-TB là công cụ Python giải captcha OCR. Nó gọi mô hình nhận dạng ký tự
(ddddocr, PP-OCR, Tesseract) trên ảnh captcha ngắn và trả về chuỗi đã chuẩn hoá
về charset `[0-9a-z]`.

## Bố cục mã nguồn

- `src/ocr_tb/registry.py` — định nghĩa các model OCR. Thêm model = thêm class kế thừa `OcrModel`.
- `src/ocr_tb/solver.py` — nạp model một lần, chuỗi fallback, chuẩn hoá kết quả.
- `src/ocr_tb/preprocess.py` — biến thể tiền xử lý ảnh (raw/gray/otsu/upscale2x_otsu).
- `src/ocr_tb/server.py` — HTTP API FastAPI. Endpoint nằm trong `create_app()`.
- `src/ocr_tb/bench.py` — chạy benchmark, chấm điểm theo nhãn tay, xuất báo cáo.
- `src/ocr_tb/cli.py` — định nghĩa lệnh CLI bằng argparse.
- `src/ocr_tb/update.py` — kiểm tra và cập nhật phiên bản từ GitHub Releases.
- `tests/test_ocr_tb.py` — test phải chạy được offline, không tải model mạng.

## Quy tắc bắt buộc

1. Python 3.10–3.13, không dùng cú pháp mới hơn 3.10.
2. Mọi code chạy được trên Windows, Linux và macOS — không hard-code đường dẫn theo hệ điều hành.
3. Thêm dependency mới phải cập nhật `pyproject.toml` và README.
4. Mọi thay đổi hành vi (port mặc định, định dạng output, endpoint) phải ghi vào `CHANGELOG.md`.
5. Code chạy trong HTTP server phải an toàn với nhiều luồng (thread pool).
6. Test mới không được phụ thuộc mạng; nếu cần model chưa tải thì `pytest.skip`.
7. Vòng lặp OCR không được chặn vô hạn; luôn có giới hạn thời gian.

## Lệnh kiểm tra

```bash
pytest tests -q
ruff check src tests
python -m ocr_tb info
```