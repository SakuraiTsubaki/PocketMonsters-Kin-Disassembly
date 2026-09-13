#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

RANGES = {
    "jp-rev0": (0x19FB, 0x1E60),
    "jp-revA": (0x19FB, 0x1E60),
    "kr":      (0x1AA1, 0x1F10),
    "en":      (0x1A4E, 0x1EB3),
    "de":      (0x1A72, 0x1EE0),
    "fr":      (0x1A57, 0x1EC5),
    "it":      (0x1A6C, 0x1ED8),
    "es":      (0x1A6B, 0x1ED7),
}

YES_NO = {
    "jp-rev0": (0x1C3E, "CA B2 50 B2 B2 B4 50"),   # はい / いいえ
    "jp-revA": (0x1C3E, "CA B2 50 B2 B2 B4 50"),
    "kr":      (0x1D0A, "07 19 50 06 C6 02 CF 07 20 50"), # 예 / 아니오
    "en":      (0x1C91, "98 84 92 50 8D 8E 50"),   # YES / NO
    "de":      (0x1CBD, "89 80 50 8D 84 88 8D 50"),# JA / NEIN
    "fr":      (0x1CA2, "8E 94 88 50 8D 8E 8D 50"),# OUI / NON
    "it":      (0x1CB7, "92 C8 50 8D 8E 50"),      # SÌ / NO
    "es":      (0x1CB6, "92 C9 50 8D 8E 50"),      # SÍ / NO
}

# Localized western Gold inserts an 8-byte position guard at menu+0x205.
# Immediate value differs by locale and exactly matches the retail ROM.
WESTERN_GUARD_IMMEDIATE = {"de": 0x0D, "fr": 0x0E, "it": 0x0F, "es": 0x0F}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    roms: dict[str, bytes] = {}

    for rid in RANGES:
        path = args.rom_dir / by_id[rid]["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        roms[rid] = path.read_bytes()

    for rid, (address, raw_hex) in YES_NO.items():
        expected = bytes.fromhex(raw_hex)
        actual = roms[rid][address:address + len(expected)]
        assert actual == expected, (rid, hex(address), actual.hex(" "), expected.hex(" "))
        print(f"PASS {rid}: Yes/No data at {address:#06x}")

    assert roms["jp-rev0"][0x1C3E:0x1C45] == roms["jp-revA"][0x1C3E:0x1C45]

    for rid, immediate in WESTERN_GUARD_IMMEDIATE.items():
        start, _ = RANGES[rid]
        address = start + 0x205
        expected = bytes((0x78, 0xFE, 0x0E, 0x20, 0x03, 0x3E, immediate, 0x47))
        actual = roms[rid][address:address + len(expected)]
        assert actual == expected, (rid, hex(address), actual.hex(" "), expected.hex(" "))
        print(f"PASS {rid}: localized Yes/No position guard at {address:#06x}")

    # EN/JP/KR do not contain the localized-western guard at that relative point.
    for rid in ("en", "jp-rev0", "jp-revA", "kr"):
        start, _ = RANGES[rid]
        address = start + 0x205
        assert roms[rid][address:address + 3] != bytes.fromhex("78 FE 0E"), rid

    print("PASS Bank 00 localized Yes/No menu checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
