PYTHON ?= python3

.PHONY: help verify-reference analyze-bank00 test-bank00-vectors status

help:
	@echo "PocketMonsters-Kin-Disassembly targets"
	@echo "  make verify-reference ROM=/path/to/reference.gbc"
	@echo "  make analyze-bank00 ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-vectors ROMDIR=/path/to/reference-rom-directory"
	@echo "  make status"

verify-reference:
	@test -n "$(ROM)" || (echo "ROM=/path/to/reference.gbc is required" && exit 2)
	$(PYTHON) tools/verify_reference_rom.py "$(ROM)"

analyze-bank00:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tools/analyze_bank00.py --rom-dir "$(ROMDIR)"

test-bank00-vectors:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_vectors.py --rom-dir "$(ROMDIR)"

status:
	@echo "Disassembly status: 8 Gold reference releases registered."
	@echo "Japanese Rev 0/Rev A: Banks 00-3F."
	@echo "Korean/English/German/French/Italian/Spanish: Banks 00-7F."
	@echo "Bank 00: cross-release vector/header survey complete; reconstruction in progress."
	@echo "Bank-by-bank reconstruction ledger: manifests/bank_status.csv"
	@echo "Build targets will be enabled as reconstructed source becomes available."
