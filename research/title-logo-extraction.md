# Gold title-logo extraction

This unit preserves public PNG renderings and reproducible provenance for every
verified Gold-language ROM in the local release catalog. Japanese is the origin
reference; Korean follows it, then English and the four other official European
languages. No ROM bytes or compressed streams are committed.

## Locating the data

The title routine loads an LZ stream address into `HL`, a VRAM destination into
`DE`, and its ROM bank into `A` before calling the far decompressor. Converting
the banked address with `bank * 0x4000 + (address - 0x4000)` gives the file
offset recorded in each analysis report.

Japanese revisions 0 and 1 both point from loader code at `0x6469` to the same
combined 114-tile logo at `0xE45C8`. Korean loader code at `0x6355` points to a
distinct combined 127-tile logo at `0x98000`. Their decompressed hashes are
different, preserving the language-specific artwork rather than treating one
as a substitute for the other.

English and the other European versions use two streams. Every lower logo
starts at `0x98000`; localization changes its decompressed hash. The shared
upper Pokémon mark starts at `0x98476` in English and `0x98706` in German,
French, Italian, and Spanish because their lower compressed streams are longer.
All five upper streams decompress to the same 60-tile hash.

## Independent source check

The public `pret/pokegold` source at commit
`62388c7204e5d13aa05b4231e220b6760584d1b5` names the two English streams in
`gfx/misc.asm`, while `engine/movie/title.asm` documents their load order and
VRAM destinations. Converting `logo_bottom_gold.png` to Game Boy 2bpp (omitting
the eight trailing canvas-only blank tiles) exactly matches the 1,792
decompressed ROM bytes. Converting `logo_top_gold.png` exactly matches all 960
decompressed bytes. This byte-level comparison rejects unrelated valid LZ
streams that merely happen to have a plausible size.

## Reproduction

Run `tools/extract_gb_lz_2bpp.py` from `SakuraiTsubaki/Disassembly` with the ROM
SHA-256, source offset, and 20 tiles per row recorded in the corresponding JSON
report. The tool verifies the complete local ROM before reading, records hashes
of the compressed and decompressed data, and emits only a deterministic PNG and
metadata suitable for publication.
