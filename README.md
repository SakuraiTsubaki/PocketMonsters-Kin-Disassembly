# Pocket Monsters Kin — Disassembly

![Status](https://img.shields.io/badge/status-bank_00_analysis-blue)
![Project](https://img.shields.io/badge/project-disassembly-blue)
![ROMs](https://img.shields.io/badge/ROM_binaries-not_included-success)

Disassembly and source-reconstruction project for **Pocket Monsters Kin / Pokémon Gold**.

## 🎯 Goals

- Reconstruct game code and data into readable, editable assembly/source form.
- Document ROM, bank, section, data, script, asset, and version differences.
- Keep analysis, tooling, metadata, and documentation reproducible.
- Build a clean foundation for long-term reverse-engineering work.

## 🚧 Status

The exact-match RGBDS baseline workflow is active and **Bank 00 is open for ROM-grounded reconstruction**. Eight supplied Gold ROM images have been locally fingerprinted; Japanese Rev.0 and Rev.1 are the current direct reconstruction targets.

The first Bank 00 reset/RST/interrupt/entry bytes have been decoded and recorded as **Observed** evidence. They are not considered **Matched** source until they assemble, link, and reproduce each selected retail revision byte-for-byte.

See [Project status](docs/PROJECT_STATUS.md) and [Bank 00 reconstruction log](analysis/banks/bank00.md) for the current verification state.

## 🗂️ Scope

- ROM, bank, section, and code analysis
- Game data structures
- Scripts and event data
- Graphics and asset metadata
- Audio and resource formats
- Maps and world data
- Tools, notes, manifests, and verification data

## 📌 Repository policy

ROM images and rebuilt playable ROM binaries are **not included**. The repository contains reconstructed source, extracted/recreated project data, tooling, analysis, documentation, and reproducible verification metadata.

Unknown bytes remain local `INCBIN` ranges until understood. Revision or regional differences are preserved rather than normalized away.

## 🧭 Roadmap

- [x] Establish the supplied baseline version/revision inventory
- [x] Open Bank 00 and record revision-scoped evidence
- [ ] Produce the first RGBDS source replacement that exactly matches both selected Japanese revisions
- [ ] Continue bank/section/data-structure mapping
- [ ] Expand source reconstruction bank by bank
- [ ] Document assets, scripts, formats, and regional/revision differences
- [ ] Expand regression and reproducibility checks

## 📚 Documentation

| Document | Purpose |
| --- | --- |
| [Project status](docs/PROJECT_STATUS.md) | Current stage, coverage, validation level, and next milestones |
| [Bank 00 log](analysis/banks/bank00.md) | Current Bank 00 fingerprints, observations, revision differences, and next source step |
| [Disassembly baseline](docs/DISASSEMBLY_BASELINE.md) | Exact-match local-ROM reconstruction workflow |
| [Roadmap](docs/ROADMAP.md) | Recommended disassembly phases and long-term progression |
| [Version coverage](docs/VERSIONS.md) | Regions, languages, revisions, releases, builds, and hashes |
| [Research guide](docs/RESEARCH_GUIDE.md) | Evidence, confidence, and research-recording workflow |
| [Verification guide](docs/VERIFICATION.md) | Standards for Observed, Reproduced, and Matched results |
| [Repository structure](docs/REPOSITORY_STRUCTURE.md) | Intended long-term source, data, asset, tooling, and manifest layout |
| [Documentation hub](docs/README.md) | Entry point for format, code, script, asset, version, and verification notes |

## 🧱 Repository structure

The repository grows only when verified project material exists. Long-term areas may include `asm/`, `data/`, `assets/`, `tools/`, `tests/`, and `manifests/`; target architecture and verified evidence determine the detailed layout.

See [Repository Structure](docs/REPOSITORY_STRUCTURE.md) for the organization policy.

## 🔬 Research and verification

Research findings identify the relevant target version/revision and separate hypotheses from **Observed**, **Reproduced**, and **Matched** results. Exact source reconstruction requires assembly/link success plus byte-identical comparison against the selected local retail image.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules, evidence expectations, commit guidance, and pull-request requirements.
