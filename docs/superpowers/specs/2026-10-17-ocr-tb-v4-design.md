# OCR-TB CLI v4 — Implementation Specification

**Mục tiêu:** Xây dựng CLI OCR offline bằng JavaScript cho các ảnh chứa chuỗi chữ-số ngắn, có viền và đường nhiễu như ba mẫu đã cung cấp.

**Công nghệ:** Node.js 24, ESM, Sharp, Tesseract.js 7.0.0, `node:test`.

**Ưu tiên:** Baseline có khả năng đánh giá thực tế → pipeline chuẩn hóa ảnh → độ tin cậy vận hành → tối ưu có kiểm chứng.

## 1. Ground truth

| Sample | Expected |
|---|---|
| 01.png | `3h8a` |
| 02.png | `3akp` |
| 03.png | `ehxe` |

Cả ba có kích thước 200 × 50 px, nền sáng, ký tự đen, có đường nhiễu và khung viền màu đen.

Giữ nguyên file gốc và checksum SHA-256. Ánh xạ ảnh–nhãn phải được kiểm tra trước khi benchmark.

Ground truth chỉ được truy cập bởi module evaluation, không được truyền vào module nhận dạng hoặc chọn candidate.

## 2. Kiến trúc runtime

```text
Main CLI Process
│
├── Argument Parser
├── File Discovery
├── Batch Scheduler
├── Timeout Supervisor
├── Result Aggregator
├── Text / JSON Writer
│
└── IPC (JSON metadata only)
    │
    ▼
    Child OCR Process
    │
    ├── Input Validation
    ├── Sharp Preprocessing
    ├── Border Detection
    ├── Image Variant Generator
    ├── Tesseract.js Worker
    ├── Candidate Selection
    └── Result Serialization
```

Main process chỉ truyền:

- Đường dẫn ảnh.
- ID công việc.
- Cấu hình OCR.
- Đường dẫn debug nếu được bật.

Không truyền ảnh dưới dạng Buffer qua IPC.

Child process đọc file, giải mã, xử lý ảnh và thực hiện OCR. Sau khi hoàn tất, child gửi kết quả JSON nhỏ gọn về main process.

Không sử dụng `shell: true` khi khởi tạo child.

Dùng một Tesseract worker được tái sử dụng qua các ảnh. Child được tái tạo sau timeout hoặc lỗi fatal.

## 3. Preprocessing v4

### 3.1. Chuẩn hóa đầu vào

Thứ tự:

1. Validate file và kích thước.
2. Giải mã bằng Sharp.
3. Chuẩn hóa EXIF orientation.
4. Làm phẳng alpha lên nền trắng.
5. Phát hiện khung viền nếu có.
6. Tạo các biến thể tiền xử lý.
7. Thêm viền trắng.
8. Truyền Buffer cục bộ cho Tesseract worker.

### 3.2. Border detection

Phát hiện riêng các cạnh ngoài cùng.

Điều kiện ban đầu:

- Pixel tối có grayscale ≤ 32.
- Tỷ lệ pixel tối tại mỗi cạnh ≥ 98%.
- Các cạnh tạo thành khung liên tục.
- Ảnh đủ lớn để loại viền an toàn.

Khi điều kiện được thỏa mãn:

- Tạo bản ảnh loại bỏ khung đen ngoài cùng 1 px.
- Bảo toàn bản ảnh gốc để đối chứng.
- Thử cắt 2 px ở chế độ experiment.
- Không tiếp tục cắt nhiều lớp chỉ vì gặp thêm pixel tối.
- Không sử dụng `trim()` một cách vô điều kiện vì có thể nhận nhầm màu nền từ pixel góc đen.

Metadata:

```json
{
  "borderDetected": true,
  "borderRemovedPx": 1,
  "borderDetectionMethod": "dark-edge-ratio"
}
```

Đối với ba ảnh mẫu, điều kiện viền ngoài cùng đã được xác minh.

### 3.3. Biến thể mặc định

| ID | Input | Preprocessing |
|---|---|---|
| V0 | Ảnh nguyên bản | Thêm viền trắng |
| V1 | Ảnh đã bỏ khung nếu phát hiện | Resize 4× |
| V2 | Ảnh đã bỏ khung nếu phát hiện | Grayscale + normalize + resize 4× |
| V3 | Ảnh đã bỏ khung nếu phát hiện | Grayscale + normalize + resize 4× + threshold 160 |

Thêm viền trắng 16 px sau các phép xử lý.

Giữ các giới hạn kích thước sau xử lý:

- Cạnh dài tối đa 3.000 px.
- Tổng pixel tối đa 10 megapixel.
- Không vượt ngưỡng xử lý cho ảnh đầu vào 20 megapixel.

Không tự xóa đường nhiễu trong chế độ mặc định.

### 3.4. Biến thể thực nghiệm

Bổ sung nhưng không chạy mặc định:

- E1: Crop bỏ 2 px khung viền.
- E2: Otsu threshold.
- E3: Resize 3× và 5×.
- E4: PSM 8.
- E5: PSM 13.
- E6: Phân tích đường nhiễu và tạo bản xử lý thử nghiệm.

Các biến thể này phục vụ benchmark độc lập. Không tự động đưa toàn bộ kết quả thực nghiệm vào hệ thống bỏ phiếu, tránh tăng số phiếu một cách thiên lệch.

## 4. Tesseract configuration

- Language: `eng`.
- OEM: `LSTM_ONLY`.
- PSM mặc định: 7.
- Whitelist: `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789`.
- Khởi tạo DAWG theo cấu hình đã chốt.
- Worker được tái sử dụng.
- Không tải model lúc runtime.

Dùng đường dẫn tài nguyên local tuyệt đối được xác định từ vị trí package, không phụ thuộc thư mục làm việc hiện tại.

Pin phiên bản chính xác trong `package-lock.json`, xác minh tương thích giữa Tesseract.js và tesseract.js-core.

Chuẩn bị đầy đủ tài nguyên JS/WASM tương ứng với phiên bản đang sử dụng. `corePath` trỏ tới thư mục chứa các bản dựng core cần thiết.

Chạy `ocr-tb doctor` để kiểm tra dependency native, model, checksum và khả năng khởi tạo worker mà không có Internet.

## 5. Candidate selection

Chuẩn hóa text bằng cách loại bỏ whitespace; giữ nguyên hoa/thường và toàn bộ ký tự được nhận dạng.

Gom nhóm theo text chính xác.

Thứ tự chọn:

1. Số phiếu.
2. Confidence cao nhất trong nhóm.
3. Tie-break priority: V2 → V3 → V1 → V0.

Tie-break priority là cấu hình thử nghiệm ban đầu, không phải kết luận biến thể V2 luôn tốt nhất.

Khi hòa số phiếu giữa các ứng viên, dù được phân định bằng confidence, thêm lý do `vote_tie` và đánh dấu `needs_review`.

Nếu chỉ một biến thể nhận dạng được hoặc confidence nhỏ hơn 80, cũng đánh dấu `needs_review`.

Không tính confidence trung bình giữa các biến thể.

**Lưu ý:** Đồng thuận không phải bằng chứng độc lập. Không dùng số phiếu để tuyên bố xác suất nhận dạng đúng.

## 6. Timeout và worker recovery

- Timeout xử lý mỗi ảnh: 30 giây.
- Timeout khởi tạo OCR worker: 60 giây.
- Main process quản lý deadline.
- Child process không tự quyết định thời hạn của mình.
- Khi timeout, main yêu cầu kết thúc child.
- Chờ xác nhận sự kiện thoát của tiến trình.
- Nếu không thể xác nhận việc kết thúc, báo lỗi vận hành.
- Không xử lý ảnh tiếp theo trên child lỗi.
- Tạo child mới và khởi tạo worker mới sau khi child cũ đã kết thúc hoặc được xử lý theo chính sách phục hồi.

Trên Windows, kiểm tra riêng tình huống child bị treo và tài nguyên không được giải phóng.

Khi user nhấn Ctrl+C, dừng lập lịch công việc mới, giải phóng worker và kết thúc có kiểm soát.

Không tuyên bố việc gửi tín hiệu kết thúc đồng nghĩa chắc chắn đã giải phóng toàn bộ tài nguyên.

## 7. JSON và trạng thái

Giữ schema của v3, bổ sung metadata tiền xử lý.

```json
{
  "file": "01.png",
  "text": "",
  "status": "unrecognized",
  "confidence": null,
  "votes": 0,
  "candidates": [],
  "reviewReasons": [],
  "preprocessing": {
    "borderDetected": true,
    "borderRemovedPx": 1
  },
  "durationMs": 0,
  "error": null
}
```

Đây là ví dụ schema, không phải kết quả OCR thực tế.

Các trạng thái:

- `ok`
- `needs_review`
- `unrecognized`
- `error`

Các lý do review có thể gồm:

- `single_vote`
- `low_confidence`
- `missing_confidence`
- `vote_tie`
- `variant_failure`

Mọi ảnh trong batch phải có một đối tượng kết quả tương ứng, kể cả khi gặp lỗi.

## 8. Evaluation v4

Sử dụng hai chỉ số Character Error Rate.

### CER Valid Only

Chỉ đánh giá các ảnh không có lỗi vận hành.

```text
cerValidOnly =
  Tổng Levenshtein trên ảnh hợp lệ
  / Tổng ký tự nhãn trên ảnh hợp lệ
```

Nếu không có ảnh hợp lệ, trả `null`.

### CER Overall

Đánh giá toàn bộ ảnh có nhãn.

Với ảnh lỗi vận hành, đặt predicted text thành chuỗi rỗng chỉ trong bước tính metric.

```text
cerOverall =
  Tổng Levenshtein trên toàn bộ ảnh
  / Tổng ký tự nhãn
```

Một ảnh có nhãn dài 4 ký tự nhưng bị lỗi vận hành đóng góp bốn phép xóa vào tử số.

Lưu ý CER có thể lớn hơn 100% khi dự đoán chứa nhiều ký tự thừa. Không được tự giới hạn CER ở 100%.

### Chỉ số bổ sung

- Exact match trên toàn bộ ảnh.
- Exact match trên các ảnh xử lý thành công.
- `autoAcceptCoverage`.
- `autoAcceptAccuracy`.
- Tỷ lệ lỗi vận hành.
- Thời gian khởi tạo worker.
- Thời gian xử lý trung bình/ảnh.
- Latency p50/p95 khi bộ dữ liệu đủ lớn.
- Mức tăng/giảm accuracy theo từng biến thể.

Bộ ba ảnh hiện tại chỉ dùng để kiểm tra khả thi, không dùng để xác nhận độ chính xác tổng quát.

## 9. Baseline và kiểm chứng

### Baseline A — OCR thô

Chạy V0 trên cả ba mẫu.

Ghi:

- Predicted text.
- Confidence.
- Exact match.
- CER.
- Latency.

### Baseline B — Tiền xử lý

Chạy V1, V2, V3 có loại khung ngoài cùng.

Lưu đầu ra từng phép OCR.

So sánh với Baseline A.

### Baseline C — Border ablation

Đánh giá ba điều kiện:

- Không xóa viền.
- Xóa viền 1 px.
- Xóa viền 2 px.

Giữ các điều kiện khác giống nhau.

### Baseline D — Alternative PSM

Chỉ sau khi có kết quả A–C, thử PSM 8 và 13 với các biến thể có triển vọng.

Không tự động chọn tổ hợp có kết quả tốt nhất trên ba ảnh để làm cấu hình sản xuất. Cấu hình được đề xuất phải được xác nhận bằng dữ liệu mới.

## 10. Nghiệm thu và sản phẩm bàn giao

MVP phải đáp ứng:

- Chạy offline.
- Model và WASM local.
- Không có fallback Internet.
- Phát hiện và xử lý khung đen ngoài cùng.
- Giữ bản gốc làm đối chứng.
- Nhận dạng single và batch.
- Không thay đổi ảnh đầu vào.
- Không truyền Buffer ảnh qua IPC.
- Giữ một worker OCR được tái sử dụng.
- Timeout có cơ chế kết thúc child thật.
- Kết quả JSON ổn định.
- Có `analysis.json`.
- Có exact match, CER valid và CER overall.
- Có unit test, integration test.
- Có báo cáo trên ba ảnh gốc.
- Không suy diễn accuracy trên ảnh chưa thấy.

**Điểm dừng Phase 1:** Có bảng benchmark thực nghiệm cho ba ảnh và các biến thể, thể hiện chính xác những chuỗi OCR nhận dạng được hoặc không nhận dạng được.

**Definition of Done:** Công cụ chạy ổn định, offline, kết quả có thể tái lập, lỗi được kiểm soát và chất lượng nhận dạng được đánh giá minh bạch.