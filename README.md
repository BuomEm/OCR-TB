<div align="center">

# OCR-TB

**Giải captcha OCR cho Node.js, Python, Linux, Windows, Docker — không cần GPU, không cần API key.**

[![CI](https://github.com/BuomEm/OCR-TB/actions/workflows/ci.yml/badge.svg)](https://github.com/BuomEm/OCR-TB/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-3776ab.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS%20|%20Docker-lightgrey.svg)](https://github.com/BuomEm/OCR-TB)

Dựng trên **ddddocr**, **PP-OCRv5/v6**, **Tesseract 5** — tự chọn model nhanh nhất
và chính xác nhất, có sẵn HTTP server để gọi từ ứng dụng khác.

</div>

---

## 📊 Kết quả đo thật

Bộ **100 ảnh captcha ViettelPost** (200×50, 4 ký tự `a-z0-9`, nhiễu nét cong),
được gán nhãn tay và chạy trên CPU thông thường:

| Hạng | Cấu hình | Chính xác tuyệt đối | Char acc | Tốc độ | RAM tiến trình |
|---|---|---|---|---|---|
| 🥇 | `ddddocr/alnum` | **99%** | 99.8% | 59 ms/ảnh | ~95 MB |
| 🥈 | `ddddocr/default` | **98%** | 99.6% | 22 ms/ảnh | ~95 MB |
| 🥉 | `ppocr_v6_small` + `otsu` | **93%** | 98.4% | 25 ms/ảnh | ~110 MB |
| 4 | `ppocr_v6_small` (thô) | 85% | 96.8% | 16 ms/ảnh | ~110 MB |
| 5 | `ppocr_v5_en` | 58% | 88.9% | 21 ms/ảnh | ~110 MB |
| 6 | `tesseract5 --psm 8` | 17% | 61.9% | 278 ms/ảnh | ~26 MB (process riêng) |

> Báo cáo đầy đủ: [`docs/benchmark/report-vietelpost-100.md`](docs/benchmark/report-vietelpost-100.md) ·
> [dữ liệu thô CSV](docs/benchmark/score-vietelpost-100.csv)

### Ảnh mẫu đi kèm repo

<table>
  <tr>
    <td align="center"><img src="samples/01.jpg" width="200" alt="captcha 01"><br><code>3h8a</code></td>
    <td align="center"><img src="samples/02.jpg" width="200" alt="captcha 02"><br><code>3akp</code></td>
    <td align="center"><img src="samples/03.jpg" width="200" alt="captcha 03"><br><code>ehxe</code></td>
  </tr>
  <tr>
    <td align="center" colspan="3"><sub>Cả 3 ảnh đều được OCR-TB đọc đúng bằng <code>ddddocr/default</code>, dưới 25 ms/ảnh.</sub></td>
  </tr>
</table>

**Ba phát hiện đáng chú ý:**

1. **Tiền xử lý ảnh không có công thức chung.** `otsu` giúp PP-OCR (85% → 93%) nhưng
   phá ddddocr (98% → 67%), vì binarize cắt mất nét mảnh của ký tự trên ảnh nhiễu.
2. **Tesseract không hợp với captcha nhiễu.** `--psm 7`/`--psm 6` (chế độ thường được
   khuyên cho captcha 1 dòng) trả về chuỗi rỗng ở 73–87/100 ảnh. Chỉ `--psm 8` còn dùng được.
3. **Lỗi của các model khác nhau.** ddddocr và PP-OCR chỉ giống nhau 92% → có thể
   fallback qua lại để tăng độ chính xác (đã có sẵn trong `ocr-tb solve --fallback`).

---

## ✨ Tính năng

| | |
|---|---|
| 🧩 **4 nhóm model** | ddddocr, PP-OCRv5 English, PP-OCRv6 small, Tesseract 5 |
| 🪄 **Fallback tự động** | ddddocr sai độ dài → tự chuyển sang PP-OCR |
| 🌐 **HTTP server** | FastAPI: `/solve`, `/solve/upload`, `/solve/batch`, `/health`, `/models` |
| 💻 **CLI** | `ocr-tb solve <file hoặc thư mục>` — JSON hoặc bảng |
| 📊 **Bộ benchmark** | chạy 100 ảnh, xuất báo cáo Markdown/CSV/JSON, so sánh từng model |
| 🧪 **Đo RAM & đĩa** | `ocr-tb memory` — đo thực tế RSS và dung lượng model |
| 🖼️ **Tiền xử lý ảnh** | `raw`, `gray`, `otsu`, `upscale2x_otsu` |
| 🐳 **Docker** | image `python:3.12-slim`, chạy bằng user không phải root |
| 🧠 **Không cần GPU** | toàn bộ chạy CPU-only qua ONNX Runtime |
| 🪶 **Nhẹ** | model ddddocr ~95 MB RAM, cache model dùng lại vĩnh viễn |

---

## 🚀 Cài đặt

### 🪟 Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/BuomEm/OCR-TB/main/install.ps1 | iex
```

Hoặc clone rồi chạy:

```powershell
git clone https://github.com/BuomEm/OCR-TB.git
cd OCR-TB
.\install.ps1
```

Lệnh sẽ được tạo tại `%LOCALAPPDATA%\Programs\ocr-tb\bin\ocr-tb.cmd`.
Thêm vào PATH:

```powershell
[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path','User') + ';$env:LOCALAPPDATA\Programs\ocr-tb\bin', 'User')
```

### 🐧 Linux / 🍎 macOS

```bash
git clone https://github.com/BuomEm/OCR-TB.git
cd OCR-TB
sudo bash install.sh              # cài vào /opt/ocr-tb
# hoặc không cần sudo:
bash install.sh --user-only
```

Chạy nền bằng systemd:

```bash
sudo bash install-service.sh
systemctl status ocr-tb
```

### 🐳 Docker

```bash
git clone https://github.com/BuomEm/OCR-TB.git && cd OCR-TB
docker build -t ocr-tb:1.0.0 .

docker run --rm -p 8080:8080 ocr-tb:1.0.0                      # HTTP server
docker run --rm ocr-tb:1.0.0 solve /data/samples                # CLI
docker run --rm -v "$PWD/samples:/data" ocr-tb:1.0.0 solve /data --json
```

### 🐍 Cài bằng pip (đã có sẵn môi trường Python)

```bash
pip install "ocr-tb[server]"
ocr-tb models pull        # tải model PP-OCR (khoảng 37 MB)
```

> **Ghi chú Linux:** `rapidocr-onnxruntime` kéo theo `opencv-python`, nếu thiếu thư viện
> hệ thống sẽ báo lỗi `ImportError: libGL.so.1`. Sửa bằng:
> `sudo apt install -y libgl1 libglib2.0-0` (Docker đã cài sẵn).

---

## ⚡ Bắt đầu nhanh

### CLI

```bash
ocr-tb solve cap.png                          # 1 ảnh
ocr-tb solve ./samples                        # cả thư mục
ocr-tb solve ./samples --json                 # kết quả dạng JSON
```

Kết quả:

```text
01.jpg	3h8a	[ddddocr/default/raw]	21 ms
02.jpg	3akp	[ddddocr/default/raw]	19 ms
03.jpg	ehxe	[ddddocr/default/raw]	18 ms
```

### Dùng model khác / chuỗi fallback

```bash
ocr-tb solve cap.png --model ppocr_v6_small --variant otsu
ocr-tb solve cap.png --fallback --expect-length 4
```

```
cap.png	3dkb	[ppocr_v6_small/rec_only/otsu]	17 ms
    (fallback) ddddocr/default -> 'x3dkb'
```

### HTTP server

```bash
ocr-tb serve --host 0.0.0.0 --port 8080
```

```bash
# upload 1 ảnh
curl -X POST -F "file=@cap.png" -F "expect_length=4" \
  http://127.0.0.1:8080/solve/upload

# base64 + chọn model
curl -X POST -H 'Content-Type: application/json' \
  -d '{"image_base64":"<base64>","model":"ppocr_v6_small","variant":"otsu"}' \
  http://127.0.0.1:8080/solve

# nhiều ảnh
curl -X POST -H 'Content-Type: application/json' \
  -d '{"images_base64":["<base64-1>","<base64-2>"]}' \
  http://127.0.0.1:8080/solve/batch
```

Phản hồi:

```json
{
  "text": "3b6a",
  "normalized": "3b6a",
  "model": "ddddocr",
  "config": "default",
  "variant": "raw",
  "confidence": null,
  "elapsed_ms": 26.7,
  "attempts": [ ... ]
}
```

Tài liệu OpenAPI tự sinh tại `http://127.0.0.1:8080/docs`.

### Gọi từ Node.js

```js
const form = new FormData();
form.append("file", new Blob([pngBuffer], { type: "image/png" }), "cap.png");
form.append("expect_length", "4");

const res = await fetch("http://127.0.0.1:8080/solve/upload", { method: "POST", body: form });
const { normalized } = await res.json();
console.log("captcha:", normalized);
```

---

## 📊 Benchmark

```bash
export OCR_TB_IMAGES=/duong/dan/anh-captcha      # thư mục ảnh
ocr-tb label make --open                         # bảng gán nhãn tay (HTML)
ocr-tb label check                               # xem tiến độ gán nhãn

ocr-tb bench run --variants raw,otsu             # chạy tất cả model
ocr-tb bench run --models ddddocr --limit 100    # chỉ ddddocr
ocr-tb bench score                               # chấm lại run gần nhất
```

Kết quả nằm ở `$OCR_TB_HOME/data`:

```
data/
  labels.csv                  nhãn thủ công
  labeling.html               bảng gán nhãn trên trình duyệt
  runs/<run_id>/rows.jsonl    từng dòng dự đoán (model, config, biến thể, thời gian, ảnh)
  runs/<run_id>/summary.json  tổng hợp thời gian/lỗi
  runs/<run_id>/env.json      phiên bản thư viện + thông tin máy
  report/report-<run_id>.md  báo cáo xếp hạng
  report/score-<run_id>.csv   bảng điểm
  report/details-<run_id>.csv chi tiết từng ảnh
```

Mỗi dòng `rows.jsonl` lưu đủ để so sánh lại về sau: model, config, biến thể tiền xử lý,
tên file, kích thước ảnh, chỉ số độ khó (`ink_ratio`, `edge_density`), raw text, text đã
chuẩn hoá, confidence, thời gian và lỗi.

**Chỉ số:** `exact_accuracy` (khớp tuyệt đối), `char_accuracy` (1 − levenshtein/max len),
`length_match_rate`, `empty_outputs`, `timing` mean/p50/p95/max.

---

## 🤖 Bảng model

| Model id | Nguồn | Dung lượng | Ghi chú |
|---|---|---|---|
| `ddddocr` | `pip ddddocr` | 84.7 MB (gồm cả model không dùng) | nằm trong package, không cần tải thêm |
| `ppocr_v6_small` | `PaddlePaddle/PP-OCRv6_small_rec_onnx` | 20.2 MB | `ocr-tb models pull` |
| `ppocr_v5_en` | `PaddlePaddle/en_PP-OCRv5_mobile_rec_onnx` | 7.5 MB | `ocr-tb models pull` |
| `tesseract5` | `apt install tesseract-ocr` / `winget` | ~26 MB RAM | cài riêng, không tải qua mạng |

### Biến thể tiền xử lý

| Tên | Ảnh hưởng đo được |
|---|---|
| `raw` | ddddocr 98% · ppocr_v6 85% |
| `otsu` | ddddocr 67% · ppocr_v6 93% |
| `upscale2x_otsu` | ddddocr 61% · ppocr_v6 91% |
| `gray` | tương đương `raw` |

---

## ⚙️ Cấu hình

| Biến môi trường | Mặc định | Ý nghĩa |
|---|---|---|
| `OCR_TB_HOME` | `~/.cache/ocr-tb` | thư mục gốc (Windows: `%LOCALAPPDATA%\ocr-tb`) |
| `OCR_TB_CACHE` | `$OCR_TB_HOME/models` | cache model ONNX |
| `OCR_TB_IMAGES` | `$OCR_TB_HOME/data/captcha` | thư mục ảnh cho benchmark |
| `OCR_TB_MODEL` | `ddddocr` | model dùng mặc định |
| `OCR_TB_CONFIG` | rỗng | config dùng mặc định |
| `OCR_TB_VARIANT` | `raw` | tiền xử lý mặc định |
| `OCR_TB_HOST` / `OCR_TB_PORT` | `0.0.0.0` / `8080` | HTTP server |
| `OCR_TB_TIMEOUT` | `15` | timeout mỗi lượt giải (giây) |
| `HF_ENDPOINT` | `https://huggingface.co` | mirror tải model |

```bash
ocr-tb info        # môi trường, phiên bản, trạng thái model
ocr-tb memory      # đo RSS khi nạp/chạy model + dung lượng đĩa
ocr-tb models list # model + config + trạng thái cache
```

---

## 🗂️ Cấu trúc dự án

```text
OCR-TB/
├── src/ocr_tb/
│   ├── cli.py          lệnh CLI
│   ├── solver.py       nạp model, fallback chain
│   ├── registry.py     4 model OCR
│   ├── preprocess.py   raw / gray / otsu / upscale2x_otsu
│   ├── server.py       FastAPI
│   ├── bench.py        benchmark + báo cáo + labeling
│   ├── download.py     tải model về cache
│   ├── memory.py       đo RAM/dung lượng
│   ├── config.py       đường dẫn + biến môi trường
│   └── util.py         thống kê, levenshtein, io
├── tests/              29 test (offline)
├── samples/            3 ảnh captcha mẫu + nhãn
├── examples/           script Node lấy ảnh captcha từ API
├── docs/benchmark/     báo cáo benchmark 100 ảnh
├── install.sh          cài Linux/macOS
├── install.ps1         cài Windows
├── install-service.sh  systemd service
├── Dockerfile
└── pyproject.toml
```

---

## 🧪 Phát triển

```bash
git clone https://github.com/BuomEm/OCR-TB.git
cd OCR-TB
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[server,dev]"
pytest tests -q
```

CI kiểm tra trên **ubuntu / windows / macos × Python 3.11, 3.12** và build Docker
mỗi lần push.

**Thêm model mới:** viết class kế thừa `OcrModel` trong `src/ocr_tb/registry.py`,
thêm vào `build_registry()`.
**Thêm tiền xử lý:** đăng ký hàm vào `VARIANTS` trong `src/ocr_tb/preprocess.py`.

---

## ❓ Câu hỏi thường gặp

**Có cần GPU không?**
Không. Toàn bộ chạy CPU qua ONNX Runtime, đo trên CPU thường đã đạt 22 ms/ảnh.

**Cần mạng khi chạy không?**
Không, sau khi `ocr-tb models pull` xong. ddddocr có sẵn trong package pip.

**Mất bao lâu RAM?**
Tiến trình chỉ dùng ddddocr: ~95 MB sau khi nạp model (~66 MB tính từ lúc import).
Dùng thêm PP-OCR: ~110 MB. Chạy `ocr-tb memory` để đo trên máy của bạn.

**Có cần cài Tesseract không?**
Không bắt buộc — Tesseract chỉ để so sánh trong benchmark. Cài khi cần:
`sudo apt install tesseract-ocr` hoặc `winget install UB-Mannheim.TesseractOCR`.

**Chuẩn hoá kết quả thế nào?**
Lowercase và chỉ giữ ký tự `[0-9a-z]`, đúng charset captcha. Dùng `POST /normalize`
để chuẩn hoá chuỗi bất kỳ.

**Chạy nhiều request song song?**
Server dùng thread pool (`--threads`, mặc định 4). Nhiều worker hơn thì tăng `--threads`
và `--workers` của uvicorn nếu triển khai nhiều tiến trình.

---

## 🙏 Cảm ơn

Các dự án mã nguồn mở được sử dụng:

- [ddddocr](https://github.com/sml2h3/ddddocr) — OCR chuyên dụng cho captcha
- [PaddleOCR / PP-OCR](https://github.com/PaddlePaddle/PaddleOCR) — bản ONNX export chính thức
- [RapidOCR](https://github.com/RapidAI/RapidOCR) — hạ tầng ONNX cho PP-OCR
- [Tesseract](https://github.com/tesseract-ocr/tesseract) — OCR phổ biến, CPU-only

---

## 📄 Giấy phép

MIT — xem [LICENSE](LICENSE). Tác giả: **BuomEm**.