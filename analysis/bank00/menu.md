# Bank 00 — menu

The Bank 00 menu engine is structurally shared across the Gold family but contains real implementation and localization deltas. The retail ROMs are the byte-level authority; public disassemblies are used only to cross-check symbol names and control-flow meaning.

## Verified module ranges

| release | start | end exclusive | size | SHA-1 |
|---|---:|---:|---:|---|
| JP Rev 0 | `0x19FB` | `0x1E60` | 1125 | `3bc0bf4d03893c7667a31ca7b464ad2bb7d82e94` |
| JP Rev A | `0x19FB` | `0x1E60` | 1125 | `3bc0bf4d03893c7667a31ca7b464ad2bb7d82e94` |
| KR | `0x1AA1` | `0x1F10` | 1135 | `5a74c1b5bb2508897663e2044de081cf4df49c8a` |
| EN | `0x1A4E` | `0x1EB3` | 1125 | `6f567aa7c90117497e0e3d03ea3472270f76d679` |
| DE | `0x1A72` | `0x1EE0` | 1134 | `884280320a70e2bf82b59be95c5e3fa605f6f046` |
| FR | `0x1A57` | `0x1EC5` | 1134 | `29e975fdac88f14d414b4233ac4fa520e8493c97` |
| IT | `0x1A6C` | `0x1ED8` | 1132 | `18059c2fca2a4c40e60b4682354aa42500b4f870` |
| ES | `0x1A6B` | `0x1ED7` | 1132 | `0f9e2d86f3bd2714960d08b593e54a5883e10df0` |

Japanese Rev 0 and Rev A are byte-identical across the complete menu module.

## Korean implementation deltas

Korean Gold changes more than text:

- `RestoreTileBackup` is a banked `farcall_reg Function1fc5a0` wrapper.
- `PopWindow` switches to WRAM bank 3 while copying the menu-header stack frame, then returns to bank 1.
- `GetWindowStackTop` likewise reads the stacked pointer through WRAM bank 3.
- The Yes/No box is one row taller (`menu_coords 10, 4, 15, 9`) and does not set `STATICMENU_NO_TOP_SPACING`.
- Yes/No strings are `예` / `아니오` using the Korean two-byte character encoding.

The currently lifted Korean-specific executable fragments live in `src/home/menu/kr_variants.asm`.

## Localized western Yes/No behavior

DE/FR/IT/ES contain an eight-byte guard at module offset `0x205` that is absent from EN/JP/KR. It adjusts the requested left coordinate when the caller places a Yes/No box at x=14. The retail immediates are:

| locale | replacement x | right-edge width | data |
|---|---:|---:|---|
| DE | 13 | +6 | `JA` / `NEIN` |
| FR | 14 | +5 | `OUI` / `NON` |
| IT | 15 | +4 | `SÌ` / `NO` |
| ES | 15 | +4 | `SÍ` / `NO` |

English uses `YES` / `NO`; Japanese uses `はい` / `いいえ`.

This completely explains the western menu-size deltas relative to EN:

- DE/FR: +8 bytes guard +1 net string byte = +9 bytes.
- IT/ES: +8 bytes guard -1 net string byte = +7 bytes.

The family-conditioned source is in `src/home/menu/yes_no.asm` and the exact ROM data/signatures are locked by `tests/test_bank00_menu_locales.py`.

## Verification state

- Complete range/SHA-1 locks: `tests/test_bank00_menu_ranges.py`
- Localized Yes/No data and western position-guard checks: `tests/test_bank00_menu_locales.py`
- Korean banked window-stack fragments: reconstructed in source

The module remains `in_progress` until the remaining Korean-specific replacements/inserts are identified and the full semantic menu source is reconstructed. `byte_perfect_all_releases` remains open until an in-place RGBDS build is available.
