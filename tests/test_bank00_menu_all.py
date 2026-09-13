#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TESTS = [
    "tests/test_bank00_menu_ranges.py",
    "tests/test_bank00_menu_locales.py",
    "tests/test_bank00_kr_menu.py",
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Run Bank 00 menu-family regressions.")
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    for test in TESTS:
        subprocess.run([
            sys.executable, test,
            "--rom-dir", str(args.rom_dir),
            "--manifest", str(args.manifest),
        ], check=True)
    print(f"PASS Bank 00 menu suite: {len(TESTS)} regression programs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
