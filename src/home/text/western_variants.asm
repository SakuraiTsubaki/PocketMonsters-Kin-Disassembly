; Region-specific fragments for the western Bank 00 text engine.
; These are ROM-verified deltas layered onto the English semantic core.

; DE/IT/ES add two control bytes after the ordinary western WBR/BSP handling.
MACRO western_extra_control_dispatch
IF DEF(BUILD_DE) || DEF(BUILD_IT) || DEF(BUILD_ES)
	cp $1e
	jp z, NextChar
	cp $1d
	jp z, PlaceHyphenSplit
ENDC
ENDM

; English sends the two legacy diacritic bytes through Diacritic. Localized
; western ROMs place them directly and skip the diacritic conversion path.
MACRO western_diacritic_dispatch
IF DEF(BUILD_EN)
	cp $e4
	jr z, .diacritic
	cp $e5
	jr nz, .not_diacritic
ELSE
	cp $e4
	jr z, .place
	cp $e5
	jr z, .place
	jr .not_diacritic
ENDC
ENDM

IF DEF(BUILD_DE) || DEF(BUILD_IT) || DEF(BUILD_ES)
PlaceHyphenSplit::
	ld [hl], '-'
	jp LineFeedChar
ENDC

; Enemy-name grammar differs in FR/IT. Invoke this macro from the .enemy path
; inside PlaceBattlersName after `push de` / turn selection.
MACRO western_place_battler_enemy
IF DEF(BUILD_FR) || DEF(BUILD_IT)
	ld de, wEnemyMonNickname
	call PlaceString
	ld h, b
	ld l, c
	ld de, EnemyText
	jr PlaceCommandCharacter
ELSE
	ld de, EnemyText
	call PlaceString
	ld h, b
	ld l, c
	ld de, wEnemyMonNickname
	jr PlaceCommandCharacter
ENDC
ENDM

; FR/IT print trainer name before class name. Their separator bytes are kept as
; raw values until the per-locale charmap files are reconstructed.
MACRO western_place_regular_trainer_name
IF DEF(BUILD_FR) || DEF(BUILD_IT)
	push hl
	callfar Battle_GetTrainerName
	pop hl
	ld de, wStringBuffer1
	call PlaceString
	ld h, b
	ld l, c
IF DEF(BUILD_FR)
	ld a, $7f
ELSE
	ld a, $f4
ENDC
	ld [hli], a
	ld de, wOTClassName
	jr PlaceCommandCharacter
ELSE
	ld de, wOTClassName
	call PlaceString
	ld h, b
	ld l, c
	ld de, String_Space
	call PlaceString
	push bc
	callfar Battle_GetTrainerName
	pop hl
	ld de, wStringBuffer1
	jr PlaceCommandCharacter
ENDC
ENDM

; All localized western Gold ROMs preserve the byte at $c506 across the
; Paragraph clear. The semantic WRAM symbol is intentionally not guessed yet.
MACRO western_paragraph_save_state
IF !DEF(BUILD_EN)
	ld a, [$c506]
	push af
ENDC
ENDM

MACRO western_paragraph_restore_state
IF DEF(BUILD_EN)
	call UnloadBlinkingCursor
ELSE
	pop af
	ld [$c506], a
ENDC
ENDM

; English has the full 11-byte Diacritic implementation. The four localized
; western ROMs retain only a one-byte return at this location.
MACRO western_diacritic_body
IF DEF(BUILD_EN)
	push af
	push hl
	ld a, b
	ld bc, -SCREEN_WIDTH
	add hl, bc
	ld [hl], a
	pop hl
	pop af
	ret
ELSE
	ret
ENDC
ENDM
