PYTHON ?= python3

.PHONY: help verify-reference analyze-bank00 map-bank00-modules test-bank00-vectors test-bank00-vblank test-bank00-delay test-bank00-time-palettes-fade test-bank00-lcd test-bank00-time test-bank00-init test-bank00-serial test-bank00-joypad test-bank00-decompress test-bank00-palettes test-bank00-gfx test-bank00-text-ranges status

help:
	@echo "PocketMonsters-Kin-Disassembly targets"
	@echo "  make verify-reference ROM=/path/to/reference.gbc"
	@echo "  make analyze-bank00 ROMDIR=/path/to/reference-rom-directory"
	@echo "  make map-bank00-modules ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-vectors ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-vblank ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-delay ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-time-palettes-fade ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-lcd ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-time ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-init ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-serial ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-joypad ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-decompress ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-palettes ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-gfx ROMDIR=/path/to/reference-rom-directory"
	@echo "  make test-bank00-text-ranges ROMDIR=/path/to/reference-rom-directory"
	@echo "  make status"

verify-reference:
	@test -n "$(ROM)" || (echo "ROM=/path/to/reference.gbc is required" && exit 2)
	$(PYTHON) tools/verify_reference_rom.py "$(ROM)"

analyze-bank00:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tools/analyze_bank00.py --rom-dir "$(ROMDIR)"

map-bank00-modules:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tools/map_bank00_modules.py --rom-dir "$(ROMDIR)"

test-bank00-vectors:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_vectors.py --rom-dir "$(ROMDIR)"

test-bank00-vblank:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_vblank.py --rom-dir "$(ROMDIR)"

test-bank00-delay:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_delay.py --rom-dir "$(ROMDIR)"

test-bank00-time-palettes-fade:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_time_palettes_fade.py --rom-dir "$(ROMDIR)"

test-bank00-lcd:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_lcd.py --rom-dir "$(ROMDIR)"

test-bank00-time:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_time.py --rom-dir "$(ROMDIR)"

test-bank00-init:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_init.py --rom-dir "$(ROMDIR)"

test-bank00-serial:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_serial.py --rom-dir "$(ROMDIR)"

test-bank00-joypad:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_joypad.py --rom-dir "$(ROMDIR)"

test-bank00-decompress:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_decompress.py --rom-dir "$(ROMDIR)"

test-bank00-palettes:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_palettes.py --rom-dir "$(ROMDIR)"

test-bank00-gfx:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_gfx.py --rom-dir "$(ROMDIR)"

test-bank00-text-ranges:
	@test -n "$(ROMDIR)" || (echo "ROMDIR=/path/to/reference-rom-directory is required" && exit 2)
	$(PYTHON) tests/test_bank00_text_ranges.py --rom-dir "$(ROMDIR)"

status:
	@echo "Disassembly status: 8 Gold reference releases registered."
	@echo "Japanese Rev 0/Rev A: Banks 00-3F."
	@echo "Korean/English/German/French/Italian/Spanish: Banks 00-7F."
	@echo "Bank 00: 52 ROM0 module boundaries mapped."
	@echo "Bank 00 source reconstructed through gfx; text family reconstruction is in progress."
	@echo "Bank-by-bank reconstruction ledger: manifests/bank_status.csv"
	@echo "Bank 00 module ledger: analysis/bank00/module_status.csv"
	@echo "Full byte-perfect build status remains open until complete RGBDS constants/macros/layout are reconstructed."
