#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": {"start": 0x0AD9, "end": 0x0BC8, "sha1": "c62fe76780ceb698b2f88fe090e29e2a697cac55"},
    "jp-revA": {"start": 0x0AD9, "end": 0x0BC8, "sha1": "c62fe76780ceb698b2f88fe090e29e2a697cac55"},
    "kr":      {"start": 0x0AE3, "end": 0x0BD2, "sha1": "87849a8e637169bdd44478b3e5b208dade3f65dd"},
    "en":      {"start": 0x0AF0, "end": 0x0BDF, "sha1": "701ae28844ac58c98a6193e6392cd0ad7f2370e5"},
    "de":      {"start": 0x0AF0, "end": 0x0BDF, "sha1": "701ae28844ac58c98a6193e6392cd0ad7f2370e5"},
    "fr":      {"start": 0x0AF0, "end": 0x0BDF, "sha1": "701ae28844ac58c98a6193e6392cd0ad7f2370e5"},
    "it":      {"start": 0x0AF0, "end": 0x0BDF, "sha1": "701ae28844ac58c98a6193e6392cd0ad7f2370e5"},
    "es":      {"start": 0x0AF0, "end": 0x0BDF, "sha1": "701ae28844ac58c98a6193e6392cd0ad7f2370e5"},
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
        assert len(data) == 239, (rid, len(data))
        assert digest == exp["sha1"], (rid, digest, exp["sha1"])
        modules[rid] = data
        print(f"PASS {rid}: 239 bytes {digest}")

    assert modules["jp-rev0"] == modules["jp-revA"]
    assert modules["en"] == modules["de"] == modules["fr"] == modules["it"] == modules["es"]
    print("PASS decompress structural checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
