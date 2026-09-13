#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "rom_baselines.json"


def digest(path: Path, name: str) -> str:
    h = hashlib.new(name)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a local Pocket Monsters Kin reference ROM against recorded baselines."
    )
    parser.add_argument("rom", type=Path)
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    path = args.rom
    if not path.is_file():
        raise SystemExit(f"not a file: {path}")

    size = path.stat().st_size
    sha1 = digest(path, "sha1")
    sha256 = digest(path, "sha256")

    print(f"file:   {path}")
    print(f"size:   {size}")
    print(f"sha1:   {sha1}")
    print(f"sha256: {sha256}")

    for revision in data["revisions"]:
        if (
            size == revision["size"]
            and sha1 == revision["sha1"]
            and sha256 == revision["sha256"]
        ):
            print(f"match:  {revision['id']}")
            return 0

    print("match:  none")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
