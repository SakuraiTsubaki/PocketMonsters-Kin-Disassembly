; Shared Bank 00 text-engine routines used by the Japanese, Korean, and
; western Gold families. Family-specific box drawing, dictionary dispatch,
; localized substitution data, scrolling, and command-table differences live
; in jp_variants.asm, kr_variants.asm, western_variants.asm, and locale files.

RadioTerminator::
	ld hl, .stop
	ret
.stop:
	text_end

PrintText::
	call SetUpTextbox
	; fallthrough

PrintTextboxText::
	bccoord TEXTBOX_INNERX, TEXTBOX_INNERY
	call PrintTextboxTextAt
	ret

SetUpTextbox::
	push hl
	call SpeechTextbox
	call UpdateSprites
	call ApplyTilemap
	pop hl
	ret

PlaceString::
	push hl
	; fallthrough

PlaceNextChar::
	ld a, [de]
	cp '@'
	jr nz, CheckDict
	ld b, h
	ld c, l
	pop hl
	ret

DummyChar:: ; unreferenced
	pop de
	; fallthrough

NextChar::
	inc de
	jp PlaceNextChar

MACRO text_print_name
	push de
	ld de, \1
	jp PlaceCommandCharacter
ENDM

PrintMomsName:   text_print_name wMomsName
PrintPlayerName: text_print_name wPlayerName
PrintRivalName:  text_print_name wRivalName
PrintRedsName:   text_print_name wRedsName
PrintGreensName: text_print_name wGreensName

PlaceMoveTargetsName::
	ldh a, [hBattleTurn]
	xor 1
	jr PlaceBattlersName

PlaceMoveUsersName::
	ldh a, [hBattleTurn]
	; fallthrough into the family-specific PlaceBattlersName implementation

PlaceCommandCharacter::
; Family-specific code selects DE before entering here.
	call PlaceString
	ld h, b
	ld l, c
	pop de
	jp NextChar

NextLineChar::
	pop hl
	ld bc, SCREEN_WIDTH * 2
	add hl, bc
	push hl
	jp NextChar

LineChar::
	pop hl
	hlcoord TEXTBOX_INNERX, TEXTBOX_INNERY + 2
	push hl
	jp NextChar

ContText::
	push de
	ld de, .cont
	ld b, h
	ld c, l
	call PlaceString
	ld h, b
	ld l, c
	pop de
	jp NextChar
.cont:
	db "<_CONT>@"

DoneText::
	pop hl
	ld de, .stop
	dec de
	ret
.stop:
	text_end

LoadBlinkingCursor::
	ld a, '▼'
	ldcoord_a 18, 17
	ret

UnloadBlinkingCursor::
	ld a, '─'
	ldcoord_a 18, 17
	ret

PokeFluteTerminator:: ; unreferenced
	ld hl, .stop
	ret
.stop:
	text_end

PrintTextboxTextAt::
	ld a, [wTextboxFlags]
	push af
	set TEXT_DELAY_F, a
	ld [wTextboxFlags], a
	call DoTextUntilTerminator
	pop af
	ld [wTextboxFlags], a
	ret

DoTextUntilTerminator::
	ld a, [hli]
	cp TX_END
	ret z
	call .TextCommand
	jr DoTextUntilTerminator

.TextCommand:
	push hl
	push bc
	ld c, a
	ld b, 0
	ld hl, TextCommands
	add hl, bc
	add hl, bc
	ld e, [hl]
	inc hl
	ld d, [hl]
	pop bc
	pop hl
	; Equivalent to jp de while preserving the LR35902 stack convention.
	push de
	ret
