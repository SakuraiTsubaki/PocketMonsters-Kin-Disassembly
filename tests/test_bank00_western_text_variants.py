#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

TEXT_RANGES = {
    "en": (0x0EBD, 0x1458),
    "de": (0x0EBD, 0x147C),
    "fr": (0x0EBD, 0x1461),
    "it": (0x0EBD, 0x1476),
    "es": (0x0EBD, 0x1475),
}

# DE/IT/ES Gold recognize two extra western localization control bytes:
# $1e -> NextChar and $1d -> PlaceHyphenSplit. The jump destination of the
# latter is 0x10d4 in all three ROMs.
EXTRA_CONTROL_DISPATCH = bytes.fromhex("FE 1E CA 7F 0F FE 1D CA D4 10")

# English routes the two legacy diacritic bytes through Diacritic.
EN_DIACRITIC_DISPATCH = bytes.fromhex("FE E4 28 04 FE E5 20 07")
# All four localized western ROMs instead place those glyphs directly.
LOCALIZED_DIACRITIC_DISPATCH = bytes.fromhex("FE E4 28 35 FE E5 28 31 18 07")

# PlaceHyphenSplit: ld [hl], '-'; jp LineFeedChar. Destination differs because
# the localized text block is relocated, but the five-byte routine starts at
# 0x10d4 in DE/IT/ES Gold.
HYPHEN_PREFIX = bytes.fromhex("36 E3 C3")

# Paragraph begins by preserving a localized text state byte at $c506 in all
# non-English western ROMs. English immediately reads wLinkMode instead.
EN_PARAGRAPH_PREFIX = bytes.fromhex("D5 FA 42 D0")
LOCALIZED_PARAGRAPH_PREFIX = bytes.fromhex("D5 FA 06 C5 F5 FA 42 D0")

# Audited function starts for grammar-sensitive battle name rendering.
BATTLE_STARTS = {
    "en": 0x10E5,
    "de": 0x10F6,
    "fr": 0x10E7,
    "it": 0x10F6,
    "es": 0x10F6,
}
PARAGRAPH_STARTS = {
    "en": 0x1187,
    "de": 0x119B,
    "fr": 0x1188,
    "it": 0x1198,
    "es": 0x119B,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    roms = {}
    for rid in TEXT_RANGES:
        path = args.rom_dir / by_id[rid]["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        roms[rid] = path.read_bytes()

    # Extra control-byte dispatch exists in DE/IT/ES, not EN/FR.
    for rid in ("de", "it", "es"):
        assert roms[rid].find(EXTRA_CONTROL_DISPATCH, 0x0F83, 0x1075) == 0x1014, rid
        assert roms[rid][0x10D4:0x10D7] == HYPHEN_PREFIX, rid
    for rid in ("en", "fr"):
        assert roms[rid].find(EXTRA_CONTROL_DISPATCH, 0x0F83, 0x1075) == -1, rid

    # Diacritic handling is English-specific; every localized western Gold ROM
    # has the direct-placement form instead.
    assert roms["en"].find(EN_DIACRITIC_DISPATCH, 0x0F83, 0x1075) == 0x1028
    for rid in ("de", "fr", "it", "es"):
        pos = roms[rid].find(LOCALIZED_DIACRITIC_DISPATCH, 0x0F83, 0x1080)
        assert pos in (0x1028, 0x1032), (rid, hex(pos) if pos >= 0 else pos)

    # FR/IT put the enemy nickname before their localized suffix; EN/DE/ES
    # begin the enemy branch with a pointer to the localized EnemyText prefix.
    for rid in ("fr", "it"):
        start = BATTLE_STARTS[rid]
        assert roms[rid][start + 10:start + 12] == bytes.fromhex("F6 CA"), rid
    for rid in ("en", "de", "es"):
        start = BATTLE_STARTS[rid]
        assert roms[rid][start + 10:start + 12] != bytes.fromhex("F6 CA"), rid

    # All localized western Gold ROMs preserve $c506 around Paragraph's clear;
    # English does not.
    assert roms["en"][PARAGRAPH_STARTS["en"]:PARAGRAPH_STARTS["en"] + 4] == EN_PARAGRAPH_PREFIX
    for rid in ("de", "fr", "it", "es"):
        start = PARAGRAPH_STARTS[rid]
        assert roms[rid][start:start + len(LOCALIZED_PARAGRAPH_PREFIX)] == LOCALIZED_PARAGRAPH_PREFIX, rid

    for rid, (start, end) in TEXT_RANGES.items():
        assert end > start
        print(f"PASS {rid}: text variants {start:#06x}-{end - 1:#06x}")

    print("PASS western Bank 00 text-engine variant checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
