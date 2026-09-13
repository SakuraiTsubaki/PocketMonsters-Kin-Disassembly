#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": {"start": 0x0E8F, "end": 0x142D, "sha1": "a2dc9d244a4562cc63c9b2ba4b3f677bf6ef7e26"},
    "jp-revA": {"start": 0x0E8F, "end": 0x142D, "sha1": "a2dc9d244a4562cc63c9b2ba4b3f677bf6ef7e26"},
    "kr":      {"start": 0x0ECF, "end": 0x153F, "sha1": "2ec906ea9a7412ee1d0b2e352d1b459c325b87b4"},
    "en":      {"start": 0x0EBD, "end": 0x1458, "sha1": "1998e8bb8083f841c9a30f1f26afab5215e99c3b"},
    "de":      {"start": 0x0EBD, "end": 0x147C, "sha1": "bed1834b227ae260892ea5fe91aca6a0215d75c0"},
    "fr":      {"start": 0x0EBD, "end": 0x1461, "sha1": "0f047ac3f8c6f9556f318eb864e19f8bebd34b7c"},
    "it":      {"start": 0x0EBD, "end": 0x1476, "sha1": "cb51c3ae89dcd41f275758fdf915721d83df4104"},
    "es":      {"start": 0x0EBD, "end": 0x1475, "sha1": "fa803e93e8c1aa66b056177046d7d8ded2442edd"},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    modules = {}

    for rid, exp in EXPECTED.items():
        rom = args.rom_dir / by_id[rid]["reference_filename"]
        if not rom.is_file():
            raise SystemExit(f"missing reference ROM: {rom}")
        data = rom.read_bytes()[exp["start"]:exp["end"]]
        digest = hashlib.sha1(data).hexdigest()
        assert digest == exp["sha1"], (rid, digest, exp["sha1"])
        modules[rid] = data
        print(f"PASS {rid}: {len(data)} bytes {digest}")

    assert modules["jp-rev0"] == modules["jp-revA"]
    expected_sizes = {
        "jp-rev0": 1438, "jp-revA": 1438, "kr": 1648, "en": 1435,
        "de": 1471, "fr": 1444, "it": 1465, "es": 1464,
    }
    for rid, size in expected_sizes.items():
        assert len(modules[rid]) == size, (rid, len(modules[rid]), size)

    print("PASS text range/hash checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
