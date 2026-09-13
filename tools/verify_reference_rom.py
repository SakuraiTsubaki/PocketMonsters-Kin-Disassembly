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
        description="Verify a local Pocket Monsters Kin / Pokemon Gold reference ROM against recorded regional baselines."
    )
    parser.add_argument("rom", type=Path)
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    path = args.rom
    if not path.is_file():
        raise SystemExit(f"not a file: {path}")

    size = path.stat().st_size
    md5 = digest(path, "md5")
    sha1 = digest(path, "sha1")
    sha256 = digest(path, "sha256")

    print(f"file:   {path}")
    print(f"size:   {size}")
    print(f"md5:    {md5}")
    print(f"sha1:   {sha1}")
    print(f"sha256: {sha256}")

    for release in data["releases"]:
        if (
            size == release["size"]
            and md5 == release["md5"]
            and sha1 == release["sha1"]
            and sha256 == release["sha256"]
        ):
            print(f"match:  {release['id']} ({release['region']} / {release['locale']})")
            return 0

    print("match:  none")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
