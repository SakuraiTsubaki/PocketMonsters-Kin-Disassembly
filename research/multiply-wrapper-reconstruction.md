# Gold Multiply wrapper reconstruction

All eight verified Gold releases contain the complete 11-byte wrapper immediately after `SimpleDivide`. It preserves HL and BC, loads the release-specific bank 1 `_Multiply` target, invokes `RST $08` (`FarCall`), restores the registers, and returns. Japanese rev0/rev1 target `$01:$6ab0`; Korean `$01:$6898`; the five Western targets are retained per report.

The routine multiplies the three-byte `hMultiplicand` by `hMultiplier`, producing `hProduct`. Naming and macro expansion follow `pret/pokegold@ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`, `home/math.asm` and `macros/farcall.asm`. No ROM bytes are published.
