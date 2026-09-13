; Bank 00 video/BG-map transfer engine for all tracked Gold releases.
; Shared code is kept once; BUILD_JP and BUILD_KR select the retail family
; differences audited against the read-only ROMs.

UpdateBGMapBuffer::
; Copy [hBGMapTileCount] 16x8 tiles from wBGMapBuffer to the BG-map
; addresses stored in wBGMapBufferPointers. Tile count is consumed in pairs.
	ldh a, [hBGMapUpdate]
	and a
	ret z

	ld [hSPBuffer], sp
	ld hl, wBGMapBufferPointers
	ld sp, hl
	ld hl, wBGMapPalBuffer
	ld de, wBGMapBuffer

.next
rept 2
	pop bc
	ld a, 1
	ldh [rVBK], a
	ld a, [hli]
	ld [bc], a
	inc c
	ld a, [hli]
	ld [bc], a
	dec c

	ld a, 0
	ldh [rVBK], a
	ld a, [de]
	inc de
	ld [bc], a
	inc c
	ld a, [de]
	inc de
	ld [bc], a
endr

	ldh a, [hBGMapTileCount]
	dec a
	dec a
	ldh [hBGMapTileCount], a
	jr nz, .next

	ldh a, [hSPBuffer]
	ld l, a
	ldh a, [hSPBuffer + 1]
	ld h, a
	ld sp, hl

	xor a
	ldh [hBGMapUpdate], a
	scf
	ret

WaitTop::
	ldh a, [hBGMapMode]
	and a
	ret z

IF DEF(BUILD_KR)
; Korean Gold forces the third counter to top before synchronizing.
	xor a
	ldh [hBGMapThird], a
.loop
	call DelayFrame
	ldh a, [hBGMapThird]
	and a
	jr nz, .loop
ELSE
; Japanese and western builds wait until the top third comes around naturally.
	ldh a, [hBGMapThird]
	and a
	jr z, .done
	call DelayFrame
	jr WaitTop
.done
ENDC
	xor a
	ldh [hBGMapMode], a
	ret

IF DEF(BUILD_KR)

UpdateBGMap::
; Korean Gold relocates the large update routine to another bank.
	farcall_reg _UpdateBGMap
	ret

Delay4::
; Korean-only four-frame helper. Cutscene VBlank skips the first delay.
	ldh a, [hVBlank]
	cp VBLANK_CUTSCENE
	jr z, .delay3
	call DelayFrame
.delay3
	call DelayFrame
	call DelayFrame
	jp DelayFrame

ELSE

UpdateBGMap::
; Update the BG map in thirds from wTilemap/wAttrmap.
	ldh a, [hBGMapMode]
	and a
	ret z

	dec a
	jr z, .Tiles

IF DEF(BUILD_JP)
; Japanese retail Gold only supports BG Map 0 modes here; non-tile mode is
; the attribute map path. Western Gold adds modes 3/4 for BG Map 1 below.
.Attr:
	ld a, 1
	ldh [rVBK], a
	hlcoord 0, 0, wAttrmap
	call .update
	ld a, 0
	ldh [rVBK], a
	ret
ELSE
	dec a
	jr z, .Attr

	; BG Map 1 modes 3/4 (western releases only).
	dec a
	ldh a, [hBGMapAddress]
	ld l, a
	ldh a, [hBGMapAddress + 1]
	ld h, a
	push hl

	xor a
	ldh [hBGMapAddress], a
	ld a, HIGH(vBGMap1)
	ldh [hBGMapAddress + 1], a

	ldh a, [hBGMapMode]
	push af
	cp 3
	call z, .Tiles
	pop af
	cp 4
	call z, .Attr

	pop hl
	ld a, l
	ldh [hBGMapAddress], a
	ld a, h
	ldh [hBGMapAddress + 1], a
	ret

.Attr:
	ld a, 1
	ldh [rVBK], a
	hlcoord 0, 0, wAttrmap
	call .update
	ld a, 0
	ldh [rVBK], a
	ret
ENDC

.Tiles:
	hlcoord 0, 0

.update
	ld [hSPBuffer], sp
	ldh a, [hBGMapThird]
	and a
	jr z, .top
	dec a
	jr z, .middle

DEF THIRD_HEIGHT EQU SCREEN_HEIGHT / 3

; Bottom third.
	ld de, 2 * THIRD_HEIGHT * SCREEN_WIDTH
	add hl, de
	ld sp, hl
	ldh a, [hBGMapAddress + 1]
	ld h, a
	ldh a, [hBGMapAddress]
	ld l, a
	ld de, 2 * THIRD_HEIGHT * TILEMAP_WIDTH
	add hl, de
	xor a
	jr .start

.middle
	ld de, THIRD_HEIGHT * SCREEN_WIDTH
	add hl, de
	ld sp, hl
	ldh a, [hBGMapAddress + 1]
	ld h, a
	ldh a, [hBGMapAddress]
	ld l, a
	ld de, THIRD_HEIGHT * TILEMAP_WIDTH
	add hl, de
	ld a, 2
	jr .start

.top
	ld sp, hl
	ldh a, [hBGMapAddress + 1]
	ld h, a
	ldh a, [hBGMapAddress]
	ld l, a
	ld a, 1

.start
	ldh [hBGMapThird], a
	ld a, THIRD_HEIGHT
	ld bc, TILEMAP_WIDTH - (SCREEN_WIDTH - 1)

.row
rept SCREEN_WIDTH / 2 - 1
	pop de
	ld [hl], e
	inc l
	ld [hl], d
	inc l
endr
	pop de
	ld [hl], e
	inc l
	ld [hl], d
	add hl, bc
	dec a
	jr nz, .row

	ldh a, [hSPBuffer]
	ld l, a
	ldh a, [hSPBuffer + 1]
	ld h, a
	ld sp, hl
	ret

ENDC ; !BUILD_KR

Serve1bppRequest::
	ld a, [wRequested1bppSize]
	and a
	ret z

	ld [hSPBuffer], sp
	ld hl, wRequested1bppSource
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld sp, hl

	ld hl, wRequested1bppDest
	ld a, [hli]
	ld h, [hl]
	ld l, a

	ld a, [wRequested1bppSize]
	ld b, a
	xor a
	ld [wRequested1bppSize], a

.next
rept 3
	pop de
	ld [hl], e
	inc l
	ld [hl], e
	inc l
	ld [hl], d
	inc l
	ld [hl], d
	inc l
endr
	pop de
	ld [hl], e
	inc l
	ld [hl], e
	inc l
	ld [hl], d
	inc l
	ld [hl], d

	inc hl
	dec b
	jr nz, .next

	ld a, l
	ld [wRequested1bppDest], a
	ld a, h
	ld [wRequested1bppDest + 1], a
	ld [wRequested1bppSource], sp

	ldh a, [hSPBuffer]
	ld l, a
	ldh a, [hSPBuffer + 1]
	ld h, a
	ld sp, hl
	ret

Serve2bppRequest::
	ld a, [wRequested2bppSize]
	and a
	ret z

	ld [hSPBuffer], sp
	ld hl, wRequested2bppSource
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld sp, hl

	ld hl, wRequested2bppDest
	ld a, [hli]
	ld h, [hl]
	ld l, a

	ld a, [wRequested2bppSize]
	ld b, a
	xor a
	ld [wRequested2bppSize], a

.next
rept 7
	pop de
	ld [hl], e
	inc l
	ld [hl], d
	inc l
endr
	pop de
	ld [hl], e
	inc l
	ld [hl], d

	inc hl
	dec b
	jr nz, .next

	ld a, l
	ld [wRequested2bppDest], a
	ld a, h
	ld [wRequested2bppDest + 1], a
	ld [wRequested2bppSource], sp

	ldh a, [hSPBuffer]
	ld l, a
	ldh a, [hSPBuffer + 1]
	ld h, a
	ld sp, hl
	ret

AnimateTileset::
	ldh a, [hMapAnims]
	and a
	ret z
	ldh a, [hROMBank]
	push af
	ld a, BANK(_AnimateTileset)
	rst Bankswitch
	call _AnimateTileset
	pop af
	rst Bankswitch
	ret

Video_DummyFunction:: ; unreferenced
	ret

EnableSpriteDisplay:: ; unreferenced
	ld hl, rLCDC
	set B_LCDC_OBJS, [hl]
	ret

FillBGMap0WithBlack::
	nop
	ldh a, [hBlackOutBGMapThird]
	and a
	ret z
	dec a
	jr z, .one
	dec a
	jr z, .two

DEF BG_THIRD_HEIGHT EQU (TILEMAP_HEIGHT - SCREEN_HEIGHT) / 2

	ld a, 2
	ldh [hBlackOutBGMapThird], a
	ld hl, hBGMapAddress
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld de, SCREEN_WIDTH
	add hl, de
	ld b, SCREEN_HEIGHT
	ld a, '■'
.loop1
rept TILEMAP_WIDTH - SCREEN_WIDTH
	ld [hli], a
endr
	add hl, de
	dec b
	jr nz, .loop1
	ret

.two
	ld a, 1
	ld de, TILEMAP_WIDTH * SCREEN_HEIGHT
	jr .go

.one
	xor a
	ld de, TILEMAP_WIDTH * (SCREEN_HEIGHT + BG_THIRD_HEIGHT)

.go
	ldh [hBlackOutBGMapThird], a
	ld hl, hBGMapAddress
	ld a, [hli]
	ld h, [hl]
	ld l, a
	add hl, de
	ld b, BG_THIRD_HEIGHT * 2
	ld a, '■'
.loop2
rept TILEMAP_WIDTH / 2
	ld [hli], a
endr
	dec b
	jr nz, .loop2
	ret
