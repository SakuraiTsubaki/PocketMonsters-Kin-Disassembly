; Spanish Bank 00 embedded text-engine strings.

TMCharText::      db "MT@"
TrainerCharText:: db "ENTREN.@"
PCCharText::      db "PC@"
RocketCharText::  db "ROCKET@"
PlacePOKeText::   db "POKé@"
KougekiText::     db "こうげき@"
SixDotsCharText:: db "……@"
EnemyText::       db "Enem. @"
PlacePKMNText::   db "<PK><MN>@"
PlacePOKEText::   db "<PO><KE>@"
String_Space::    db " @"
PlaceJPRouteText::
PlaceWatashiText::
PlaceKokoWaText:: db "-<LF>@"

WeekdaySunday::    db "DOMINGO@"
WeekdayMonday::    db "LUNES@"
WeekdayTuesday::   db "MARTES@"
WeekdayWednesday:: db "MI", $c7, "RCOLES@" ; accented glyph, exact ROM byte
WeekdayThursday::  db "JUEVES@"
WeekdayFriday::    db "VIERNES@"
WeekdaySaturday::  db "S", $bf, "BADO@" ; accented glyph, exact ROM byte
WeekdaySuffix::    db "@"
