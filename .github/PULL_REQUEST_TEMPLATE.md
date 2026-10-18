## Mô tả

<!-- Mô tả ngắn gọn thay đổi này làm gì. -->

## Vì sao

<!-- Vấn đề hoặc yêu cầu mà thay đổi này giải quyết. Nếu là fix bug, dẫn tới issue: #123 -->

## Cách thay đổi

<!-- Những phần bị ảnh hưởng: src/ocr_tb/..., CLI, HTTP API, benchmark... -->

## Cách kiểm tra

<!-- Lệnh để tái hiện và xác nhận thay đổi hoạt động. -->

```bash
pytest tests -q
ocr-tb solve samples
```

## Ảnh hưởng tương thích

- [ ] Không phá API/CLI hiện có
- [ ] Cần cập nhật README/CHANGELOG
- [ ] Cần thêm entry trong `CHANGELOG.md`

<!-- Ghi rõ nếu có thay đổi hành vi, ví dụ đổi port mặc định hay đổi cấu trúc output. -->