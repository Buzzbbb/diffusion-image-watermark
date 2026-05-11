"""Command line interface for the project."""

from __future__ import annotations

import argparse
from pathlib import Path

from .core import PROJECT_NAME, PROJECT_SLUG, run_demo, write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=PROJECT_NAME)
    parser.add_argument("--message", default="demo payload", help="message or watermark payload")
    parser.add_argument("--report", default="", help="optional markdown report path")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    result = run_demo(args.message)
    print(f"[{{PROJECT_SLUG}}] recovered={{result.recovered}}")
    for key, value in result.metrics.items():
        print(f"{{key}}={{value}}")
    if args.report:
        path = write_report(Path(args.report), args.message)
        print(f"report={{path}}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
