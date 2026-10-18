"""CLI của OCR-TB.

    ocr-tb solve <file|thư mục> [--model ddddocr] [--config default] [--variant raw]
    ocr-tb serve [--host 0.0.0.0] [--port 2424]
    ocr-tb models list | pull [model_id...] | path
    ocr-tb bench run  [--models ...] [--variants raw,otsu] [--limit N]
    ocr-tb bench score [--run-id ...]
    ocr-tb label make | check
    ocr-tb info
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import (
    APP_NAME,
    DEFAULT_CONFIG,
    DEFAULT_MODEL,
    DEFAULT_VARIANT,
    SERVER_HOST,
    SERVER_PORT,
    VERSION,
    describe_paths,
    enable_utf8_console,
    ensure_dirs,
)
from .preprocess import VARIANTS
from .solver import DEFAULT_CHAIN, Solver
from .util import REPORT_DIR, list_images


def _fail(message: str) -> int:
    print(f"[{APP_NAME}] LỖI: {message}", file=sys.stderr)
    return 1


def _parse_chain(model: str | None, config: str | None, variant: str | None) -> list[dict[str, str]] | None:
    if not model:
        return None
    return [{"model": model, "config": config or "default", "variant": variant or "raw"}]


def _version_string() -> str:
    from .update import current_version

    return f"{APP_NAME} {current_version()}"


def cmd_solve(args: argparse.Namespace) -> int:
    paths: list[Path] = []
    for target in args.paths:
        path = Path(target)
        if path.is_dir():
            paths.extend(list_images(path))
        elif path.exists():
            paths.append(path)
        else:
            print(f"Bỏ qua (không tồn tại): {target}", file=sys.stderr)

    if not paths:
        return _fail("không có ảnh nào để xử lý")

    ensure_dirs()
    solver = Solver()
    chain = _parse_chain(args.model, args.config, args.variant)
    if args.fallback and chain is None:
        chain = DEFAULT_CHAIN

    results = []
    for path in paths:
        try:
            result = solver.solve(path.read_bytes(), chain=chain, expect_length=args.expect_length)
        except Exception as error:  # noqa: BLE001
            print(f"LỖI {path.name}: {type(error).__name__}: {error}", file=sys.stderr)
            results.append({"file": path.name, "error": f"{type(error).__name__}: {error}"})
            continue

        results.append({"file": path.name, **result.to_dict()})
        if args.json:
            continue
        extra = f" conf={result.confidence}" if result.confidence is not None else ""
        print(f"{path.name}\t{result.normalized or '(rỗng)'}\t[{result.model_id}/{result.config_id}/{result.variant}]"
              f"\t{result.elapsed_ms:.0f} ms{extra}")
        if len(result.attempts) > 1:
            for attempt in result.attempts[:-1]:
                print(f"    (fallback) {attempt.get('model')}/{attempt.get('config')} -> {attempt.get('text')!r}")

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


def cmd_serve(args: argparse.Namespace) -> int:  # pragma: no cover
    from .server import run
    from .update import update_notice

    notice = update_notice()
    if notice:
        print(notice)

    run(args.host, args.port, args.threads)
    return 0


def cmd_models(args: argparse.Namespace) -> int:
    from .download import cache_status, pull_model, pull_all
    from .registry import build_registry

    if args.action == "list":
        registry = build_registry()
        cache = {row["model_id"]: row for row in cache_status()}
        payload = []
        for model in registry:
            entry = model.describe()
            if not model.builtin:
                entry["cache"] = cache.get(model.remote_id if hasattr(model, "remote_id") else model.id, {})
            payload.append(entry)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.action == "path":
        from .config import CACHE_DIR

        print(CACHE_DIR)
        return 0

    if args.action == "pull":
        ensure_dirs()
        if args.model_ids:
            for model_id in args.model_ids:
                try:
                    pull_model(model_id, force=args.force)
                except KeyError as error:
                    return _fail(str(error))
        else:
            pull_all(force=args.force)
        return 0

    return _fail(f"hành động không hợp lệ: {args.action}")


def cmd_bench(args: argparse.Namespace) -> int:
    from .bench import run_benchmark, score_run
    from .util import ensure_bench_dirs

    ensure_bench_dirs()
    if args.action == "run":
        run_benchmark(
            models=[m.strip() for m in args.models.split(",")] if args.models else None,
            configs=args.configs,
            variants=[v.strip() for v in args.variants.split(",")] if args.variants else None,
            limit=args.limit,
            repeat=args.repeat,
            warmup=args.warmup,
            run_id=args.run_id,
        )
        if not args.no_score:
            payload = score_run(args.run_id or "")
            _print_top(payload)
        return 0

    if args.action == "score":
        _print_top(score_run(args.run_id or ""))
        return 0

    return _fail(f"hành động không hợp lệ: {args.action}")


def _print_top(payload: dict) -> None:
    run_id = payload["run_id"]
    print(f"\nBáo cáo : {REPORT_DIR / f'report-{run_id}.md'}")
    print(f"Điểm CSV: {REPORT_DIR / f'score-{run_id}.csv'}")
    print(f"Chi tiết: {REPORT_DIR / f'details-{run_id}.csv'}")
    print(f"Nhãn: {payload['labeled_images']}/{payload['total_images']} ảnh")
    print("\nTop 5:")
    for index, item in enumerate(payload["ranked"][:5], start=1):
        score = item["score"]
        accuracy = f"{score['exact_accuracy']}%" if score["exact_accuracy"] is not None else "chưa chấm"
        print(f"  {index}. {item['name']}: chính xác {accuracy}, {score['timing']['mean']} ms/ảnh")


def cmd_label(args: argparse.Namespace) -> int:
    from .bench import label_progress, write_labeling_html, write_labels_template

    if args.action == "make":
        template = write_labels_template()
        page = write_labeling_html(args.expect_length)
        print(f"Đã tạo:\n  {template}\n  {page}")
        if args.open:
            import webbrowser

            webbrowser.open(page.as_uri())
        return 0

    if args.action == "check":
        progress = label_progress()
        print(f"Tổng ảnh : {progress['total']}")
        print(f"Đã gán   : {progress['labeled']}")
        print(f"Thiếu     : {progress['missing']}")
        if progress["missing_sample"]:
            print("  ví dụ:", ", ".join(progress["missing_sample"]))
        return 0

    return _fail(f"hành động không hợp lệ: {args.action}")


def cmd_info(args: argparse.Namespace) -> int:
    from .download import cache_status, missing_models
    from .registry import build_registry
    from .util import library_versions, platform_info, workdir

    payload = {
        "app": APP_NAME,
        "version": VERSION,
        "paths": {**describe_paths(), "images": str(workdir())},
        "platform": platform_info(),
        "libraries": library_versions(),
        "models": [model.describe() for model in build_registry()],
        "cache": cache_status(),
        "missing_downloads": missing_models(),
        "default_chain": DEFAULT_CHAIN,
        "variants": list(VARIANTS),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    from .update import apply_update, check_status

    status = check_status()
    print(f"{APP_NAME} hiện tại : {status['current']}")
    print(f"Kiểm tra release   : {status['message']}")
    if status.get("latest"):
        print(f"Trang release      : {status['latest']['url']}")

    if args.check:
        return 0
    if status.get("update_available") is False:
        print("Không có bản mới, không cần cập nhật.")
        return 0
    if not args.yes:
        answer = input("Cập nhật ngay? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Đã huỷ.")
            return 0

    code = apply_update(assume_yes=True, dry_run=args.dry_run)
    if code == 0:
        print("\nCập nhật xong. Kiểm tra bằng: ocr-tb --version")
    else:
        print(f"\nCập nhật thất bại (exit {code}). Xem README mục 'Cập nhật'.", file=sys.stderr)
    return code


def cmd_memory(args: argparse.Namespace) -> int:
    from pathlib import Path as _Path

    from .memory import format_report, measure

    image_dir = _Path(args.images).expanduser() if args.images else None
    print(format_report(measure(image_dir)))
    return 0


def cmd_record_install(args: argparse.Namespace) -> int:
    """Script cài đặt gọi lệnh này để `ocr-tb update` biết cập nhật theo cách nào."""
    from .update import record_install

    path = record_install(args.method, repo_dir=args.repo_dir, extra={"prefix": args.prefix})
    print(f"Đã ghi thông tin cài đặt: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=APP_NAME, description="OCR-TB: giải captcha + benchmark OCR")
    parser.add_argument("--version", action="version", version=_version_string())
    sub = parser.add_subparsers(dest="command", required=True)

    # ------------------------------------------------------------------ solve
    solve = sub.add_parser("solve", help="giải 1 hoặc nhiều ảnh captcha")
    solve.add_argument("paths", nargs="+", help="file ảnh hoặc thư mục chứa ảnh")
    solve.add_argument("--model", default=None, help=f"model id (mặc định {DEFAULT_MODEL})")
    solve.add_argument("--config", default=DEFAULT_CONFIG or None, help="config của model")
    solve.add_argument("--variant", default=None, choices=sorted(VARIANTS), help="tiền xử lý ảnh")
    solve.add_argument("--expect-length", type=int, default=None, help="dừng chuỗi fallback khi đạt độ dài này")
    solve.add_argument("--fallback", action="store_true", help="dùng chuỗi model dự phòng khi không chỉ định --model")
    solve.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    solve.set_defaults(func=cmd_solve)

    # ------------------------------------------------------------------ serve
    serve = sub.add_parser("serve", help="chạy HTTP server")
    serve.add_argument("--host", default=SERVER_HOST)
    serve.add_argument("--port", type=int, default=SERVER_PORT)
    serve.add_argument("--threads", type=int, default=4, help="số luồng xử lý song song")
    serve.set_defaults(func=cmd_serve)

    # ------------------------------------------------------------------ models
    models = sub.add_parser("models", help="quản lý model")
    models.add_argument("action", choices=["list", "pull", "path"])
    models.add_argument("model_ids", nargs="*", help="model id cần tải (bỏ trống = tất cả)")
    models.add_argument("--force", action="store_true", help="tải lại dù đã có")
    models.set_defaults(func=cmd_models)

    # ------------------------------------------------------------------ bench
    bench = sub.add_parser("bench", help="chạy/chấm benchmark")
    bench.add_argument("action", choices=["run", "score"])
    bench.add_argument("--models", default="", help="danh sách model id")
    bench.add_argument("--configs", default="", help='vd: "ddddocr:default|alnum,tesseract5:psm8_whitelist"')
    bench.add_argument("--variants", default="raw", help="tiền xử lý: raw,gray,otsu,upscale2x_otsu")
    bench.add_argument("--limit", type=int, default=0)
    bench.add_argument("--repeat", type=int, default=1)
    bench.add_argument("--warmup", type=int, default=3)
    bench.add_argument("--run-id", default="")
    bench.add_argument("--no-score", action="store_true", help="chạy xong không chấm điểm")
    bench.set_defaults(func=cmd_bench)

    # ------------------------------------------------------------------ label
    label = sub.add_parser("label", help="tạo bảng gán nhãn thủ công")
    label.add_argument("action", choices=["make", "check"])
    label.add_argument("--expect-length", type=int, default=4, help="số ký tự của captcha")
    label.add_argument("--open", action="store_true", help="mở labeling.html bằng trình duyệt")
    label.set_defaults(func=cmd_label)

    # ------------------------------------------------------------------ info
    info = sub.add_parser("info", help="thông tin môi trường + model")
    info.set_defaults(func=cmd_info)

    # ------------------------------------------------------------------ memory
    memory = sub.add_parser("memory", help="đo RAM khi nạp/chạy model + dung lượng đĩa")
    memory.add_argument("--images", default=None, help="thư mục ảnh để đo (mặc định OCR_TB_IMAGES)")
    memory.set_defaults(func=cmd_memory)

    # ------------------------------------------------------------------ update
    update = sub.add_parser("update", help="kiểm tra và cập nhật OCR-TB từ GitHub Releases")
    update.add_argument("--check", action="store_true", help="chỉ kiểm tra, không cập nhật")
    update.add_argument("-y", "--yes", action="store_true", help="không hỏi lại")
    update.add_argument("--dry-run", action="store_true", help="in lệnh sẽ chạy mà không thực thi")
    update.set_defaults(func=cmd_update)

    # ------------------------------------------------- record-install (nội bộ)
    record = sub.add_parser("record-install", help=argparse.SUPPRESS)
    record.add_argument("--method", choices=["script", "source", "pypi"], required=True)
    record.add_argument("--repo-dir", default=None)
    record.add_argument("--prefix", default=None)
    record.set_defaults(func=cmd_record_install)

    return parser


def main(argv: list[str] | None = None) -> int:
    enable_utf8_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:  # pragma: no cover
        return 130
    except SystemExit as error:  # pragma: no cover
        return int(error.code or 0)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())


__all__ = ["build_parser", "main"]