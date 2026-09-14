# PocketMonsters-Kin-Disassembly

![Status](https://img.shields.io/badge/status-in_progress-yellow)
![Project](https://img.shields.io/badge/project-disassembly-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Byte-perfect, multi-region disassembly and source reconstruction project for **Pocket Monsters Kin / Pokémon Gold**.

## Goal

Reconstruct the supported retail releases into editable RGBDS source, data, graphics, text, audio, maps, scripts, and build/verification tooling so that a completed clean clone can rebuild each ROM **without requiring a base ROM**.

## Source baselines

Eight read-only reference ROMs are tracked by metadata only. ROM binaries are not included in this repository.

| ID | Release | Size | Banks | Header version | SHA-1 |
| --- | --- | ---: | ---: | ---: | --- |
| `jp-rev0` | Japan Rev 0 | 1 MiB | 64 | `0x00` | `8814f1039450a5d3684b1389f588ccd7ee7c3436` |
| `jp-revA` | Japan Rev A | 1 MiB | 64 | `0x01` | `a222402235d484ee8e39f3f31bae57cf13daf585` |
| `kr` | Korea Rev 0 | 2 MiB | 128 | `0x00` | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` |
| `en` | USA/Europe Rev 0 | 2 MiB | 128 | `0x00` | `d8b8a3600a465308c9953dfa04f0081c05bdcb94` |
| `de` | Germany Rev 0 | 2 MiB | 128 | `0x00` | `9254195d461ea942eaaa08cc4b83de3cf82aea0d` |
| `fr` | France Rev 0 | 2 MiB | 128 | `0x00` | `c147c0d8c2b71b7628a7233436f5c052b5b17081` |
| `it` | Italy Rev 0 | 2 MiB | 128 | `0x00` | `032608fe8947b627584a4a0eccc7bf9ad3588426` |
| `es` | Spain Rev 0 | 2 MiB | 128 | `0x00` | `162ea54c6a3cff374642e6dd842f9bffac847e7b` |

Full MD5/SHA-1/SHA-256 and cartridge-header metadata are stored in `manifests/rom_baselines.json`.

The Japanese Rev 0 and Rev A images differ in 10 banks: `00`, `04`, `05`, `09`, `0A`, `0F`, `14`, `21`, `23`, and `24`. The localized 2 MiB releases extend through Bank `7F`, so the bank-by-bank reconstruction ledger covers `00`–`7F` and records `n/a` for Japanese-only absent banks `40`–`7F`.

## Repository policy

- Original and modified ROM binaries are never committed.
- Meaningful reproducible work is committed: RGBDS source, extracted/reconstructed graphics, text, audio, maps, scripts, data, tools, manifests, checksums, symbols, address maps, comparison tables, tests, logs, and documentation.
- Reference ROMs may be used locally for extraction, reverse engineering, comparison, and verification, but the finished build must not depend on them.
- Temporary caches and disposable scratch files are excluded.

## Reconstruction model

```text
read-only reference ROMs (local analysis only)
        ↓
code + data + text + graphics + maps + audio reconstruction
        ↓
repository source/assets
        ↓
RGBDS + project build tools
        ↓
regional Gold ROM target
        ↓
byte-for-byte checksum verification
```

## Completion criteria

A supported release is complete when:

1. No build source reads bytes from a local base ROM.
2. Every ROM byte is represented by repository source/assets and deterministic build steps.
3. A clean clone plus the documented toolchain can build the target.
4. The generated image matches that release's recorded reference checksum byte-for-byte.

## Current status

Phase 0 bootstrap is complete for all eight project source releases. Bank-by-bank disassembly will proceed across Bank `00`–`7F`, with common code/data separated from language-, region-, and revision-specific differences as they are identified.

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Documentation Hub](docs/README.md) | Central entry point for project documentation |
| [Project Status](docs/PROJECT_STATUS.md) | Reconstruction and matching status |
| [Version Coverage](docs/VERSIONS.md) | Supported releases, revisions, sizes, and hashes |
| [Disassembly Standards](docs/DISASSEMBLY_STANDARDS.md) | Source reconstruction and provenance standards |
| [Project Standards](docs/PROJECT_STANDARDS.md) | Naming, assets, manifests, provenance, and repository-wide conventions |
| [Build and Matching](docs/BUILD_AND_MATCHING.md) | Reproducible build and exact-match workflow |
| [Verification](docs/VERIFICATION.md) | Evidence levels and matching criteria |
| [Asset Workflow](docs/ASSET_WORKFLOW.md) | Graphics, sprites, deduplication, manifests, and review batches |
| [Manifest Guide](manifests/README.md) | Manifest conventions and reusable asset-manifest example |
| [Contributing](CONTRIBUTING.md) | Contribution and pull-request guidance |
