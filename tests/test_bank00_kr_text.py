#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

MODULE_START = 0x0ECF
MODULE_END = 0x153F
MODULE_SHA1 = "2ec906ea9a7412ee1d0b2e352d1b459c325b87b4"

STRINGS = {
    "TMCharText":      (0x113B, "01 B2 06 2A 04 73 06 65 50"),  # 기술머신@
    "TrainerCharText": (0x1144, "09 DE 03 E9 07 9C 02 6A 50"),  # 트레이너@
    "PCCharText":      (0x114D, "09 24 0A 4B 09 9D 50"),        # 컴퓨터@
    "RocketCharText":  (0x1154, "03 FE 09 2F 02 DC 50"),        # 로켓단@
    "PlacePOKeText":   (0x115B, "0A 27 09 2F 04 93 50"),        # 포켓몬@
    "KougekiText":     (0x1162, "BA B3 27 B7 50"),              # こうげき@ (JP leftover)
    "SixDotsCharText": (0x1167, "75 75 50"),                    # ……@
    "EnemyText":       (0x116A, "07 CB 07 97 7F 50"),           # 적의 @
    "PlacePKMNText":   (0x1170, "E1 E2 50"),
    "PlacePOKEText":   (0x1173, "70 71 50"),
    "String_Space":    (0x1176, "7F 50"),
    "DummiedText":     (0x1178, "50"),
}

WEEKDAYS = {
    "Sunday":    (0x1456, "07 9F 50"),        # 일@
    "Monday":    (0x1459, "07 69 50"),        # 월@
    "Tuesday":   (0x145C, "0A AD 50"),        # 화@
    "Wednesday": (0x145F, "06 26 50"),        # 수@
    "Thursday":  (0x1462, "04 91 50"),        # 목@
    "Friday":    (0x1465, "01 AD 50"),        # 금@
    "Saturday":  (0x1468, "09 B4 50"),        # 토@
    "Suffix":    (0x146B, "07 44 07 9F 50"),  # 요일@
}


def expected_bytes(hex_text: str) -> bytes:
    return bytes.fromhex(hex_text)


def verify_table(rom: bytes, table: dict[str, tuple[int, str]]) -> None:
    for label, (address, hex_text) in table.items():
        expected = expected_bytes(hex_text)
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
    ap.add_argument(
        "--manifest",
        type=Path,
        default=Path("manifests/rom_baselines.json"),
    )
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    release = next(r for r in releases if r["id"] == "kr")
    path = args.rom_dir / release["reference_filename"]
    if not path.is_file():
        raise SystemExit(f"missing reference ROM: {path}")

    rom = path.read_bytes()
    module = rom[MODULE_START:MODULE_END]
    assert len(module) == 1648
    assert hashlib.sha1(module).hexdigest() == MODULE_SHA1

    verify_table(rom, STRINGS)
    verify_table(rom, WEEKDAYS)

    print("PASS kr: Korean Bank 00 text module + embedded strings + weekdays")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
