; Japanese Gold Bank 00 text-engine implementation-family differences.
;
; Verified against both Japanese Rev 0 and Rev A, whose complete Bank 00
; text modules ($0E8F-$142C) are byte-identical. Exact anchored signatures
; are recorded in analysis/bank00/jp_text_engine_signatures.csv.

; $0E8F
ClearBox::
; Fill a c*b box at hl with the Japanese fullwidth blank tile.
	ld a, '　'
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

; $0EA1
ClearTilemap::
	hlcoord 0, 0
	ld a, '　'
	ld bc, wTilemapEnd - wTilemap
	call ByteFill

	ldh a, [rLCDC]
	bit B_LCDC_ENABLE, a
	ret z
	jp WaitBGMap

; $0EB4
ClearScreen::
	ld a, PAL_BG_TEXT
	hlcoord 0, 0, wAttrmap
	ld bc, SCREEN_AREA
	call ByteFill
	jr ClearTilemap

; $0EC1
Textbox::
	push bc
	push hl
	call TextboxBorder
	pop hl
	pop bc
	jr TextboxPalette

; $0ECA
TextboxBorder::
; Draw the Japanese text-box border locally in ROM0.
	push hl
	ld a, '┌'
	ld [hli], a
	inc a ; '─'
	call .PlaceChars
	inc a ; '┐'
	ld [hl], a
	pop hl

	ld de, SCREEN_WIDTH
	add hl, de
.row
	push hl
	ld a, '│'
	ld [hli], a
	ld a, '　'
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

; $0EFD
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

; $0F17
SpeechTextbox::
	hlcoord TEXTBOX_X, TEXTBOX_Y
	ld b, TEXTBOX_INNERH
	ld c, TEXTBOX_INNERW
	jp Textbox

; Japanese CheckDict uses grammar particles and Japanese-specific substitution
; commands that do not exist as active commands in the western family.
MACRO JapaneseDict
	if \1 == 0
		and a
	else
		cp \1
	endc
	if STRFIND("\2", ".") == 0
		jr z, \2
	else
		jp z, \2
	endc
ENDM

; $0F55
CheckDict::
	JapaneseDict '<LINE>',    LineChar
	JapaneseDict '<NEXT>',    NextLineChar
	JapaneseDict '<NULL>',    NullChar
	JapaneseDict '<SCROLL>',  _ContTextNoPause
	JapaneseDict '<_CONT>',   _ContText
	JapaneseDict '<PARA>',    Paragraph
	JapaneseDict '<MOM>',     PrintMomsName
	JapaneseDict '<PLAYER>',  PrintPlayerName
	JapaneseDict '<RIVAL>',   PrintRivalName
	JapaneseDict '<ROUTE>',   PlaceRoute
	JapaneseDict '<WATASHI>', PlaceWatashi
	JapaneseDict '<KOKO_WA>', PlaceKokoWa
	JapaneseDict '<RED>',     PrintRedsName
	JapaneseDict '<GREEN>',   PrintGreensName
	JapaneseDict '#',         PlacePokemon
	JapaneseDict '<PC>',      PlacePC
	JapaneseDict '<ROCKET>',  PlaceRocket
	JapaneseDict '<TM>',      PlaceTM
	JapaneseDict '<TRAINER>', PlaceTrainer
	JapaneseDict '<KOUGEKI>', PlaceKougeki
	JapaneseDict '<TA!>',     PlaceTa
	JapaneseDict '<CONT>',    ContText
	JapaneseDict '<⋯>',       PlaceSixDots
	JapaneseDict '<DONE>',    DoneText
	JapaneseDict '<PROMPT>',  PromptText
	JapaneseDict '<GA>',      PlaceGa
	JapaneseDict '<WA>',      PlaceWa
	JapaneseDict '<NO>',      PlaceNo
	JapaneseDict '<WO>',      PlaceWo
	JapaneseDict '<TTE>',     PlaceTte
	JapaneseDict '<NI>',      PlaceNi
	JapaneseDict '<DEXEND>',  PlaceDexEnd
	JapaneseDict '<TARGET>',  PlaceMoveTargetsName
	JapaneseDict '<USER>',    PlaceMoveUsersName
	JapaneseDict '<ENEMY>',   PlaceEnemysName
	JapaneseDict '゜',         .diacritic
	cp '゛'
	jr nz, .not_diacritic

.diacritic
	ld b, a
	call Diacritic
	jp NextChar

.not_diacritic
	cp FIRST_REGULAR_TEXT_CHAR
	jr nc, .place
	cp 'パ'
	jr nc, .handakuten
	cp FIRST_HIRAGANA_DAKUTEN_CHAR
	jr nc, .hiragana_dakuten
	add 'カ' - 'ガ'
	jr .place_dakuten

.hiragana_dakuten
	add 'か' - 'が'
.place_dakuten
	ld b, '゛'
	call Diacritic
	jr .place

.handakuten
	cp 'ぱ'
	jr nc, .hiragana_handakuten
	add 'ハ' - 'パ'
	jr .place_handakuten

.hiragana_handakuten
	add 'は' - 'ぱ'
.place_handakuten
	ld b, '゜'
	call Diacritic

.place
	ld [hli], a
	call PrintLetterDelay
	jp NextChar

; $122C
TextScroll::
	hlcoord TEXTBOX_X, TEXTBOX_INNERY
	decoord TEXTBOX_X, TEXTBOX_INNERY - 1
	ld bc, 3 * SCREEN_WIDTH
	call CopyBytes
	hlcoord TEXTBOX_INNERX, TEXTBOX_INNERY + 2
	ld a, '　'
	ld bc, TEXTBOX_INNERW
	call ByteFill
	ld c, 5
	call DelayFrames
	ret

; $1249
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

; $1259
Diacritic::
	push af
	push hl
	ld a, b
	ld bc, -SCREEN_WIDTH
	add hl, bc
	ld [hl], a
	pop hl
	pop af
	ret
