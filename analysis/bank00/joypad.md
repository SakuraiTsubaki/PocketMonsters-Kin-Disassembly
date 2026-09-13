# Bank 00 — joypad module

## Scope

This note tracks the `joypad` portion of Bank 00 across the eight Gold releases registered in this repository.

| Release | Range | Size | SHA-1 |
| --- | ---: | ---: | --- |
| JP Rev 0 | `08DE–0AD8` | 507 | `325254caf4eb6562f06e6ca4b8dc1cd5f98fbf87` |
| JP Rev A | `08DE–0AD8` | 507 | `325254caf4eb6562f06e6ca4b8dc1cd5f98fbf87` |
| KR | `08D2–0AE2` | 529 | `251d9f295e25cfe08fdf2acc9f769ab41944902a` |
| EN | `08DF–0AEF` | 529 | `e945de06fb5fde6f0a1d2e28fba8afb622019a08` |
| DE | `08DF–0AEF` | 529 | `07c9021c3afd4cf173f7218ca0e79747d3f9714b` |
| FR | `08DF–0AEF` | 529 | `e39b3edc066ff61727cbc1437995ab1082334a70` |
| IT | `08DF–0AEF` | 529 | `695423b4deef55426d800756b160d03a0ab9bb62` |
| ES | `08DF–0AEF` | 529 | `8c219f928e16f59aa2eed876cff4872d29b760f4` |

JP Rev 0 and Rev A are byte-identical for this module.

## Semantic split

The Japanese retail implementation is 22 bytes shorter than the Korean and western implementations. The length difference is accounted for by two later auto-input helpers:

1. **10-byte `$ff` duration handling block** in `GetJoypad.updateauto`.
   - KR/EN/DE/FR/IT/ES treat duration `$ff` as an indefinite hold and keep the stream pointer on the current input/duration pair.
   - JP stores the duration and advances directly to the next pair.

2. **12-byte auto-input dispatch block** in `PromptButton.wait_input`.
   - KR/EN/DE/FR/IT/ES check `wInputType` and can far-call `_DudeAutoInput_A` before entering the normal input loop.
   - JP enters the input loop directly.

The remainder is represented by shared semantic source. Binary hashes still differ among equal-length releases because absolute RAM/call targets and character-map constants relocate between regional builds.

## Source reconstruction

`src/home/joypad.asm` contains one shared implementation with `BUILD_JP` controlling the two Japanese omissions. No ROM binary data is committed.

## Verification

`tests/test_bank00_joypad.py` verifies the exact module range and SHA-1 for all eight reference ROMs, confirms JP Rev 0/Rev A identity, verifies the 507/529-byte family split, and checks the 22-byte structural delta.

Full byte-perfect status remains **not yet closed** until the repository has the complete RGBDS constants/macros/memory layout needed to assemble this source for every release and compare the resulting object/ROM bytes.
