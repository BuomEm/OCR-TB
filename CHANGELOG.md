# Changelog

Má»i thay Ä‘á»•i Ä‘Ã¡ng chÃº Ã½ cá»§a OCR-TB Ä‘Æ°á»£c ghi láº¡i táº¡i Ä‘Ã¢y.
Cáº¥u trÃºc dá»±a theo [Keep a Changelog](https://keepachangelog.com/v1.1.0/) vÃ 
[Semantic Versioning](https://semver.org/lang/vi/).

## [1.0.0] - 2026-10-18

### Báº£n phÃ¡t hÃ nh Ä‘áº§u tiÃªn

#### ThÃªm
- `ocr-tb solve`: giáº£i 1 hoáº·c nhiá»u áº£nh captcha, há»— trá»£ thÆ° má»¥c, `--json`.
- Chuá»—i fallback: `ddddocr/default/raw` â†’ `ppocr_v6_small/rec_only/otsu`,
  dá»«ng sá»›m khi Ä‘áº¡t `--expect-length`.
- HTTP server FastAPI: `GET /health`, `GET /models`, `POST /models/pull`,
  `POST /solve`, `POST /solve/upload`, `POST /solve/batch`, `POST /normalize`.
- Bá»™ benchmark: cháº¡y nhiá»u model Ã— config Ã— biáº¿n thá»ƒ tiá»n xá»­ lÃ½, ghi `rows.jsonl`,
  xuáº¥t bÃ¡o cÃ¡o Markdown + CSV + JSON.
- GÃ¡n nhÃ£n thá»§ cÃ´ng: `ocr-tb label make` sinh `labeling.html` (lÆ°u localStorage, xuáº¥t CSV).
- Registry 4 model: `ddddocr`, `ppocr_v5_en`, `ppocr_v6_small`, `tesseract5`.
- Tiá»n xá»­ lÃ½ áº£nh: `raw`, `gray`, `otsu`, `upscale2x_otsu`.
- `ocr-tb memory`: Ä‘o RSS vÃ  dung lÆ°á»£ng Ä‘Ä©a thá»±c táº¿.
- Táº£i model ONNX vá» cache vÄ©nh viá»…n (`ocr-tb models pull`), há»— trá»£ `HF_ENDPOINT`.
- CÃ i Ä‘áº·t: `install.sh` (Linux/macOS), `install.ps1` (Windows), `install-service.sh`
  (systemd), `Dockerfile` (python:3.12-slim, user khÃ´ng pháº£i root).
- CI: test trÃªn ubuntu/windows/macos Ã— Python 3.11/3.12 + build vÃ  smoke test Docker.
- 3 áº£nh captcha máº«u kÃ¨m nhÃ£n trong `samples/`, dÃ¹ng lÃ m test há»“i quy.

#### Káº¿t quáº£ Ä‘o (100 áº£nh captcha 4 ký tự, CPU)
- `ddddocr/alnum`: 99% chÃ­nh xÃ¡c, 59 ms/áº£nh.
- `ddddocr/default`: 98% chÃ­nh xÃ¡c, 22 ms/áº£nh â€” khuyáº¿n nghá»‹.
- `ppocr_v6_small` + `otsu`: 93% chÃ­nh xÃ¡c, 25 ms/áº£nh.
- `tesseract5 --psm 8`: 17% chÃ­nh xÃ¡c â€” khÃ´ng kháº£ dá»¥ng cho captcha nhiá»…u náº·ng.

[1.0.0]: https://github.com/BuomEm/OCR-TB/releases/tag/v1.0.0