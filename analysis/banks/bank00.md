# Bank 00 — Reconstruction Log

## Address domain

- ROM file range: `0x000000–0x003FFF`
- CPU-visible range: `0x0000–0x3FFF` (`ROM0`)
- Size: `0x4000` bytes
- Targets: `jpn-gold-rev0`, `jpn-gold-rev1`

Rev.0 and Rev.1 are inspected independently. A symbol or range proven in one revision is not automatically accepted for the other.

## Local fingerprints

| Target | Bank 00 SHA-1 | Bank 00 SHA-256 |
| --- | --- | --- |
| `jpn-gold-rev0` | `4f67b272f43a254d14fa1b1075a78167ab06ef49` | `9b027ca15c252f77ac62534216e26c03a49cae3eddbc934c047cebe7c923974f` |
| `jpn-gold-rev1` | `8c9834794c7fa66fdb39dcbbbc8fc4b89936be81` | `533bfe1ce13009ab2d4f4ef165276d4c298202d3387d394b241b95ba9fb95eee` |

The two Bank 00 images differ at five bytes only: `0x014C–0x014F` and `0x3C6B`. At `0x3C6B`, Rev.0 contains `$52` and Rev.1 contains `$57`.

## Fixed hardware-defined landmarks

| CPU address | Role |
| --- | --- |
| `0x0000` | RST vector area begins |
| `0x0040` | VBlank interrupt vector |
| `0x0048` | LCD STAT interrupt vector |
| `0x0050` | Timer interrupt vector |
| `0x0058` | Serial interrupt vector |
| `0x0060` | Joypad interrupt vector |
| `0x0100` | Cartridge entry point |
| `0x0104–0x0133` | Nintendo logo field |
| `0x0134–0x014F` | Cartridge header fields |

Game-specific labels outside these hardware/header landmarks remain **unverified** until established from the selected ROM revision.

## Observed disassembly — shared Rev.0 / Rev.1 bytes

The following instructions are decoded directly from both supplied Japanese ROMs. This is **Observed** evidence; it is not yet promoted to **Matched** source until RGBDS assembles/links it and `tools/verify_match.py` confirms exact bytes.

| Address | Bytes | Instruction |
| --- | --- | --- |
| `$0000` | `F3` | `di` |
| `$0001` | `C3 00 01` | `jp $0100` |
| `$0008` | `C3 E3 2D` | `jp $2DE3` |
| `$0010` | `E0 9F` | `ldh [$FF9F], a` |
| `$0012` | `EA 00 20` | `ld [$2000], a` |
| `$0015` | `C9` | `ret` |
| `$0018` | `FF` | `rst $38` |
| `$0020` | `FF` | `rst $38` |
| `$0028` | `D5` | `push de` |
| `$0029` | `5F` | `ld e, a` |
| `$002A` | `16 00` | `ld d, $00` |
| `$002C` | `19` | `add hl, de` |
| `$002D` | `19` | `add hl, de` |
| `$002E` | `2A` | `ld a, [hli]` |
| `$002F` | `66` | `ld h, [hl]` |
| `$0030` | `6F` | `ld l, a` |
| `$0031` | `D1` | `pop de` |
| `$0032` | `E9` | `jp hl` |
| `$0038` | `FF` | `rst $38` |
| `$0040` | `C3 50 01` | `jp $0150` |
| `$0048` | `C3 1B 04` | `jp $041B` |
| `$0050` | `D9` | `reti` |
| `$0058` | `C3 A9 06` | `jp $06A9` |
| `$0060` | `C3 DE 08` | `jp $08DE` |
| `$0068–$00FF` | all `00` | zero-filled region |
| `$0100` | `00` | `nop` |
| `$0101` | `C3 C5 05` | `jp $05C5` |

## Bank 00 workflow

1. Fingerprint both Japanese retail revisions with `tools/inspect_rom.py`.
2. Compare Bank 00 SHA-1 and produce a byte-difference range list.
3. Split the local `INCBIN` only at verified boundaries.
4. Reconstruct reset/interrupt entry code first, followed by header-adjacent startup code.
5. Trace every cross-bank call/jump/pointer target before assigning semantic names.
6. Keep unknown ranges as narrow `INCBIN` blocks.
7. Rebuild and require byte-identical output after every replacement.

## Evidence ledger

| Range | Rev.0 | Rev.1 | Classification | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `0000–003F` | identical | identical | RST/vector region | direct ROM byte inspection and instruction decode | **Observed** |
| `0040–0067` | identical | identical | interrupt vectors | direct ROM byte inspection and instruction decode | **Observed** |
| `0068–00FF` | all zero | all zero | zero-filled region | direct ROM byte inspection | **Observed** |
| `0100–014F` | differs at `014C–014F` | differs at `014C–014F` | entry + cartridge header | direct ROM byte inspection + header layout | **Observed** |
| `0150–3FFF` | `$52` at `3C6B` | `$57` at `3C6B` | game code/data | bank-wide byte comparison | **Observed; classification pending** |

## Next source step

Generate the local ignored `src/banks.asm` baseline for one selected Japanese revision, replace only the verified vector/entry ranges, assemble with the pinned RGBDS version, and require a byte-identical result. Repeat independently for the other revision before promoting the range from **Observed** to **Matched**.
