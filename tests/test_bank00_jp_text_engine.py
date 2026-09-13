#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

SIGNATURES = Path("analysis/bank00/jp_text_engine_signatures.csv")
RELEASES = ("jp-rev0", "jp-revA")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument(
        "--manifest",
        type=Path,
        default=Path("manifests/rom_baselines.json"),
    )
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    rows = list(csv.DictReader(SIGNATURES.read_text(encoding="utf-8").splitlines()))

    modules = []
    for rid in RELEASES:
        release = by_id[rid]
        path = args.rom_dir / release["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        rom = path.read_bytes()
        modules.append(rom[0x0E8F:0x142D])

        for row in rows:
            start = int(row["start"], 16)
            end = int(row["end_exclusive"], 16)
            expected = bytes.fromhex(row["hex_signature"])
            actual = rom[start:end]
            assert len(actual) == int(row["size"]), (rid, row["symbol"])
            assert actual == expected, (
                rid,
                row["symbol"],
                f"{start:#06x}-{end - 1:#06x}",
                actual.hex(" ").upper(),
                expected.hex(" ").upper(),
            )

        print(f"PASS {rid}: {len(rows)} Japanese Bank 00 text-engine signatures")

    assert modules[0] == modules[1]
    print("PASS Japanese Rev 0/Rev A text modules are byte-identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
