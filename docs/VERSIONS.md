# Version Coverage

The supplied Pokémon Gold / Pocket Monsters Kin ROM set is now locally fingerprinted. ROM binaries remain local/read-only and are not committed.

| Target ID | Region | Language | Revision / release | Size / banks | SHA-1 | Local state |
| --- | --- | --- | --- | --- | --- | --- |
| `jpn-gold-rev0` | Japan | Japanese | Rev.0 | 1 MiB / 64 | `8814f1039450a5d3684b1389f588ccd7ee7c3436` | Fingerprinted; known external identity matched |
| `jpn-gold-rev1` | Japan | Japanese | Rev.1 / Rev A | 1 MiB / 64 | `a222402235d484ee8e39f3f31bae57cf13daf585` | Fingerprinted; known external identity matched |
| `usa-eur-gold` | USA / Europe | English | retail | 2 MiB / 128 | `d8b8a3600a465308c9953dfa04f0081c05bdcb94` | Fingerprinted |
| `deu-gold` | Germany | German | retail | 2 MiB / 128 | `9254195d461ea942eaaa08cc4b83de3cf82aea0d` | Fingerprinted |
| `fra-gold` | France | French | retail | 2 MiB / 128 | `c147c0d8c2b71b7628a7233436f5c052b5b17081` | Fingerprinted |
| `ita-gold` | Italy | Italian | retail | 2 MiB / 128 | `032608fe8947b627584a4a0eccc7bf9ad3588426` | Fingerprinted |
| `esp-gold` | Spain | Spanish | retail | 2 MiB / 128 | `162ea54c6a3cff374642e6dd842f9bffac847e7b` | Fingerprinted |
| `kor-gold` | Korea | Korean | retail | 2 MiB / 128 | `c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65` | Fingerprinted |

Header and global cartridge checksums validate for all eight supplied images. SHA-256 values and the Japanese Rev.0/Rev.A byte-difference summary are recorded in `manifests/rom_inventory_2026-09-16.json`.

## Current reconstruction targets

Direct bank-by-bank source reconstruction starts with `jpn-gold-rev0` and `jpn-gold-rev1`. They remain independent targets: identical ranges may be shared only after byte identity is demonstrated; revision-specific bytes must remain explicit.

The other six supplied regional/language images are retained as separate comparison targets and are not assumed to share layout, bank contents, labels, or source boundaries with the Japanese images.

## External identity cross-check

The Japanese SHA-1 identities also match the external references already recorded for this repository:

- https://github.com/Narishma-gb/pokesilver
- https://tasvideos.org/Games/294/Versions/List

Local inspection supersedes the previous "local ROM match pending" state for the two Japanese targets.
