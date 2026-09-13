#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RANGES = {
    "jp-rev0": (0x045B, 0x05AF),
    "jp-revA": (0x045B, 0x05AF),
    "kr": (0x045F, 0x05B4),
    "en": (0x045B, 0x05B0),
    "de": (0x045B, 0x05B0),
    "fr": (0x045B, 0x05B0),
    "it": (0x045B, 0x05B0),
    "es": (0x045B, 0x05B0),
}
EXPECTED_SHA1 = {
    "jp-rev0": "304ea3396159e0a18cedc57ccc418fa6c3669089",
    "jp-revA": "304ea3396159e0a18cedc57ccc418fa6c3669089",
    "kr": "2b40fc7f9396e184498373f85c2785c300f22671",
    "en": "2bbc94e1fc9af37262fbcadb4f7294336ae71f6d",
    "de": "7090ed6ccf4022ba04120dd1f337be94fde8c604",
    "fr": "3c9cb4a1627587c7dcc2ce43e901a79577cbe58e",
    "it": "4f399ec7dbf69ae847ce670fa5b5aadeff7a157b",
    "es": "70268d08c890002d93d843ccf2f52057ac9ae010",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = parser.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    for release in releases:
        rid = release["id"]
        path = args.rom_dir / release["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        bank = path.read_bytes()[:0x4000]
        start, end = RANGES[rid]
        data = bank[start:end]
        assert hashlib.sha1(data).hexdigest() == EXPECTED_SHA1[rid], f"{rid}: time module mismatch"
        if rid.startswith("jp-"):
            assert len(data) == 340
        else:
            assert len(data) == 341

    print("PASS: Bank 00 RTC/time module verified across 8 releases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
