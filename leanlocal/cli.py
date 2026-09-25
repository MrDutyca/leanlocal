"""Command-line entry point for LeanLocal."""

from __future__ import annotations

import argparse
import json

from .core import bench, check, fit, report, support_bundle


def _print(data: dict) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="leanlocal",
        description="Privacy-conscious capability checks for low-spec Linux.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("report", help="show a redacted system capability report")
    sub.add_parser("bench", help="run short low-resource benchmarks")
    sub.add_parser("check", help="check common lightweight dependencies")
    sub.add_parser("fit", help="show conservative workload guidance")
    support = sub.add_parser("support", help="write a redacted JSON support bundle")
    support.add_argument("path", nargs="?", default="support-leanlocal.json")

    args = parser.parse_args()
    if args.command == "report":
        _print(report())
    elif args.command == "bench":
        _print(bench())
    elif args.command == "check":
        _print(check())
    elif args.command == "fit":
        _print(fit())
    elif args.command == "support":
        print(support_bundle(args.path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
