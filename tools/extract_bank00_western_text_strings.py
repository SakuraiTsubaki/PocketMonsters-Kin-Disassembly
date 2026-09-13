#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

# Verified first embedded-string address in each western Bank 00 text module.
# FR/IT/ES begin one byte earlier than the first-pass mapper suggested:
# French stores "CT@" and Italian/Spanish store "MT@".
STARTS = {
    "en": 0x113B,
    "de": 0x114C,
    "fr": 0x113A,
    "it": 0x1149,
    "es": 0x114C,
}

LABELS = [
    "TMCharText",
    "TrainerCharText",
    "PCCharText",
    "RocketCharText",
    "PlacePOKeText",
    "KougekiText",
    "SixDotsCharText",
    "EnemyText",
    "PlacePKMNText",
    "PlacePOKEText",
    "String_Space",
    "DummiedText",
]

# Start with ordinary western letters, then overlay special control/Japanese
# glyphs whose byte values overlap the lower-case range in this mixed charmap.
CHARMAP: dict[int, str] = {0x50: "@", 0x7F: " ", 0xEA: "é", 0xE8: ".", 0xE3: "-", 0x22: "<LF>", 0x75: "…", 0xE1: "<PK>", 0xE2: "<MN>", 0x70: "<PO>", 0x71: "<KE>"}
CHARMAP.update({0x80 + i: ch for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")})
CHARMAP.update({0xA0 + i: ch for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz")})
CHARMAP.update({0xBA: "こ", 0xB3: "う", 0x29: "げ", 0xB7: "き"})


def decode(raw: bytes) -> str:
    return "".join(CHARMAP.get(b, f"<${b:02X}>") for b in raw)


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract Bank 00 embedded western text-engine strings from verified Gold ROMs.")
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    ap.add_argument("--output", type=Path, default=Path("analysis/bank00/text_strings.csv"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    rows = []

    for locale, first in STARTS.items():
        rel = by_id[locale]
        rom_path = args.rom_dir / rel["reference_filename"]
        if not rom_path.is_file():
            raise SystemExit(f"missing reference ROM: {rom_path}")
        rom = rom_path.read_bytes()
        pos = first
        for label in LABELS:
            start = pos
            raw = bytearray()
            while True:
                b = rom[pos]
                pos += 1
                raw.append(b)
                if b == 0x50:
                    break
            rows.append([
                locale,
                label,
                f"0x{start:04X}",
                f"0x{pos:04X}",
                len(raw),
                decode(bytes(raw)),
                " ".join(f"{b:02X}" for b in raw),
            ])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["locale", "label", "start", "end_exclusive", "size", "decoded", "hex"])
        w.writerows(rows)

    for row in rows:
        print(", ".join(str(v) for v in row[:6]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
