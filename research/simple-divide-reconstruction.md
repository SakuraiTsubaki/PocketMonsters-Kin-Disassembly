# Gold SimpleDivide reconstruction

All eight SHA-256-gated Gold releases were inspected at the exact `SimpleDivide` target recorded by their verified `RandomRange`. Each contains the same complete nine-byte repeated-subtraction routine: input dividend A and nonzero divisor C; output quotient B and remainder A.

Japanese rev0/rev1 use `$3171`; Korean `$3253`; English `$31b5`; German `$31e2`; Spanish `$31d9`; French `$31c7`; Italian `$31da`. Every build has code hash `076069c0b328a081fe3c9743adb8359b5739d024cbe928ee03b1e57e97cf357a`.

Naming and semantics follow `pret/pokegold@ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`, `home/math.asm`. No ROM bytes are published.
