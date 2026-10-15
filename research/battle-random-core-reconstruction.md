# Gold _BattleRandom core reconstruction

The target reached by the verified `BattleRandom` wrapper was decoded independently in all eight SHA-256-gated Gold releases. Every target is a 55-byte routine with the same complete control-flow shape. Non-link battles tail-jump to the release's verified `Random`; link battles consume one of ten shared bytes. At the stream boundary, all ten seeds are updated by `seed = (seed * 5 + 1) mod 256`, the count is reset, and the previously selected value remains in A.

Japanese rev0/rev1 use `$0f:$6c31`, link mode `$d03c`, count `$cbb7`, and seeds `$d0d5`. Korean uses `$0f:$6c62`, `$d0fd`, `$cbcb`, and `$d1a0`. Western releases use link mode `$d042`, count `$cbc3`, and seeds `$d0e3`; French relocates the routine to `$0f:$6c13`, while the others use `$0f:$6c11`.

The source naming and synchronization semantics are corroborated by `pret/pokegold@ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`, `engine/battle/core.asm`. Reports contain structural operands and hashes, not ROM bytes. Review order is Japanese, Korean, English, then the remaining official languages.
