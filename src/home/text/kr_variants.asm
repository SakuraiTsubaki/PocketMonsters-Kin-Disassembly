; Korean Gold Bank 00 text-engine implementation-family differences.
;
; These routines are reconstructed from the Korean retail ROM and are kept
; separate from the western/Japanese text paths. Exact ROM signatures are
; locked by tests/test_bank00_kr_text_engine.py and
; analysis/bank00/kr_text_engine_signatures.csv.
;
; Full module layout is still being assembled; this file intentionally
; contains the Korean-specific executable pieces that have exact ROM anchors.

; $0ECF
ClearBox::
; Fill a c*b box at hl with blank tiles through the Korean banked helper.
	farcall_reg _ClearBox
	ret

; $0EE6
ClearTilemap::
	call Function14a2
	call _ClearTilemap
	ret z
	jp WaitBGMap

; $0EF0
_ClearTilemap::
	hlcoord 0, 0
	ld a, ' '
	ld bc, wTilemapEnd - wTilemap
	call ByteFill

	ldh a, [rLCDC]
	bit B_LCDC_ENABLE, a
	ret

; $0F01
ClearScreen::
	ld a, PAL_BG_TEXT
; $0F03
ClearScreen2::
	hlcoord 0, 0, wAttrmap
	ld bc, SCREEN_AREA
	call ByteFill
	call _ClearTilemap
	ret z
	jp WaitBGMap2

; $0F12
Textbox::
	farcall_reg _Textbox
	ret

; $0F29
TextboxPalette::
	farcall_reg _TextboxPalette
	ret

; $0F40
SpeechTextbox::
	hlcoord TEXTBOX_X, TEXTBOX_Y
	ld b, TEXTBOX_INNERH
	ld c, TEXTBOX_INNERW
	jp Textbox

; This macro is inserted at the head of the Korean CheckDict routine.
; ROM $0F7E: FE 0C DA 29 12
MACRO KoreanDoubleByteDispatch
	cp $c
	jp c, DoubleByteChar
ENDM

; $1229
DoubleByteChar::
; A Korean glyph is encoded as two bytes. The first byte is the table number;
; the second byte selects the glyph within that table.
	ld b, a
	inc de
	ld a, [de]
	ld c, a
	farcall_reg PlaceDoubleByteChar
	call PrintLetterDelay
	jp NextChar

; $1249
TextScroll::
	farcall_reg _TextScroll
	ret

; $1470
SetStandardHangulFont::
	di
	ld a, BANK("WRAM 2")
	ldh [rWBK], a
	xor a
	ld [wInvertedHangulToggle], a
	ld a, $01
	ldh [rWBK], a
	ei
	ret

; $1480
SetInvertedHangulFont::
	di
	ld a, BANK("WRAM 2")
	ldh [rWBK], a
	ld a, $ff
	ld [wInvertedHangulToggle], a
	ld a, $01
	ldh [rWBK], a
	ei
	ret

; $1490
ToggleHangulFont::
; The retail source-equivalent label is anonymous/unknown; keep a semantic
; name while preserving the exact behavior and address map.
	di
	ld a, BANK("WRAM 2")
	ldh [rWBK], a
	ld a, [wInvertedHangulToggle]
	cpl
	ld [wInvertedHangulToggle], a
	ld a, $01
	ldh [rWBK], a
	ei
	ret

; $14A2
Function14a2::
	hlcoord 0, 0, wAttrmap
	ld bc, SCREEN_AREA
; $14A8
Function14a8::
	inc b
	inc c
	jr .start_loop

.loop
	res B_BG_BANK1, [hl]
	inc hl
.start_loop
	dec c
	jr nz, .loop
	dec b
	jr nz, .loop
	ret

; $14B6
Function14b6::
	push bc
	push hl
	ld bc, wAttrmap - wTilemap
	add hl, bc
	res B_BG_BANK1, [hl]
	pop hl
	pop bc
	ret

; $14C1
TrimUnusedHangulChars::
	farcall_reg _TrimUnusedHangulChars
	ret

; $14D8
FindNextEmptyHangulSlot::
	farcall_reg _FindNextEmptyHangulSlot
	ret

; $14EF
IsHangulCharDrawn::
	farcall_reg _IsHangulCharDrawn
	ret

; $1506
DrawHangulChar::
	push de
	farcall_reg _DrawHangulChar
	pop de
	ret

; $151F-$153E
PrepareVDMAData::
; Input:
;   b:de = source, two 1bpp character tiles
;   hl   = destination, two 2bpp tiles
; Korean text rendering duplicates each 1bpp plane into both 2bpp planes and
; XORs with the current inversion mask before VDMA upload.
	ldh a, [hROMBank]
	push af
	ld a, b
	rst Bankswitch

	di
	ld a, BANK("WRAM 2")
	ldh [rWBK], a
	ld a, [wInvertedHangulToggle]
	ld b, a

	ld c, 2 * TILE_1BPP_SIZE
.loop
	ld a, [de]
	inc de
	xor b
	ld [hli], a
	ld [hli], a
	dec c
	jr nz, .loop

	ld a, $01
	ldh [rWBK], a
	ei

	pop af
	rst Bankswitch
	ret
