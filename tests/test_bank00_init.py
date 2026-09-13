#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RANGES = {
    "jp-rev0": (0x05AF, 0x06A9),
    "jp-revA": (0x05AF, 0x06A9),
    "kr": (0x05B4, 0x0698),
    "en": (0x05B0, 0x06AA),
    "de": (0x05B0, 0x06AA),
    "fr": (0x05B0, 0x06AA),
    "it": (0x05B0, 0x06AA),
    "es": (0x05B0, 0x06AA),
}
EXPECTED_SHA1 = {
    "jp-rev0": "272298e61951fc0b178f2519ad0266c9371cb21d",
    "jp-revA": "272298e61951fc0b178f2519ad0266c9371cb21d",
    "kr": "6fd11b4f995d028d848f065e00b07a61daf8093a",
    "en": "79a7fd3476b44efbde2ba5c78854c8825fc6e018",
    "de": "f7827c3b83e09e5e0eaa2557ed0c5b4ada3e1ed0",
    "fr": "693191316f09d8de4a998454db6fcf1e104615f2",
    "it": "7e579af72eea1acc815031d81ebd927af74ccbb5",
    "es": "051860d7b52750eec7e8581fa975c4e4a5f4423d",
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
        assert hashlib.sha1(data).hexdigest() == EXPECTED_SHA1[rid], f"{rid}: init module mismatch"
        assert len(data) == (228 if rid == "kr" else 250)

    print("PASS: Bank 00 init module verified across 8 releases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
