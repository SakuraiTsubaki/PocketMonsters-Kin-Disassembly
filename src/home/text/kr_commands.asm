; Korean Gold Bank 00 text command dispatcher.
; The command set matches the western family, including TX_FAR, but uses
; Korean locale data and the Korean double-byte text engine around it.

TextCommands::
	table_width 2
	dw TextCommand_START
	dw TextCommand_RAM
	dw TextCommand_BCD
	dw TextCommand_MOVE
	dw TextCommand_BOX
	dw TextCommand_LOW
	dw TextCommand_PROMPT_BUTTON
	dw TextCommand_SCROLL
	dw TextCommand_START_ASM
	dw TextCommand_DECIMAL
	dw TextCommand_PAUSE
	dw TextCommand_SOUND
	dw TextCommand_DOTS
	dw TextCommand_WAIT_BUTTON
	dw TextCommand_SOUND
	dw TextCommand_SOUND
	dw TextCommand_SOUND
	dw TextCommand_SOUND
	dw TextCommand_SOUND
	dw TextCommand_SOUND
	dw TextCommand_STRINGBUFFER
	dw TextCommand_DAY
	dw TextCommand_FAR
	assert_table_length NUM_TEXT_CMDS

TextCommand_START::
	ld d, h
	ld e, l
	ld h, b
	ld l, c
	call PlaceString
	ld h, d
	ld l, e
	inc hl
	ret

TextCommand_RAM::
	ld a, [hli]
	ld e, a
	ld a, [hli]
	ld d, a
	push hl
	ld h, b
	ld l, c
	call PlaceString
	pop hl
	ret

TextCommand_FAR::
	ldh a, [hROMBank]
	push af
	ld a, [hli]
	ld e, a
	ld a, [hli]
	ld d, a
	ld a, [hli]
	ldh [hROMBank], a
	ld [rROMB], a
	push hl
	ld h, d
	ld l, e
	call DoTextUntilTerminator
	pop hl
	pop af
	ldh [hROMBank], a
	ld [rROMB], a
	ret

TextCommand_BCD::
	ld a, [hli]
	ld e, a
	ld a, [hli]
	ld d, a
	ld a, [hli]
	push hl
	ld h, b
	ld l, c
	ld c, a
	call PrintBCDNumber
	ld b, h
	ld c, l
	pop hl
	ret

TextCommand_MOVE::
	ld a, [hli]
	ld [wMenuScrollPosition + 2], a
	ld c, a
	ld a, [hli]
	ld [wMenuScrollPosition + 3], a
	ld b, a
	ret

TextCommand_BOX::
	ld a, [hli]
	ld e, a
	ld a, [hli]
	ld d, a
	ld a, [hli]
	ld b, a
	ld a, [hli]
	ld c, a
	push hl
	ld h, d
	ld l, e
	call Textbox
	pop hl
	ret

TextCommand_LOW::
	bccoord TEXTBOX_INNERX, TEXTBOX_INNERY + 2
	ret

TextCommand_PROMPT_BUTTON::
	ld a, [wLinkMode]
	cp LINK_COLOSSEUM
	jp z, TextCommand_WAIT_BUTTON
	push hl
	call LoadBlinkingCursor
	push bc
	call PromptButton
	pop bc
	call UnloadBlinkingCursor
	pop hl
	ret

TextCommand_SCROLL::
	push hl
	call UnloadBlinkingCursor
	call TextScroll
	call TextScroll
	pop hl
	bccoord TEXTBOX_INNERX, TEXTBOX_INNERY + 2
	ret

TextCommand_START_ASM::
	jp hl

TextCommand_DECIMAL::
	ld a, [hli]
	ld e, a
	ld a, [hli]
	ld d, a
	ld a, [hli]
	push hl
	ld h, b
	ld l, c
	ld b, a
	and $f
	ld c, a
	ld a, b
	and $f0
	swap a
	set PRINTNUM_LEFTALIGN_F, a
	ld b, a
	call PrintNum
	ld b, h
	ld c, l
	pop hl
	ret

TextCommand_PAUSE::
	push hl
	push bc
	call GetJoypad
	ldh a, [hJoyDown]
	and PAD_A | PAD_B
	jr nz, .done
	ld c, 30
	call DelayFrames
.done
	pop bc
	pop hl
	ret

TextCommand_SOUND::
	push bc
	dec hl
	ld a, [hli]
	ld b, a
	push hl
	ld hl, TextSFX
.loop
	ld a, [hli]
	cp -1
	jr z, .done
	cp b
	jr z, .play
	inc hl
	inc hl
	jr .loop
.play
	push de
	ld e, [hl]
	inc hl
	ld d, [hl]
	call PlaySFX
	call WaitSFX
	pop de
.done
	pop hl
	pop bc
	ret

TextCommand_CRY:: ; unreferenced
	push de
	ld e, [hl]
	inc hl
	ld d, [hl]
	call PlayMonCry
	pop de
	pop hl
	pop bc
	ret

TextSFX::
	dbw TX_SOUND_DEX_FANFARE_50_79,  SFX_DEX_FANFARE_50_79
	dbw TX_SOUND_FANFARE,            SFX_FANFARE
	dbw TX_SOUND_DEX_FANFARE_20_49,  SFX_DEX_FANFARE_20_49
	dbw TX_SOUND_ITEM,               SFX_ITEM
	dbw TX_SOUND_CAUGHT_MON,         SFX_CAUGHT_MON
	dbw TX_SOUND_DEX_FANFARE_80_109, SFX_DEX_FANFARE_80_109
	dbw TX_SOUND_SLOT_MACHINE_START, SFX_SLOT_MACHINE_START
	db -1

TextCommand_DOTS::
	ld a, [hli]
	ld d, a
	push hl
	ld h, b
	ld l, c
.loop
	push de
	ld a, '…'
	ld [hli], a
	call GetJoypad
	ldh a, [hJoyDown]
	and PAD_A | PAD_B
	jr nz, .next
	ld c, 10
	call DelayFrames
.next
	pop de
	dec d
	jr nz, .loop
	ld b, h
	ld c, l
	pop hl
	ret

TextCommand_WAIT_BUTTON::
	push hl
	push bc
	call PromptButton
	pop bc
	pop hl
	ret

TextCommand_STRINGBUFFER::
	ld a, [hli]
	push hl
	ld e, a
	ld d, 0
	ld hl, StringBufferPointers
	add hl, de
	add hl, de
	ld a, BANK(StringBufferPointers)
	call GetFarWord
	ld d, h
	ld e, l
	ld h, b
	ld l, c
	call PlaceString
	pop hl
	ret

TextCommand_DAY::
	call GetWeekday
	push hl
	push bc
	ld c, a
	ld b, 0
	ld hl, .Days
	add hl, bc
	add hl, bc
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld d, h
	ld e, l
	pop hl
	call PlaceString
	ld h, b
	ld l, c
	ld de, WeekdaySuffix
	call PlaceString
	pop hl
	ret

.Days:
	dw WeekdaySunday
	dw WeekdayMonday
	dw WeekdayTuesday
	dw WeekdayWednesday
	dw WeekdayThursday
	dw WeekdayFriday
	dw WeekdaySaturday
