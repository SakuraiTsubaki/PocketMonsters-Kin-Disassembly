# Bank 00 — text engine survey

## Verified module ranges

| Release | Range | Size | SHA-1 |
| --- | ---: | ---: | --- |
| JP Rev 0 | `0E8F–142C` | 1438 | `a2dc9d244a4562cc63c9b2ba4b3f677bf6ef7e26` |
| JP Rev A | `0E8F–142C` | 1438 | `a2dc9d244a4562cc63c9b2ba4b3f677bf6ef7e26` |
| KR | `0ECF–153E` | 1648 | `2ec906ea9a7412ee1d0b2e352d1b459c325b87b4` |
| EN | `0EBD–1457` | 1435 | `1998e8bb8083f841c9a30f1f26afab5215e99c3b` |
| DE | `0EBD–147B` | 1471 | `bed1834b227ae260892ea5fe91aca6a0215d75c0` |
| FR | `0EBD–1460` | 1444 | `0f047ac3f8c6f9556f318eb864e19f8bebd34b7c` |
| IT | `0EBD–1475` | 1465 | `cb51c3ae89dcd41f275758fdf915721d83df4104` |
| ES | `0EBD–1474` | 1464 | `fa803e93e8c1aa66b056177046d7d8ded2442edd` |

JP Rev 0 and Rev A are byte-identical for this module.

## Reconstruction families

The Bank 00 text engine should not be forced into one monolithic source file. The verified ROMs fall into three implementation families:

### Japanese

The Japanese engine keeps the original single-byte Japanese text path and dakuten/handakuten handling. Its module begins at `0x0E8F` and is 1438 bytes.

### Korean

The Korean build is structurally different, not merely translated text. Important confirmed differences include:

- `ClearBox`, `Textbox`, `TextboxPalette`, `TextScroll`, and other operations are moved behind the Korean-only register-preserving `farcall_reg` mechanism.
- `CheckDict` has a Korean double-byte dispatch path (`DoubleByteChar`).
- `DoubleByteChar` consumes a second byte and calls the Korean double-byte glyph placement routine.
- Several embedded command strings are Korean (`기술머신`, `트레이너`, `컴퓨터`, `로켓단`, `포켓몬`, `적의`).
- The verified module starts at `0x0ECF`, not the earlier first-pass inferred `0x0EE1`. The boundary is proven by the byte expansion of `farcall_reg _ClearBox` at `0x0ECF`.

The Korean module is 1648 bytes.

### Western

EN/DE/FR/IT/ES share the western text-engine architecture. Their module begins at `0x0EBD`; module-size differences are primarily driven by localized embedded strings and relocation of later labels/calls. These five builds should therefore share western engine code with locale-specific string data.

## Planned source layout

```text
src/home/text.asm                 # implementation-family dispatcher
src/home/text/jp.asm              # Japanese engine
src/home/text/kr.asm              # Korean engine / double-byte path
src/home/text/western.asm         # shared western engine
src/home/text/locales/en.asm      # embedded EN strings
src/home/text/locales/de.asm      # embedded DE strings
src/home/text/locales/fr.asm      # embedded FR strings
src/home/text/locales/it.asm      # embedded IT strings
src/home/text/locales/es.asm      # embedded ES strings
```

This keeps executable behavior separate from localized text while still allowing byte-identical regional builds once constants, charmap, linker layout, and locale data are fully reconstructed.

## Verification

`tests/test_bank00_text_ranges.py` locks the exact start/end offsets, sizes, and SHA-1 values for all eight reference ROMs. Full source reconstruction is still in progress and is not marked byte-perfect until each family assembles against the reconstructed project constants/macros/layout and reproduces the verified bytes.
