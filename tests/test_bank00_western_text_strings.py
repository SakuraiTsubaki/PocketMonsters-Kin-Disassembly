#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

EMBEDDED = {
    "en": (0x113B, ["93 8C 50","93 91 80 88 8D 84 91 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","84 AD A4 AC B8 7F 50","E1 E2 50","70 71 50","7F 50","50"]),
    "de": (0x114C, ["93 8C 50","93 91 80 88 8D 84 91 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","86 A4 A6 AD E8 7F 50","E1 E2 50","70 71 50","7F 50","E3 22 50"]),
    "fr": (0x113B, ["93 50","83 91 84 92 92 84 94 91 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","7F A4 AD AD A4 AC A8 50","E1 E2 50","70 71 50","7F 50","50"]),
    "it": (0x114A, ["93 50","80 8B 8B 84 8D E8 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","7F AD A4 AC A8 A2 AE 50","E1 E2 50","70 71 50","7F 50","E3 22 50"]),
    "es": (0x114D, ["93 50","84 8D 93 91 84 8D E8 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","84 AD A4 AC E8 7F 50","E1 E2 50","70 71 50","7F 50","E3 22 50"]),
}

WEEKDAYS = {
    "en": (0x1430, ["92 94 8D 50","8C 8E 8D 50","93 94 84 92 50","96 84 83 8D 84 92 50","93 87 94 91 92 50","85 91 88 50","92 80 93 94 91 50","83 80 98 50"]),
    "de": (0x143F, ["92 8E 8D 8D 93 80 86 50","8C 8E 8D 93 80 86 50","83 88 84 8D 92 93 80 86 50","8C 88 93 93 96 8E 82 87 50","83 8E 8D 8D 84 91 92 93 80 86 50","85 91 84 88 93 80 86 50","92 80 8C 92 93 80 86 50","50"]),
    "fr": (0x142C, ["83 88 8C 80 8D 82 87 84 50","8B 94 8D 83 88 50","8C 80 91 83 88 50","8C 84 91 82 91 84 83 88 50","89 84 94 83 88 50","95 84 8D 83 91 84 83 88 50","92 80 8C 84 83 88 50","50"]),
    "it": (0x143C, ["83 8E 8C 84 8D 88 82 80 50","8B 94 8D 84 83 C8 50","8C 80 91 93 84 83 C8 50","8C 84 91 82 8E 8B 84 83 C8 50","86 88 8E 95 84 83 C8 50","95 84 8D 84 91 83 C8 50","92 80 81 80 93 8E 50","50"]),
    "es": (0x143F, ["83 8E 8C 88 8D 86 8E 50","8B 94 8D 84 92 50","8C 80 91 93 84 92 50","8C 88 C7 91 82 8E 8B 84 92 50","89 94 84 95 84 92 50","95 88 84 91 8D 84 92 50","92 BF 81 80 83 8E 50","50"]),
}


def read_terminated_strings(rom: bytes, start: int, count: int) -> list[str]:
    pos = start
    result = []
    for _ in range(count):
        raw = bytearray()
        while True:
            b = rom[pos]
            pos += 1
            raw.append(b)
            if b == 0x50:
                break
        result.append(" ".join(f"{b:02X}" for b in raw))
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}

    for locale in EMBEDDED:
        rom_path = args.rom_dir / by_id[locale]["reference_filename"]
        if not rom_path.is_file():
            raise SystemExit(f"missing reference ROM: {rom_path}")
        rom = rom_path.read_bytes()

        start, expected = EMBEDDED[locale]
        actual = read_terminated_strings(rom, start, len(expected))
        assert actual == expected, (locale, "embedded", actual, expected)

        start, expected = WEEKDAYS[locale]
        actual = read_terminated_strings(rom, start, len(expected))
        assert actual == expected, (locale, "weekdays", actual, expected)
        print(f"PASS {locale}: embedded + weekday strings")

    print("PASS western Bank 00 localized string checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
