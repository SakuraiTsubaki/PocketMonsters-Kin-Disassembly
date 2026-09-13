; Italian Bank 00 embedded text-engine strings.

TMCharText::      db "T@"
TrainerCharText:: db "ALLEN.@"
PCCharText::      db "PC@"
RocketCharText::  db "ROCKET@"
PlacePOKeText::   db "POKé@"
KougekiText::     db "こうげき@"
SixDotsCharText:: db "……@"
EnemyText::       db " nemico@"
PlacePKMNText::   db "<PK><MN>@"
PlacePOKEText::   db "<PO><KE>@"
String_Space::    db " @"
PlaceJPRouteText::
PlaceWatashiText::
PlaceKokoWaText:: db "-<LF>@"

WeekdaySunday::    db "DOMENICA@"
WeekdayMonday::    db "LUNED", $c8, "@" ; final accented glyph, exact ROM byte
WeekdayTuesday::   db "MARTED", $c8, "@"
WeekdayWednesday:: db "MERCOLED", $c8, "@"
WeekdayThursday::  db "GIOVED", $c8, "@"
WeekdayFriday::    db "VENERD", $c8, "@"
WeekdaySaturday::  db "SABATO@"
WeekdaySuffix::    db "@"
