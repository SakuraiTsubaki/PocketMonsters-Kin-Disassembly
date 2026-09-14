# Cartridge Identity Matrix — Pocket Monsters Kin / Pokémon Gold

Started: 2026-09-14

Purpose: track physical/product-code lineage separately from ROM checksum identity. Product-code equality/difference is not assumed to imply byte equality/difference without separate evidence.

Primary public hardware source in this pass: Game Boy Hardware Database (GBHWDB), cross-linked to No-Intro identities.

## Gold family product identities

| Origin/region | Public release identity | Product / ROM ID | Notes |
| --- | --- | --- | --- |
| Japan | Pocket Monsters Kin | `DMG-AAUJ-0` | Japanese origin retail Rev.0 |
| Japan | Pocket Monsters Kin Rev.1 | `DMG-AAUJ-1` | Japanese retail revision |
| Korea | Pocket Monsters Geum | `CGB-AAUK-0` | Korean release uses a CGB-prefixed product identity rather than the Japanese/localized DMG identities |
| USA/English | Pokemon Gold Version | `DMG-AAUE-0` | English market identity |
| Europe/Australia English | Pokemon Gold Version | `DMG-AAUP-0` | GBHWDB has observed EUR and AUS label variants under this product identity |
| Germany | Pokemon Goldene Edition | `DMG-AAUD-0` | German localization |
| France | Pokemon Version Or | `DMG-AAUF-0` | French localization |
| Italy | Pokemon Versione Oro | `DMG-AAUI-0` | Italian localization |
| Spain | Pokemon Edicion Oro | `DMG-AAUS-0` | Spanish localization |

## Observed board/hardware evidence

GBHWDB records Gold-family examples on `DMG-KGDU-10` boards and MBC3-family mappers. Public observations include MBC3A and MBC3B examples for English-market cartridges and MBC3B examples for German cartridges. These are physical cartridge observations, not yet a complete board census.

Important separation:

- `ROM identity` = software/checksum/revision.
- `product identity` = region/language/catalogue code.
- `label/release suffix` = e.g. USA/EUR/AUS/NOE observed physical-market label.
- `board assembly` = PCB/mapper/RAM/supervisor/crystal components.

These layers must not be collapsed into one “version” field.

## Japanese-origin comparison rule

Every regional Gold identity above will ultimately be compared against Japanese `DMG-AAUJ-0` first, then Japanese `DMG-AAUJ-1` where chronology/code ancestry requires it. English is a comparison branch, not the origin.

## Evidence status

All rows are currently `PUBLIC_REFERENCE` from public hardware/catalogue evidence. The Japanese and regional ROM SHA-1 identities are tracked separately in `analysis/release_matrix.md`.

## Remaining hardware census

- Capture a dedicated GBHWDB/photographic entry for every regional product identity, not merely the variant index.
- Record label codes/stamps, PCB revisions, mapper manufacturer/revision, SRAM, supervisor/reset IC and 32.768 kHz crystal presence per observed cartridge.
- Distinguish multiple physical board populations that contain the same ROM identity.
- Investigate why Korean Gold is catalogued as `CGB-AAUK-0` and relate that physical identity to its 2 MiB ROM/data-layout differences.
- Cross-check product codes against boxes/manuals and official regional documentation.

Sources:
- https://gbhwdb.gekkio.fi/cartridges/DMG-AAUD-0/
- https://gbhwdb.gekkio.fi/cartridges/gbc.html
- https://gbhwdb.gekkio.fi/cartridges/DMG-KGDU.html
