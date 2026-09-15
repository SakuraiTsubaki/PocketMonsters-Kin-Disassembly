# Version Coverage

The clean baseline now tracks the two known Japanese retail revisions of **Pocket Monsters Kin** as distinct targets.

| Target ID | Region | Language | Revision / release | Hashes | Status |
| --- | --- | --- | --- | --- | --- |
| `jpn-gold-rev0` | Japan | Japanese | Rev.0 | SHA-1 `8814f1039450a5d3684b1389f588ccd7ee7c3436`; MD5 `85be569fe89f58c40f60480313314c67` | External reference identified; local ROM match pending |
| `jpn-gold-rev1` | Japan | Japanese | Rev.1 / Rev A | SHA-1 `a222402235d484ee8e39f3f31bae57cf13daf585`; MD5 `79aece8a042e4fa57aba9455c4d21a97` | External reference identified; local ROM match pending |

## Verification state

These hashes are independently cross-referenced against the Japanese Gold/Silver disassembly maintained by Narishma-gb and the TASVideos game-version database. They are recorded as **external-reference** identities until a locally supplied ROM dump is inspected and matches one of the registered hashes.

Reference sources:

- https://github.com/Narishma-gb/pokesilver
- https://tasvideos.org/Games/294/Versions/List

Run `python3 tools/inspect_rom.py <local-rom.gbc> --json out/rom-report.json` to fingerprint a local dump without modifying it. The inspector also records cartridge-header metadata and per-16 KiB bank hashes.

Do not infer equivalence from title or appearance alone. Rev.0 and Rev.1 remain separate reconstruction targets until their differences are mapped explicitly.
