#!/usr/bin/env python3
"""Verify that a rebuilt ROM matches the local reference byte-for-byte."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

BANK_SIZE = 0x4000


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("rebuilt", type=Path)
    args = parser.parse_args()

    reference = args.reference.read_bytes()
    rebuilt = args.rebuilt.read_bytes()

    print(f"reference SHA-1: {sha1(reference)}")
    print(f"rebuilt   SHA-1: {sha1(rebuilt)}")

    if len(reference) != len(rebuilt):
        print(f"size mismatch: reference=0x{len(reference):X}, rebuilt=0x{len(rebuilt):X}")
        return 1

    if reference == rebuilt:
        print("MATCH: rebuilt ROM is byte-identical to the reference")
        return 0

    for offset, (a, b) in enumerate(zip(reference, rebuilt)):
        if a != b:
            bank = offset // BANK_SIZE
            bank_offset = offset % BANK_SIZE
            cpu_address = bank_offset if bank == 0 else 0x4000 + bank_offset
            print(
                "first mismatch: "
                f"file=0x{offset:06X}, bank=0x{bank:02X}, cpu=0x{cpu_address:04X}, "
                f"reference=0x{a:02X}, rebuilt=0x{b:02X}"
            )
            break
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
