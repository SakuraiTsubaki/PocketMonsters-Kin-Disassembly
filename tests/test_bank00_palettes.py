#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": {"start": 0x0BC8, "end": 0x0D59, "sha1": "2fa035f9ec8f3c9b0a34e24f9f2cb68e06ce5020"},
    "jp-revA": {"start": 0x0BC8, "end": 0x0D59, "sha1": "2fa035f9ec8f3c9b0a34e24f9f2cb68e06ce5020"},
    "kr":      {"start": 0x0BD2, "end": 0x0D6E, "sha1": "ef0fa92090f79f35b46d21380d68cc1f750a1e3a"},
    "en":      {"start": 0x0BDF, "end": 0x0D70, "sha1": "acad8b569237e839087216ed8608074557a3f982"},
    "de":      {"start": 0x0BDF, "end": 0x0D70, "sha1": "9359a67c430b7ce60f885daed6897f192c5a4475"},
    "fr":      {"start": 0x0BDF, "end": 0x0D70, "sha1": "99c93609baa8fc3b8da51065f1b79358e35a031a"},
    "it":      {"start": 0x0BDF, "end": 0x0D70, "sha1": "9fc11729e2d95016f0a2d6fb790d995132ef5896"},
    "es":      {"start": 0x0BDF, "end": 0x0D70, "sha1": "c791c48b630a54f44a14668b7c1bbcafd940e7a4"},
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
    assert len(modules["kr"]) == 412
    for rid in ("jp-rev0", "jp-revA", "en", "de", "fr", "it", "es"):
        assert len(modules[rid]) == 401
    assert len(modules["kr"]) - len(modules["en"]) == 11

    print("PASS palettes structural checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
