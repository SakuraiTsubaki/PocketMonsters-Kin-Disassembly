#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

VBLANK_START = 0x0150
VBLANK_END = 0x032E
HANDLERS_START = 0x0170
HANDLERS_END = 0x0180
CUTSCENE_START = 0x01F4
CUTSCENE_END = 0x023E

EXPECTED_HANDLERS = bytes.fromhex(
    "80 01 f4 01 b0 02 c4 02 55 02 78 02 80 01 80 01"
)
LCD_POINTER_SEQUENCE = bytes.fromhex(
    "f0 c8 b7 28 05 4f fa 00 c7 e2"
)


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
    banks = {}
    for release in releases:
        path = args.rom_dir / release["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        banks[release["id"]] = path.read_bytes()[:0x4000]

    required = {"jp-rev0", "jp-revA", "kr", "en", "de", "fr", "it", "es"}
    missing = required.difference(banks)
    if missing:
        raise SystemExit(f"missing release ids in manifest: {sorted(missing)}")

    for rid, bank in banks.items():
        module = bank[VBLANK_START:VBLANK_END]
        assert len(module) == 478, (rid, len(module))
        assert bank[HANDLERS_START:HANDLERS_END] == EXPECTED_HANDLERS, rid

    assert (
        banks["jp-rev0"][VBLANK_START:VBLANK_END]
        == banks["jp-revA"][VBLANK_START:VBLANK_END]
    ), "Japanese Rev 0 and Rev A VBlank modules differ"

    for rid in ("kr", "en", "de", "fr", "it", "es"):
        cutscene = banks[rid][CUTSCENE_START:CUTSCENE_END]
        assert LCD_POINTER_SEQUENCE in cutscene, (
            rid,
            "expected LCD-pointer cutscene sequence not found",
        )

    for rid in ("jp-rev0", "jp-revA"):
        cutscene = banks[rid][CUTSCENE_START:CUTSCENE_END]
        assert LCD_POINTER_SEQUENCE not in cutscene, (
            rid,
            "Japanese cutscene unexpectedly contains western/Korean LCD-pointer path",
        )

    print("PASS: Bank 00 VBlank structure verified across 8 Gold releases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
