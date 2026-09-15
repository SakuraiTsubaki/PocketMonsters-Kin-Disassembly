#!/usr/bin/env python3
"""Validate Generation III target sprite assets and manifests.

This validator intentionally uses only the Python standard library so it can run
in a clean repository checkout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path
from typing import Iterable

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
VALID_STATUSES = {
    "planned",
    "source-audited",
    "pixel-adapted",
    "encoded",
    "validated",
}


class ValidationError(Exception):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_png_metadata(path: Path) -> dict:
    with path.open("rb") as f:
        if f.read(8) != PNG_SIGNATURE:
            raise ValidationError(f"{path}: invalid PNG signature")

        width = height = bit_depth = color_type = None
        palette_entries = None
        trns = None

        while True:
            raw_len = f.read(4)
            if not raw_len:
                break
            if len(raw_len) != 4:
                raise ValidationError(f"{path}: truncated PNG chunk length")
            length = struct.unpack(">I", raw_len)[0]
            chunk_type = f.read(4)
            data = f.read(length)
            crc = f.read(4)
            if len(chunk_type) != 4 or len(data) != length or len(crc) != 4:
                raise ValidationError(f"{path}: truncated PNG chunk")

            if chunk_type == b"IHDR":
                if length != 13:
                    raise ValidationError(f"{path}: invalid IHDR length")
                width, height, bit_depth, color_type, _, _, _ = struct.unpack(
                    ">IIBBBBB", data
                )
            elif chunk_type == b"PLTE":
                if length % 3:
                    raise ValidationError(f"{path}: invalid PLTE length")
                palette_entries = length // 3
            elif chunk_type == b"tRNS":
                trns = data
            elif chunk_type == b"IEND":
                break

    if None in (width, height, bit_depth, color_type):
        raise ValidationError(f"{path}: missing IHDR")

    return {
        "width": width,
        "height": height,
        "bit_depth": bit_depth,
        "color_type": color_type,
        "palette_entries": palette_entries,
        "trns": trns,
    }


def validate_png(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        meta = read_png_metadata(path)
    except ValidationError as e:
        return [str(e)]

    if (meta["width"], meta["height"]) != (64, 64):
        errors.append(
            f"{path}: expected 64x64, got {meta['width']}x{meta['height']}"
        )
    if meta["color_type"] != 3:
        errors.append(
            f"{path}: expected indexed-color PNG (color type 3), "
            f"got {meta['color_type']}"
        )
    if meta["palette_entries"] is None:
        errors.append(f"{path}: missing PLTE")
    elif meta["palette_entries"] > 16:
        errors.append(
            f"{path}: palette contains {meta['palette_entries']} entries; max is 16"
        )

    trns = meta["trns"]
    if trns is None or len(trns) < 1:
        errors.append(f"{path}: missing tRNS/index-0 transparency")
    else:
        if trns[0] != 0:
            errors.append(f"{path}: palette index 0 is not fully transparent")
        if any(alpha != 255 for alpha in trns[1:]):
            errors.append(
                f"{path}: semi/fully transparent palette entries other than index 0"
            )

    return errors


def decompress_gba_lz77(data: bytes) -> bytes:
    if len(data) < 4 or data[0] != 0x10:
        raise ValidationError("not a GBA LZ77 type-0x10 stream")

    out_len = data[1] | (data[2] << 8) | (data[3] << 16)
    src = 4
    out = bytearray()

    while len(out) < out_len:
        if src >= len(data):
            raise ValidationError("truncated GBA LZ77 flag byte")
        flags = data[src]
        src += 1

        for bit in range(7, -1, -1):
            if len(out) >= out_len:
                break

            if flags & (1 << bit):
                if src + 1 >= len(data):
                    raise ValidationError("truncated GBA LZ77 back-reference")
                a = data[src]
                b = data[src + 1]
                src += 2

                length = (a >> 4) + 3
                disp = ((a & 0x0F) << 8) | b
                distance = disp + 1

                if distance > len(out):
                    raise ValidationError("invalid GBA LZ77 back-reference distance")

                for _ in range(length):
                    if len(out) >= out_len:
                        break
                    out.append(out[-distance])
            else:
                if src >= len(data):
                    raise ValidationError("truncated GBA LZ77 literal")
                out.append(data[src])
                src += 1

    return bytes(out)


def validate_lz_roundtrip(compressed: Path, raw: Path) -> list[str]:
    try:
        decoded = decompress_gba_lz77(compressed.read_bytes())
    except ValidationError as e:
        return [f"{compressed}: {e}"]

    expected = raw.read_bytes()
    if decoded != expected:
        return [f"{compressed}: decompressed data does not match {raw}"]
    return []


def require_file(repo: Path, rel: str, required: bool, errors: list[str]) -> Path | None:
    path = repo / rel
    if not path.is_file():
        if required:
            errors.append(f"missing required file: {rel}")
        return None
    return path


def validate_manifest(manifest_path: Path, repo: Path) -> list[str]:
    errors: list[str] = []

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{manifest_path}: cannot parse JSON: {e}"]

    target = manifest.get("target")
    if not isinstance(target, dict):
        return [f"{manifest_path}: missing target object"]

    status = target.get("status")
    if status not in VALID_STATUSES:
        errors.append(
            f"{manifest_path}: target.status must be one of "
            + ", ".join(sorted(VALID_STATUSES))
        )
    required_outputs = status in {"encoded", "validated"}

    for side in ("front", "back"):
        side_obj = target.get(side)
        if not isinstance(side_obj, dict):
            errors.append(f"{manifest_path}: missing target.{side}")
            continue

        if side_obj.get("canvas") != [64, 64]:
            errors.append(f"{manifest_path}: target.{side}.canvas must be [64, 64]")

        files = side_obj.get("files", {})
        png_rel = files.get("png")
        raw_rel = files.get("4bpp")
        lz_rel = files.get("4bpp_lz")

        if not all(isinstance(v, str) for v in (png_rel, raw_rel, lz_rel)):
            errors.append(
                f"{manifest_path}: target.{side}.files must define png, 4bpp, 4bpp_lz"
            )
            continue

        png_path = require_file(repo, png_rel, required_outputs, errors)
        raw_path = require_file(repo, raw_rel, required_outputs, errors)
        lz_path = require_file(repo, lz_rel, required_outputs, errors)

        if png_path:
            errors.extend(validate_png(png_path))
        if raw_path and raw_path.stat().st_size != 2048:
            errors.append(
                f"{raw_rel}: expected 2048-byte 64x64 4bpp payload, "
                f"got {raw_path.stat().st_size}"
            )
        if raw_path and lz_path:
            errors.extend(validate_lz_roundtrip(lz_path, raw_path))

    palette = target.get("palette")
    if not isinstance(palette, dict):
        errors.append(f"{manifest_path}: missing target.palette")
    else:
        if palette.get("transparent_index") != 0:
            errors.append(f"{manifest_path}: palette transparent_index must be 0")
        if palette.get("max_entries") != 16:
            errors.append(f"{manifest_path}: palette max_entries must be 16")

        for kind in ("normal", "shiny"):
            pal_obj = palette.get(kind)
            if not isinstance(pal_obj, dict):
                errors.append(f"{manifest_path}: missing palette.{kind}")
                continue

            binary_rel = pal_obj.get("binary")
            compressed_rel = pal_obj.get("compressed")
            source_rel = pal_obj.get("source")

            if not all(
                isinstance(v, str) for v in (source_rel, binary_rel, compressed_rel)
            ):
                errors.append(
                    f"{manifest_path}: palette.{kind} must define "
                    "source, binary, compressed"
                )
                continue

            source_path = require_file(repo, source_rel, required_outputs, errors)
            binary_path = require_file(repo, binary_rel, required_outputs, errors)
            compressed_path = require_file(
                repo, compressed_rel, required_outputs, errors
            )

            if binary_path and binary_path.stat().st_size != 32:
                errors.append(
                    f"{binary_rel}: expected 32-byte 16-color GBA palette, "
                    f"got {binary_path.stat().st_size}"
                )
            if binary_path and compressed_path:
                errors.extend(validate_lz_roundtrip(compressed_path, binary_path))

            _ = source_path

    hashes = manifest.get("hashes", {})
    if not isinstance(hashes, dict):
        errors.append(f"{manifest_path}: hashes must be an object")
    else:
        for rel, expected in hashes.items():
            if not isinstance(rel, str) or not isinstance(expected, str):
                errors.append(f"{manifest_path}: hashes entries must be string:string")
                continue
            path = repo / rel
            if not path.is_file():
                errors.append(f"{manifest_path}: hashed file does not exist: {rel}")
                continue
            actual = sha256_file(path)
            if actual.lower() != expected.lower():
                errors.append(
                    f"{manifest_path}: SHA-256 mismatch for {rel}: "
                    f"expected {expected}, got {actual}"
                )

    if status == "validated":
        validation = manifest.get("validation", {})
        if not isinstance(validation, dict) or not validation:
            errors.append(f"{manifest_path}: validated target needs validation object")
        else:
            false_keys = [key for key, value in validation.items() if value is not True]
            if false_keys:
                errors.append(
                    f"{manifest_path}: validated target has incomplete gates: "
                    + ", ".join(false_keys)
                )

    return errors


def iter_manifests(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            yield from sorted(path.glob("*.json"))
        else:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("manifests/sprites/gen3")],
        help="manifest JSON files or directories",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="repository root (default: current directory)",
    )
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    manifests = list(iter_manifests(args.paths))
    manifests = [p for p in manifests if p.name != "example.target-manifest.json"]

    if not manifests:
        print("No target manifests selected.")
        return 0

    total_errors = 0
    for manifest in manifests:
        errors = validate_manifest(manifest, repo)
        if errors:
            total_errors += len(errors)
            print(f"FAIL {manifest}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {manifest}")

    if total_errors:
        print(f"\n{total_errors} validation error(s).")
        return 1

    print(f"\nValidated {len(manifests)} manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
