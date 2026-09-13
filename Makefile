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
	@echo "Disassembly status: 8 Gold reference releases registered."
	@echo "Japanese Rev 0/Rev A: Banks 00-3F."
	@echo "Korean/English/German/French/Italian/Spanish: Banks 00-7F."
	@echo "Bank-by-bank reconstruction ledger: manifests/bank_status.csv"
	@echo "Build targets will be enabled as reconstructed source becomes available."
