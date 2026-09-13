#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "jp-rev0": (0x1E93, 0x1F0A, "cf8320bfcce948ddf1bf9fa21bde688c7c1c422f"),
    "jp-revA": (0x1E93, 0x1F0A, "cf8320bfcce948ddf1bf9fa21bde688c7c1c422f"),
    "kr":      (0x1F43, 0x1FBA, "9e98bb0960af27c895fb056fc104ecda5273df2e"),
    "en":      (0x1EE6, 0x1F5D, "e590e7dca59e1cc06549afced0ab22e8992b40e2"),
    "de":      (0x1F13, 0x1F8A, "e590e7dca59e1cc06549afced0ab22e8992b40e2"),
    "fr":      (0x1EF8, 0x1F6F, "e590e7dca59e1cc06549afced0ab22e8992b40e2"),
    "it":      (0x1F0B, 0x1F82, "e590e7dca59e1cc06549afced0ab22e8992b40e2"),
    "es":      (0x1F0A, 0x1F81, "e590e7dca59e1cc06549afced0ab22e8992b40e2"),
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
        assert len(data) == 119, (rid, len(data))
        assert hashlib.sha1(data).hexdigest() == sha1, rid
        modules[rid] = data
        print(f"PASS {rid}: game_time {start:#06x}-{end - 1:#06x}")
    assert modules["jp-rev0"] == modules["jp-revA"]
    for rid in ("de", "fr", "it", "es"):
        assert modules[rid] == modules["en"], rid
    print("PASS EN/DE/FR/IT/ES game_time modules are byte-identical")
    print("PASS JP Rev 0/Rev A game_time modules are byte-identical")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
