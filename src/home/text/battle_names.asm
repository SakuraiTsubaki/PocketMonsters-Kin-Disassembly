; Bank 00 text-engine battle/trainer-name rendering.
; The entry points are shared, but grammar/order differs by language family.

PlaceMoveTargetsName::
	ldh a, [hBattleTurn]
	xor 1
	jr PlaceBattlersName

PlaceMoveUsersName::
	ldh a, [hBattleTurn]
	; fallthrough

PlaceBattlersName:
	push de
	and a
	jr nz, .enemy

	ld de, wBattleMonNickname
	jr PlaceCommandCharacter

.enemy
IF DEF(BUILD_FR) || DEF(BUILD_IT)
	; French and Italian put the enemy nickname before their localized suffix.
	ld de, wEnemyMonNickname
	call PlaceString
	ld h, b
	ld l, c
	ld de, EnemyText
	jr PlaceCommandCharacter
ELSE
	; JP, KR, EN, DE and ES use a prefix before the enemy nickname.
	ld de, EnemyText
	call PlaceString
	ld h, b
	ld l, c
	ld de, wEnemyMonNickname
	jr PlaceCommandCharacter
ENDC

PlaceEnemysName::
	push de

	ld a, [wLinkMode]
	and a
	jr nz, .linkbattle

	ld a, [wTrainerClass]
	cp RIVAL1
	jr z, .rival
	cp RIVAL2
	jr z, .rival

IF DEF(BUILD_JP)
	; Japanese: class + の + trainer name.
	ld de, wOTClassName
	call PlaceString
	ld h, b
	ld l, c
	ld de, NoCharText
	call PlaceString
	push bc
	callfar Battle_GetTrainerName
	pop hl
	ld de, wStringBuffer1
	jr PlaceCommandCharacter
ELIF DEF(BUILD_FR) || DEF(BUILD_IT)
	; French/Italian: trainer name first, then localized separator and class.
	push hl
	callfar Battle_GetTrainerName
	pop hl
	ld de, wStringBuffer1
	call PlaceString
	ld h, b
	ld l, c
IF DEF(BUILD_FR)
	ld a, $7f ; space
ELSE
	ld a, $f4 ; Italian separator byte in the retail ROM
ENDC
	ld [hli], a
	ld de, wOTClassName
	jr PlaceCommandCharacter
ELSE
	; Korean and EN/DE/ES western builds: class + space + trainer name.
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

.rival
	ld de, wRivalName
	jr PlaceCommandCharacter

.linkbattle
	ld de, wOTClassName
	; fallthrough

PlaceCommandCharacter::
	call PlaceString
	ld h, b
	ld l, c
	pop de
	jp NextChar
