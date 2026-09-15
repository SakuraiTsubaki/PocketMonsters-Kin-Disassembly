# Project Status

## Current stage

**Active full-scope disassembly — dual Japanese revision baseline committed, Bank 00 reconstruction started, all Generation II workstreams active**

The repository is ROM-grounded. Original ROM binaries remain local/read-only and excluded from Git; reproducible source, manifests, analysis, and verification metadata are committed. Bank 00 is the current direct source-reconstruction front, while full-ROM inventory/classification proceeds in parallel across every major Generation II subsystem.

| Area | Status |
| --- | --- |
| Version/revision inventory | 8 supplied Gold ROMs fingerprinted; Japanese Rev 0 / Rev A identities locally verified; Korean and western targets retained separately |
| ROM / bank / section mapping | Japanese 64-bank baselines committed for both revisions; all 8 ROM sizes/bank counts recorded; whole-ROM classification active |
| Code reconstruction | Bank 00 reset/RST/interrupt vectors + cartridge entry reconstructed as RGBDS source; control-flow expansion active |
| Revision analysis | Rev 0 vs Rev A: 10,841 differing bytes, 426 contiguous ranges, 10 affected banks |
| Data reconstruction | Full-ROM table/structure inventory and pointer classification active; source replacement follows verified boundaries |
| Scripts / events / flags | Inventory and classification active |
| Graphics / sprites / tiles / palettes / fonts / UI | Inventory and classification active |
| Audio / music / SFX / cries / radio | Inventory and classification active |
| Maps / world / encounters | Map, tileset, collision, warp, object and encounter inventory active |
| Battle / field / time / breeding / Pokégear systems | Cross-bank subsystem mapping active |
| Link / trade / battle / Time Capsule | Protocol and data-conversion mapping active |
| Localization / regional comparison | Japanese, western and Korean technical comparison active |
| Unused / debug / bugs / revision fixes | Inventory and evidence tracking active |
| Generation I / Kanto comparison | Cross-generation mapping active |
| Build / matching verification | Reconstructed Bank 00 vector/entry bytes audited against both ROMs; exact-match path retained |
| Generation II full-scope tracker | All workstreams active; see `manifests/workstreams.json` |

## Completed in current pass

1. Fingerprinted all eight supplied Gold ROMs and validated header/global checksums.
2. Generated and committed complete 64-bank INCBIN baselines for Japanese Rev 0 and Rev A.
3. Added dual-revision build targets (`make rev0`, `make reva`).
4. Diffed the two Japanese revisions and identified affected banks: `00 04 05 09 0A 0F 14 21 23 24`.
5. Reconstructed the first 260 bytes of Bank 00 vectors/entry as RGBDS source and corrected them against ROM bytes plus an independent public Gold/Silver disassembly cross-check.
6. Activated parallel full-scope Generation II workstreams for data, maps, scripts/events, systems, graphics, audio, text/localization, communications, unused/debug material, bugs, and cross-generation comparison.

## Immediate next milestone

Continue Bank $00 from `$0150` (VBlank path), identify code/data boundaries and stable labels, and replace each verified INCBIN slice while preserving exact-match reconstruction for both Japanese revisions. In parallel, continue whole-ROM classification so later banks can move directly from inventory to verified source reconstruction without collapsing regional/revision differences.
