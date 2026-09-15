; Pocket Monsters Kin (Japan) — Bank 00 reset/RST/interrupt/header reconstruction.
;
; Scope: Japanese Rev.0 / Rev.A only.
; Provenance: recovered from this repository's preserved ROM-derived work
; (commit 6c42951a69d9f9bbe290992a7e888790136f288f), then reduced to the
; Japanese/common path for the clean restart.
;
; Byte-for-byte matching remains pending until the local reference ROMs are
; mounted again. Do not treat unresolved external symbols as reconstructed yet.

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

SECTION "rst18", ROM0[$0018]
    rst $38

SECTION "rst20", ROM0[$0020]
    rst $38

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

SECTION "rst38", ROM0[$0038]
    rst $38

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

; $0104..$014f is cartridge-header space. Release-specific Nintendo-logo,
; cartridge metadata, revision, and checksum bytes are emitted/patched by the
; eventual matching build pipeline.
    ds $0150 - @, $00
