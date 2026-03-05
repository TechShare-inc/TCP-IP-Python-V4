#!/usr/bin/env python3
"""Lightweight checks for tutorial example files."""

from __future__ import annotations

from pathlib import Path
import re


PATTERN = re.compile(r"^\d{2}_[a-z0-9_]+\.py$")


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "examples"
    files = sorted(p for p in root.glob("*.py"))
    bad = [p.name for p in files if not PATTERN.match(p.name)]
    if bad:
        print("Invalid example filenames:")
        for name in bad:
            print("-", name)
        return 1
    print(f"OK: {len(files)} example files match NN_topic.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
