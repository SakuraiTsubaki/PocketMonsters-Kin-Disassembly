; Pocket Monsters Kin disassembly entry point.
; Japanese Rev 0 is the default build; define REV_A for Japanese Rev A.

IF DEF(REV_A)
    INCLUDE "src/jp/rev_a/banks.asm"
ELSE
    INCLUDE "src/jp/rev0/banks.asm"
ENDC
