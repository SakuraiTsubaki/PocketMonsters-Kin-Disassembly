; Small Bank 00 text-engine routines/data that differ by build family.

GameFreakText:: ; unreferenced retail leftover
IF DEF(BUILD_JP) || DEF(BUILD_KR)
	text "ゲームフリーク！"
ELSE
	; Western Gold uses the same raw glyph bytes as JP here, but its charmap
	; renders the fourth kana code as hiragana り.
	text "ゲームフりーク！"
ENDC
	done

IF !DEF(BUILD_JP)
PlaceFarString::
; A = source ROM bank, DE = source string, HL = destination tilemap cursor.
; This routine exists in Korean and western Gold, but not Japanese Gold.
	ld b, a
	ldh a, [hROMBank]
	push af
	ld a, b
	rst Bankswitch
	call PlaceString
	pop af
	rst Bankswitch
	ret
ENDC
