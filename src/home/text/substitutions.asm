; Bank 00 command-character substitution entry points.
; text_print_name is defined by common.asm.

IF DEF(BUILD_JP)
PlaceTrainer: text_print_name TrainerCharText
PlaceTM:      text_print_name TMCharText
PlacePC:      text_print_name PCCharText
PlaceRocket:  text_print_name RocketCharText
PlacePokemon: text_print_name PokemonCharText
PlaceKougeki: text_print_name KougekiCharText
PlaceTa:      text_print_name TaCharText
PlaceSixDots: text_print_name SixDotsCharText
PlaceGa:      text_print_name GaCharText
PlaceWa:      text_print_name WaCharText
PlaceNo:      text_print_name NoCharText
PlaceWo:      text_print_name WoCharText
PlaceNi:      text_print_name NiCharText
PlaceTte:     text_print_name TteCharText
PlaceRoute:   text_print_name RouteCharText
PlaceWatashi: text_print_name WatashiCharText
PlaceKokoWa:  text_print_name KokoWaCharText
ELSE
TrainerChar:  text_print_name TrainerCharText
TMChar:       text_print_name TMCharText
PCChar:       text_print_name PCCharText
RocketChar:   text_print_name RocketCharText
PlacePOKe:    text_print_name PlacePOKeText
PlaceKougeki: text_print_name KougekiText
SixDotsChar:  text_print_name SixDotsCharText
PlacePKMN:    text_print_name PlacePKMNText
PlacePOKE:    text_print_name PlacePOKEText
PlaceJPRoute: text_print_name PlaceJPRouteText
PlaceWatashi: text_print_name PlaceWatashiText
PlaceKokoWa:  text_print_name PlaceKokoWaText
ENDC
