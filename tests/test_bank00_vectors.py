#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "manifests" / "rom_baselines.json"

COMMON = {
    0x0000: bytes.fromhex("F3 C3 00 01"),
    0x0010: bytes.fromhex("E0 9F EA 00 20 C9"),
    0x0028: bytes.fromhex("D5 5F 16 00 19 19 2A 66 6F D1 E9"),
    0x0040: bytes.fromhex("C3 50 01"),
    0x0048: bytes.fromhex("C3 1B 04"),
    0x0050: bytes.fromhex("D9"),
}

KOREAN_RST18 = bytes.fromhex("F0 41 E6 03 28 FA F0 41 E6 03 20 FA C9")
KOREAN_RST38 = bytes.fromhex("00 3E 39 3D 20 FD C9")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify known Bank 00 vector/header structures.")
    parser.add_argument("--rom-dir", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = 0

    for release in manifest["releases"]:
        path = args.rom_dir / release["reference_filename"]
        if not path.is_file():
            print(f"MISS {release['id']}: {path}")
            failures += 1
            continue

        bank = path.read_bytes()[:0x4000]
        errors: list[str] = []
        for offset, expected in COMMON.items():
            actual = bank[offset : offset + len(expected)]
            if actual != expected:
                errors.append(f"0x{offset:04X}: {actual.hex()} != {expected.hex()}")

        if release["id"] == "kr":
            if bank[0x0018:0x0025] != KOREAN_RST18:
                errors.append("Korean RST18 timing routine mismatch")
            if bank[0x0038:0x003F] != KOREAN_RST38:
                errors.append("Korean RST38 delay routine mismatch")
        else:
            for offset in (0x0018, 0x0020, 0x0038):
                if bank[offset] != 0xFF:
                    errors.append(f"0x{offset:04X}: expected rst $38 opcode FF")

        if bank[0x0100] != 0x00 or bank[0x0101] != 0xC3:
            errors.append("entry point is not nop ; jp")

        if errors:
            failures += 1
            print(f"FAIL {release['id']}")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"PASS {release['id']}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
