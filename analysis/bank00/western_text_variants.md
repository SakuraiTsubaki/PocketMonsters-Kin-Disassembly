# Bank 00 western text-engine variants

This note records differences verified directly against the five tracked western Pokémon Gold ROMs. Public disassemblies are used only as semantic cross-checks; the ROM bytes remain authoritative.

## Exact text-module sizes

| Release | Range | Bytes | Delta vs EN |
| --- | --- | ---: | ---: |
| EN | `0x0EBD-0x1457` | 1435 | 0 |
| DE | `0x0EBD-0x147B` | 1471 | +36 |
| FR | `0x0EBD-0x1460` | 1444 | +9 |
| IT | `0x0EBD-0x1475` | 1465 | +30 |
| ES | `0x0EBD-0x1474` | 1464 | +29 |

## Embedded-string corrections

The first-pass repeated-sequence mapper was one byte late for three TM labels. Direct ROM parsing verifies:

- FR: `CT@` begins at `0x113A`.
- IT: `MT@` begins at `0x1149`.
- ES: `MT@` begins at `0x114C`.

DE/IT/ES also contain two distinct trailing strings after `String_Space`: `-<LF>@` followed by `@`. The three `<ROUTE>/<WATASHI>/<KOKO_WA>` handler routines point to the final shared `@`; the `-<LF>@` string is separate dummied data.

## `CheckDict`

English has the legacy diacritic path. All four localized western ROMs instead route bytes `$e4` and `$e5` directly to the normal placement path.

DE/IT/ES additionally contain this ten-byte dispatch at `0x1014`:

```asm
cp $1e
jp z, NextChar
cp $1d
jp z, PlaceHyphenSplit
```

FR does not contain these two extra dispatches.

DE/IT/ES also contain `PlaceHyphenSplit` at `0x10D4`:

```asm
ld [hl], '-'
jp LineFeedChar
```

## Battle-name grammar

EN/DE/ES print `EnemyText` before `wEnemyMonNickname`.

FR/IT reverse that order: the nickname is printed first and their localized enemy text is a suffix (`" ennemi"`, `" nemico"`).

The regular trainer-name path is also reordered in FR/IT: trainer name first, then a locale-specific separator byte, then class name. In the original Gold ROMs the separator byte is `$7f` in FR and `$f4` in IT.

## Paragraph handling

All four localized western ROMs preserve the byte at absolute WRAM address `$c506` around the paragraph clear operation. English does not. The semantic WRAM label remains provisional until the WRAM map is reconstructed; source should preserve the address-derived behavior rather than invent a name.

## Diacritic routine

The English `Diacritic` implementation occupies 11 bytes after `Text_WaitBGMap`. In DE/FR/IT/ES this collapses to a one-byte `ret`, for a net `-10` bytes. This matches the localized `CheckDict` direct-placement behavior.

## Size reconciliation

After correcting the inline strings and weekday blocks, the remaining code-size deltas versus EN are:

| Release | Code-only delta | Explained by verified structural differences |
| --- | ---: | --- |
| DE | +12 | CheckDict +12, hyphen routine +5, Paragraph +5, Diacritic -10 |
| FR | -6 | CheckDict +2, Paragraph +5, Diacritic -10, battle/trainer grammar -3 |
| IT | +9 | CheckDict +12, hyphen routine +5, Paragraph +5, Diacritic -10, battle/trainer grammar -3 |
| ES | +12 | CheckDict +12, hyphen routine +5, Paragraph +5, Diacritic -10 |

The equations close exactly, so all western text-module size differences are now accounted for structurally or as verified localized data.

## Validation

- `tests/test_bank00_western_text_strings.py` locks the inline and weekday string bytes.
- `tests/test_bank00_western_text_variants.py` locks the extra control dispatch, direct diacritic placement, hyphen routine, enemy-name grammar, and localized paragraph prologue.
- `tools/map_bank00_text_symbols.py` generates candidate cross-version symbol addresses; repeated identical routines are intentionally marked as candidates until semantic control-flow audit confirms them.
