PYTHON ?= python3

.PHONY: help verify-reference status

help:
	@echo "PocketMonsters-Kin-Disassembly bootstrap targets"
	@echo "  make verify-reference ROM=/path/to/reference.gbc"
	@echo "  make status"

verify-reference:
	@test -n "$(ROM)" || (echo "ROM=/path/to/reference.gbc is required" && exit 2)
	$(PYTHON) tools/verify_reference_rom.py "$(ROM)"

status:
	@echo "Disassembly status: bootstrap complete; Bank 00-3F pending."
	@echo "Build target will be enabled as reconstructed source becomes available."
