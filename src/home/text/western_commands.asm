; Western (EN/DE/FR/IT/ES) Bank 00 text command dispatcher.
; Reconstructed semantically and checked against pret/pokegold plus the
; tracked original ROM ranges. Locale-specific embedded strings live in
; src/home/text/locales/.

TextCommands::
; Entries correspond to TX_* constants.
	table_width 2
	dw TextCommand_START         ; TX_START
	dw TextCommand_RAM           ; TX_RAM
	dw TextCommand_BCD           ; TX_BCD
	dw TextCommand_MOVE          ; TX_MOVE
	dw TextCommand_BOX           ; TX_BOX
	dw TextCommand_LOW           ; TX_LOW
	dw TextCommand_PROMPT_BUTTON ; TX_PROMPT_BUTTON
	dw TextCommand_SCROLL        ; TX_SCROLL
	dw TextCommand_START_ASM     ; TX_START_ASM
	dw TextCommand_DECIMAL       ; TX_DECIMAL
	dw TextCommand_PAUSE         ; TX_PAUSE
	dw TextCommand_SOUND         ; TX_SOUND_DEX_FANFARE_50_79
	dw TextCommand_DOTS          ; TX_DOTS
	dw TextCommand_WAIT_BUTTON   ; TX_WAIT_BUTTON
	dw TextCommand_SOUND         ; TX_SOUND_DEX_FANFARE_20_49
	dw TextCommand_SOUND         ; TX_SOUND_ITEM
	dw TextCommand_SOUND         ; TX_SOUND_CAUGHT_MON
	dw TextCommand_SOUND         ; TX_SOUND_DEX_FANFARE_80_109
	dw TextCommand_SOUND         ; TX_SOUND_FANFARE
	dw TextCommand_SOUND         ; TX_SOUND_SLOT_MACHINE_START
	dw TextCommand_STRINGBUFFER  ; TX_STRINGBUFFER
	dw TextCommand_DAY           ; TX_DAY
	dw TextCommand_FAR           ; TX_FAR
	assert_table_length NUM_TEXT_CMDS

TextCommand_START::
; Write text until "@".
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
; Write text from a RAM address (little endian).
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
; Write text from a different ROM bank (little endian pointer + bank).
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
	ld de, .Day
	call PlaceString
	pop hl
	ret

.Days:
	dw .Sun
	dw .Mon
	dw .Tues
	dw .Wednes
	dw .Thurs
	dw .Fri
	dw .Satur
.Sun:    db "SUN@"
.Mon:    db "MON@"
.Tues:   db "TUES@"
.Wednes: db "WEDNES@"
.Thurs:  db "THURS@"
.Fri:    db "FRI@"
.Satur:  db "SATUR@"
.Day:    db "DAY@"
