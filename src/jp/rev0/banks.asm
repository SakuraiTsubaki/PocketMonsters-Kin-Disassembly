; Stage 0/1 matching baseline for Japanese Rev 0.
; Bank $00 vectors/entry are reconstructed source; remaining bytes are local-ROM INCBINs.

INCLUDE "src/common/bank00_vectors.asm"

SECTION "ROM Bank 00 header", ROM0[$0104]
INCBIN "baserom.gbc", $000104, $004c

SECTION "ROM Bank 00 body", ROM0[$0150]
INCBIN "baserom.gbc", $000150, $3eb0

SECTION "ROM Bank 01", ROMX[$4000], BANK[$01]
INCBIN "baserom.gbc", $004000, $4000

SECTION "ROM Bank 02", ROMX[$4000], BANK[$02]
INCBIN "baserom.gbc", $008000, $4000

SECTION "ROM Bank 03", ROMX[$4000], BANK[$03]
INCBIN "baserom.gbc", $00c000, $4000

SECTION "ROM Bank 04", ROMX[$4000], BANK[$04]
INCBIN "baserom.gbc", $010000, $4000

SECTION "ROM Bank 05", ROMX[$4000], BANK[$05]
INCBIN "baserom.gbc", $014000, $4000

SECTION "ROM Bank 06", ROMX[$4000], BANK[$06]
INCBIN "baserom.gbc", $018000, $4000

SECTION "ROM Bank 07", ROMX[$4000], BANK[$07]
INCBIN "baserom.gbc", $01c000, $4000

SECTION "ROM Bank 08", ROMX[$4000], BANK[$08]
INCBIN "baserom.gbc", $020000, $4000

SECTION "ROM Bank 09", ROMX[$4000], BANK[$09]
INCBIN "baserom.gbc", $024000, $4000

SECTION "ROM Bank 0A", ROMX[$4000], BANK[$0A]
INCBIN "baserom.gbc", $028000, $4000

SECTION "ROM Bank 0B", ROMX[$4000], BANK[$0B]
INCBIN "baserom.gbc", $02c000, $4000

SECTION "ROM Bank 0C", ROMX[$4000], BANK[$0C]
INCBIN "baserom.gbc", $030000, $4000

SECTION "ROM Bank 0D", ROMX[$4000], BANK[$0D]
INCBIN "baserom.gbc", $034000, $4000

SECTION "ROM Bank 0E", ROMX[$4000], BANK[$0E]
INCBIN "baserom.gbc", $038000, $4000

SECTION "ROM Bank 0F", ROMX[$4000], BANK[$0F]
INCBIN "baserom.gbc", $03c000, $4000

SECTION "ROM Bank 10", ROMX[$4000], BANK[$10]
INCBIN "baserom.gbc", $040000, $4000

SECTION "ROM Bank 11", ROMX[$4000], BANK[$11]
INCBIN "baserom.gbc", $044000, $4000

SECTION "ROM Bank 12", ROMX[$4000], BANK[$12]
INCBIN "baserom.gbc", $048000, $4000

SECTION "ROM Bank 13", ROMX[$4000], BANK[$13]
INCBIN "baserom.gbc", $04c000, $4000

SECTION "ROM Bank 14", ROMX[$4000], BANK[$14]
INCBIN "baserom.gbc", $050000, $4000

SECTION "ROM Bank 15", ROMX[$4000], BANK[$15]
INCBIN "baserom.gbc", $054000, $4000

SECTION "ROM Bank 16", ROMX[$4000], BANK[$16]
INCBIN "baserom.gbc", $058000, $4000

SECTION "ROM Bank 17", ROMX[$4000], BANK[$17]
INCBIN "baserom.gbc", $05c000, $4000

SECTION "ROM Bank 18", ROMX[$4000], BANK[$18]
INCBIN "baserom.gbc", $060000, $4000

SECTION "ROM Bank 19", ROMX[$4000], BANK[$19]
INCBIN "baserom.gbc", $064000, $4000

SECTION "ROM Bank 1A", ROMX[$4000], BANK[$1A]
INCBIN "baserom.gbc", $068000, $4000

SECTION "ROM Bank 1B", ROMX[$4000], BANK[$1B]
INCBIN "baserom.gbc", $06c000, $4000

SECTION "ROM Bank 1C", ROMX[$4000], BANK[$1C]
INCBIN "baserom.gbc", $070000, $4000

SECTION "ROM Bank 1D", ROMX[$4000], BANK[$1D]
INCBIN "baserom.gbc", $074000, $4000

SECTION "ROM Bank 1E", ROMX[$4000], BANK[$1E]
INCBIN "baserom.gbc", $078000, $4000

SECTION "ROM Bank 1F", ROMX[$4000], BANK[$1F]
INCBIN "baserom.gbc", $07c000, $4000

SECTION "ROM Bank 20", ROMX[$4000], BANK[$20]
INCBIN "baserom.gbc", $080000, $4000

SECTION "ROM Bank 21", ROMX[$4000], BANK[$21]
INCBIN "baserom.gbc", $084000, $4000

SECTION "ROM Bank 22", ROMX[$4000], BANK[$22]
INCBIN "baserom.gbc", $088000, $4000

SECTION "ROM Bank 23", ROMX[$4000], BANK[$23]
INCBIN "baserom.gbc", $08c000, $4000

SECTION "ROM Bank 24", ROMX[$4000], BANK[$24]
INCBIN "baserom.gbc", $090000, $4000

SECTION "ROM Bank 25", ROMX[$4000], BANK[$25]
INCBIN "baserom.gbc", $094000, $4000

SECTION "ROM Bank 26", ROMX[$4000], BANK[$26]
INCBIN "baserom.gbc", $098000, $4000

SECTION "ROM Bank 27", ROMX[$4000], BANK[$27]
INCBIN "baserom.gbc", $09c000, $4000

SECTION "ROM Bank 28", ROMX[$4000], BANK[$28]
INCBIN "baserom.gbc", $0a0000, $4000

SECTION "ROM Bank 29", ROMX[$4000], BANK[$29]
INCBIN "baserom.gbc", $0a4000, $4000

SECTION "ROM Bank 2A", ROMX[$4000], BANK[$2A]
INCBIN "baserom.gbc", $0a8000, $4000

SECTION "ROM Bank 2B", ROMX[$4000], BANK[$2B]
INCBIN "baserom.gbc", $0ac000, $4000

SECTION "ROM Bank 2C", ROMX[$4000], BANK[$2C]
INCBIN "baserom.gbc", $0b0000, $4000

SECTION "ROM Bank 2D", ROMX[$4000], BANK[$2D]
INCBIN "baserom.gbc", $0b4000, $4000

SECTION "ROM Bank 2E", ROMX[$4000], BANK[$2E]
INCBIN "baserom.gbc", $0b8000, $4000

SECTION "ROM Bank 2F", ROMX[$4000], BANK[$2F]
INCBIN "baserom.gbc", $0bc000, $4000

SECTION "ROM Bank 30", ROMX[$4000], BANK[$30]
INCBIN "baserom.gbc", $0c0000, $4000

SECTION "ROM Bank 31", ROMX[$4000], BANK[$31]
INCBIN "baserom.gbc", $0c4000, $4000

SECTION "ROM Bank 32", ROMX[$4000], BANK[$32]
INCBIN "baserom.gbc", $0c8000, $4000

SECTION "ROM Bank 33", ROMX[$4000], BANK[$33]
INCBIN "baserom.gbc", $0cc000, $4000

SECTION "ROM Bank 34", ROMX[$4000], BANK[$34]
INCBIN "baserom.gbc", $0d0000, $4000

SECTION "ROM Bank 35", ROMX[$4000], BANK[$35]
INCBIN "baserom.gbc", $0d4000, $4000

SECTION "ROM Bank 36", ROMX[$4000], BANK[$36]
INCBIN "baserom.gbc", $0d8000, $4000

SECTION "ROM Bank 37", ROMX[$4000], BANK[$37]
INCBIN "baserom.gbc", $0dc000, $4000

SECTION "ROM Bank 38", ROMX[$4000], BANK[$38]
INCBIN "baserom.gbc", $0e0000, $4000

SECTION "ROM Bank 39", ROMX[$4000], BANK[$39]
INCBIN "baserom.gbc", $0e4000, $4000

SECTION "ROM Bank 3A", ROMX[$4000], BANK[$3A]
INCBIN "baserom.gbc", $0e8000, $4000

SECTION "ROM Bank 3B", ROMX[$4000], BANK[$3B]
INCBIN "baserom.gbc", $0ec000, $4000

SECTION "ROM Bank 3C", ROMX[$4000], BANK[$3C]
INCBIN "baserom.gbc", $0f0000, $4000

SECTION "ROM Bank 3D", ROMX[$4000], BANK[$3D]
INCBIN "baserom.gbc", $0f4000, $4000

SECTION "ROM Bank 3E", ROMX[$4000], BANK[$3E]
INCBIN "baserom.gbc", $0f8000, $4000

SECTION "ROM Bank 3F", ROMX[$4000], BANK[$3F]
INCBIN "baserom.gbc", $0fc000, $4000
