# Project Status

## Current stage

**RGBDS INCBIN baseline active — Bank 00 opened**

The repository has moved beyond initial setup. A local-ROM-only, byte-identical RGBDS reconstruction pipeline is committed and the first bank reconstruction log is open. Original ROM binaries remain excluded from Git.

| Area | Status |
| --- | --- |
| Version/revision inventory | Japanese Rev.0 / Rev.1 external identities recorded; local hash match pending |
| ROM / bank / section mapping | 16 KiB bank inventory tooling ready; Bank 00 log opened |
| Code reconstruction | Bank 00 queued from reset/interrupt/header-adjacent code outward |
| Data reconstruction | Not started |
| Scripts / events | Not started |
| Graphics / assets | Not started |
| Audio / resources | Not started |
| Maps / world data | Not started |
| Build / matching verification | RGBDS INCBIN build + byte-for-byte verifier committed; local execution pending |

## Immediate milestone

1. Fingerprint local `jpn-gold-rev0` and `jpn-gold-rev1` dumps.
2. Generate the complete per-bank INCBIN baseline for each revision.
3. Confirm byte-identical rebuilds.
4. Diff Bank 00 across revisions.
5. Replace verified Bank 00 ranges with reconstructed RGBDS source while preserving exact matches.
