; Battle RNG wrapper reconstructed across all catalogued Gold releases.
; It switches to ROM bank $0f, calls the release-specific _BattleRandom,
; preserves A through a release-specific WRAM byte, restores the bank, and returns A.

BattleRandom::
    ldh a, [hROMBank]
    push af
    ld a, BANK(_BattleRandom)
    rst Bankswitch
    call _BattleRandom
    ld [wPredefHL + 1], a
    pop af
    rst Bankswitch
    ld a, [wPredefHL + 1]
    ret
