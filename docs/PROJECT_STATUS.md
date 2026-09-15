# Project Status

## Current stage

**ROM-grounded Bank 00 analysis active — first exact-matched source replacement pending**

The repository's original exact-match workflow remains authoritative: retail ROMs stay local/read-only, `src/banks.asm` is generated locally and ignored, unknown ranges remain `INCBIN`, and reconstructed source is promoted only after revision-scoped byte-identical verification.

| Area | Status |
| --- | --- |
| Version/revision inventory | 8 supplied Gold ROMs locally fingerprinted; Japanese Rev.0 / Rev.1 match the registered identities |
| ROM / bank / section mapping | 16 KiB bank inventory available from local inspection; Japanese Bank 00 fingerprints and revision differences recorded |
| Code reconstruction | Bank 00 reset/RST/interrupt/entry bytes decoded as **Observed**; committed exact-matched source replacement still pending |
| Revision analysis | Japanese Bank 00 differs at `014C–014F` and `3C6B`; whole-ROM Rev.0/Rev.1 diff: 10,841 bytes in 426 contiguous ranges across 10 banks |
| Data reconstruction | Not started |
| Scripts / events | Not started |
| Graphics / assets | Not started |
| Audio / resources | Not started |
| Maps / world data | Not started |
| Build / matching verification | Baseline tooling and RGBDS version pin present; first reconstructed slice still requires RGBDS assemble/link + `tools/verify_match.py` |

## Completed in the current ROM-grounded pass

1. Fingerprinted all eight supplied Gold ROMs without modifying them.
2. Confirmed valid cartridge header and global checksums for all eight supplied images.
3. Locally matched Japanese Rev.0 and Rev.1 to the identities already registered in `docs/VERSIONS.md`.
4. Measured the Japanese whole-ROM revision difference: 10,841 differing bytes, 426 contiguous ranges, affected banks `00 04 05 09 0A 0F 14 21 23 24`.
5. Measured Bank 00 independently for both revisions and decoded the shared reset/RST/interrupt/entry instructions directly from ROM bytes.
6. Recorded the evidence in `analysis/banks/bank00.md` and machine-readable ROM identities in `manifests/rom_inventory_2026-09-16.json`.

## Immediate milestone

1. Generate the ignored local `src/banks.asm` baseline from `jpn-gold-rev0` with the existing bootstrap tool.
2. Replace only the verified Bank 00 vector/entry ranges.
3. Assemble/link with the pinned RGBDS version and require a byte-identical result.
4. Repeat independently against `jpn-gold-rev1`.
5. Only after both pass, promote the reconstructed range to **Matched** and continue from `$0150`.
