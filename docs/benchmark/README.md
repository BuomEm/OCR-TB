# Báo cáo benchmark OCR-TB

Thư mục này lưu kết quả đo thật để người dùng tham khảo trước khi chọn model.

| File | Nội dung |
|---|---|
| [`report-100-captcha.md`](report-100-captcha.md) | Báo cáo đầy đủ: xếp hạng, thời gian, nhầm ký tự, mức độ giống nhau giữa các model |
| [`score-100-captcha.csv`](score-100-captcha.csv) | Bảng điểm dạng CSV để vẽ biểu đồ |

## Điều kiện đo

- **Bộ ảnh:** 100 captcha thự nghiệm, 200×50 px, 4 ký tự `a-z0-9`, nhiễu đường cong.
- **Nhãn:** gán tay bởi con người, đối chiếu lại bằng mắt cho các ca bất đồng giữa model.
- **Máy:** Windows 11, CPU Intel Core thế hệ Core Ultra (8 luồng), không GPU.
- **Thư viện:** ddddocr 1.6.1, onnxruntime 1.31.0, rapidocr-onnxruntime 1.2.3, tesseract 5.4.0.
- **Cách đo thời gian:** mỗi cấu hình chạy nóng 3 ảnh trước khi đo, rồi ghi thời gian từng ảnh.

## Cách tái lập

```bash
git clone https://github.com/BuomEm/OCR-TB.git
cd OCR-TB
./install.sh
export OCR_TB_IMAGES=/duong/dan/anh-captcha
ocr-tb label make --open          # gán nhãn tay -> labels.csv
ocr-tb bench run --variants raw,otsu,upscale2x_otsu
ocr-tb bench score
```

Kết quả mới sẽ nằm ở `$OCR_TB_HOME/data` cùng cấu trúc với các file trong thư mục này.

## Cách đọc số liệu

- **Chính xác tuyệt đối** (`exact_accuracy`): chuỗi sau khi chuẩn hoá về `[0-9a-z]`
  khớp tuyệt đối với nhãn — đây là chỉ số quyết định vì API captcha chỉ nhận đáp án đúng hoàn toàn.
- **Char acc** (`char_accuracy`): `1 - levenshtein / max(len)` trung bình, cho biết mức "gần đúng".
- **Đúng độ dài nhãn**: tỉ lệ output đủ 4 ký tự — ảnh hưởng trực tiếp tới khả năng submit.
- **Output rỗng**: số ảnh model trả về chuỗi rỗng — tín hiệu model bị "đầu rưng" trên ảnh nhiễu.