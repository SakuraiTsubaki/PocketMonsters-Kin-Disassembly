#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": (0x142D, 0x1649, "67fdd75e2e265504c8d5690b8d73d92f88bac125"),
    "jp-revA": (0x142D, 0x1649, "67fdd75e2e265504c8d5690b8d73d92f88bac125"),
    "kr":      (0x153F, 0x16EF, "0381578929441194d918dcf1e921fc479a180846"),
    "en":      (0x1458, 0x169C, "31543fd77171c19840c68eb551b12d548af4c020"),
    "de":      (0x147C, 0x16C0, "4d48d93b039e6b255d0d7e77acf142a14b1465aa"),
    "fr":      (0x1461, 0x16A5, "f08b533c8c7bf2c5bc545e25fc6aec97628c5099"),
    "it":      (0x1476, 0x16BA, "29f164232b84183d45fa046c6eebbdf421b94e90"),
    "es":      (0x1475, 0x16B9, "3ce2a3872dbdf78997bacc9492ce5ca48622eb19"),
}

# Exact anchors derived from the read-only ROMs.
WAIT_TOP = {
    "jp-rev0": 0x147E,
    "jp-revA": 0x147E,
    "kr":      0x1590,
    "en":      0x14A9,
    "de":      0x14CD,
    "fr":      0x14B2,
    "it":      0x14C7,
    "es":      0x14C6,
}

KR_UPDATE_BG_MAP = (0x15A3, bytes.fromhex(
    "3B E5 F5 E5 F8 06 36 7F 2B 36 42 2B 36 D1 E1 F1 CD 73 2E 33 33 33 C9"
))
KR_DELAY4 = (0x15BA, bytes.fromhex(
    "F0 A0 FE 01 28 03 CD 2E 03 CD 2E 03 CD 2E 03 C3 2E 03"
))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    modules: dict[str, bytes] = {}

    for rid, (start, end, expected_sha1) in EXPECTED.items():
        path = args.rom_dir / by_id[rid]["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        rom = path.read_bytes()
        module = rom[start:end]
        digest = hashlib.sha1(module).hexdigest()
        assert digest == expected_sha1, (rid, digest, expected_sha1)
        assert rom[start:start + 4] == bytes.fromhex("F0 DD A7 C8"), rid
        # Every build reaches WaitTop immediately after the shared update-buffer routine.
        assert WAIT_TOP[rid] - start == 0x51, (rid, hex(WAIT_TOP[rid] - start))
        modules[rid] = module
        print(f"PASS {rid}: video {start:#06x}-{end - 1:#06x} ({len(module)} bytes)")

    assert modules["jp-rev0"] == modules["jp-revA"]
    assert len(modules["jp-rev0"]) == 540
    assert len(modules["kr"]) == 432
    for rid in ("en", "de", "fr", "it", "es"):
        assert len(modules[rid]) == 580

    kr_rom = (args.rom_dir / by_id["kr"]["reference_filename"]).read_bytes()
    start, sig = KR_UPDATE_BG_MAP
    assert kr_rom[start:start + len(sig)] == sig
    start, sig = KR_DELAY4
    assert kr_rom[start:start + len(sig)] == sig

    # JP has no western BG Map 1 mode-selection prefix. Western Gold contains
    # the third decrement followed by reads of hBGMapAddress; JP goes directly
    # to the attribute-map path after mode 1.
    western_prefix = bytes.fromhex("F0 D6 A7 C8 3D")
    for rid in ("en", "de", "fr", "it", "es"):
        start = WAIT_TOP[rid] + 0x12
        rom = (args.rom_dir / by_id[rid]["reference_filename"]).read_bytes()
        assert rom[start:start + len(western_prefix)] == western_prefix, rid

    print("PASS Bank 00 video range/hash/family checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
