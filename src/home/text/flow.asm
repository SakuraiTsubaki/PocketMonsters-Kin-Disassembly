; Bank 00 text-flow control shared across families with explicit retail deltas.
; This file covers line/paragraph/continuation/prompt behavior; rendering and
; command-dispatch details remain in the family-specific files.

IF !DEF(BUILD_JP)
LineFeedChar::
	pop hl
	ld bc, SCREEN_WIDTH
	add hl, bc
	push hl
	jp NextChar
ENDC

Paragraph::
	push de

IF DEF(BUILD_DE) || DEF(BUILD_FR) || DEF(BUILD_IT) || DEF(BUILD_ES)
	; Localized western Gold preserves this retail WRAM byte across the clear.
	; The semantic name is intentionally not guessed yet.
	ld a, [$c506]
	push af
ENDC

	ld a, [wLinkMode]
	cp LINK_COLOSSEUM
	jr z, .linkbattle
	call LoadBlinkingCursor

.linkbattle
	call Text_WaitBGMap
	call PromptButton

IF DEF(BUILD_JP) || DEF(BUILD_KR)
	; JP/KR clear the full inner-height region starting one row higher.
	hlcoord TEXTBOX_INNERX, TEXTBOX_INNERY - 1
	lb bc, TEXTBOX_INNERH, TEXTBOX_INNERW
ELSE
	; Western builds clear the lower three text rows.
	hlcoord TEXTBOX_INNERX, TEXTBOX_INNERY
	lb bc, TEXTBOX_INNERH - 1, TEXTBOX_INNERW
ENDC
	call ClearBox

IF DEF(BUILD_DE) || DEF(BUILD_FR) || DEF(BUILD_IT) || DEF(BUILD_ES)
	pop af
	ld [$c506], a
ELSE
	call UnloadBlinkingCursor
ENDC

	ld c, 20
	call DelayFrames
	hlcoord TEXTBOX_INNERX, TEXTBOX_INNERY
	pop de
	jp NextChar

_ContText::
IF DEF(BUILD_JP)
	ld a, [wLinkMode]
	cp LINK_COLOSSEUM
	jr z, .communication
	call LoadBlinkingCursor
ELSE
	ld a, [wLinkMode]
	or a
	jr nz, .communication
	call LoadBlinkingCursor
ENDC

.communication
	call Text_WaitBGMap
	push de
	call PromptButton
	pop de

IF DEF(BUILD_JP)
	call UnloadBlinkingCursor
ELSE
	ld a, [wLinkMode]
	or a
	call z, UnloadBlinkingCursor
ENDC
	; fallthrough

_ContTextNoPause::
	push de
	call TextScroll
	call TextScroll
	hlcoord TEXTBOX_INNERX, TEXTBOX_INNERY + 2
	pop de
	jp NextChar

PlaceDexEnd::
; Gen I-era dex terminator retained as a command character.
IF DEF(BUILD_JP)
	ld [hl], '。'
ELSE
	ld [hl], '.'
ENDC
	pop hl
	ret

PromptText::
	ld a, [wLinkMode]
	cp LINK_COLOSSEUM
	jr z, .ok
	call LoadBlinkingCursor
.ok
	call Text_WaitBGMap
	call PromptButton
	ld a, [wLinkMode]
	cp LINK_COLOSSEUM
	jr z, DoneText
	call UnloadBlinkingCursor
	jp DoneText

NullChar:: ; unused debug leftover
	ld b, h
	ld c, l
	pop hl
	ld de, .ErrorText
	dec de
	ret
.ErrorText:
	text_decimal hObjectStructIndex, 1, 2
	text "エラー"
	done

IF !DEF(BUILD_JP)
Text_WaitBGMap::
	push bc
	ldh a, [hOAMUpdate]
	push af
	ld a, 1
	ldh [hOAMUpdate], a
	call WaitBGMap
	pop af
	ldh [hOAMUpdate], a
	pop bc
	ret
ENDC
