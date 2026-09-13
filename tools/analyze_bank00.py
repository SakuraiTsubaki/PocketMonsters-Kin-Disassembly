#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "manifests" / "rom_baselines.json"
BANK_SIZE = 0x4000
BANK_ID = 0


def digest(data: bytes, name: str) -> str:
    h = hashlib.new(name)
    h.update(data)
    return h.hexdigest()


def contiguous_ranges(indices: list[int]) -> list[tuple[int, int]]:
    if not indices:
        return []
    out: list[tuple[int, int]] = []
    start = prev = indices[0]
    for value in indices[1:]:
        if value == prev + 1:
            prev = value
            continue
        out.append((start, prev))
        start = prev = value
    out.append((start, prev))
    return out


def load_releases(rom_dir: Path) -> list[tuple[dict, bytes]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    releases: list[tuple[dict, bytes]] = []
    missing: list[str] = []

    for release in manifest["releases"]:
        if release["bank_count"] <= BANK_ID:
            continue
        path = rom_dir / release["reference_filename"]
        if not path.is_file():
            missing.append(str(path))
            continue
        rom = path.read_bytes()
        if len(rom) != release["size"]:
            raise SystemExit(
                f"size mismatch for {path.name}: {len(rom)} != {release['size']}"
            )
        releases.append((release, rom[:BANK_SIZE]))

    if missing:
        raise SystemExit("missing reference ROMs:\n  " + "\n  ".join(missing))
    return releases


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-release survey of Pocket Monsters Kin / Pokemon Gold Bank 00."
    )
    parser.add_argument(
        "--rom-dir",
        type=Path,
        required=True,
        help="directory containing the read-only reference ROMs named in rom_baselines.json",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=REPO_ROOT / "analysis" / "bank00" / "generated",
        help="output directory (default: analysis/bank00/generated)",
    )
    args = parser.parse_args()

    releases = load_releases(args.rom_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    banks = {release["id"]: bank for release, bank in releases}

    summary: list[dict] = []
    for release, bank in releases:
        summary.append(
            {
                "release": release["id"],
                "bank": "00",
                "size": len(bank),
                "sha1": digest(bank, "sha1"),
                "sha256": digest(bank, "sha256"),
                "entry_0100_0103": bank[0x100:0x104].hex().upper(),
                "title_raw": bank[0x134:0x143].hex().upper(),
                "title_ascii": "".join(
                    chr(x) if 32 <= x < 127 else "." for x in bank[0x134:0x143]
                ),
                "game_code": bytes(bank[0x13F:0x143]).decode("ascii", "replace"),
                "cgb_flag": f"{bank[0x143]:02X}",
                "sgb_flag": f"{bank[0x146]:02X}",
                "cart_type": f"{bank[0x147]:02X}",
                "rom_size_code": f"{bank[0x148]:02X}",
                "ram_size_code": f"{bank[0x149]:02X}",
                "destination": f"{bank[0x14A]:02X}",
                "version": f"{bank[0x14C]:02X}",
                "header_checksum": f"{bank[0x14D]:02X}",
                "global_checksum": f"{bank[0x14E]:02X}{bank[0x14F]:02X}",
            }
        )

    pairwise: list[dict] = []
    ids = [release["id"] for release, _ in releases]
    for a, b in itertools.combinations(ids, 2):
        indices = [
            i for i, (left, right) in enumerate(zip(banks[a], banks[b])) if left != right
        ]
        ranges = contiguous_ranges(indices)
        pairwise.append(
            {
                "a": a,
                "b": b,
                "different_bytes": len(indices),
                "different_ranges": len(ranges),
                "first_diff": f"0x{indices[0]:04X}" if indices else "",
                "last_diff": f"0x{indices[-1]:04X}" if indices else "",
            }
        )

    variable = [
        i for i in range(BANK_SIZE) if len({banks[release_id][i] for release_id in ids}) > 1
    ]
    variable_ranges = []
    for start, end in contiguous_ranges(variable):
        variable_ranges.append(
            {
                "start": f"0x{start:04X}",
                "end": f"0x{end:04X}",
                "length": end - start + 1,
                "distinct_patterns": len(
                    {banks[release_id][start : end + 1] for release_id in ids}
                ),
            }
        )

    result = {
        "bank": "00",
        "bank_size": BANK_SIZE,
        "release_count": len(releases),
        "variable_byte_count": len(variable),
        "invariant_same_offset_byte_count": BANK_SIZE - len(variable),
        "summary": summary,
        "pairwise": pairwise,
        "variable_ranges": variable_ranges,
    }

    (args.out_dir / "analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    for filename, rows in (
        ("summary.csv", summary),
        ("pairwise.csv", pairwise),
        ("variable_ranges.csv", variable_ranges),
    ):
        with (args.out_dir / filename).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
