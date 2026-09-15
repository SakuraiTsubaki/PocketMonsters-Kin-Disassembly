# Disassembly start — 2026-09-16

The repository has moved from scaffolding to ROM-grounded source reconstruction.

## Verified source inventory

Eight locally supplied Pokémon Gold / Pocket Monsters Kin ROM images were inspected without modification. ROM binaries are not committed.

- Japanese Rev 0: 1 MiB, 64 × 16 KiB banks, mask ROM version 0.
- Japanese Rev A: 1 MiB, 64 × 16 KiB banks, mask ROM version 1.
- English (USA/Europe), German, French, Italian, Spanish, Korean: 2 MiB each, 128 × 16 KiB banks.
- Header checksum and global checksum validate for all eight supplied images.

Exact SHA-1/SHA-256 values are recorded in `manifests/rom_inventory_2026-09-16.json`.

## Japanese revision comparison

Rev 0 and Rev A differ by 10,841 bytes grouped into 426 contiguous ranges. Differences occur in banks:

`00 04 05 09 0A 0F 14 21 23 24`

Bank $00 has only five differing bytes: `$014C-$014F` (revision/checksum header bytes) and `$3C6B` (`$52` in Rev 0, `$57` in Rev A).

## Source reconstruction now present

`src/common/bank00_vectors.asm` reconstructs the verified Bank $00 reset/RST/interrupt vectors and cartridge entry point as RGBDS source. These reconstructed regions total 260 bytes and were byte-checked against both Japanese revisions.

The remainder is represented by local-ROM `INCBIN` ranges so each revision keeps an exact matching baseline while source/data slices are progressively replaced.

- `make rev0` uses local `baserom.gbc`.
- `make reva` uses local `baserom_rev_a.gbc`.

ROM binaries remain excluded from Git.

## Next bank work

Continue Bank $00 from `$0150`, identify routine/data boundaries, assign stable labels, and replace corresponding INCBIN slices. Then proceed sequentially through banks $01-$3F while tracking the ten revision-sensitive banks explicitly.
