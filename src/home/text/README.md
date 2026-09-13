# Bank 00 text source layout

This directory is the semantic reconstruction of the Gold Bank 00 text engine across the eight tracked releases.

## Families

- Japanese: `jp_variants.asm`, `jp_commands.asm`, `locales/jp.asm`
- Korean: `kr_variants.asm`, `kr_dict.asm`, `kr_commands.asm`, `locales/kr.asm`
- Western EN/DE/FR/IT/ES: `western_core.asm`, `western_variants.asm`, `western_dict.asm`, `western_commands.asm`, `western_strings.asm`, `locales/{en,de,fr,it,es}.asm`
- Shared semantic pieces: `common.asm`, `flow.asm`, `battle_names.asm`, `substitutions.asm`, `misc.asm`

`analysis/bank00/text_source_ownership.csv` maps the audited English physical symbol order to these semantic source owners. `analysis/bank00/text_symbol_candidates.csv` records the per-language western address projection. Japanese and Korean family-specific executable anchors are locked separately by their signature CSVs and tests.

## Verified family differences

Japanese Rev 0 and Rev A use the same complete Bank 00 text module. Japanese retains the full Japanese particle/substitution dictionary and omits `PlaceFarString` and `TX_FAR`.

Korean adds an eleven-table two-byte Hangul path, banked box/scroll rendering helpers, Hangul font inversion/cache management, and 1bpp-to-2bpp VDMA preparation. Korean retains `PlaceFarString` and `TX_FAR`.

Western localized builds share the English engine family but DE/IT/ES add localization control bytes and hyphen line splitting; all non-English western builds change legacy diacritic handling and paragraph state preservation; FR/IT alter battle/trainer-name grammar order. Locale strings and weekday data are stored separately per release.

## Build status

The semantic text engine is reconstructed and the known family/release deltas are represented as source. Exact ROM ranges, hashes, localized string blocks, family-specific execution signatures, and small miscellaneous routines are regression-tested against the read-only reference ROMs.

The files are intentionally organized by semantic responsibility rather than pretending that a simple concatenation already reproduces retail physical order. Final byte-perfect status remains open until the repository-wide RGBDS constants/macros/section layout can assemble these pieces at their audited addresses. Do not replace this with raw `INCBIN` data from a ROM.
