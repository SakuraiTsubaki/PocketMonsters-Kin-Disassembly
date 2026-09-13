#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": (0x19FB, 0x1E60, "3bc0bf4d03893c7667a31ca7b464ad2bb7d82e94"),
    "jp-revA": (0x19FB, 0x1E60, "3bc0bf4d03893c7667a31ca7b464ad2bb7d82e94"),
    "kr":      (0x1AA1, 0x1F10, "5a74c1b5bb2508897663e2044de081cf4df49c8a"),
    "en":      (0x1A4E, 0x1EB3, "6f567aa7c90117497e0e3d03ea3472270f76d679"),
    "de":      (0x1A72, 0x1EE0, "884280320a70e2bf82b59be95c5e3fa605f6f046"),
    "fr":      (0x1A57, 0x1EC5, "29e975fdac88f14d414b4233ac4fa520e8493c97"),
    "it":      (0x1A6C, 0x1ED8, "18059c2fca2a4c40e60b4682354aa42500b4f870"),
    "es":      (0x1A6B, 0x1ED7, "0f9e2d86f3bd2714960d08b593e54a5883e10df0"),
}
EXPECTED_SIZES = {
    "jp-rev0": 1125, "jp-revA": 1125, "kr": 1135, "en": 1125,
    "de": 1134, "fr": 1134, "it": 1132, "es": 1132,
}


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
        module = path.read_bytes()[start:end]
        digest = hashlib.sha1(module).hexdigest()
        assert len(module) == EXPECTED_SIZES[rid], (rid, len(module))
        assert digest == expected_sha1, (rid, digest, expected_sha1)
        modules[rid] = module
        print(f"PASS {rid}: menu {start:#06x}-{end - 1:#06x} ({len(module)} bytes)")

    assert modules["jp-rev0"] == modules["jp-revA"]
    print("PASS Japanese Rev 0/Rev A menu modules are identical")
    print("PASS Bank 00 menu range/hash checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
