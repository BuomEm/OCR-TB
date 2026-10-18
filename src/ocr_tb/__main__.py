"""Cho phép chạy `python -m ocr_tb`."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())