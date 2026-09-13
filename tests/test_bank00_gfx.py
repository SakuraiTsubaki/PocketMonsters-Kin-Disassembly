#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": {"start": 0x0D59, "end": 0x0E8F, "sha1": "7416ebe003d1b9d2ab74c50f35dd2d8fb8471291"},
    "jp-revA": {"start": 0x0D59, "end": 0x0E8F, "sha1": "7416ebe003d1b9d2ab74c50f35dd2d8fb8471291"},
    "kr":      {"start": 0x0D6E, "end": 0x0ECF, "sha1": "b301ae6b37605ad13fe6bb3c4c962f3d6d4d2343"},
    "en":      {"start": 0x0D70, "end": 0x0EBD, "sha1": "3881c18d6c16eb55fa5a49686d7b3a2ed1914265"},
    "de":      {"start": 0x0D70, "end": 0x0EBD, "sha1": "54da67f6e2cdfe511891bf674834d681fe3b316a"},
    "fr":      {"start": 0x0D70, "end": 0x0EBD, "sha1": "3941f47772ebbdc10f96885b077be9272cb1bf56"},
    "it":      {"start": 0x0D70, "end": 0x0EBD, "sha1": "93993f8212abf830bc1a86b6dcba7cbff3516cc7"},
    "es":      {"start": 0x0D70, "end": 0x0EBD, "sha1": "708a688a2e749f1562129a886b0a0840d419b526"},
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
    assert len(modules["jp-rev0"]) == 310
    assert len(modules["kr"]) == 353
    for rid in ("en", "de", "fr", "it", "es"):
        assert len(modules[rid]) == 333

    # Japanese lacks the 23-byte DuplicateGet2bpp routine.
    assert 333 - 310 == 23
    # Korean adds two 10-byte transfer-drain wait helpers.
    assert 353 - 333 == 20

    print("PASS gfx structural checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
