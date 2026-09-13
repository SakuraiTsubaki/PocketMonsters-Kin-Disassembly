#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

MODULES = {
    "time_palettes": {
        "range": (0x0343, 0x0360),
        "sha1": {
            "jp-rev0": "d6bae28461a8e499075577d1ff5613b5cf7bb22d",
            "jp-revA": "d6bae28461a8e499075577d1ff5613b5cf7bb22d",
            "kr": "5ccb606af2086ba08aa943bfec3267d78078dd11",
            "en": "b2ab6bcfce49d28d3c0836f2305ed9aeeca4193e",
            "de": "fccdbcfbfb9bbef4f523a5bedf63714a8ad30cf1",
            "fr": "fccdbcfbfb9bbef4f523a5bedf63714a8ad30cf1",
            "it": "db9643d8f529148f400c29190117fa98c57b7da7",
            "es": "db9643d8f529148f400c29190117fa98c57b7da7",
        },
    },
    "fade": {
        "range": (0x0360, 0x041B),
        "sha1": {
            "jp-rev0": "6f4270a8908dac37f15d791f0a12304894e1b9bf",
            "jp-revA": "6f4270a8908dac37f15d791f0a12304894e1b9bf",
            "kr": "2d06557d4c1b2e741e03ce0331958346746a952c",
            "en": "148b91c5162f14a5fc67882de1db18ad77b7b44b",
            "de": "148b91c5162f14a5fc67882de1db18ad77b7b44b",
            "fr": "148b91c5162f14a5fc67882de1db18ad77b7b44b",
            "it": "148b91c5162f14a5fc67882de1db18ad77b7b44b",
            "es": "148b91c5162f14a5fc67882de1db18ad77b7b44b",
        },
    },
}


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


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
    files = {r["id"]: args.rom_dir / r["reference_filename"] for r in releases}

    for rid, path in files.items():
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        bank = path.read_bytes()[:0x4000]
        for name, spec in MODULES.items():
            start, end = spec["range"]
            actual = sha1(bank[start:end])
            expected = spec["sha1"][rid]
            assert actual == expected, f"{rid}: {name} SHA-1 mismatch: {actual} != {expected}"

    assert files.keys() >= MODULES["fade"]["sha1"].keys()
    print("PASS: Bank 00 time_palettes and fade module bytes verified across 8 releases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
