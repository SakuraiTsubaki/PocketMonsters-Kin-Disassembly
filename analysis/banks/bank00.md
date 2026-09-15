# Bank 00 — Reconstruction Log

## Address domain

- ROM file range: `0x000000–0x003FFF`
- CPU-visible range: `0x0000–0x3FFF` (`ROM0`)
- Size: `0x4000` bytes
- Targets: `jpn-gold-rev0`, `jpn-gold-rev1`

Rev.0 and Rev.1 must be inspected independently. A symbol or range proven in one revision is not automatically accepted for the other.

## Fixed hardware-defined landmarks

These addresses come from the Game Boy cartridge/CPU memory layout and may be used before game-specific labels are established:

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
| `0000–003F` | pending | pending | RST/vector region | hardware layout + ROM inspection required | queued |
| `0040–0067` | pending | pending | interrupt vectors | hardware layout + ROM inspection required | queued |
| `0068–00FF` | pending | pending | game code/data | ROM inspection required | queued |
| `0100–014F` | pending | pending | entry + cartridge header | hardware/header layout + ROM inspection | queued |
| `0150–3FFF` | pending | pending | game code/data | ROM inspection required | queued |

No game-specific symbol names are considered verified in this log yet.
