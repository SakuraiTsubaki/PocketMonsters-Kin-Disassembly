; Select the embedded western Bank 00 text-engine strings.
; Exactly one BUILD_* locale symbol must be defined by the final build.

IF DEF(BUILD_EN)
    INCLUDE "src/home/text/locales/en.asm"
ELIF DEF(BUILD_DE)
    INCLUDE "src/home/text/locales/de.asm"
ELIF DEF(BUILD_FR)
    INCLUDE "src/home/text/locales/fr.asm"
ELIF DEF(BUILD_IT)
    INCLUDE "src/home/text/locales/it.asm"
ELIF DEF(BUILD_ES)
    INCLUDE "src/home/text/locales/es.asm"
ELSE
    FAIL "western text build requires BUILD_EN/DE/FR/IT/ES"
ENDC
