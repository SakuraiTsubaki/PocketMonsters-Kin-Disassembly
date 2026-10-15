# Gold BattleRandom reconstruction

All eight catalogued Gold releases were SHA-256 gated and inspected at the byte immediately following the already verified `Random` routine. Each contains the complete 18-byte `BattleRandom` wrapper shape: save the current ROM bank, switch to bank `$0f`, call `_BattleRandom`, preserve A through WRAM, restore the original bank, reload A, and return.

Japanese rev0/rev1 are the origin reference at `$3071`, targeting `$0f:$6c31` with temporary `$cfd7`. The official Korean release is at `$314e`, targeting `$0f:$6c62` with temporary `$d09d`. English and most European releases target `$0f:$6c11` with temporary `$cfdd`; French targets `$0f:$6c13`. These release-specific operands are retained in the per-release reports rather than flattened into a false single build identity.

Names and semantics are corroborated by `pret/pokegold@ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`, `home/random.asm`. Reports retain identity, locations, operands, and code hashes without publishing ROM bytes. Language review order is Japanese, Korean, English, then the other official localizations.
