#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": (0x1649, 0x1959, "c57eeb51d98337b5b94de67f9d734bfe8fc1569e"),
    "jp-revA": (0x1649, 0x1959, "c57eeb51d98337b5b94de67f9d734bfe8fc1569e"),
    "kr":      (0x16EF, 0x19FF, "c57f490728c72a8cb55a0c8fc15a16461f5b0b17"),
    "en":      (0x169C, 0x19AC, "445d2f45cf83e2271217946947d2010adcb72cfc"),
    "de":      (0x16C0, 0x19D0, "86f1d7580d67bd53bf66d29631824739b8d22468"),
    "fr":      (0x16A5, 0x19B5, "d9d0c8da6c43febd8acd29e446cd8d35b93c6766"),
    "it":      (0x16BA, 0x19CA, "073de31b763a6c9977866bf19d3d5b3542e0fcb0"),
    "es":      (0x16B9, 0x19C9, "d212ccb706d160e5ef7317af4b6669661f4b2039"),
}

# GetSpritePalette starts identically in every build up through the bank id.
HEAD = bytes.fromhex("E5 D5 C5 4F 3E 05")
# DoesObjectHaveASprite / SetSpriteDirection / GetSpriteDirection tail is
# structurally identical in every tracked release.
TAIL = bytes.fromhex(
    "21 00 00 09 7E A7 C9 "
    "F5 21 08 00 09 7E E6 F3 5F F1 E6 0C B3 77 C9 "
    "21 08 00 09 7E E6 0C C9"
)


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
        assert len(module) == 0x310, (rid, len(module))
        assert digest == expected_sha1, (rid, digest, expected_sha1)
        assert module.startswith(HEAD), rid
        assert module.endswith(TAIL), rid
        modules[rid] = module
        print(f"PASS {rid}: map_objects {start:#06x}-{end - 1:#06x} ({len(module)} bytes)")

    assert modules["jp-rev0"] == modules["jp-revA"]
    print("PASS Japanese Rev 0/Rev A map_objects modules are identical")
    print("PASS Bank 00 map_objects range/hash/structure checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
