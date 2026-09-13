; Localized Bank 00 yes/no box behavior for all tracked Gold releases.

YesNoBox::
IF DEF(BUILD_KR)
	lb bc, SCREEN_WIDTH - 6, 6
ELSE
	lb bc, SCREEN_WIDTH - 6, 7
ENDC

PlaceYesNoBox::
	jr _YesNoBox

PlaceGenericTwoOptionBox:: ; unreferenced
	call LoadMenuHeader
	jr InterpretTwoOptionMenu

_YesNoBox::
	push bc
	ld hl, YesNoMenuHeader
	call CopyMenuHeader
	pop bc

; Localized western releases add the retail overflow/width adjustment block.
IF DEF(BUILD_DE) || DEF(BUILD_FR) || DEF(BUILD_IT) || DEF(BUILD_ES)
	ld a, b
	cp SCREEN_WIDTH - 6
	jr nz, .position_ok
IF DEF(BUILD_DE)
	ld a, SCREEN_WIDTH - 7 ; 13
ELIF DEF(BUILD_FR)
	ld a, SCREEN_WIDTH - 6 ; 14 (retail no-op adjustment)
ELSE
	ld a, SCREEN_WIDTH - 5 ; 15 (IT/ES)
ENDC
	ld b, a
.position_ok
ENDC

	ld a, b
	ld [wMenuBorderLeftCoord], a
IF DEF(BUILD_DE)
	add 6
ELIF DEF(BUILD_IT) || DEF(BUILD_ES)
	add 4
ELSE
	add 5
ENDC
	ld [wMenuBorderRightCoord], a
	ld a, c
	ld [wMenuBorderTopCoord], a
IF DEF(BUILD_KR)
	add 5
ELSE
	add 4
ENDC
	ld [wMenuBorderBottomCoord], a
	call PushWindow

InterpretTwoOptionMenu::
	call VerticalMenu
	push af
	ld c, $f
	call DelayFrames
	call CloseWindow
	pop af
	jr c, .no
	ld a, [wMenuCursorY]
	cp 2
	jr z, .no
	and a
	ret
.no
	ld a, 2
	ld [wMenuCursorY], a
	scf
	ret

YesNoMenuHeader::
	db MENU_BACKUP_TILES
IF DEF(BUILD_KR)
	menu_coords 10, 4, 15, 9
ELIF DEF(BUILD_DE)
	menu_coords 10, 5, 16, 9
ELIF DEF(BUILD_IT) || DEF(BUILD_ES)
	menu_coords 10, 5, 14, 9
ELSE
	menu_coords 10, 5, 15, 9
ENDC
	dw .MenuData
	db 1

.MenuData
IF DEF(BUILD_KR)
	db STATICMENU_CURSOR
	db 2
	db "예@"
	db "아니오@"
ELSE
	db STATICMENU_CURSOR | STATICMENU_NO_TOP_SPACING
	db 2
IF DEF(BUILD_JP)
	db "はい@"
	db "いいえ@"
ELIF DEF(BUILD_DE)
	db "JA@"
	db "NEIN@"
ELIF DEF(BUILD_FR)
	db "OUI@"
	db "NON@"
ELIF DEF(BUILD_IT)
	db "SÌ@"
	db "NO@"
ELIF DEF(BUILD_ES)
	db "SÍ@"
	db "NO@"
ELSE
	db "YES@"
	db "NO@"
ENDC
ENDC
