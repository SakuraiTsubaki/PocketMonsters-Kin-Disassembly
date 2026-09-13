#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RANGES = {
    "jp-rev0": (0x06A9, 0x08DE), "jp-revA": (0x06A9, 0x08DE),
    "kr": (0x0698, 0x08D2), "en": (0x06AA, 0x08DF),
    "de": (0x06AA, 0x08DF), "fr": (0x06AA, 0x08DF),
    "it": (0x06AA, 0x08DF), "es": (0x06AA, 0x08DF),
}
EXPECTED_SHA1 = {
    "jp-rev0": "0f9e1b7de3032de9cb59cb090fdfc845e1923d19",
    "jp-revA": "0f9e1b7de3032de9cb59cb090fdfc845e1923d19",
    "kr": "d29a1bf900f55ee2d3eb8a3f0009baaac4fa18d3",
    "en": "ebc72de0cc7961d3bb5635fe8bd74e3a42b99d21",
    "de": "4febc5100f3ee602a1f1790d218387039fdf1c9e",
    "fr": "f329a87b8233e59b5bdb0629a209657c15bd4ed6",
    "it": "dbd4106b913253c312e1ed85f542b2404a5902e3",
    "es": "b730e239c19a1f72fc0e28eac6a92982bb93a8f1",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()
    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    for rel in releases:
        rid = rel["id"]
        path = args.rom_dir / rel["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        bank = path.read_bytes()[:0x4000]
        start, end = RANGES[rid]
        data = bank[start:end]
        assert hashlib.sha1(data).hexdigest() == EXPECTED_SHA1[rid], f"{rid}: serial module mismatch"
        assert len(data) == (570 if rid == "kr" else 565)
    print("PASS: Bank 00 serial module verified across 8 releases")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
