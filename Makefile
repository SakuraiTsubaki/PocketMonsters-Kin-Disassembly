PYTHON ?= python3
RGBASM ?= rgbasm
RGBLINK ?= rgblink
BUILD_DIR ?= build

ROM_REV0 ?= baserom.gbc
ROM_REVA ?= baserom_rev_a.gbc

.PHONY: all rev0 reva verify-rev0 verify-reva clean

all: rev0 reva

$(BUILD_DIR):
	@mkdir -p $@

$(BUILD_DIR)/kin-rev0.o: main.asm src/common/bank00_vectors.asm src/jp/rev0/banks.asm | $(BUILD_DIR)
	$(RGBASM) -o $@ main.asm

$(BUILD_DIR)/kin-rev0.gbc: $(BUILD_DIR)/kin-rev0.o
	$(RGBLINK) -o $@ $<

$(BUILD_DIR)/kin-reva.o: main.asm src/common/bank00_vectors.asm src/jp/rev_a/banks.asm | $(BUILD_DIR)
	$(RGBASM) -DREV_A=1 -o $@ main.asm

$(BUILD_DIR)/kin-reva.gbc: $(BUILD_DIR)/kin-reva.o
	$(RGBLINK) -o $@ $<

rev0: $(BUILD_DIR)/kin-rev0.gbc verify-rev0
reva: $(BUILD_DIR)/kin-reva.gbc verify-reva

verify-rev0: $(BUILD_DIR)/kin-rev0.gbc
	$(PYTHON) tools/verify_match.py $(ROM_REV0) $<

verify-reva: $(BUILD_DIR)/kin-reva.gbc
	$(PYTHON) tools/verify_match.py $(ROM_REVA) $<

clean:
	rm -rf $(BUILD_DIR) out
