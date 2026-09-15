; Bank $00 vectors and cartridge entry point.
; Verified identical in Japanese Rev 0 and Rev A.

SECTION "ROM0 reset vector", ROM0[$0000]
    di
    jp $0100
    ds 4, 0

SECTION "ROM0 RST $08", ROM0[$0008]
    jp $2de3
    ds 5, 0

SECTION "ROM0 RST $10", ROM0[$0010]
    ldh [$ff9f], a
    ld [$2000], a
    ret
    ds 2, 0

SECTION "ROM0 RST $18", ROM0[$0018]
    rst $38
    ds 7, 0

SECTION "ROM0 RST $20", ROM0[$0020]
    rst $38
    ds 7, 0

SECTION "ROM0 RST $28", ROM0[$0028]
    push de
    ld e, a
    ld d, $00
    add hl, de
    add hl, hl
    ld a, [hli]
    ld h, [hl]
    ld l, a
    pop de
    jp hl
    ds 5, 0

SECTION "ROM0 RST $38", ROM0[$0038]
    rst $38
    ds 7, 0

SECTION "ROM0 VBlank vector", ROM0[$0040]
    jp $0150
    ds 5, 0

SECTION "ROM0 LCD vector", ROM0[$0048]
    jp $041b
    ds 5, 0

SECTION "ROM0 Timer vector", ROM0[$0050]
    reti
    ds 7, 0

SECTION "ROM0 Serial vector", ROM0[$0058]
    jp $06a9
    ds 5, 0

SECTION "ROM0 Joypad vector", ROM0[$0060]
    jp $08de
    ds $9d, 0

SECTION "ROM0 cartridge entry", ROM0[$0100]
    nop
    jp $05c5
