#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_SHA1 = "ad10101d2a65bf96d9518c3a99c0ba35e7278ec4"
EXPECTED_BYTES = bytes.fromhex("C6 10 5F F0 9F F5 3E 02 D7 CD C9 4A F1 D7 C9")
RANGES = {
    "jp-rev0": (0x1959, 0x1968),
    "jp-revA": (0x1959, 0x1968),
    "kr":      (0x19FF, 0x1A0E),
    "en":      (0x19AC, 0x19BB),
    "de":      (0x19D0, 0x19DF),
    "fr":      (0x19B5, 0x19C4),
    "it":      (0x19CA, 0x19D9),
    "es":      (0x19C9, 0x19D8),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}

    for rid, (start, end) in RANGES.items():
        path = args.rom_dir / by_id[rid]["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        module = path.read_bytes()[start:end]
        assert module == EXPECTED_BYTES, rid
        assert hashlib.sha1(module).hexdigest() == EXPECTED_SHA1, rid
        print(f"PASS {rid}: sine {start:#06x}-{end - 1:#06x}")

    print("PASS Bank 00 sine is byte-identical across all 8 releases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
