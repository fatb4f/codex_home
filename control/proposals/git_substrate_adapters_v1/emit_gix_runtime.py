#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from git_projection_common import GitProjectionError, resolve_maturin


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="emit-gix-runtime",
        description="Check availability for a real gix runtime surface.",
    )
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        maturin_bin, maturin_resolution = resolve_maturin()
        runtime_source = os.environ.get("GIX_RUNTIME_SOURCE", "")
        source_exists = bool(runtime_source) and Path(runtime_source).expanduser().exists()
        status = "ok" if maturin_bin and source_exists else "runtime_unavailable"
        payload = {
            "status": status,
            "runtime_kind": "gix",
            "maturin_bin": maturin_bin,
            "maturin_resolution": maturin_resolution,
            "runtime_source": runtime_source or None,
            "runtime_source_exists": source_exists,
            "missing": [
                name
                for name, ok in (
                    ("maturin", maturin_bin is not None),
                    ("gix_runtime_source", source_exists),
                )
                if not ok
            ],
        }
        if args.check_only:
            print(json.dumps(payload, indent=2))
            return 0 if status == "ok" else 2
        if status != "ok":
            raise GitProjectionError("gix runtime unavailable")
        print(json.dumps(payload, indent=2))
        return 0
    except GitProjectionError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
