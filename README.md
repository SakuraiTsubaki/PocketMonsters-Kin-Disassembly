# PocketMonsters-Kin-Disassembly

Byte-perfect disassembly project for the Japanese **Pocket Monsters Kin (ポケットモンスター 金 / Pokémon Gold)** ROM.

## Goal

Reconstruct the original game into editable RGBDS source, data, graphics, text, audio, maps, scripts, and build/verification tooling so that the completed repository can rebuild the supported ROM revisions **without requiring a base ROM**.

## Source baselines

Two read-only reference ROM revisions are tracked by metadata only. ROM binaries are not included in this repository.

| Revision | Size | Header version | SHA-1 |
| --- | ---: | ---: | --- |
| Rev 0 | 1 MiB | `0x00` | `8814f1039450a5d3684b1389f588ccd7ee7c3436` |
| Rev A | 1 MiB | `0x01` | `a222402235d484ee8e39f3f31bae57cf13daf585` |

Both images contain 64 ROM banks of 16 KiB each (`00`–`3F`). Initial comparison shows 10 differing banks between Rev 0 and Rev A: `00`, `04`, `05`, `09`, `0A`, `0F`, `14`, `21`, `23`, and `24`.

## Repository policy

- Original and modified ROM binaries are never committed.
- Meaningful reproducible work is committed: RGBDS source, extracted/reconstructed assets, scripts, manifests, checksums, symbol/address maps, comparison data, tests, logs, and documentation.
- Reference ROMs may be used locally during reverse engineering and verification, but the finished build must not depend on them.
- Temporary caches and disposable build scratch files are excluded.

## Completion criteria

A supported revision is considered complete when:

1. No source file reads bytes from a local base ROM.
2. All ROM bytes are represented by repository source/assets and deterministic build steps.
3. A clean clone plus documented toolchain can build the ROM.
4. The resulting image matches the recorded reference checksum byte-for-byte.

## Current status

Repository bootstrap and ROM baseline verification are in progress. Bank-by-bank disassembly will proceed from Bank `00` through Bank `3F`, while revision differences are tracked explicitly.
