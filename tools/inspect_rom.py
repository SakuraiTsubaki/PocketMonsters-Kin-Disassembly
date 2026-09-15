#!/usr/bin/env python3
"""Inspect a local Game Boy / Game Boy Color ROM without modifying it.

This tool is intentionally read-only. It records whole-ROM hashes, cartridge
header metadata, checksum results, and per-16 KiB ROM-bank hashes so later
reverse-engineering work can cite a reproducible target identity.

ROM binaries and bank dumps are never written by this tool.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zlib
from pathlib import Path
from typing import Any

BANK_SIZE = 0x4000
HEADER_START = 0x0100
HEADER_END = 0x014F

ROM_SIZE_BANKS = {
    0x00: 2,
    0x01: 4,
    0x02: 8,
    0x03: 16,
    0x04: 32,
    0x05: 64,
    0x06: 128,
    0x07: 256,
    0x08: 512,
    0x52: 72,
    0x53: 80,
    0x54: 96,
}

RAM_SIZE_BYTES = {
    0x00: 0,
    0x01: 2 * 1024,
    0x02: 8 * 1024,
    0x03: 32 * 1024,
    0x04: 128 * 1024,
    0x05: 64 * 1024,
}

CARTRIDGE_TYPES = {
    0x00: "ROM ONLY",
    0x01: "MBC1",
    0x02: "MBC1+RAM",
    0x03: "MBC1+RAM+BATTERY",
    0x05: "MBC2",
    0x06: "MBC2+BATTERY",
    0x08: "ROM+RAM",
    0x09: "ROM+RAM+BATTERY",
    0x0F: "MBC3+TIMER+BATTERY",
    0x10: "MBC3+TIMER+RAM+BATTERY",
    0x11: "MBC3",
    0x12: "MBC3+RAM",
    0x13: "MBC3+RAM+BATTERY",
    0x19: "MBC5",
    0x1A: "MBC5+RAM",
    0x1B: "MBC5+RAM+BATTERY",
    0x1C: "MBC5+RUMBLE",
    0x1D: "MBC5+RUMBLE+RAM",
    0x1E: "MBC5+RUMBLE+RAM+BATTERY",
}


def digest(data: bytes, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def crc32(data: bytes) -> str:
    return f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"


def decode_ascii(raw: bytes) -> str:
    return "".join(chr(b) if 0x20 <= b <= 0x7E else "." for b in raw)


def header_checksum(rom: bytes) -> int:
    value = 0
    for byte in rom[0x0134:0x014D]:
        value = (value - byte - 1) & 0xFF
    return value


def global_checksum(rom: bytes) -> int:
    return (sum(rom[:0x014E]) + sum(rom[0x0150:])) & 0xFFFF


def read_targets(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.is_file():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    targets = payload.get("targets", [])
    if not isinstance(targets, list):
        raise ValueError(f"targets is not a list in {path}")
    return targets


def identify_target(report: dict[str, Any], targets: list[dict[str, Any]]) -> dict[str, Any] | None:
    sha1 = report["hashes"]["sha1"]
    md5 = report["hashes"]["md5"]
    for target in targets:
        if target.get("sha1", "").lower() == sha1 or target.get("md5", "").lower() == md5:
            return {
                "id": target.get("id"),
                "region": target.get("region"),
                "language": target.get("language"),
                "revision": target.get("revision"),
                "matched_by": "sha1" if target.get("sha1", "").lower() == sha1 else "md5",
            }
    return None


def inspect_rom(path: Path, targets_path: Path | None) -> dict[str, Any]:
    rom = path.read_bytes()
    if len(rom) < 0x0150:
        raise ValueError(f"ROM is too small to contain a complete cartridge header: {len(rom)} bytes")

    cgb_flag = rom[0x0143]
    if cgb_flag == 0x80:
        cgb_mode = "CGB enhanced / DMG compatible"
    elif cgb_flag == 0xC0:
        cgb_mode = "CGB only"
    else:
        cgb_mode = "DMG / non-CGB flag"

    rom_size_code = rom[0x0148]
    declared_banks = ROM_SIZE_BANKS.get(rom_size_code)
    actual_banks = (len(rom) + BANK_SIZE - 1) // BANK_SIZE

    stored_header_checksum = rom[0x014D]
    calculated_header_checksum = header_checksum(rom)
    stored_global_checksum = int.from_bytes(rom[0x014E:0x0150], "big")
    calculated_global_checksum = global_checksum(rom)

    report: dict[str, Any] = {
        "file": {
            "name": path.name,
            "size_bytes": len(rom),
        },
        "hashes": {
            "sha1": digest(rom, "sha1"),
            "sha256": digest(rom, "sha256"),
            "md5": digest(rom, "md5"),
            "crc32": crc32(rom),
        },
        "header": {
            "entry_point_hex": rom[0x0100:0x0104].hex(),
            "title_raw_hex": rom[0x0134:0x0144].hex(),
            "title_ascii_view": decode_ascii(rom[0x0134:0x0144]),
            "cgb_flag": f"0x{cgb_flag:02x}",
            "cgb_mode": cgb_mode,
            "new_licensee_raw_hex": rom[0x0144:0x0146].hex(),
            "sgb_flag": f"0x{rom[0x0146]:02x}",
            "cartridge_type_code": f"0x{rom[0x0147]:02x}",
            "cartridge_type": CARTRIDGE_TYPES.get(rom[0x0147], "unknown / not mapped by inspector"),
            "rom_size_code": f"0x{rom_size_code:02x}",
            "declared_rom_banks": declared_banks,
            "declared_rom_size_bytes": declared_banks * BANK_SIZE if declared_banks is not None else None,
            "ram_size_code": f"0x{rom[0x0149]:02x}",
            "declared_ram_size_bytes": RAM_SIZE_BYTES.get(rom[0x0149]),
            "destination_code": f"0x{rom[0x014A]:02x}",
            "old_licensee_code": f"0x{rom[0x014B]:02x}",
            "mask_rom_version": rom[0x014C],
            "header_checksum_stored": f"0x{stored_header_checksum:02x}",
            "header_checksum_calculated": f"0x{calculated_header_checksum:02x}",
            "header_checksum_valid": stored_header_checksum == calculated_header_checksum,
            "global_checksum_stored": f"0x{stored_global_checksum:04x}",
            "global_checksum_calculated": f"0x{calculated_global_checksum:04x}",
            "global_checksum_valid": stored_global_checksum == calculated_global_checksum,
        },
        "banking": {
            "bank_size_bytes": BANK_SIZE,
            "actual_bank_count": actual_banks,
            "declared_bank_count_matches_file": declared_banks == actual_banks if declared_banks is not None else None,
            "banks": [],
        },
    }

    for bank in range(actual_banks):
        start = bank * BANK_SIZE
        chunk = rom[start:start + BANK_SIZE]
        report["banking"]["banks"].append(
            {
                "bank": bank,
                "bank_hex": f"0x{bank:02x}",
                "file_offset_start": f"0x{start:06x}",
                "file_offset_end_exclusive": f"0x{start + len(chunk):06x}",
                "size_bytes": len(chunk),
                "sha1": digest(chunk, "sha1"),
                "crc32": crc32(chunk),
            }
        )

    targets = read_targets(targets_path)
    report["target_match"] = identify_target(report, targets)
    return report


def print_summary(report: dict[str, Any]) -> None:
    hashes = report["hashes"]
    header = report["header"]
    banking = report["banking"]
    target = report["target_match"]

    print(f"File: {report['file']['name']}")
    print(f"Size: {report['file']['size_bytes']} bytes")
    print(f"SHA-1: {hashes['sha1']}")
    print(f"SHA-256: {hashes['sha256']}")
    print(f"MD5: {hashes['md5']}")
    print(f"CRC32: {hashes['crc32']}")
    print(f"Target: {target['id']} ({target['revision']})" if target else "Target: no known manifest match")
    print(f"Title bytes: {header['title_raw_hex']}  [{header['title_ascii_view']}]")
    print(f"CGB: {header['cgb_mode']} ({header['cgb_flag']})")
    print(f"Cartridge: {header['cartridge_type']} ({header['cartridge_type_code']})")
    print(f"ROM banks: {banking['actual_bank_count']} actual / {header['declared_rom_banks']} declared")
    print(f"Header checksum valid: {header['header_checksum_valid']}")
    print(f"Global checksum valid: {header['global_checksum_valid']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect and fingerprint a local GB/GBC ROM read-only.")
    parser.add_argument("rom", type=Path, help="Path to the local ROM dump")
    parser.add_argument(
        "--targets",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "manifests" / "targets.json",
        help="Target manifest used for hash identification",
    )
    parser.add_argument("--json", type=Path, dest="json_path", help="Optional JSON report output path")
    args = parser.parse_args()

    try:
        report = inspect_rom(args.rom, args.targets)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print_summary(report)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"JSON report: {args.json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
