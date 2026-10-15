# Gold RandomRange reconstruction

All eight SHA-256-gated Gold releases contain the same complete 26-byte control-flow shape immediately after `BattleRandom`. The routine accepts a nonzero exclusive upper bound in A, computes the incomplete high-tail size, rejects random samples that fall in that tail, then calls the release-specific `SimpleDivide`. This is rejection sampling, so modulo reduction does not favor lower outputs.

Japanese rev0/rev1 place it at `$3083`; Korean at `$3160`; English at `$30c7`; German `$30f4`; Spanish `$30eb`; French `$30d9`; Italian `$30ec`. Each report binds both calls to that release's verified `Random` and discovered `SimpleDivide`; every Gold build reads `hRandomAdd=$ffe3`.

Naming and semantics follow `pret/pokegold@ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`, `home/random.asm`. No ROM bytes are published.
