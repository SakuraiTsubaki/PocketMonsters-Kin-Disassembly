#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": (0x1968, 0x19FB, "8261c082ae047ffa9132d125e2842dd1baee90df"),
    "jp-revA": (0x1968, 0x19FB, "8261c082ae047ffa9132d125e2842dd1baee90df"),
    "kr":      (0x1A0E, 0x1AA1, "d7c294931cdfd9ee2c4dcb8a9e314f8da5ce3b67"),
    "en":      (0x19BB, 0x1A4E, "b62ad08d9e6fb9f50b6b09a5845016841ce74e4d"),
    "de":      (0x19DF, 0x1A72, "9db3cb4089391f0f962ca3747de70968c687644a"),
    "fr":      (0x19C4, 0x1A57, "828f8bc3543d0a5ff2710496f08284961d64e307"),
    "it":      (0x19D9, 0x1A6C, "f6d172fdf67d82785e2a020e888a7ee2f4a4b2a2"),
    "es":      (0x19D8, 0x1A6B, "e355ac87d5e799f7ec78d275e45532114930b9d3"),
}

# The module begins with InitMovementBuffer. Absolute RAM addresses relocate,
# but the instruction skeleton is invariant.
HEAD_OPS = bytes.fromhex("EA")


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
        assert len(module) == 0x93, (rid, len(module))
        assert hashlib.sha1(module).hexdigest() == expected_sha1, rid
        assert module.startswith(HEAD_OPS), rid
        modules[rid] = module
        print(f"PASS {rid}: movement {start:#06x}-{end - 1:#06x} ({len(module)} bytes)")

    assert modules["jp-rev0"] == modules["jp-revA"]
    print("PASS Japanese Rev 0/Rev A movement modules are identical")
    print("PASS Bank 00 movement range/hash checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
