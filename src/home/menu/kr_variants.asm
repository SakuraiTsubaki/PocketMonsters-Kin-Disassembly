; Korean Gold-specific Bank 00 menu implementation fragments.
; These replace ordinary JP/Western window-stack and clear helpers because
; Korean Gold moves several operations out of ROM0 and uses WRAM bank 3 for
; stacked menu metadata.

RestoreTileBackup::
	farcall_reg Function1fc5a0
	ret

PopWindow::
	di
	ld a, $03
	ldh [rWBK], a
	ld b, wMenuHeaderEnd - wMenuHeader
	ld de, wMenuHeader
.loop
	ld a, [hld]
	ld [de], a
	inc de
	dec b
	jr nz, .loop
	ld a, $01
	ldh [rWBK], a
	ei
	ret

GetWindowStackTop::
	ld hl, wWindowStackPointer
	ld a, [hli]
	ld h, [hl]
	ld l, a
	inc hl
	di
	ld a, $03
	ldh [rWBK], a
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld a, $01
	ldh [rWBK], a
	ei
	ret

; Korean-only helper at retail ROM address $1C17.
; It temporarily raises the menu top border while pushing the window, then
; restores the caller-visible coordinate.
Function1c17::
	call CopyMenuHeader
	ld a, [wMenuBorderTopCoord]
	dec a
	ld [wMenuBorderTopCoord], a
	call PushWindow
	ld a, [wMenuBorderTopCoord]
	inc a
	ld [wMenuBorderTopCoord], a
	ret

ClearWindowData::
; Korean Gold relocates the larger local clear routine out of ROM0.
	farcall_reg _ClearWindowData
	ret
