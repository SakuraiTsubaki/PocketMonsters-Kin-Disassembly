#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

START = 0x032E
END = 0x0343

W_VBLANK_OCCURRED = {
    "jp-rev0": 0xCF1E,
    "jp-revA": 0xCF1E,
    "kr": 0xCEBF,
    "en": 0xCEEA,
    "de": 0xCEEA,
    "fr": 0xCEEA,
    "it": 0xCEEA,
    "es": 0xCEEA,
}


def expected(addr: int) -> bytes:
    lo = addr & 0xFF
    hi = addr >> 8
    return bytes([
        0x3E, 0x01,
        0xEA, lo, hi,
        0x76, 0x00,
        0xFA, lo, hi,
        0xA7,
        0x20, 0xF8,
        0xC9,
        0xCD, 0x2E, 0x03,
        0x0D,
        0x20, 0xFA,
        0xC9,
    ])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom-dir", type=Path, required=True)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("manifests/rom_baselines.json"),
    )
    args = parser.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    seen = set()

    for release in releases:
        rid = release["id"]
        if rid not in W_VBLANK_OCCURRED:
            continue
        path = args.rom_dir / release["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        bank = path.read_bytes()[:0x4000]
        actual = bank[START:END]
        assert actual == expected(W_VBLANK_OCCURRED[rid]), f"{rid}: Delay module mismatch"
        seen.add(rid)

    missing = set(W_VBLANK_OCCURRED).difference(seen)
    assert not missing, f"missing releases: {sorted(missing)}"

    print("PASS: Bank 00 DelayFrame/DelayFrames bytes accounted for across 8 releases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
