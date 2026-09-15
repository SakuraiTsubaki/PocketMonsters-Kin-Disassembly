# Disassembly Baseline

This repository now starts from an **exact RGBDS INCBIN baseline** rather than from guessed labels or copied source.

## Stage 0 — local ROM fingerprint

The original ROM remains local and untracked. Run:

```sh
make ROM=/path/to/local-rom.gbc inspect
```

`tools/inspect_rom.py` records whole-file hashes, cartridge-header metadata, ROM/RAM size declarations, and SHA-1 for every 16 KiB ROM bank.

For Japanese Pocket Monsters Kin, Rev.0 and Rev.1 are independent targets. Never combine their bytes or inferred labels until a difference has been demonstrated and documented.

## Stage 1 — byte-identical INCBIN reconstruction

Run:

```sh
make ROM=/path/to/local-rom.gbc
```

`tools/bootstrap_incbin.py` generates `src/banks.asm` from the local ROM size. Bank 0 is emitted as `ROM0`; every remaining 16 KiB bank is emitted as a fixed `ROMX` section with an `INCBIN` slice. RGBDS then links the complete image and `tools/verify_match.py` requires a byte-for-byte match.

The generated `src/banks.asm` is a local bootstrap artifact, not the finished disassembly.

## Stage 2 — bank-by-bank reconstruction

Work proceeds from Bank 00 onward. For each bank:

1. Inventory code, pointer tables, text, graphics, maps, audio, padding, and unknown ranges.
2. Give a range a symbol only when its role is supported by data flow, references, or external evidence.
3. Replace the corresponding `INCBIN` range with reconstructed RGBDS source or a structured data include.
4. Rebuild immediately.
5. Keep the ROM byte-identical before moving to the next range.
6. Record revision-specific differences instead of normalizing them away.

Large banks may be split into smaller verified ranges. Unknown bytes remain as narrow `INCBIN` blocks until understood; this is preferable to speculative source.

## Stage 3 — structured extraction

Once a range is understood, move it into the appropriate long-term area (`engine/`, `data/`, `maps/`, `text/`, `gfx/`, `audio/`, etc.) with manifests and tests where useful. Extracted or recreated assets may be committed; the original ROM image may not.

## Verification rule

A change is not considered reconstructed merely because it assembles. The default completion condition is:

**source assembles + links + rebuilt bytes match the selected retail revision exactly.**
