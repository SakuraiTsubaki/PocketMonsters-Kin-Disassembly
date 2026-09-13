#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

START = 0x041B
END = {
    "jp-rev0": 0x045B,
    "jp-revA": 0x045B,
    "kr": 0x045F,
    "en": 0x045B,
    "de": 0x045B,
    "fr": 0x045B,
    "it": 0x045B,
    "es": 0x045B,
}
EXPECTED_SHA1 = {
    "jp-rev0": "159bfbb1b39df60400032968e65d97b3ef267528",
    "jp-revA": "159bfbb1b39df60400032968e65d97b3ef267528",
    "kr": "d8950b6f6ffefd26d446ebbfc81d98e6681ac8ab",
    "en": "159bfbb1b39df60400032968e65d97b3ef267528",
    "de": "159bfbb1b39df60400032968e65d97b3ef267528",
    "fr": "159bfbb1b39df60400032968e65d97b3ef267528",
    "it": "159bfbb1b39df60400032968e65d97b3ef267528",
    "es": "159bfbb1b39df60400032968e65d97b3ef267528",
}
KR_GUARD = bytes.fromhex("f0 44 fe 90 30 0d")


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
        data = bank[START:END[rid]]
        actual = hashlib.sha1(data).hexdigest()
        assert actual == EXPECTED_SHA1[rid], f"{rid}: LCD SHA-1 mismatch"
        if rid == "kr":
            assert KR_GUARD in data[:16], "Korean LCD LY/VBlank guard missing"
            assert len(data) == 68
        else:
            assert KR_GUARD not in data[:16], f"{rid}: unexpected Korean LCD guard"
            assert len(data) == 64

    print("PASS: Bank 00 LCD module verified across 8 releases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
