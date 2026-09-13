#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from difflib import SequenceMatcher
from pathlib import Path

BANK_SIZE = 0x4000

# English ROM0 module boundaries audited against pret/pokegold home/*.asm
# first global symbols and the public symbols build. These are semantic file
# boundaries, not arbitrary internal labels.
MODULE_STARTS = [
    ("vblank", 0x0150), ("delay", 0x032E), ("time_palettes", 0x0343),
    ("fade", 0x0360), ("lcd", 0x041B), ("time", 0x045B),
    ("init", 0x05B0), ("serial", 0x06AA), ("joypad", 0x08DF),
    ("decompress", 0x0AF0), ("palettes", 0x0BDF), ("gfx", 0x0D70),
    ("text", 0x0EBD), ("video", 0x1458), ("map_objects", 0x169C),
    ("sine", 0x19AC), ("movement", 0x19BB), ("menu", 0x1A4E),
    ("printer", 0x1EB3), ("game_time", 0x1EE6), ("map", 0x1F5D),
    ("farcall", 0x2E27), ("predef", 0x2E49), ("window", 0x2E80),
    ("flag", 0x2F2F), ("sprite_updates", 0x2F93), ("string", 0x2FB6),
    ("region", 0x2FD7), ("item", 0x3055), ("random", 0x30A2),
    ("sram", 0x30E1), ("call_regs", 0x30FC), ("clear_sprites", 0x30FF),
    ("copy", 0x311A), ("copy_tilemap", 0x3158), ("copy_name", 0x317B),
    ("array", 0x3186), ("math", 0x31A3), ("print_text", 0x31E2),
    ("queue_script", 0x3423), ("compare", 0x3431), ("tilemap", 0x3449),
    ("pokedex_flags", 0x35C3), ("names", 0x35EE),
    ("scrolling_menu", 0x3751), ("stone_queue", 0x37AC),
    ("trainers", 0x3844), ("pokemon", 0x39BA), ("print_bcd", 0x3ADE),
    ("battle", 0x3B3A), ("sprite_anims", 0x3D0D), ("audio", 0x3D4F),
    ("end", 0x4000),
]


def load_manifest(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["releases"]


def load_bank00(rom_dir: Path, releases: list[dict]) -> dict[str, bytes]:
    result = {}
    for rel in releases:
        path = rom_dir / rel["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        result[rel["id"]] = path.read_bytes()[:BANK_SIZE]
    return result


def map_addr(addr: int, blocks):
    for block in blocks:
        if block.a <= addr < block.a + block.size:
            return block.b + (addr - block.a), "exact"
    prev = next((b for b in reversed(blocks) if b.a + b.size <= addr), None)
    nxt = next((b for b in blocks if b.a > addr), None)
    if prev and nxt:
        prev_delta = prev.b - prev.a
        next_delta = nxt.b - nxt.a
        if prev_delta == next_delta and (
            addr - (prev.a + prev.size) <= 32 or nxt.a - addr <= 32
        ):
            return addr + prev_delta, "inferred_same_delta"
        if addr - (prev.a + prev.size) <= 8:
            return addr + prev_delta, "near_prev"
        if nxt.a - addr <= 8:
            return addr + next_delta, "near_next"
    return None, "unresolved"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Map audited English Bank 00 semantic module boundaries into all tracked Gold releases."
    )
    parser.add_argument("--rom-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    parser.add_argument("--out-dir", type=Path, default=Path("analysis/bank00"))
    args = parser.parse_args()

    releases = load_manifest(args.manifest)
    banks = load_bank00(args.rom_dir, releases)
    if "en" not in banks:
        raise SystemExit("manifest must contain release id 'en'")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    reference = banks["en"]
    blocks_by_release = {}
    coverage_rows = []

    for rel in releases:
        rid = rel["id"]
        if rid == "en":
            blocks_by_release[rid] = None
            coverage_rows.append([rid, BANK_SIZE, "1.000000", 1, BANK_SIZE])
            continue
        matcher = SequenceMatcher(None, reference, banks[rid], autojunk=False)
        blocks = matcher.get_matching_blocks()
        blocks_by_release[rid] = blocks
        matched = sum(b.size for b in blocks)
        largest = max((b.size for b in blocks), default=0)
        coverage_rows.append([rid, matched, f"{matched / BANK_SIZE:.6f}", len(blocks), largest])

    with (args.out_dir / "matching_coverage.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["release", "matched_bytes_vs_en", "coverage_ratio", "matching_blocks", "largest_block"])
        w.writerows(coverage_rows)

    fields = ["module", "en_start"]
    for rel in releases:
        fields += [rel["id"], rel["id"] + "_confidence"]

    with (args.out_dir / "module_map.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for module, addr in MODULE_STARTS[:-1]:
            row = [module, f"0x{addr:04X}"]
            for rel in releases:
                rid = rel["id"]
                if rid == "en":
                    mapped, confidence = addr, "reference"
                else:
                    mapped, confidence = map_addr(addr, blocks_by_release[rid])
                row += ["" if mapped is None else f"0x{mapped:04X}", confidence]
            w.writerow(row)

    with (args.out_dir / "module_ranges_en.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["module", "start", "end_exclusive", "size"])
        for (module, start), (_, end) in zip(MODULE_STARTS, MODULE_STARTS[1:]):
            w.writerow([module, f"0x{start:04X}", f"0x{end:04X}", end - start])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
