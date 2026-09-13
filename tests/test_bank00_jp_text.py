#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

MODULE_START = 0x0E8F
MODULE_END = 0x142D
MODULE_SHA1 = "a2dc9d244a4562cc63c9b2ba4b3f677bf6ef7e26"

EMBEDDED_START = 0x1139
EMBEDDED = [
    "DC 2B 9D 8B AB 50",       # わざマシン@
    "93 A7 E3 94 E3 50",       # トレーナー@
    "40 8E 89 AB 50",          # パソコン@
    "A8 88 AC 93 30 DE 50",    # ロケットだん@
    "43 88 A1 AB 50",          # ポケモン@
    "BA B3 29 B7 50",          # こうげき@
    "C0 E7 50",                # た！@
    "75 75 50",                # ⋯⋯@
    "C3 B7 C9 7F 50",          # てきの　@
    "26 7F 50", "CA 7F 50", "C9 7F 50", "DD 7F 50", "C6 7F 50",
    "DF C3 50",                # って@
    "3A DE 7F 34 B3 DB 50",    # ばん　どうろ@
    "DC C0 BC 50",             # わたし@
    "BA BA CA 7F 50",          # ここは　@
]

WEEKDAY_START = 0x1416
WEEKDAYS = [
    "C6 C1 50", "29 C2 50", "B6 50", "BD B2 50",
    "D3 B8 50", "B7 DE 50", "34 50", "D6 B3 3B 50",
]


def read_strings(rom: bytes, start: int, count: int) -> list[str]:
    pos = start
    result = []
    for _ in range(count):
        raw = bytearray()
        while True:
            b = rom[pos]; pos += 1; raw.append(b)
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
    modules = []
    for rid in ("jp-rev0", "jp-revA"):
        path = args.rom_dir / by_id[rid]["reference_filename"]
        if not path.is_file(): raise SystemExit(f"missing reference ROM: {path}")
        rom = path.read_bytes()
        module = rom[MODULE_START:MODULE_END]
        assert len(module) == 1438
        assert hashlib.sha1(module).hexdigest() == MODULE_SHA1, rid
        assert read_strings(rom, EMBEDDED_START, len(EMBEDDED)) == EMBEDDED, (rid, "embedded")
        assert read_strings(rom, WEEKDAY_START, len(WEEKDAYS)) == WEEKDAYS, (rid, "weekdays")
        modules.append(module)
        print(f"PASS {rid}: Japanese text module + strings")

    assert modules[0] == modules[1]
    print("PASS Japanese Rev 0/Rev A Bank 00 text modules are identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
