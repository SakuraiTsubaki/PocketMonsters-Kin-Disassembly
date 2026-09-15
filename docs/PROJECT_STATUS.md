# Project Status

## Current stage

**Disassembly started — Japanese Kin Bank 00**

The clean baseline has moved into game-specific source reconstruction. Current work is intentionally scoped to **Pocket Monsters Kin (Japan)** before regional branches are reintroduced.

| Area | Status |
| --- | --- |
| Version/revision inventory | In progress — Japanese Rev.0 / Rev.A evidence restored from preserved project history; local ROM re-verification pending |
| ROM / bank / section mapping | In progress — 1 MiB / 64-bank baseline and Rev.0↔Rev.A changed-bank map restored |
| Code reconstruction | Started — Bank 00 reset/RST/interrupt/header, VBlank, frame-delay, and startup/init paths reconstructed |
| Data reconstruction | Not started in clean tree |
| Scripts / events | Not started in clean tree |
| Graphics / assets | Not started in clean tree |
| Audio / resources | Not started in clean tree |
| Maps / world data | Not started in clean tree |
| Build / matching verification | Pending — reference ROMs are not currently mounted in the active workspace |

## Active source files

- `asm/home/header.asm`
- `asm/home/vblank.asm`
- `asm/home/delay.asm`
- `asm/home/init.asm`
- `manifests/rom_baselines.json`

## Evidence policy for the restart

Preserved commits from this repository may be used as **project-owned historical evidence**, but old directory trees are not restored wholesale. Each module is reintroduced deliberately into the clean structure, scoped to the target currently being reconstructed, and remains pending byte-for-byte matching until the corresponding local ROM is available again.

Next milestone: continue Japanese Bank 00 through LCD/time/serial/joypad and establish a minimal assemblable ROM0 skeleton before expanding into later home modules.
