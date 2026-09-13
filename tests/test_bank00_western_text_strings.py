#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {
    "en": (0x113B, ["93 8C 50","93 91 80 88 8D 84 91 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","84 AD A4 AC B8 7F 50","E1 E2 50","70 71 50","7F 50","50"]),
    "de": (0x114C, ["93 8C 50","93 91 80 88 8D 84 91 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","86 A4 A6 AD E8 7F 50","E1 E2 50","70 71 50","7F 50","E3 22 50"]),
    "fr": (0x113B, ["93 50","83 91 84 92 92 84 94 91 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","7F A4 AD AD A4 AC A8 50","E1 E2 50","70 71 50","7F 50","50"]),
    "it": (0x114A, ["93 50","80 8B 8B 84 8D E8 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","7F AD A4 AC A8 A2 AE 50","E1 E2 50","70 71 50","7F 50","E3 22 50"]),
    "es": (0x114D, ["93 50","84 8D 93 91 84 8D E8 50","8F 82 50","91 8E 82 8A 84 93 50","8F 8E 8A EA 50","BA B3 29 B7 50","75 75 50","84 AD A4 AC E8 7F 50","E1 E2 50","70 71 50","7F 50","E3 22 50"]),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}

    for locale, (start, expected_strings) in EXPECTED.items():
        rom_path = args.rom_dir / by_id[locale]["reference_filename"]
        if not rom_path.is_file():
            raise SystemExit(f"missing reference ROM: {rom_path}")
        rom = rom_path.read_bytes()
        pos = start
        actual = []
        for _ in expected_strings:
            raw = bytearray()
            while True:
                b = rom[pos]
                pos += 1
                raw.append(b)
                if b == 0x50:
                    break
            actual.append(" ".join(f"{b:02X}" for b in raw))
        assert actual == expected_strings, (locale, actual, expected_strings)
        print(f"PASS {locale}: {len(actual)} embedded strings")

    print("PASS western embedded text-string checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
