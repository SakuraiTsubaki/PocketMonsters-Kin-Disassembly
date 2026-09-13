; Bank 00 reset/RST/interrupt/header reconstruction.
; Derived from all eight tracked Pocket Monsters Kin / Pokemon Gold baselines.
;
; BUILD_KR selects the Korean ROM0-specific RST timing routines.
; Other release-specific address differences are resolved by the final linker layout.

SECTION "rst0", ROM0[$0000]
ResetVector::
    di
    jp Start

SECTION "rst8", ROM0[$0008]
FarCall::
    jp FarCall_hl

SECTION "rst10", ROM0[$0010]
Bankswitch::
    ldh [hROMBank], a
    ld [rROMB], a
    ret

IF DEF(BUILD_KR)

SECTION "Korean rst18 timing", ROM0[$0018]
KoreanRST18TimingLoop::
.wait_not_mode0
    ldh a, [rSTAT]
    and $03
    jr z, .wait_not_mode0
.wait_mode0
    ldh a, [rSTAT]
    and $03
    jr nz, .wait_mode0
    ret

ELSE

SECTION "rst18", ROM0[$0018]
    rst $38

SECTION "rst20", ROM0[$0020]
    rst $38

ENDC

SECTION "rst28", ROM0[$0028]
JumpTable::
    push de
    ld e, a
    ld d, 0
    add hl, de
    add hl, de
    ld a, [hli]
    ld h, [hl]
    ld l, a
    pop de
    jp hl

IF DEF(BUILD_KR)

SECTION "Korean rst38 delay", ROM0[$0038]
KoreanRST38Delay::
    nop
    ld a, $39
.loop
    dec a
    jr nz, .loop
    ret

ELSE

SECTION "rst38", ROM0[$0038]
    rst $38

ENDC

SECTION "vblank", ROM0[$0040]
    jp VBlank

SECTION "lcd", ROM0[$0048]
    jp LCD

SECTION "timer", ROM0[$0050]
    reti

SECTION "serial", ROM0[$0058]
    jp Serial

SECTION "joypad", ROM0[$0060]
    jp Joypad

SECTION "Header", ROM0[$0100]
Start::
    nop
    jp _Start

; 0x0104..0x014f is cartridge-header space. The final build will patch
; release-specific Nintendo-logo/header/checksum fields deterministically.
    ds $0150 - @, $00
