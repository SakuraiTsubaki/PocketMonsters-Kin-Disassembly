#!/usr/bin/env python3
"""Fingerprint a local Game Boy/Game Boy Color ROM without modifying it."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

BANK_SIZE = 0x4000
ROM_SIZE_CODES = {
    0x00: 32 * 1024,
    0x01: 64 * 1024,
    0x02: 128 * 1024,
    0x03: 256 * 1024,
    0x04: 512 * 1024,
    0x05: 1024 * 1024,
    0x06: 2 * 1024 * 1024,
    0x07: 4 * 1024 * 1024,
    0x08: 8 * 1024 * 1024,
    0x52: 1152 * 1024,
    0x53: 1280 * 1024,
    0x54: 1536 * 1024,
}
RAM_SIZE_CODES = {
    0x00: 0,
    0x01: 2 * 1024,
    0x02: 8 * 1024,
    0x03: 32 * 1024,
    0x04: 128 * 1024,
    0x05: 64 * 1024,
}


def digest(name: str, data: bytes) -> str:
    return hashlib.new(name, data).hexdigest()


def build_report(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 0x150:
        raise SystemExit("file is too small to contain a Game Boy cartridge header")

    cgb_flag = data[0x143]
    title_end = 0x143 if cgb_flag in (0x80, 0xC0) else 0x144
    title_raw = data[0x134:title_end].rstrip(b"\x00")
    title = title_raw.decode("ascii", errors="replace")
    rom_size_code = data[0x148]
    ram_size_code = data[0x149]

    banks = []
    for index, start in enumerate(range(0, len(data), BANK_SIZE)):
        chunk = data[start : start + BANK_SIZE]
        banks.append(
            {
                "bank": index,
                "start": start,
                "size": len(chunk),
                "sha1": digest("sha1", chunk),
            }
        )

    return {
        "file": path.name,
        "size": len(data),
        "md5": digest("md5", data),
        "sha1": digest("sha1", data),
        "sha256": digest("sha256", data),
        "header": {
            "title": title,
            "cgb_flag": cgb_flag,
            "new_licensee": data[0x144:0x146].decode("ascii", errors="replace"),
            "sgb_flag": data[0x146],
            "cartridge_type": data[0x147],
            "rom_size_code": rom_size_code,
            "declared_rom_size": ROM_SIZE_CODES.get(rom_size_code),
            "ram_size_code": ram_size_code,
            "declared_ram_size": RAM_SIZE_CODES.get(ram_size_code),
            "destination_code": data[0x14A],
            "old_licensee": data[0x14B],
            "mask_rom_version": data[0x14C],
            "header_checksum": data[0x14D],
            "global_checksum": int.from_bytes(data[0x14E:0x150], "big"),
        },
        "bank_size": BANK_SIZE,
        "bank_count": len(banks),
        "banks": banks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    report = build_report(args.rom)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
