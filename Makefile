PYTHON ?= python3
RGBASM ?= rgbasm
RGBLINK ?= rgblink

ROM ?= baserom.gbc
BUILD_DIR ?= build
TARGET ?= pocketmonsters-kin
BANKS_ASM := src/banks.asm
OBJECT := $(BUILD_DIR)/main.o
OUTPUT := $(BUILD_DIR)/$(TARGET).gbc

.PHONY: all bootstrap inspect verify clean

all: $(OUTPUT) verify

bootstrap: $(BANKS_ASM)

inspect:
	$(PYTHON) tools/inspect_rom.py $(ROM) --json out/rom-report.json

$(BANKS_ASM): $(ROM) tools/bootstrap_incbin.py
	$(PYTHON) tools/bootstrap_incbin.py $(ROM) --output $(BANKS_ASM) --manifest out/incbin-banks.json

$(OBJECT): main.asm $(BANKS_ASM)
	@mkdir -p $(BUILD_DIR)
	$(RGBASM) -o $@ main.asm

$(OUTPUT): $(OBJECT)
	$(RGBLINK) -o $@ $<

verify: $(OUTPUT)
	$(PYTHON) tools/verify_match.py $(ROM) $(OUTPUT)

clean:
	rm -rf $(BUILD_DIR) out $(BANKS_ASM)
