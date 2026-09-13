; Korean Gold Bank 00 PlaceString dictionary/character dispatch.
; Bytes $01-$0B select one of the eleven Korean two-byte character tables.

MACRO kr_dict
	if \1 == 0
		and a
	else
		cp \1
	endc
	if ISCONST(\2)
		jr nz, .not\@
		ld a, \2
	.not\@:
	elif STRFIND("\2", ".") == 0
		jr z, \2
	else
		jp z, \2
	endc
ENDM

CheckDict::
	cp $c
	jp c, DoubleByteChar

	kr_dict '<LINE>',    LineChar
	kr_dict '<NEXT>',    NextLineChar
	kr_dict '<NULL>',    NullChar
	kr_dict '<SCROLL>',  _ContTextNoPause
	kr_dict '<_CONT>',   _ContText
	kr_dict '<PARA>',    Paragraph
	kr_dict '<MOM>',     PrintMomsName
	kr_dict '<PLAYER>',  PrintPlayerName
	kr_dict '<RIVAL>',   PrintRivalName
	kr_dict '<ROUTE>',   PlaceJPRoute
	kr_dict '<WATASHI>', PlaceWatashi
	kr_dict '<KOKO_WA>', PlaceKokoWa
	kr_dict '<RED>',     PrintRedsName
	kr_dict '<GREEN>',   PrintGreensName
	kr_dict '#',         PlacePOKe
	kr_dict '<PC>',      PCChar
	kr_dict '<ROCKET>',  RocketChar
	kr_dict '<TM>',      TMChar
	kr_dict '<TRAINER>', TrainerChar
	kr_dict '<KOUGEKI>', PlaceKougeki
	kr_dict '<LF>',      LineFeedChar
	kr_dict '<CONT>',    ContText
	kr_dict '<……>',      SixDotsChar
	kr_dict '<DONE>',    DoneText
	kr_dict '<PROMPT>',  PromptText
	kr_dict '<PKMN>',    PlacePKMN
	kr_dict '<POKE>',    PlacePOKE
	kr_dict '<WBR>',     NextChar
	kr_dict '<BSP>',     ' '
	kr_dict '<DEXEND>',  PlaceDexEnd
	kr_dict '<TARGET>',  PlaceMoveTargetsName
	kr_dict '<USER>',    PlaceMoveUsersName
	kr_dict '<ENEMY>',   PlaceEnemysName
	kr_dict '゜',         .diacritic
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
