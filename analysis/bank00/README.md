# Bank 00 — cross-release first-pass survey

## Scope

This report compares ROM Bank `00` (`0x000000–0x003FFF`) across all eight Pocket Monsters Kin / Pokémon Gold reference releases currently tracked by the project:

- Japanese Rev 0
- Japanese Rev A
- Korean
- English (USA/Europe)
- German
- French
- Italian
- Spanish

The analysis is derived directly from the read-only reference ROMs. No ROM bytes are committed as standalone bank binaries.

## Bank hashes

| Release | SHA-1 | Entry jump | Game code | CGB | ROM size code |
| --- | --- | --- | --- | --- | --- |
| `jp-rev0` | `4f67b272f43a254d14fa1b1075a78167ab06ef49` | `0x05C5` | `AAUJ` | `0x80` | `0x05` |
| `jp-revA` | `8c9834794c7fa66fdb39dcbbbc8fc4b89936be81` | `0x05C5` | `AAUJ` | `0x80` | `0x05` |
| `kr` | `c4663c8a646657dcc0b96722f0976432958a2243` | `0x05CA` | `AAUK` | `0xC0` | `0x06` |
| `en` | `f8fc41c03e5260dfb9a0d9c17f116020608ab5d5` | `0x05C6` | `AAUE` | `0x80` | `0x06` |
| `de` | `414b7cbc2347aa7665be19f5fcbbe23132a808f7` | `0x05C6` | `AAUD` | `0x80` | `0x06` |
| `fr` | `8a7f9e3ad51cb058a863317e2a956760c642d3d6` | `0x05C6` | `AAUF` | `0x80` | `0x06` |
| `it` | `7d94545baea24182ec2f75f907f9f7d9988fd79b` | `0x05C6` | `AAUI` | `0x80` | `0x06` |
| `es` | `cdfe4549f5a04f113ce9a76e7ef6fa9741ac4e58` | `0x05C6` | `AAUS` | `0x80` | `0x06` |

## Direct byte comparison

At fixed offsets, **15,478 / 16,384 bytes vary across the eight releases**, leaving only **906 bytes identical at the same offsets in all eight**. This does **not** mean only those invariant bytes are shared semantically; localization and regional layout changes relocate otherwise-equivalent code/data, so address-aware reconstruction is required.

Japanese Rev 0 vs Rev A differs by only **5 bytes** in Bank 00:

| Offset | Rev 0 | Rev A | Meaning |
| --- | --- | --- | --- |
| `0x014C` | `00` | `01` | cartridge header version |
| `0x014D` | `48` | `47` | header checksum |
| `0x014E` | `8A` | `84` | global checksum high byte |
| `0x014F` | `70` | `60` | global checksum low byte |
| `0x3C6B` | `52` | `57` | non-header revision change; semantic identification pending |

## Reset / interrupt vector findings

The common vector structure matches the expected Generation II ROM0 organization: reset at `0x0000`, helper RST entries, hardware interrupt jumps, and the cartridge entry point at `0x0100`.

### Common across all eight releases

- `0x0000`: `di ; jp $0100`
- `0x0010`: ROM-bank switch helper bytes are identical
- `0x0028`: jump-table helper bytes are identical
- `0x0040`: VBlank vector jumps to `$0150`
- `0x0048`: LCD vector jumps to `$041B`
- `0x0050`: timer interrupt is `reti`

The FarCall, serial, joypad, and main-entry targets vary because the ROM0 layout differs by release.

### Korean-only low-level ROM0 behavior

Korean Gold differs structurally in the RST area:

```asm
; 0x0018..0x0024, Korean release
ldh a, [rSTAT]
and $03
jr z, .wait_not_mode0
ldh a, [rSTAT]
and $03
jr nz, .wait_mode0
ret
```

This occupies the `0x0018`/`0x0020` RST space that other tracked releases fill with trap-style `rst $38` entries.

Korean `0x0038` also contains a short delay loop instead of the trap byte used by the Japanese and western releases:

```asm
nop
ld a, $39
.loop
    dec a
    jr nz, .loop
ret
```

This is an important early indication that the Korean build has ROM0 timing/rendering support changes, not merely translated text or replacement font assets.

## Entry-point families

| Family | Entry instruction at `0x0100` | `_Start` target |
| --- | --- | --- |
| Japanese Rev 0 / Rev A | `nop ; jp` | `$05C5` |
| Korean | `nop ; jp` | `$05CA` |
| EN / DE / FR / IT / ES | `nop ; jp` | `$05C6` |

## Reference cross-check

The public `pret/pokegold` disassembly places reset/RST vectors, hardware interrupt vectors, and the cartridge entry in `home/header.asm`, then builds the remainder of ROM0 from `home/*.asm` modules. We use that only as a semantic cross-check; this project's addresses and release-specific behavior are verified against its own reference ROM set.

## Reconstruction decision

Bank 00 will be reconstructed as **shared semantic modules with release-specific layout/implementation branches**, not as one binary template with text substitutions. In particular:

1. Japanese Rev A is a small revision of the Japanese layout and should share almost all ROM0 source with Rev 0.
2. Western releases share an entry-point family but still differ substantially in localized data/layout.
3. Korean requires explicit ROM0-specific code paths for its low-level RST/timing behavior.
4. Address equivalence must be tracked symbolically; raw same-offset comparison is insufficient after the vector/header region.

## Status

**Bank 00: analysis in progress.** Vector/header structure and first cross-release differences are confirmed. Next substage is symbol/function boundary mapping through the rest of ROM0, followed by source reconstruction and per-release byte-perfect verification.
