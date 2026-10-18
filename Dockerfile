# OCR-TB: ghi captcha OCR + HTTP server
# Build:  docker build -t ocr-tb:1.0.0 tools/ocr-tb
# Run:    docker run --rm -p 8080:8080 ocr-tb:1.0.0
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OCR_TB_HOME=/opt/ocr-tb \
    OCR_TB_CACHE=/opt/ocr-tb/models \
    OCR_TB_HOST=0.0.0.0 \
    OCR_TB_PORT=8080

# libGL/libglib: opencv-python cần khi cài qua rapidocr; tesseract cho benchmark.
RUN apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        libgl1 \
        libglib2.0-0 \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --upgrade pip && pip install ".[server]" \
    && ocr-tb models pull ppocr_v6_small

# Không chạy bằng root.
RUN useradd --create-home --uid 10001 ocrtb \
    && mkdir -p /opt/ocr-tb \
    && chown -R ocrtb:ocrtb /opt/ocr-tb /app
USER ocrtb

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -fsS "http://127.0.0.1:${OCR_TB_PORT}/health" || exit 1

ENTRYPOINT ["ocr-tb"]
CMD ["serve"]