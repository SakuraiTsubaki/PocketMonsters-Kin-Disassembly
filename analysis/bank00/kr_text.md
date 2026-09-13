# Bank 00 — Korean text engine checkpoint

This checkpoint records the Korean Gold Bank 00 text engine that has been independently locked against the read-only Korean retail ROM.

## Module boundary

- ROM range: `0x0ECF–0x153E`
- End exclusive: `0x153F`
- Size: `1648` bytes
- SHA-1: `2ec906ea9a7412ee1d0b2e352d1b459c325b87b4`

The Korean module is structurally distinct from both Japanese and western builds. Its beginning is a banked `ClearBox` wrapper and its tail contains Korean-only Hangul font/cache/VDMA support.

## Embedded Korean string block

The verified substitution-string block begins at `0x113B`.

| Symbol | Address | Text |
| --- | ---: | --- |
| `TMCharText` | `0x113B` | `기술머신@` |
| `TrainerCharText` | `0x1144` | `트레이너@` |
| `PCCharText` | `0x114D` | `컴퓨터@` |
| `RocketCharText` | `0x1154` | `로켓단@` |
| `PlacePOKeText` | `0x115B` | `포켓몬@` |
| `KougekiText` | `0x1162` | `こうげき@` (Japanese leftover) |
| `SixDotsCharText` | `0x1167` | `<…><…>@` |
| `EnemyText` | `0x116A` | `적의 @` |
| `PlacePKMNText` | `0x1170` | `<PK><MN>@` |
| `PlacePOKEText` | `0x1173` | `<PO><KE>@` |
| `String_Space` | `0x1176` | ` @` |
| dummied alias text | `0x1178` | `@` |

Exact bytes are tracked in `kr_text_strings.csv`, reproduced as readable source in `src/home/text/locales/kr.asm`, and checked by `tests/test_bank00_kr_text.py`.

## Weekday block

The Korean weekday pointer table begins at `0x1448`; the strings are:

- `0x1456` `일@`
- `0x1459` `월@`
- `0x145C` `화@`
- `0x145F` `수@`
- `0x1462` `목@`
- `0x1465` `금@`
- `0x1468` `토@`
- `0x146B` `요일@`

Each Hangul syllable uses a two-byte codepoint: byte 1 selects one of tables `$01–$0B`, and byte 2 selects the glyph within that table. String terminator `$50` remains single-byte.

## Korean double-byte path

`CheckDict` contains the ROM-verified sequence at `0x0F7E`:

```text
FE 0C DA 29 12
```

This is `cp $0C` / `jp c, DoubleByteChar`, dispatching first bytes `$01–$0B` into the Korean two-byte glyph path.

`DoubleByteChar` is exactly `0x1229–0x1248` (32 bytes). It consumes the second byte, calls the banked `PlaceDoubleByteChar` helper through `farcall_reg`, applies the letter delay, then resumes `NextChar`.

## ROM0 banked text wrappers

The following Korean-only/relocated routines have exact signatures in `kr_text_engine_signatures.csv` and source in `src/home/text/kr_variants.asm`:

- `ClearBox` — `0x0ECF–0x0EE5`
- `Textbox` — `0x0F12–0x0F28`
- `TextboxPalette` — `0x0F29–0x0F3F`
- `CheckDict` double-byte gate — `0x0F7E–0x0F82`
- `DoubleByteChar` — `0x1229–0x1248`
- `TextScroll` — `0x1249–0x125F`

All 14 currently recorded Korean text-engine signatures were rechecked directly against `Pocket Monsters Geum (Korea).gbc` and match byte-for-byte.

## Hangul rendering tail

The Korean module contains a 207-byte Korean-only tail from `0x1470` through `0x153E`. SHA-1 of this exact tail is:

`20a94e480fc608b77cb19a8e944db7a7c4abfaa1`

Mapped routines:

- `SetStandardHangulFont` — `0x1470`
- `SetInvertedHangulFont` — `0x1480`
- inversion toggle routine — `0x1490`
- attrmap bank-bit clearing — `0x14A2` / `0x14A8`
- single-tile attrmap bank-bit clearing — `0x14B6`
- `TrimUnusedHangulChars` — `0x14C1`
- `FindNextEmptyHangulSlot` — `0x14D8`
- `IsHangulCharDrawn` — `0x14EF`
- `DrawHangulChar` — `0x1506`
- `PrepareVDMAData` — `0x151F–0x153E`

`PrepareVDMAData` switches to WRAM bank 2, XORs each 1bpp source byte with the current Hangul inversion mask, duplicates it into both 2bpp planes, restores WRAM/ROM banking, and returns.

## Reconstruction status

Exact and source-backed now:

- module boundary and complete-module SHA-1
- embedded Korean substitution strings
- weekday strings
- Korean two-byte dispatch boundary
- banked `ClearBox`/`Textbox`/`TextboxPalette` wrappers
- `DoubleByteChar`
- banked `TextScroll`
- Korean Hangul font inversion/cache helpers
- Hangul slot-management wrappers
- `PrepareVDMAData`

The remaining work inside this module is to merge these Korean-specific pieces with the shared text routines and command dispatcher into one contiguous buildable family source, then verify assembled bytes for the entire `0x0ECF–0x153E` range.