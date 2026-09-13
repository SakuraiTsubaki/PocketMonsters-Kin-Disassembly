#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

GAME_FREAK = {
    "jp-rev0": (0x0F21, "00 08 E3 9F 9B D8 E3 87 E7 57"),
    "jp-revA": (0x0F21, "00 08 E3 9F 9B D8 E3 87 E7 57"),
    "kr":      (0x0F4A, "00 0F E3 9F 9B D8 E3 87 E7 5E"),
    "en":      (0x0F4F, "00 08 E3 9F 9B D8 E3 87 E7 57"),
    "de":      (0x0F4F, "00 08 E3 9F 9B D8 E3 87 E7 57"),
    "fr":      (0x0F4F, "00 08 E3 9F 9B D8 E3 87 E7 57"),
    "it":      (0x0F4F, "00 08 E3 9F 9B D8 E3 87 E7 57"),
    "es":      (0x0F4F, "00 08 E3 9F 9B D8 E3 87 E7 57"),
}

PLACE_FAR_STRING = {
    "kr": (0x1287, "47 F0 9F F5 78 D7 CD 6F 0F F1 D7 C9"),
    "en": (0x1261, "47 F0 9F F5 78 D7 CD 74 0F F1 D7 C9"),
    "de": (0x1270, "47 F0 9F F5 78 D7 CD 74 0F F1 D7 C9"),
    "fr": (0x125D, "47 F0 9F F5 78 D7 CD 74 0F F1 D7 C9"),
    "it": (0x126D, "47 F0 9F F5 78 D7 CD 74 0F F1 D7 C9"),
    "es": (0x1270, "47 F0 9F F5 78 D7 CD 74 0F F1 D7 C9"),
}


def check(rom: bytes, address: int, hex_text: str, label: str) -> None:
    expected = bytes.fromhex(hex_text)
    actual = rom[address:address + len(expected)]
    assert actual == expected, (
        label,
        f"{address:#06x}",
        actual.hex(" ").upper(),
        expected.hex(" ").upper(),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    roms: dict[str, bytes] = {}
    for rid in GAME_FREAK:
        path = args.rom_dir / by_id[rid]["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        roms[rid] = path.read_bytes()
        check(roms[rid], *GAME_FREAK[rid], f"{rid}:GameFreakText")
        print(f"PASS {rid}: GameFreakText")

    # PlaceFarString is present in Korean and all five western releases.
    for rid, spec in PLACE_FAR_STRING.items():
        check(roms[rid], *spec, f"{rid}:PlaceFarString")
        print(f"PASS {rid}: PlaceFarString")

    # The Japanese text module has no matching PlaceFarString routine.
    prefix = bytes.fromhex("47 F0 9F F5 78 D7 CD")
    for rid in ("jp-rev0", "jp-revA"):
        start, end = 0x0E8F, 0x142D
        assert roms[rid].find(prefix, start, end) == -1, rid
        print(f"PASS {rid}: PlaceFarString absent")

    print("PASS Bank 00 text misc checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
