# Release Matrix — Pocket Monsters Kin / Pokémon Gold

Started: 2026-09-14

This matrix is rebuilt from public sources only. A listed checksum is a public reference, not proof of local ROM possession or local byte-for-byte verification.

## Retail lineage

| Lineage | Market / language | Publicly reported identity | SHA-1 | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Origin | Japan / Japanese | Pocket Monsters Kin, Rev.0 | `8814f1039450a5d3684b1389f588ccd7ee7c3436` | Narishma-gb/pokesilver; TASVideos | Two public sources | `CROSS_VERIFIED` |
| Origin revision | Japan / Japanese | Pocket Monsters Kin, Rev.1 / Rev A | `a222402235d484ee8e39f3f31bae57cf13daf585` | Narishma-gb/pokesilver; TASVideos/Dorando | Multiple public sources | `CROSS_VERIFIED` |
| International | USA/Europe / English | Pokemon - Gold Version (USA, Europe) | `d8b8a3600a465308c9953dfa04f0081c05bdcb94` | pret/pokegold; TASVideos/Dorando | Multiple public sources | `CROSS_VERIFIED` |
| Localization | Germany / German | Pokemon - Goldene Edition | `9254195d461ea942eaaa08cc4b83de3cf82aea0d` | OpenRetro No-Intro import; Dorando | Two public catalogues | `CROSS_VERIFIED` |
| Localization | France / French | Pokemon - Version Or | `c147c0d8c2b71b7628a7233436f5c052b5b17081` | OpenRetro No-Intro import; Dorando | Two public catalogues | `CROSS_VERIFIED` |
| Localization | Italy / Italian | Pokemon - Versione Oro | `032608fe8947b627584a4a0eccc7bf9ad3588426` | OpenRetro No-Intro import; Dorando | Two public catalogues | `CROSS_VERIFIED` |
| Localization | Spain / Spanish | Pokemon - Edicion Oro | `162ea54c6a3cff374642e6dd842f9bffac847e7b` | OpenRetro No-Intro import; Dorando | Two public catalogues | `CROSS_VERIFIED` |
| Localization | Korea / Korean | Pocket Monsters Geum | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` | Narishma-gb/pokegold-kr; OpenRetro/Dorando | Multiple public sources | `CROSS_VERIFIED` |

## Non-retail / development references kept separate

| Identity | SHA-1 | Classification | Public source |
| --- | --- | --- | --- |
| MONSGD.COM (Debug Gold Rev.1) | `04943f02787e2df51429c3ce4de6a75cb414a14a` | Debug/development | Narishma-gb/pokesilver |
| Debug Gold Rev.1 with corrected header | `8fe02e26e5d836fe399b78ef417f64c62cc45dec` | Debug/development reconstruction identity | Narishma-gb/pokesilver |
| mons2_gld_ps3_debug.bin | `53783c57378122805c5b4859d19e1a224f02a1ed` | Debug/development | pret/pokegold |
| DMGAAUP0.J56.patch | `b8253b915ade89c784c71adfdb11cf60bc1f7b59` | Patch/development artifact | pret/pokegold |
| Space World material | see dedicated source project | Prototype/development | pret/pokegold-spaceworld |

## Sources used in this pass

- https://github.com/Narishma-gb/pokesilver
- https://github.com/pret/pokegold
- https://github.com/Narishma-gb/pokegold-kr
- https://tasvideos.org/Games/294/Versions/List
- https://openretro.org/gbc/pokemon-gold-version/edit
- https://dorando.emuverse.com/html/pocket-monsters-kin.html

## Unresolved census tasks

- Verify whether additional retail revisions exist for any localized Gold release.
- Record cartridge product codes, header version bytes, ROM/header checksums and board/cartridge variants per identity.
- Find region-specific manuals, boxes, official sites and release notices for every localization.
- Distinguish physical-market variants that share identical ROM bytes from distinct binary releases.
- Trace localization source projects/forks where no dedicated complete disassembly is currently known.

No row is `BYTE_VERIFIED` locally.