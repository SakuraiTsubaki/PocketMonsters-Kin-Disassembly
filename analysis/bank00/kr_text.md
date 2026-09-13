# Bank 00 — Korean text engine checkpoint

This checkpoint records the Korean Gold Bank 00 text-engine data that is now independently locked against the read-only retail ROM.

## Module boundary

- ROM range: `0x0ECF–0x153E`
- End exclusive: `0x153F`
- Size: `1648` bytes
- SHA-1: `2ec906ea9a7412ee1d0b2e352d1b459c325b87b4`

The start at `0x0ECF` is the Korean `ClearBox` wrapper and is earlier than the first-pass text boundary. The module is structurally distinct from both Japanese and western builds.

## Verified Korean string block

`0x113B–0x1178` contains the command-substitution strings used by the text engine. Exact byte ranges and encodings are tracked in `kr_text_strings.csv` and reproduced in `src/home/text/locales/kr.asm`.

Confirmed strings include:

- `기술머신`
- `트레이너`
- `컴퓨터`
- `로켓단`
- `포켓몬`
- `적의 `
- Japanese leftover `こうげき`
- the shared `<PK><MN>`, `<PO><KE>`, space, and dummied terminator strings

## Verified weekday block

The weekday text at `0x1456–0x146F` is:

- `일`, `월`, `화`, `수`, `목`, `금`, `토`
- suffix `요일`

Each Hangul syllable is stored as a two-byte Korean character-table code; the terminator remains `$50`.

## Double-byte dispatch

The Korean `CheckDict` path contains the ROM-verified sequence at `0x0F7E`:

```text
FE 0C DA 29 12
```

This is `cp $0C` followed by `jp c,$1229`, proving that byte values below `$0C` are dispatched to the Korean double-byte character path rather than the normal single-byte dictionary/character path.

The complete Korean engine source is still being lifted. This checkpoint marks the localized strings, weekday strings, module boundary/hash, and double-byte dispatch boundary as exact; executable source reconstruction remains in progress.
