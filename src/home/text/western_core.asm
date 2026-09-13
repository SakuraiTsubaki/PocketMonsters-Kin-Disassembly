; Western (EN/DE/FR/IT/ES) Bank 00 text rendering core.
; western_variants.asm must be included before this file so the localized
; Diacritic body can be selected correctly.

ClearBox::
	ld a, ' '
	ld de, SCREEN_WIDTH
.row
	push hl
	push bc
.col
	ld [hli], a
	dec c
	jr nz, .col
	pop bc
	pop hl
	add hl, de
	dec b
	jr nz, .row
	ret

ClearTilemap::
	hlcoord 0, 0
	ld a, ' '
	ld bc, wTilemapEnd - wTilemap
	call ByteFill
	ldh a, [rLCDC]
	bit B_LCDC_ENABLE, a
	ret z
	jp WaitBGMap

ClearScreen::
	ld a, PAL_BG_TEXT
	hlcoord 0, 0, wAttrmap
	ld bc, SCREEN_AREA
	call ByteFill
	jr ClearTilemap

Textbox::
	push bc
	push hl
	call TextboxBorder
	pop hl
	pop bc
	jr TextboxPalette

TextboxBorder::
	push hl
	ld a, '┌'
	ld [hli], a
	inc a
	call .PlaceChars
	inc a
	ld [hl], a
	pop hl

	ld de, SCREEN_WIDTH
	add hl, de
.row
	push hl
	ld a, '│'
	ld [hli], a
	ld a, ' '
	call .PlaceChars
	ld [hl], '│'
	pop hl
	ld de, SCREEN_WIDTH
	add hl, de
	dec b
	jr nz, .row

	ld a, '└'
	ld [hli], a
	ld a, '─'
	call .PlaceChars
	ld [hl], '┘'
	ret

.PlaceChars:
	ld d, c
.loop
	ld [hli], a
	dec d
	jr nz, .loop
	ret

TextboxPalette::
	ld de, wAttrmap - wTilemap
	add hl, de
	inc b
	inc b
	inc c
	inc c
	ld a, PAL_BG_TEXT
.col
	push bc
	push hl
.row
	ld [hli], a
	dec c
	jr nz, .row
	pop hl
	ld de, SCREEN_WIDTH
	add hl, de
	pop bc
	dec b
	jr nz, .col
	ret

SpeechTextbox::
	hlcoord TEXTBOX_X, TEXTBOX_Y
	ld b, TEXTBOX_INNERH
	ld c, TEXTBOX_INNERW
	jp Textbox

TextScroll::
	hlcoord TEXTBOX_X, TEXTBOX_INNERY
	decoord TEXTBOX_X, TEXTBOX_INNERY - 1
	ld bc, 3 * SCREEN_WIDTH
	call CopyBytes
	hlcoord TEXTBOX_INNERX, TEXTBOX_INNERY + 2
	ld a, ' '
	ld bc, TEXTBOX_INNERW
	call ByteFill
	ld c, 5
	call DelayFrames
	ret

Diacritic::
	western_diacritic_body
