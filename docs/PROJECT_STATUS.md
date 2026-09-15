# Project Status

## Current stage

**Active disassembly — dual Japanese revision baseline committed, Bank 00 reconstruction started**

The repository is now ROM-grounded. Original ROM binaries remain local/read-only and excluded from Git; reproducible source, manifests, analysis, and verification metadata are committed.

| Area | Status |
| --- | --- |
| Version/revision inventory | 8 supplied Gold ROMs fingerprinted; Japanese Rev 0 / Rev A identities locally verified |
| ROM / bank / section mapping | Japanese 64-bank baselines committed for both revisions; all 8 ROM sizes/bank counts recorded |
| Code reconstruction | Bank 00 reset/RST/interrupt vectors + cartridge entry reconstructed as RGBDS source |
| Revision analysis | Rev 0 vs Rev A: 10,841 differing bytes, 426 contiguous ranges, 10 affected banks |
| Data reconstruction | Not started |
| Scripts / events | Not started |
| Graphics / assets | Not started |
| Audio / resources | Not started |
| Maps / world data | Not started |
| Build / matching verification | Reconstructed Bank 00 vector/entry bytes audited against both ROMs; full RGBDS rebuild awaits an environment with RGBDS installed |

## Completed in current pass

1. Fingerprinted all eight supplied Gold ROMs and validated header/global checksums.
2. Generated and committed complete 64-bank INCBIN baselines for Japanese Rev 0 and Rev A.
3. Added dual-revision build targets (`make rev0`, `make reva`).
4. Diffed the two Japanese revisions and identified affected banks: `00 04 05 09 0A 0F 14 21 23 24`.
5. Reconstructed the first 260 bytes of Bank 00 vectors/entry as RGBDS source and corrected them against ROM bytes plus an independent public Gold/Silver disassembly cross-check.

## Immediate next milestone

Continue Bank $00 from `$0150` (VBlank path), identify code/data boundaries and stable labels, then replace each verified INCBIN slice while preserving exact-match reconstruction for both Japanese revisions.
