#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": (0x1E60, 0x1E93, "dbc69d655c76abd864294aa637f01cb90421d63b"),
    "jp-revA": (0x1E60, 0x1E93, "dbc69d655c76abd864294aa637f01cb90421d63b"),
    "kr":      (0x1F10, 0x1F43, "9019dd9dff73904858d81550271ebe5aae7db836"),
    "en":      (0x1EB3, 0x1EE6, "9019dd9dff73904858d81550271ebe5aae7db836"),
    "de":      (0x1EE0, 0x1F13, "9019dd9dff73904858d81550271ebe5aae7db836"),
    "fr":      (0x1EC5, 0x1EF8, "9019dd9dff73904858d81550271ebe5aae7db836"),
    "it":      (0x1ED8, 0x1F0B, "9019dd9dff73904858d81550271ebe5aae7db836"),
    "es":      (0x1ED7, 0x1F0A, "9019dd9dff73904858d81550271ebe5aae7db836"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    args = ap.parse_args()
    releases = json.loads(args.manifest.read_text(encoding="utf-8"))["releases"]
    by_id = {r["id"]: r for r in releases}
    modules = {}

    for rid, (start, end, sha1) in EXPECTED.items():
        path = args.rom_dir / by_id[rid]["reference_filename"]
        if not path.is_file(): raise SystemExit(f"missing reference ROM: {path}")
        data = path.read_bytes()[start:end]
        assert len(data) == 51, (rid, len(data))
        assert hashlib.sha1(data).hexdigest() == sha1, rid
        modules[rid] = data
        print(f"PASS {rid}: printer {start:#06x}-{end - 1:#06x}")

    assert modules["jp-rev0"] == modules["jp-revA"]
    western = modules["en"]
    for rid in ("kr", "de", "fr", "it", "es"):
        assert modules[rid] == western, rid
    print("PASS KR/EN/DE/FR/IT/ES printer modules are byte-identical")
    print("PASS Japanese Rev 0/Rev A printer modules are byte-identical")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
