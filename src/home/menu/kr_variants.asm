; Korean Gold-specific Bank 00 menu implementation fragments.
; These replace the ordinary JP/Western window-backup access paths because
; Korean Gold stores/restores parts of the menu stack through WRAM bank 3.

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
