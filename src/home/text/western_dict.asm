; Western (EN/DE/FR/IT/ES) Bank 00 PlaceString dictionary/character dispatch.
; western_variants.asm must be included before this file.

MACRO western_dict
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
	western_dict '<LINE>',    LineChar
	western_dict '<NEXT>',    NextLineChar
	western_dict '<NULL>',    NullChar
	western_dict '<SCROLL>',  _ContTextNoPause
	western_dict '<_CONT>',   _ContText
	western_dict '<PARA>',    Paragraph
	western_dict '<MOM>',     PrintMomsName
	western_dict '<PLAYER>',  PrintPlayerName
	western_dict '<RIVAL>',   PrintRivalName
	western_dict '<ROUTE>',   PlaceJPRoute
	western_dict '<WATASHI>', PlaceWatashi
	western_dict '<KOKO_WA>', PlaceKokoWa
	western_dict '<RED>',     PrintRedsName
	western_dict '<GREEN>',   PrintGreensName
	western_dict '#',         PlacePOKe
	western_dict '<PC>',      PCChar
	western_dict '<ROCKET>',  RocketChar
	western_dict '<TM>',      TMChar
	western_dict '<TRAINER>', TrainerChar
	western_dict '<KOUGEKI>', PlaceKougeki
	western_dict '<LF>',      LineFeedChar
	western_dict '<CONT>',    ContText
	western_dict '<……>',      SixDotsChar
	western_dict '<DONE>',    DoneText
	western_dict '<PROMPT>',  PromptText
	western_dict '<PKMN>',    PlacePKMN
	western_dict '<POKE>',    PlacePOKE
	western_dict '<WBR>',     NextChar
	western_dict '<BSP>',     ' '

	; DE/IT/ES add the $1e/$1d localization controls here.
	western_extra_control_dispatch

	western_dict '<DEXEND>',  PlaceDexEnd
	western_dict '<TARGET>',  PlaceMoveTargetsName
	western_dict '<USER>',    PlaceMoveUsersName
	western_dict '<ENEMY>',   PlaceEnemysName

	; English uses the original diacritic path. DE/FR/IT/ES place the legacy
	; glyph bytes directly; this macro preserves the retail branch layout.
	western_diacritic_dispatch

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
	ld b, 'ﾞ'
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
	ld b, 'ﾟ'
	call Diacritic

.place
	ld [hli], a
	call PrintLetterDelay
	jp NextChar
