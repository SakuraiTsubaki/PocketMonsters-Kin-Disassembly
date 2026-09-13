# Bank 00 semantic module map

Bank `00` (`0x0000–0x3FFF`) is being reconstructed as semantic ROM0/home modules rather than as an opaque binary bank.

## Method

- English Gold is used as the semantic reference because the public `pret/pokegold` symbols identify ROM0 function/module boundaries.
- All addresses recorded for this project are verified against the eight local read-only Gold reference ROMs.
- Cross-release address projection uses exact matching blocks where possible. Confidence is recorded per boundary in `module_map.csv`.
- The public disassembly is a naming/structure cross-check only; this repository tracks its own ROM baselines and release-specific differences.

## Current result

The `0x0150–0x3FFF` portion of Bank 00 is divided into **52 semantic modules**, from `vblank` through `audio`.

Cross-release exact-byte alignment against English Bank 00 finds the following total matching coverage:

| Release | Matching bytes | Coverage |
| --- | ---: | ---: |
| Japanese Rev 0 | 13,915 | 84.93% |
| Japanese Rev A | 13,914 | 84.92% |
| Korean | 13,209 | 80.62% |
| German | 15,441 | 94.24% |
| French | 15,361 | 93.76% |
| Italian | 15,406 | 94.03% |
| Spanish | 15,322 | 93.52% |

For the **52 module starts**:

- German / French / Italian / Spanish: **52/52 exact**
- Japanese Rev 0 / Rev A: **51/52 exact**, `names` inferred from the same relocation delta on both sides
- Korean: **51/52 exact**, `text` mapped from the immediately preceding exact block and requires manual confirmation

The complete address table is in `module_map.csv`.

## Major relocation examples

| Module | JP Rev 0 | KR | EN | DE | FR | IT | ES |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `text` | `0x0EC1` | `~0x0F0D` | `0x0EEF` | `0x0EEF` | `0x0EEF` | `0x0EEF` | `0x0EEF` |
| `video` | `0x142D` | `0x153F` | `0x1458` | `0x147C` | `0x1461` | `0x1476` | `0x1475` |
| `map` | `0x1F0A` | `0x1FBA` | `0x1F5D` | `0x1F8A` | `0x1F6F` | `0x1F82` | `0x1F81` |
| `names` | `~0x3550` | `0x35C3` | `0x35EE` | `0x35E5` | `0x3599` | `0x35DD` | `0x35AB` |
| `audio` | `0x3C70` | `0x3D1A` | `0x3D4F` | `0x3D46` | `0x3CDE` | `0x3D3E` | `0x3CF0` |

The relocations show why a single fixed-address Bank 00 source cannot represent every release without layout-aware build definitions.

## Reconstruction order

The working order is the physical Bank 00 order:

`vblank → delay → time_palettes → fade → lcd → time → init → serial → joypad → decompress → palettes → gfx → text → video → map_objects → sine → movement → menu → printer → game_time → map → farcall → predef → window → flag → sprite_updates → string → region → item → random → sram → call_regs → clear_sprites → copy → copy_tilemap → copy_name → array → math → print_text → queue_script → compare → tilemap → pokedex_flags → names → scrolling_menu → stone_queue → trainers → pokemon → print_bcd → battle → sprite_anims → audio`.

Each module moves through:

1. boundary verified per release;
2. function/data boundaries mapped;
3. editable RGBDS source reconstructed;
4. release-specific differences represented explicitly;
5. module bytes compared against all applicable reference ROMs;
6. status marked byte-perfect only after all bytes in that module are accounted for.

`module_status.csv` is the module-level ledger for this process.
