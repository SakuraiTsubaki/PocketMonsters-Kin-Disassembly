#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TESTS = [
    "tests/test_bank00_text_ranges.py",
    "tests/test_bank00_western_text_strings.py",
    "tests/test_bank00_western_text_variants.py",
    "tests/test_bank00_jp_text.py",
    "tests/test_bank00_kr_text.py",
    "tests/test_bank00_kr_text_engine.py",
    "tests/test_bank00_text_misc.py",
]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Run the complete Bank 00 text-family regression suite."
    )
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument(
        "--manifest",
        type=Path,
        default=Path("manifests/rom_baselines.json"),
    )
    args = ap.parse_args()

    for test in TESTS:
        cmd = [
            sys.executable,
            test,
            "--rom-dir",
            str(args.rom_dir),
            "--manifest",
            str(args.manifest),
        ]
        print(f"==> {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

    print(f"PASS Bank 00 text suite: {len(TESTS)} regression programs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
