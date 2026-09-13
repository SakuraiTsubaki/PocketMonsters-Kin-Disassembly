#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

SIGNATURES = Path("analysis/bank00/kr_menu_signatures.csv")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    release = next(r for r in releases if r["id"] == "kr")
    path = args.rom_dir / release["reference_filename"]
    if not path.is_file():
        raise SystemExit(f"missing reference ROM: {path}")
    rom = path.read_bytes()

    rows = list(csv.DictReader(SIGNATURES.read_text(encoding="utf-8").splitlines()))
    for row in rows:
        start = int(row["start"], 16)
        end = int(row["end_exclusive"], 16)
        expected = bytes.fromhex(row["hex_signature"])
        actual = rom[start:end]
        assert len(actual) == int(row["size"]), row["symbol"]
        assert actual == expected, (row["symbol"], actual.hex(" "), expected.hex(" "))
        print(f"PASS {row['symbol']}: {start:#06x}-{end - 1:#06x}")

    print(f"PASS kr: {len(rows)} Korean Bank 00 menu signatures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
