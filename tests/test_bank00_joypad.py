#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": {"start": 0x08DE, "end": 0x0AD9, "sha1": "325254caf4eb6562f06e6ca4b8dc1cd5f98fbf87"},
    "jp-revA": {"start": 0x08DE, "end": 0x0AD9, "sha1": "325254caf4eb6562f06e6ca4b8dc1cd5f98fbf87"},
    "kr":      {"start": 0x08D2, "end": 0x0AE3, "sha1": "251d9f295e25cfe08fdf2acc9f769ab41944902a"},
    "en":      {"start": 0x08DF, "end": 0x0AF0, "sha1": "e945de06fb5fde6f0a1d2e28fba8afb622019a08"},
    "de":      {"start": 0x08DF, "end": 0x0AF0, "sha1": "07c9021c3afd4cf173f7218ca0e79747d3f9714b"},
    "fr":      {"start": 0x08DF, "end": 0x0AF0, "sha1": "e39b3edc066ff61727cbc1437995ab1082334a70"},
    "it":      {"start": 0x08DF, "end": 0x0AF0, "sha1": "695423b4deef55426d800756b160d03a0ab9bb62"},
    "es":      {"start": 0x08DF, "end": 0x0AF0, "sha1": "8c219f928e16f59aa2eed876cff4872d29b760f4"},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()

    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    modules: dict[str, bytes] = {}

    for rid, exp in EXPECTED.items():
        rel = by_id[rid]
        rom = args.rom_dir / rel["reference_filename"]
        if not rom.is_file():
            raise SystemExit(f"missing reference ROM: {rom}")
        data = rom.read_bytes()[exp["start"]:exp["end"]]
        digest = hashlib.sha1(data).hexdigest()
        assert digest == exp["sha1"], (rid, digest, exp["sha1"])
        modules[rid] = data
        print(f"PASS {rid}: {len(data)} bytes {digest}")

    assert modules["jp-rev0"] == modules["jp-revA"]
    assert len(modules["jp-rev0"]) == 507
    for rid in ("kr", "en", "de", "fr", "it", "es"):
        assert len(modules[rid]) == 529

    # The later regional implementation has two code additions relative to JP:
    # 10 bytes for $ff auto-input duration handling and 12 bytes for PromptButton
    # auto-input dispatch. Address/immediate relocation bytes elsewhere are release-specific.
    assert len(modules["en"]) - len(modules["jp-rev0"]) == 22

    print("PASS joypad structural checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
