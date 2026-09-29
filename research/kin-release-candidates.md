# Study: establish Pocket Monsters Kin / Pokémon Gold release candidates

- Status: draft
- Release ID: two Japanese revisions, one Korean release, and five other localized releases
- Input SHA-256: recorded in `research/releases.csv`
- Last updated: 2026-09-21

## Question

Which distinct local Pokémon Gold identities can be established while prioritizing the Japanese origin releases and official Korean release?

## Environment and tool versions

- Host: Windows
- Inspector: shared `SakuraiTsubaki/Disassembly tools/inspect_gb_rom.py` version 1.0.1
- Repository baseline: `bbd2babeb8840c609f7a943d379e244e7615a4e1`

## Exact procedure

Hash each complete ROM, parse its CGB/SGB and revision fields, validate Nintendo logo and both checksums, then preserve metadata and validation evidence without ROM bytes.

## Observations

Eight unique identities were observed: Japanese revisions 0 and 1, Korean revision 0, and English, German, Spanish, French, and Italian revision-zero releases. All passed logo and checksum validation.

The Korean image differs structurally in observable header metadata: it is 2 MiB, uses CGB flag 0xc0 (color-only), and has SGB flag 0x00. The Japanese images are 1 MiB, CGB-compatible (0x80), and SGB-enhanced (0x03). Other localized images are 2 MiB and CGB-compatible/SGB-enhanced.

## Derived results

The Korean release is retained as its own first-class identity rather than inferred from English or Japanese data. Japanese revisions remain the origin references.

## Interpretation and confidence

Hashes and header fields are direct observations. Release labels remain candidates until independently confirmed.

## Reproduction

Run the shared inspector with `--require-valid`, compare with `analysis/kin-release-header-report.json`, and verify its SHA-256 against the manifest.

## Limitations and next questions

Independent confirmation is required before `verified`. Bank mapping must preserve the size and platform-mode differences across Japanese, Korean, and other localized builds.
