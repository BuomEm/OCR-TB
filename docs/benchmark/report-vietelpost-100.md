# Benchmark OCR captcha ViettelPost — run `full-100-raw-otsu`

- Thời điểm chạy: 2026-10-18 07:26:38
- Số ảnh: 100 | số ảnh đã có nhãn: 100
- Máy: Intel64 Family 6 Model 142 Stepping 10, GenuineIntel (8 luồng)
- Hệ điều hành: Windows-11-10.0.26200-SP0
- Thư viện: ddddocr=1.6.1, onnxruntime=1.31.0, rapidocr_onnxruntime=1.2.3, pytesseract=0.3.13, cv2=5.0.0.93, numpy=2.5.4, pillow=13.0.0, tesseract=5.4.0.20240606

## Kết luận

**Khuyến nghị: `ddddocr/alnum/raw`** — độ chính xác tuyệt đối 99.0%
Nhanh nhất: `ppocr_v6_small/rec_only/raw` (16.26 ms/ảnh) với độ chính xác 85.0%.
`ddddocr/default/raw` thấp hơn 1.0 điểm, 21.73 ms/ảnh.
`ddddocr/old/raw` thấp hơn 1.0 điểm, 34.31 ms/ảnh.
`ppocr_v6_small/rec_only/otsu` thấp hơn 6.0 điểm, 25.22 ms/ảnh.

## Bảng xếp hạng

| # | Cấu hình | Chính xác tuyệt đối | Char acc | Đúng độ dài nhãn | Rỗng | Lỗi | mean ms | p95 ms |
|---|---|---|---|---|---|---|---|---|
| 1 | `ddddocr/alnum/raw` | **99.0%** | 99.8% | 99.0% | 0 | 0 | 59.26 | 72.62 |
| 2 | `ddddocr/default/raw` | **98.0%** | 99.6% | 98.0% | 0 | 0 | 21.73 | 27.63 |
| 3 | `ddddocr/old/raw` | **98.0%** | 99.6% | 98.0% | 0 | 0 | 34.31 | 44.11 |
| 4 | `ppocr_v6_small/rec_only/otsu` | **93.0%** | 98.4% | 97.0% | 0 | 0 | 25.22 | 35.93 |
| 5 | `ppocr_v6_small/rec_only/upscale2x_otsu` | **91.0%** | 97.9% | 97.0% | 0 | 0 | 25.68 | 35.77 |
| 6 | `ppocr_v6_small/rec_only/raw` | **85.0%** | 96.75% | 89.0% | 0 | 0 | 16.26 | 19.92 |
| 7 | `ddddocr/default/otsu` | **67.0%** | 93.3% | 69.0% | 0 | 0 | 24.38 | 33.04 |
| 8 | `ddddocr/old/otsu` | **67.0%** | 93.3% | 69.0% | 0 | 0 | 37.78 | 62.91 |
| 9 | `ddddocr/alnum/otsu` | **67.0%** | 93.3% | 69.0% | 0 | 0 | 48.88 | 61.97 |
| 10 | `ddddocr/old/upscale2x_otsu` | **61.0%** | 92.15% | 62.0% | 0 | 0 | 32.41 | 42.4 |
| 11 | `ddddocr/default/upscale2x_otsu` | **61.0%** | 92.15% | 62.0% | 0 | 0 | 35.68 | 47.45 |
| 12 | `ddddocr/alnum/upscale2x_otsu` | **61.0%** | 92.15% | 62.0% | 0 | 0 | 48.23 | 67.18 |
| 13 | `ppocr_v5_en/rec_only/raw` | **58.0%** | 88.85% | 74.0% | 0 | 0 | 20.72 | 29.5 |
| 14 | `ppocr_v5_en/rec_only/upscale2x_otsu` | **51.0%** | 87.85% | 73.0% | 0 | 0 | 20.27 | 29.09 |
| 15 | `ppocr_v5_en/rec_only/otsu` | **49.0%** | 86.9% | 76.0% | 0 | 0 | 23.08 | 32.35 |
| 16 | `tesseract5/psm8_whitelist/upscale2x_otsu` | **18.0%** | 59.45% | 54.0% | 0 | 0 | 203.1 | 273.47 |
| 17 | `tesseract5/psm8_whitelist/raw` | **17.0%** | 61.85% | 53.0% | 0 | 0 | 277.99 | 527.28 |
| 18 | `tesseract5/psm13_raw/upscale2x_otsu` | **13.0%** | 53.64% | 53.0% | 0 | 0 | 187.63 | 230.29 |
| 19 | `tesseract5/psm13_raw/raw` | **9.0%** | 54.71% | 50.0% | 0 | 0 | 203.74 | 268.47 |
| 20 | `tesseract5/psm8_whitelist/otsu` | **8.0%** | 49.92% | 46.0% | 0 | 0 | 266.08 | 413.61 |
| 21 | `tesseract5/psm13_raw/otsu` | **7.0%** | 44.97% | 49.0% | 0 | 0 | 221.86 | 279.98 |
| 22 | `tesseract5/psm7_whitelist/raw` | **4.0%** | 12.65% | 10.0% | 77 | 0 | 257.68 | 484.2 |
| 23 | `tesseract5/psm6_whitelist/raw` | **4.0%** | 12.4% | 10.0% | 73 | 0 | 217.65 | 298.32 |
| 24 | `tesseract5/psm6_whitelist/upscale2x_otsu` | **3.0%** | 8.16% | 9.0% | 74 | 0 | 209.91 | 302.94 |
| 25 | `tesseract5/psm7_whitelist/upscale2x_otsu` | **3.0%** | 6.8% | 8.0% | 87 | 0 | 178.31 | 209.86 |
| 26 | `tesseract5/psm7_whitelist/otsu` | **1.0%** | 9.95% | 7.0% | 77 | 0 | 218.04 | 298.63 |
| 27 | `tesseract5/psm6_whitelist/otsu` | **1.0%** | 9.17% | 8.0% | 73 | 0 | 184.32 | 248.25 |
| 28 | `tesseract5/psm7_raw/otsu` | **1.0%** | 8.36% | 13.0% | 77 | 0 | 193.95 | 287.08 |
| 29 | `tesseract5/psm7_raw/upscale2x_otsu` | **1.0%** | 5.77% | 9.0% | 87 | 0 | 209.31 | 277.67 |
| 30 | `tesseract5/psm7_raw/raw` | **0.0%** | 10.41% | 12.0% | 77 | 0 | 218.17 | 287.64 |

## Chi tiết từng cấu hình

### `ddddocr/alnum/raw`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 99.0% | char acc: 99.8% | sai trung bình: 0.01 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 59.26 ms | p50 58.44 ms | p95 72.62 ms | max 92.16 ms | tổng 5.93 s
- Nhầm ký tự nhiều nhất: `3->x`×1, `d->3`×1, `k->d`×1, `b->k`×1, `∅->b`×1

### `ddddocr/default/raw`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 98.0% | char acc: 99.6% | sai trung bình: 0.02 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 21.73 ms | p50 21.61 ms | p95 27.63 ms | max 30.73 ms | tổng 2.17 s
- Nhầm ký tự nhiều nhất: `e->f`×1, `7->e`×1, `k->7`×1, `∅->k`×1, `3->x`×1, `d->3`×1, `k->d`×1, `b->k`×1, `∅->b`×1

### `ddddocr/old/raw`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 98.0% | char acc: 99.6% | sai trung bình: 0.02 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 34.31 ms | p50 33.31 ms | p95 44.11 ms | max 53.16 ms | tổng 3.43 s
- Nhầm ký tự nhiều nhất: `e->f`×1, `7->e`×1, `k->7`×1, `∅->k`×1, `3->x`×1, `d->3`×1, `k->d`×1, `b->k`×1, `∅->b`×1

### `ppocr_v6_small/rec_only/otsu`

- Model: PP-OCRv6 small (rec, ONNX)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 93.0% | char acc: 98.4% | sai trung bình: 0.07 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Confidence trung bình: 0.77
- Thời gian: mean 25.22 ms | p50 24.0 ms | p95 35.93 ms | max 63.31 ms | tổng 2.52 s
- Nhầm ký tự nhiều nhất: `b->6`×2, `4->a`×2, `d->7`×1, `b->d`×1, `x->b`×1, `c->x`×1, `∅->c`×1, `h->s`×1, `k->h`×1, `x->k`×1

### `ppocr_v6_small/rec_only/upscale2x_otsu`

- Model: PP-OCRv6 small (rec, ONNX)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 91.0% | char acc: 97.9% | sai trung bình: 0.09 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Confidence trung bình: 0.7743
- Thời gian: mean 25.68 ms | p50 24.02 ms | p95 35.77 ms | max 59.84 ms | tổng 2.57 s
- Nhầm ký tự nhiều nhất: `∅->c`×2, `p->0`×2, `d->7`×1, `b->d`×1, `x->b`×1, `c->x`×1, `d->f`×1, `e->d`×1, `b->e`×1, `a->b`×1

### `ppocr_v6_small/rec_only/raw`

- Model: PP-OCRv6 small (rec, ONNX)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 85.0% | char acc: 96.75% | sai trung bình: 0.15 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Confidence trung bình: 0.7643
- Thời gian: mean 16.26 ms | p50 16.39 ms | p95 19.92 ms | max 23.38 ms | tổng 1.63 s
- Nhầm ký tự nhiều nhất: `a->7`×3, `∅->a`×3, `∅->c`×2, `7->a`×2, `e->a`×1, `7->e`×1, `k->7`×1, `∅->k`×1, `d->7`×1, `b->d`×1

### `ddddocr/default/otsu`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 67.0% | char acc: 93.3% | sai trung bình: 0.33 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 24.38 ms | p50 23.54 ms | p95 33.04 ms | max 41.58 ms | tổng 2.44 s
- Nhầm ký tự nhiều nhất: `a->7`×5, `∅->b`×5, `∅->k`×4, `b->d`×4, `∅->a`×4, `p->a`×4, `∅->8`×3, `∅->c`×3, `∅->7`×3, `3->7`×3

### `ddddocr/old/otsu`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 67.0% | char acc: 93.3% | sai trung bình: 0.33 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 37.78 ms | p50 33.38 ms | p95 62.91 ms | max 97.92 ms | tổng 3.78 s
- Nhầm ký tự nhiều nhất: `a->7`×5, `∅->b`×5, `∅->k`×4, `b->d`×4, `∅->a`×4, `p->a`×4, `∅->8`×3, `∅->c`×3, `∅->7`×3, `3->7`×3

### `ddddocr/alnum/otsu`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 67.0% | char acc: 93.3% | sai trung bình: 0.33 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 48.88 ms | p50 48.07 ms | p95 61.97 ms | max 75.7 ms | tổng 4.89 s
- Nhầm ký tự nhiều nhất: `a->7`×5, `∅->b`×5, `∅->k`×4, `b->d`×4, `∅->a`×4, `p->a`×4, `∅->8`×3, `∅->c`×3, `∅->7`×3, `3->7`×3

### `ddddocr/old/upscale2x_otsu`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 61.0% | char acc: 92.15% | sai trung bình: 0.39 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 32.41 ms | p50 31.11 ms | p95 42.4 ms | max 52.73 ms | tổng 3.24 s
- Nhầm ký tự nhiều nhất: `∅->b`×5, `∅->k`×4, `∅->3`×4, `a->7`×4, `∅->a`×4, `∅->p`×4, `∅->8`×3, `b->d`×3, `∅->7`×3, `7->4`×3

### `ddddocr/default/upscale2x_otsu`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 61.0% | char acc: 92.15% | sai trung bình: 0.39 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 35.68 ms | p50 33.97 ms | p95 47.45 ms | max 61.33 ms | tổng 3.57 s
- Nhầm ký tự nhiều nhất: `∅->b`×5, `∅->k`×4, `∅->3`×4, `a->7`×4, `∅->a`×4, `∅->p`×4, `∅->8`×3, `b->d`×3, `∅->7`×3, `7->4`×3

### `ddddocr/alnum/upscale2x_otsu`

- Model: ddddocr (ONNX, không detection)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 61.0% | char acc: 92.15% | sai trung bình: 0.39 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 48.23 ms | p50 48.12 ms | p95 67.18 ms | max 73.19 ms | tổng 4.82 s
- Nhầm ký tự nhiều nhất: `∅->b`×5, `∅->k`×4, `∅->3`×4, `a->7`×4, `∅->a`×4, `∅->p`×4, `∅->8`×3, `b->d`×3, `∅->7`×3, `7->4`×3

### `ppocr_v5_en/rec_only/raw`

- Model: PP-OCRv5 English (mobile rec, ONNX)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 58.0% | char acc: 88.85% | sai trung bình: 0.51 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Confidence trung bình: 0.7113
- Thời gian: mean 20.72 ms | p50 19.67 ms | p95 29.5 ms | max 37.69 ms | tổng 2.07 s
- Nhầm ký tự nhiều nhất: `∅->a`×5, `∅->k`×4, `7->t`×4, `∅->b`×3, `p->a`×3, `∅->d`×3, `7->e`×2, `k->a`×2, `7->4`×2, `∅->c`×2

### `ppocr_v5_en/rec_only/upscale2x_otsu`

- Model: PP-OCRv5 English (mobile rec, ONNX)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 51.0% | char acc: 87.85% | sai trung bình: 0.55 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Confidence trung bình: 0.6998
- Thời gian: mean 20.27 ms | p50 18.19 ms | p95 29.09 ms | max 32.63 ms | tổng 2.03 s
- Nhầm ký tự nhiều nhất: `∅->a`×6, `∅->k`×5, `a->7`×4, `7->4`×3, `c->e`×3, `a->e`×3, `p->a`×3, `7->e`×2, `∅->c`×2, `a->m`×2

### `ppocr_v5_en/rec_only/otsu`

- Model: PP-OCRv5 English (mobile rec, ONNX)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 49.0% | char acc: 86.9% | sai trung bình: 0.58 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Confidence trung bình: 0.6945
- Thời gian: mean 23.08 ms | p50 23.3 ms | p95 32.35 ms | max 45.02 ms | tổng 2.31 s
- Nhầm ký tự nhiều nhất: `∅->a`×5, `p->a`×4, `∅->k`×3, `7->4`×3, `b->6`×3, `4->a`×3, `8->x`×2, `∅->8`×2, `7->e`×2, `7->t`×2

### `tesseract5/psm8_whitelist/upscale2x_otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 18.0% | char acc: 59.45% | sai trung bình: 1.76 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 203.1 ms | p50 187.76 ms | p95 273.47 ms | max 381.08 ms | tổng 20.31 s
- Nhầm ký tự nhiều nhất: `7->∅`×7, `∅->a`×5, `7->e`×5, `p->n`×5, `∅->e`×4, `a->∅`×4, `b->h`×4, `c->e`×4, `7->t`×3, `6->t`×3

### `tesseract5/psm8_whitelist/raw`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 17.0% | char acc: 61.85% | sai trung bình: 1.65 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 277.99 ms | p50 228.56 ms | p95 527.28 ms | max 949.79 ms | tổng 27.8 s
- Nhầm ký tự nhiều nhất: `7->∅`×7, `∅->a`×5, `3->s`×5, `d->e`×4, `∅->b`×4, `7->a`×4, `p->o`×4, `p->n`×4, `k->∅`×3, `h->e`×3

### `tesseract5/psm13_raw/upscale2x_otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 13.0% | char acc: 53.64% | sai trung bình: 2.06 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 187.63 ms | p50 183.03 ms | p95 230.29 ms | max 298.44 ms | tổng 18.76 s
- Nhầm ký tự nhiều nhất: `c->e`×6, `7->∅`×5, `∅->x`×5, `∅->a`×5, `p->n`×5, `4->a`×5, `3->s`×5, `x->e`×4, `6->t`×4, `∅->h`×4

### `tesseract5/psm13_raw/raw`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 9.0% | char acc: 54.71% | sai trung bình: 2.04 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 203.74 ms | p50 186.12 ms | p95 268.47 ms | max 353.11 ms | tổng 20.37 s
- Nhầm ký tự nhiều nhất: `∅->b`×7, `∅->a`×7, `4->a`×6, `7->t`×6, `c->e`×6, `b->h`×5, `x->e`×5, `∅->7`×5, `d->e`×5, `a->e`×5

### `tesseract5/psm8_whitelist/otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 8.0% | char acc: 49.92% | sai trung bình: 2.12 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 266.08 ms | p50 237.07 ms | p95 413.61 ms | max 430.65 ms | tổng 26.61 s
- Nhầm ký tự nhiều nhất: `k->e`×8, `4->a`×8, `x->a`×8, `c->e`×7, `7->t`×6, `b->∅`×6, `a->∅`×6, `k->∅`×5, `p->o`×5, `3->s`×5

### `tesseract5/psm13_raw/otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 7.0% | char acc: 44.97% | sai trung bình: 2.39 ký tự/ảnh
- Output rỗng: 0 | exception: 0
- Thời gian: mean 221.86 ms | p50 227.04 ms | p95 279.98 ms | max 323.04 ms | tổng 22.19 s
- Nhầm ký tự nhiều nhất: `7->t`×9, `3->s`×9, `4->a`×9, `x->e`×5, `∅->c`×5, `∅->a`×5, `x->a`×5, `k->e`×5, `a->∅`×5, `p->o`×4

### `tesseract5/psm7_whitelist/raw`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 4.0% | char acc: 12.65% | sai trung bình: 3.52 ký tự/ảnh
- Output rỗng: 77 | exception: 0
- Thời gian: mean 257.68 ms | p50 215.29 ms | p95 484.2 ms | max 562.89 ms | tổng 25.77 s
- Nhầm ký tự nhiều nhất: `a->∅`×49, `7->∅`×32, `3->∅`×30, `x->∅`×22, `k->∅`×21, `c->∅`×21, `h->∅`×21, `6->∅`×20, `4->∅`×19, `b->∅`×19

### `tesseract5/psm6_whitelist/raw`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 4.0% | char acc: 12.4% | sai trung bình: 3.56 ký tự/ảnh
- Output rỗng: 73 | exception: 0
- Thời gian: mean 217.65 ms | p50 214.61 ms | p95 298.32 ms | max 370.71 ms | tổng 21.77 s
- Nhầm ký tự nhiều nhất: `a->∅`×50, `7->∅`×33, `3->∅`×28, `x->∅`×21, `c->∅`×21, `6->∅`×20, `h->∅`×20, `4->∅`×19, `e->∅`×18, `k->∅`×18

### `tesseract5/psm6_whitelist/upscale2x_otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 3.0% | char acc: 8.16% | sai trung bình: 3.72 ký tự/ảnh
- Output rỗng: 74 | exception: 0
- Thời gian: mean 209.91 ms | p50 184.2 ms | p95 302.94 ms | max 473.52 ms | tổng 20.99 s
- Nhầm ký tự nhiều nhất: `a->∅`×53, `7->∅`×31, `3->∅`×29, `6->∅`×25, `x->∅`×23, `h->∅`×21, `k->∅`×20, `c->∅`×19, `d->∅`×18, `4->∅`×18

### `tesseract5/psm7_whitelist/upscale2x_otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 3.0% | char acc: 6.8% | sai trung bình: 3.74 ký tự/ảnh
- Output rỗng: 87 | exception: 0
- Thời gian: mean 178.31 ms | p50 174.61 ms | p95 209.86 ms | max 246.69 ms | tổng 17.83 s
- Nhầm ký tự nhiều nhất: `a->∅`×55, `7->∅`×34, `3->∅`×32, `x->∅`×24, `6->∅`×24, `p->∅`×22, `4->∅`×22, `k->∅`×21, `b->∅`×21, `d->∅`×20

### `tesseract5/psm7_whitelist/otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 1.0% | char acc: 9.95% | sai trung bình: 3.63 ký tự/ảnh
- Output rỗng: 77 | exception: 0
- Thời gian: mean 218.04 ms | p50 216.32 ms | p95 298.63 ms | max 368.47 ms | tổng 21.8 s
- Nhầm ký tự nhiều nhất: `a->∅`×51, `7->∅`×31, `3->∅`×30, `k->∅`×23, `x->∅`×22, `h->∅`×22, `6->∅`×21, `b->∅`×21, `c->∅`×20, `4->∅`×19

### `tesseract5/psm6_whitelist/otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 1.0% | char acc: 9.17% | sai trung bình: 3.72 ký tự/ảnh
- Output rỗng: 73 | exception: 0
- Thời gian: mean 184.32 ms | p50 176.21 ms | p95 248.25 ms | max 283.84 ms | tổng 18.43 s
- Nhầm ký tự nhiều nhất: `a->∅`×50, `7->∅`×33, `3->∅`×28, `x->∅`×21, `h->∅`×21, `k->∅`×20, `c->∅`×20, `b->∅`×20, `6->∅`×19, `4->∅`×19

### `tesseract5/psm7_raw/otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 1.0% | char acc: 8.36% | sai trung bình: 3.72 ký tự/ảnh
- Output rỗng: 77 | exception: 0
- Thời gian: mean 193.95 ms | p50 175.32 ms | p95 287.08 ms | max 365.63 ms | tổng 19.4 s
- Nhầm ký tự nhiều nhất: `a->∅`×49, `7->∅`×30, `3->∅`×30, `x->∅`×22, `k->∅`×21, `h->∅`×21, `6->∅`×20, `c->∅`×19, `4->∅`×19, `b->∅`×19

### `tesseract5/psm7_raw/upscale2x_otsu`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 1.0% | char acc: 5.77% | sai trung bình: 3.79 ký tự/ảnh
- Output rỗng: 87 | exception: 0
- Thời gian: mean 209.31 ms | p50 197.81 ms | p95 277.67 ms | max 322.07 ms | tổng 20.93 s
- Nhầm ký tự nhiều nhất: `a->∅`×54, `7->∅`×33, `3->∅`×32, `6->∅`×24, `x->∅`×23, `p->∅`×22, `k->∅`×21, `4->∅`×21, `b->∅`×21, `d->∅`×20

### `tesseract5/psm7_raw/raw`

- Model: Tesseract 5 (CPU, psm)
- Ảnh chạy: 100 | đã chấm: 100
- Chính xác tuyệt đối: 0.0% | char acc: 10.41% | sai trung bình: 3.64 ký tự/ảnh
- Output rỗng: 77 | exception: 0
- Thời gian: mean 218.17 ms | p50 216.77 ms | p95 287.64 ms | max 370.16 ms | tổng 21.82 s
- Nhầm ký tự nhiều nhất: `a->∅`×49, `7->∅`×30, `3->∅`×30, `x->∅`×22, `k->∅`×21, `h->∅`×21, `c->∅`×20, `6->∅`×19, `b->∅`×19, `e->∅`×18

## Độ khó theo mực chữ (nhóm mẫu)

| Nhóm | Số ảnh | Tỉ lệ đúng (mẫu) |
|---|---|---|
| ink_19-24% | 1 | 100.0% |
| ink_21-26% | 5 | 100.0% |
| ink_22-27% | 14 | 100.0% |
| ink_23-28% | 22 | 100.0% |
| ink_24-29% | 27 | 100.0% |
| ink_25-30% | 19 | 94.74% |
| ink_26-31% | 10 | 100.0% |
| ink_27-32% | 1 | 100.0% |
| ink_28-33% | 1 | 100.0% |

## Mức độ giống nhau giữa các cấu hình (trên ảnh đã có nhãn)

| A | B | Ảnh | Giống nhau | Tỉ lệ |
|---|---|---|---|---|
| `ddddocr/alnum/otsu` | `ddddocr/alnum/otsu` | 100 | 100 | 100.0% |
| `ddddocr/alnum/otsu` | `ddddocr/alnum/raw` | 100 | 68 | 68.0% |
| `ddddocr/alnum/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/alnum/otsu` | `ddddocr/default/otsu` | 100 | 100 | 100.0% |
| `ddddocr/alnum/otsu` | `ddddocr/default/raw` | 100 | 69 | 69.0% |
| `ddddocr/alnum/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/alnum/otsu` | `ddddocr/old/otsu` | 100 | 100 | 100.0% |
| `ddddocr/alnum/otsu` | `ddddocr/old/raw` | 100 | 69 | 69.0% |
| `ddddocr/alnum/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/alnum/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 39 | 39.0% |
| `ddddocr/alnum/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 47 | 47.0% |
| `ddddocr/alnum/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 41 | 41.0% |
| `ddddocr/alnum/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 65 | 65.0% |
| `ddddocr/alnum/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 61 | 61.0% |
| `ddddocr/alnum/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 60 | 60.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 6 | 6.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm13_raw/raw` | 100 | 7 | 7.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 10 | 10.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 6 | 6.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 11 | 11.0% |
| `ddddocr/alnum/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ddddocr/alnum/raw` | `ddddocr/alnum/otsu` | 100 | 68 | 68.0% |
| `ddddocr/alnum/raw` | `ddddocr/alnum/raw` | 100 | 100 | 100.0% |
| `ddddocr/alnum/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 62 | 62.0% |
| `ddddocr/alnum/raw` | `ddddocr/default/otsu` | 100 | 68 | 68.0% |
| `ddddocr/alnum/raw` | `ddddocr/default/raw` | 100 | 99 | 99.0% |
| `ddddocr/alnum/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 62 | 62.0% |
| `ddddocr/alnum/raw` | `ddddocr/old/otsu` | 100 | 68 | 68.0% |
| `ddddocr/alnum/raw` | `ddddocr/old/raw` | 100 | 99 | 99.0% |
| `ddddocr/alnum/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 62 | 62.0% |
| `ddddocr/alnum/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 48 | 48.0% |
| `ddddocr/alnum/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 57 | 57.0% |
| `ddddocr/alnum/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 50 | 50.0% |
| `ddddocr/alnum/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 92 | 92.0% |
| `ddddocr/alnum/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 84 | 84.0% |
| `ddddocr/alnum/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 90 | 90.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm13_raw/otsu` | 100 | 7 | 7.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm13_raw/raw` | 100 | 9 | 9.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 3 | 3.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 3 | 3.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 8 | 8.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 16 | 16.0% |
| `ddddocr/alnum/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 17 | 17.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 78 | 78.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 62 | 62.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 78 | 78.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 63 | 63.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 78 | 78.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 63 | 63.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 32 | 32.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 42 | 42.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 35 | 35.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 59 | 59.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 55 | 55.0% |
| `ddddocr/alnum/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 4 | 4.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 5 | 5.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 10 | 10.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 5 | 5.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 9 | 9.0% |
| `ddddocr/alnum/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 11 | 11.0% |
| `ddddocr/default/otsu` | `ddddocr/alnum/otsu` | 100 | 100 | 100.0% |
| `ddddocr/default/otsu` | `ddddocr/alnum/raw` | 100 | 68 | 68.0% |
| `ddddocr/default/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/default/otsu` | `ddddocr/default/otsu` | 100 | 100 | 100.0% |
| `ddddocr/default/otsu` | `ddddocr/default/raw` | 100 | 69 | 69.0% |
| `ddddocr/default/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/default/otsu` | `ddddocr/old/otsu` | 100 | 100 | 100.0% |
| `ddddocr/default/otsu` | `ddddocr/old/raw` | 100 | 69 | 69.0% |
| `ddddocr/default/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/default/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 39 | 39.0% |
| `ddddocr/default/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 47 | 47.0% |
| `ddddocr/default/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 41 | 41.0% |
| `ddddocr/default/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 65 | 65.0% |
| `ddddocr/default/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 61 | 61.0% |
| `ddddocr/default/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 60 | 60.0% |
| `ddddocr/default/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 6 | 6.0% |
| `ddddocr/default/otsu` | `tesseract5/psm13_raw/raw` | 100 | 7 | 7.0% |
| `ddddocr/default/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 10 | 10.0% |
| `ddddocr/default/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/default/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/default/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/default/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/default/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/default/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 6 | 6.0% |
| `ddddocr/default/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 11 | 11.0% |
| `ddddocr/default/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ddddocr/default/raw` | `ddddocr/alnum/otsu` | 100 | 69 | 69.0% |
| `ddddocr/default/raw` | `ddddocr/alnum/raw` | 100 | 99 | 99.0% |
| `ddddocr/default/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 63 | 63.0% |
| `ddddocr/default/raw` | `ddddocr/default/otsu` | 100 | 69 | 69.0% |
| `ddddocr/default/raw` | `ddddocr/default/raw` | 100 | 100 | 100.0% |
| `ddddocr/default/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 63 | 63.0% |
| `ddddocr/default/raw` | `ddddocr/old/otsu` | 100 | 69 | 69.0% |
| `ddddocr/default/raw` | `ddddocr/old/raw` | 100 | 100 | 100.0% |
| `ddddocr/default/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 63 | 63.0% |
| `ddddocr/default/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 48 | 48.0% |
| `ddddocr/default/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 57 | 57.0% |
| `ddddocr/default/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 50 | 50.0% |
| `ddddocr/default/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 91 | 91.0% |
| `ddddocr/default/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 84 | 84.0% |
| `ddddocr/default/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 89 | 89.0% |
| `ddddocr/default/raw` | `tesseract5/psm13_raw/otsu` | 100 | 7 | 7.0% |
| `ddddocr/default/raw` | `tesseract5/psm13_raw/raw` | 100 | 9 | 9.0% |
| `ddddocr/default/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ddddocr/default/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ddddocr/default/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 3 | 3.0% |
| `ddddocr/default/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ddddocr/default/raw` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ddddocr/default/raw` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/default/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ddddocr/default/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 3 | 3.0% |
| `ddddocr/default/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ddddocr/default/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 8 | 8.0% |
| `ddddocr/default/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 16 | 16.0% |
| `ddddocr/default/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 17 | 17.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 78 | 78.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 62 | 62.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 78 | 78.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 63 | 63.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 78 | 78.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 63 | 63.0% |
| `ddddocr/default/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/default/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 32 | 32.0% |
| `ddddocr/default/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 42 | 42.0% |
| `ddddocr/default/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 35 | 35.0% |
| `ddddocr/default/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 59 | 59.0% |
| `ddddocr/default/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 55 | 55.0% |
| `ddddocr/default/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 4 | 4.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 5 | 5.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 10 | 10.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 5 | 5.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 9 | 9.0% |
| `ddddocr/default/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 11 | 11.0% |
| `ddddocr/old/otsu` | `ddddocr/alnum/otsu` | 100 | 100 | 100.0% |
| `ddddocr/old/otsu` | `ddddocr/alnum/raw` | 100 | 68 | 68.0% |
| `ddddocr/old/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/old/otsu` | `ddddocr/default/otsu` | 100 | 100 | 100.0% |
| `ddddocr/old/otsu` | `ddddocr/default/raw` | 100 | 69 | 69.0% |
| `ddddocr/old/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/old/otsu` | `ddddocr/old/otsu` | 100 | 100 | 100.0% |
| `ddddocr/old/otsu` | `ddddocr/old/raw` | 100 | 69 | 69.0% |
| `ddddocr/old/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 78 | 78.0% |
| `ddddocr/old/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 39 | 39.0% |
| `ddddocr/old/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 47 | 47.0% |
| `ddddocr/old/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 41 | 41.0% |
| `ddddocr/old/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 65 | 65.0% |
| `ddddocr/old/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 61 | 61.0% |
| `ddddocr/old/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 60 | 60.0% |
| `ddddocr/old/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 6 | 6.0% |
| `ddddocr/old/otsu` | `tesseract5/psm13_raw/raw` | 100 | 7 | 7.0% |
| `ddddocr/old/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 10 | 10.0% |
| `ddddocr/old/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/old/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/old/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/old/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/old/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/old/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 6 | 6.0% |
| `ddddocr/old/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 11 | 11.0% |
| `ddddocr/old/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ddddocr/old/raw` | `ddddocr/alnum/otsu` | 100 | 69 | 69.0% |
| `ddddocr/old/raw` | `ddddocr/alnum/raw` | 100 | 99 | 99.0% |
| `ddddocr/old/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 63 | 63.0% |
| `ddddocr/old/raw` | `ddddocr/default/otsu` | 100 | 69 | 69.0% |
| `ddddocr/old/raw` | `ddddocr/default/raw` | 100 | 100 | 100.0% |
| `ddddocr/old/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 63 | 63.0% |
| `ddddocr/old/raw` | `ddddocr/old/otsu` | 100 | 69 | 69.0% |
| `ddddocr/old/raw` | `ddddocr/old/raw` | 100 | 100 | 100.0% |
| `ddddocr/old/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 63 | 63.0% |
| `ddddocr/old/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 48 | 48.0% |
| `ddddocr/old/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 57 | 57.0% |
| `ddddocr/old/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 50 | 50.0% |
| `ddddocr/old/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 91 | 91.0% |
| `ddddocr/old/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 84 | 84.0% |
| `ddddocr/old/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 89 | 89.0% |
| `ddddocr/old/raw` | `tesseract5/psm13_raw/otsu` | 100 | 7 | 7.0% |
| `ddddocr/old/raw` | `tesseract5/psm13_raw/raw` | 100 | 9 | 9.0% |
| `ddddocr/old/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ddddocr/old/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ddddocr/old/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 3 | 3.0% |
| `ddddocr/old/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ddddocr/old/raw` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ddddocr/old/raw` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/old/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ddddocr/old/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 3 | 3.0% |
| `ddddocr/old/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ddddocr/old/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 8 | 8.0% |
| `ddddocr/old/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 16 | 16.0% |
| `ddddocr/old/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 17 | 17.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 78 | 78.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 62 | 62.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 78 | 78.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 63 | 63.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 78 | 78.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 63 | 63.0% |
| `ddddocr/old/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ddddocr/old/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 32 | 32.0% |
| `ddddocr/old/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 42 | 42.0% |
| `ddddocr/old/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 35 | 35.0% |
| `ddddocr/old/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 59 | 59.0% |
| `ddddocr/old/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 55 | 55.0% |
| `ddddocr/old/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 4 | 4.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 5 | 5.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 10 | 10.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 0 | 0.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 1 | 1.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 5 | 5.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 9 | 9.0% |
| `ddddocr/old/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 11 | 11.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/alnum/otsu` | 100 | 39 | 39.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/alnum/raw` | 100 | 48 | 48.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 32 | 32.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/default/otsu` | 100 | 39 | 39.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/default/raw` | 100 | 48 | 48.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 32 | 32.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/old/otsu` | 100 | 39 | 39.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/old/raw` | 100 | 48 | 48.0% |
| `ppocr_v5_en/rec_only/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 32 | 32.0% |
| `ppocr_v5_en/rec_only/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 100 | 100.0% |
| `ppocr_v5_en/rec_only/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 62 | 62.0% |
| `ppocr_v5_en/rec_only/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 71 | 71.0% |
| `ppocr_v5_en/rec_only/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 53 | 53.0% |
| `ppocr_v5_en/rec_only/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 48 | 48.0% |
| `ppocr_v5_en/rec_only/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 50 | 50.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 5 | 5.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm13_raw/raw` | 100 | 5 | 5.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 10 | 10.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 2 | 2.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 2 | 2.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 6 | 6.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 9 | 9.0% |
| `ppocr_v5_en/rec_only/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 13 | 13.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/alnum/otsu` | 100 | 47 | 47.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/alnum/raw` | 100 | 57 | 57.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 42 | 42.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/default/otsu` | 100 | 47 | 47.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/default/raw` | 100 | 57 | 57.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 42 | 42.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/old/otsu` | 100 | 47 | 47.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/old/raw` | 100 | 57 | 57.0% |
| `ppocr_v5_en/rec_only/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 42 | 42.0% |
| `ppocr_v5_en/rec_only/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 62 | 62.0% |
| `ppocr_v5_en/rec_only/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 100 | 100.0% |
| `ppocr_v5_en/rec_only/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 65 | 65.0% |
| `ppocr_v5_en/rec_only/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 59 | 59.0% |
| `ppocr_v5_en/rec_only/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 56 | 56.0% |
| `ppocr_v5_en/rec_only/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 58 | 58.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm13_raw/otsu` | 100 | 7 | 7.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm13_raw/raw` | 100 | 8 | 8.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 2 | 2.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 2 | 2.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 8 | 8.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 14 | 14.0% |
| `ppocr_v5_en/rec_only/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 14 | 14.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 41 | 41.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 50 | 50.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 35 | 35.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 41 | 41.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 50 | 50.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 35 | 35.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 41 | 41.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 50 | 50.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 35 | 35.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 71 | 71.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 65 | 65.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 53 | 53.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 52 | 52.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 53 | 53.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 6 | 6.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 9 | 9.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 10 | 10.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 2 | 2.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 2 | 2.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 7 | 7.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 13 | 13.0% |
| `ppocr_v5_en/rec_only/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/alnum/otsu` | 100 | 65 | 65.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/alnum/raw` | 100 | 92 | 92.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 59 | 59.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/default/otsu` | 100 | 65 | 65.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/default/raw` | 100 | 91 | 91.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 59 | 59.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/old/otsu` | 100 | 65 | 65.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/old/raw` | 100 | 91 | 91.0% |
| `ppocr_v6_small/rec_only/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 59 | 59.0% |
| `ppocr_v6_small/rec_only/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 53 | 53.0% |
| `ppocr_v6_small/rec_only/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 59 | 59.0% |
| `ppocr_v6_small/rec_only/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 53 | 53.0% |
| `ppocr_v6_small/rec_only/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 100 | 100.0% |
| `ppocr_v6_small/rec_only/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 84 | 84.0% |
| `ppocr_v6_small/rec_only/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 88 | 88.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 7 | 7.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm13_raw/raw` | 100 | 9 | 9.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 13 | 13.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 4 | 4.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 4 | 4.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 8 | 8.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 17 | 17.0% |
| `ppocr_v6_small/rec_only/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 17 | 17.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/alnum/otsu` | 100 | 61 | 61.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/alnum/raw` | 100 | 84 | 84.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/default/otsu` | 100 | 61 | 61.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/default/raw` | 100 | 84 | 84.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/old/otsu` | 100 | 61 | 61.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/old/raw` | 100 | 84 | 84.0% |
| `ppocr_v6_small/rec_only/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ppocr_v6_small/rec_only/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 48 | 48.0% |
| `ppocr_v6_small/rec_only/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 56 | 56.0% |
| `ppocr_v6_small/rec_only/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 52 | 52.0% |
| `ppocr_v6_small/rec_only/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 84 | 84.0% |
| `ppocr_v6_small/rec_only/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 100 | 100.0% |
| `ppocr_v6_small/rec_only/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 86 | 86.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm13_raw/otsu` | 100 | 6 | 6.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm13_raw/raw` | 100 | 8 | 8.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 13 | 13.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 4 | 4.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 4 | 4.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 8 | 8.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 14 | 14.0% |
| `ppocr_v6_small/rec_only/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 17 | 17.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 60 | 60.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 90 | 90.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 60 | 60.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 89 | 89.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 60 | 60.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 89 | 89.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 55 | 55.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 50 | 50.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 58 | 58.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 53 | 53.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 88 | 88.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 86 | 86.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 100 | 100.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 6 | 6.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 9 | 9.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 12 | 12.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 4 | 4.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 0 | 0.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 1 | 1.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 4 | 4.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 8 | 8.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 17 | 17.0% |
| `ppocr_v6_small/rec_only/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 17 | 17.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/alnum/otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/alnum/raw` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/default/otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/default/raw` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/old/otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/old/raw` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm13_raw/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 6 | 6.0% |
| `tesseract5/psm13_raw/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm13_raw/raw` | 100 | 14 | 14.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 22 | 22.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 21 | 21.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm7_raw/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 8 | 8.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 50 | 50.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 13 | 13.0% |
| `tesseract5/psm13_raw/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 16 | 16.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/alnum/otsu` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/alnum/raw` | 100 | 9 | 9.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/default/otsu` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/default/raw` | 100 | 9 | 9.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/old/otsu` | 100 | 7 | 7.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/old/raw` | 100 | 9 | 9.0% |
| `tesseract5/psm13_raw/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 8 | 8.0% |
| `tesseract5/psm13_raw/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 9 | 9.0% |
| `tesseract5/psm13_raw/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 9 | 9.0% |
| `tesseract5/psm13_raw/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 8 | 8.0% |
| `tesseract5/psm13_raw/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 9 | 9.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm13_raw/otsu` | 100 | 14 | 14.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm13_raw/raw` | 100 | 100 | 100.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 25 | 25.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm7_raw/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm7_raw/raw` | 100 | 21 | 21.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 15 | 15.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 47 | 47.0% |
| `tesseract5/psm13_raw/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 18 | 18.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 10 | 10.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 12 | 12.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 10 | 10.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 10 | 10.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 12 | 12.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 10 | 10.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 10 | 10.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 12 | 12.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 10 | 10.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 10 | 10.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 12 | 12.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 10 | 10.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 13 | 13.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 13 | 13.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 22 | 22.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 25 | 25.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 17 | 17.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 19 | 19.0% |
| `tesseract5/psm13_raw/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 57 | 57.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/alnum/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/alnum/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/default/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/default/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/old/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/old/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm6_whitelist/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 7 | 7.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm13_raw/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 77 | 77.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 65 | 65.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 78 | 78.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm7_raw/raw` | 100 | 74 | 74.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 72 | 72.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 90 | 90.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 75 | 75.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 73 | 73.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 19 | 19.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/alnum/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/alnum/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/default/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/default/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/old/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/old/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm6_whitelist/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm13_raw/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm13_raw/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 77 | 77.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 100 | 100.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 68 | 68.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm7_raw/otsu` | 100 | 75 | 75.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm7_raw/raw` | 100 | 75 | 75.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 73 | 73.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 75 | 75.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 90 | 90.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 76 | 76.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 19 | 19.0% |
| `tesseract5/psm6_whitelist/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 7 | 7.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 65 | 65.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 68 | 68.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 67 | 67.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 67 | 67.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 78 | 78.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 68 | 68.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 71 | 71.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 85 | 85.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 5 | 5.0% |
| `tesseract5/psm6_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/alnum/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/alnum/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/default/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/default/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/old/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/old/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 21 | 21.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm13_raw/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 78 | 78.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 75 | 75.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 67 | 67.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm7_raw/raw` | 100 | 81 | 81.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 76 | 76.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 85 | 85.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 81 | 81.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 76 | 76.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 8 | 8.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm7_raw/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/alnum/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/alnum/raw` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/default/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/default/raw` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/old/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/old/raw` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm13_raw/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm13_raw/raw` | 100 | 21 | 21.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 74 | 74.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 75 | 75.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 67 | 67.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm7_raw/otsu` | 100 | 81 | 81.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm7_raw/raw` | 100 | 100 | 100.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 77 | 77.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 80 | 80.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 84 | 84.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 76 | 76.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 5 | 5.0% |
| `tesseract5/psm7_raw/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 72 | 72.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 73 | 73.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 78 | 78.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 76 | 76.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 77 | 77.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 76 | 76.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 77 | 77.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 93 | 93.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm7_raw/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/alnum/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/alnum/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/default/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/default/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/old/otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/old/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 0 | 0.0% |
| `tesseract5/psm7_whitelist/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 8 | 8.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm13_raw/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 90 | 90.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 75 | 75.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 68 | 68.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 85 | 85.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm7_raw/raw` | 100 | 80 | 80.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 76 | 76.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 81 | 81.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 77 | 77.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 21 | 21.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm7_whitelist/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/alnum/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/alnum/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/default/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/default/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/old/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/old/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm7_whitelist/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm7_whitelist/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm7_whitelist/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm13_raw/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm13_raw/raw` | 100 | 5 | 5.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 75 | 75.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 90 | 90.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 71 | 71.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm7_raw/otsu` | 100 | 81 | 81.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm7_raw/raw` | 100 | 84 | 84.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 77 | 77.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 81 | 81.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 100 | 100.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 80 | 80.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 21 | 21.0% |
| `tesseract5/psm7_whitelist/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 9 | 9.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 1 | 1.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 73 | 73.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 76 | 76.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 85 | 85.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 76 | 76.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 76 | 76.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 93 | 93.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 77 | 77.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 80 | 80.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 5 | 5.0% |
| `tesseract5/psm7_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/alnum/otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/alnum/raw` | 100 | 8 | 8.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/default/otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/default/raw` | 100 | 8 | 8.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/old/otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/old/raw` | 100 | 8 | 8.0% |
| `tesseract5/psm8_whitelist/otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm8_whitelist/otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 6 | 6.0% |
| `tesseract5/psm8_whitelist/otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 8 | 8.0% |
| `tesseract5/psm8_whitelist/otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 7 | 7.0% |
| `tesseract5/psm8_whitelist/otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 8 | 8.0% |
| `tesseract5/psm8_whitelist/otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 8 | 8.0% |
| `tesseract5/psm8_whitelist/otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 8 | 8.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm13_raw/otsu` | 100 | 50 | 50.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm13_raw/raw` | 100 | 15 | 15.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 19 | 19.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm7_raw/otsu` | 100 | 8 | 8.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm7_raw/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 1 | 1.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 21 | 21.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 4 | 4.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 100 | 100.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 19 | 19.0% |
| `tesseract5/psm8_whitelist/otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 21 | 21.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/alnum/otsu` | 100 | 11 | 11.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/alnum/raw` | 100 | 16 | 16.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/alnum/upscale2x_otsu` | 100 | 9 | 9.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/default/otsu` | 100 | 11 | 11.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/default/raw` | 100 | 16 | 16.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/default/upscale2x_otsu` | 100 | 9 | 9.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/old/otsu` | 100 | 11 | 11.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/old/raw` | 100 | 16 | 16.0% |
| `tesseract5/psm8_whitelist/raw` | `ddddocr/old/upscale2x_otsu` | 100 | 9 | 9.0% |
| `tesseract5/psm8_whitelist/raw` | `ppocr_v5_en/rec_only/otsu` | 100 | 9 | 9.0% |
| `tesseract5/psm8_whitelist/raw` | `ppocr_v5_en/rec_only/raw` | 100 | 14 | 14.0% |
| `tesseract5/psm8_whitelist/raw` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 13 | 13.0% |
| `tesseract5/psm8_whitelist/raw` | `ppocr_v6_small/rec_only/otsu` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/raw` | `ppocr_v6_small/rec_only/raw` | 100 | 14 | 14.0% |
| `tesseract5/psm8_whitelist/raw` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm13_raw/otsu` | 100 | 13 | 13.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm13_raw/raw` | 100 | 47 | 47.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 19 | 19.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm6_whitelist/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm6_whitelist/raw` | 100 | 19 | 19.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm7_raw/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm7_raw/raw` | 100 | 5 | 5.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 2 | 2.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm7_whitelist/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm7_whitelist/raw` | 100 | 21 | 21.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm8_whitelist/otsu` | 100 | 19 | 19.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm8_whitelist/raw` | 100 | 100 | 100.0% |
| `tesseract5/psm8_whitelist/raw` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 35 | 35.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/alnum/otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/alnum/raw` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/alnum/upscale2x_otsu` | 100 | 11 | 11.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/default/otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/default/raw` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/default/upscale2x_otsu` | 100 | 11 | 11.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/old/otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/old/raw` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ddddocr/old/upscale2x_otsu` | 100 | 11 | 11.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/otsu` | 100 | 13 | 13.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/raw` | 100 | 14 | 14.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ppocr_v5_en/rec_only/upscale2x_otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/otsu` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/raw` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `ppocr_v6_small/rec_only/upscale2x_otsu` | 100 | 17 | 17.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/otsu` | 100 | 16 | 16.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/raw` | 100 | 18 | 18.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm13_raw/upscale2x_otsu` | 100 | 57 | 57.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/raw` | 100 | 7 | 7.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm6_whitelist/upscale2x_otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/otsu` | 100 | 3 | 3.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/raw` | 100 | 3 | 3.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm7_raw/upscale2x_otsu` | 100 | 5 | 5.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/otsu` | 100 | 4 | 4.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/raw` | 100 | 9 | 9.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm7_whitelist/upscale2x_otsu` | 100 | 12 | 12.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/otsu` | 100 | 21 | 21.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/raw` | 100 | 35 | 35.0% |
| `tesseract5/psm8_whitelist/upscale2x_otsu` | `tesseract5/psm8_whitelist/upscale2x_otsu` | 100 | 100 | 100.0% |

## Ghi chú

- `char acc` dùng công thức 1 - levenshtein/max(len), không phân biệt thứ tự lỗi.
- `Rỗng` là số ảnh model trả về chuỗi rỗng sau khi chuẩn hoá về `[0-9a-z]`.
- Số liệu thô nằm ở `captcha/bench/runs/<run_id>/rows.jsonl`.
