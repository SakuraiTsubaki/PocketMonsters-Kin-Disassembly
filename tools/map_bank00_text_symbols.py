#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from difflib import SequenceMatcher
from pathlib import Path

BANK_SIZE = 0x4000

# Audited English Gold Bank 00 text symbols (pret/pokegold symbols used only
# to name the English addresses; target addresses are derived from ROM bytes).
EN_SYMBOLS = [
    ("ClearBox", 0x0EBD), ("ClearTilemap", 0x0ECF), ("ClearScreen", 0x0EE2),
    ("Textbox", 0x0EEF), ("TextboxBorder", 0x0EF8), ("TextboxPalette", 0x0F2B),
    ("SpeechTextbox", 0x0F45), ("GameFreakText", 0x0F4F), ("RadioTerminator", 0x0F59),
    ("PrintText", 0x0F5E), ("PrintTextboxText", 0x0F61), ("SetUpTextbox", 0x0F68),
    ("PlaceString", 0x0F74), ("PlaceNextChar", 0x0F75), ("DummyChar", 0x0F7E),
    ("NextChar", 0x0F7F), ("CheckDict", 0x0F83), ("PrintMomsName", 0x1066),
    ("PrintPlayerName", 0x106D), ("PrintRivalName", 0x1074), ("PrintRedsName", 0x107B),
    ("PrintGreensName", 0x1082), ("TrainerChar", 0x1089), ("TMChar", 0x1090),
    ("PCChar", 0x1097), ("RocketChar", 0x109E), ("PlacePOKe", 0x10A5),
    ("PlaceKougeki", 0x10AC), ("SixDotsChar", 0x10B3), ("PlacePKMN", 0x10BA),
    ("PlacePOKE", 0x10C1), ("PlaceJPRoute", 0x10C8), ("PlaceWatashi", 0x10CF),
    ("PlaceKokoWa", 0x10D6), ("PlaceMoveTargetsName", 0x10DD),
    ("PlaceMoveUsersName", 0x10E3), ("PlaceBattlersName", 0x10E5),
    ("PlaceEnemysName", 0x10FB), ("PlaceCommandCharacter", 0x1132),
    ("TMCharText", 0x113B), ("NextLineChar", 0x116D), ("LineFeedChar", 0x1176),
    ("LineChar", 0x117F), ("Paragraph", 0x1187), ("_ContText", 0x11B0),
    ("_ContTextNoPause", 0x11C8), ("ContText", 0x11D6), ("PlaceDexEnd", 0x11E7),
    ("PromptText", 0x11EB), ("DoneText", 0x1205), ("NullChar", 0x120C),
    ("TextScroll", 0x121D), ("Text_WaitBGMap", 0x123A), ("Diacritic", 0x124A),
    ("LoadBlinkingCursor", 0x1255), ("UnloadBlinkingCursor", 0x125B),
    ("PlaceFarString", 0x1261), ("PokeFluteTerminator", 0x126D),
    ("PrintTextboxTextAt", 0x1272), ("DoTextUntilTerminator", 0x1283),
    ("TextCommands", 0x129D), ("TextCommand_START", 0x12CB),
    ("TextCommand_RAM", 0x12D6), ("TextCommand_FAR", 0x12E2),
    ("TextCommand_BCD", 0x12FD), ("TextCommand_MOVE", 0x130D),
    ("TextCommand_BOX", 0x1318), ("TextCommand_LOW", 0x1328),
    ("TextCommand_PROMPT_BUTTON", 0x132C), ("TextCommand_SCROLL", 0x1342),
    ("TextCommand_START_ASM", 0x1351), ("TextCommand_DECIMAL", 0x1352),
    ("TextCommand_PAUSE", 0x136D), ("TextCommand_SOUND", 0x1380),
    ("TextCommand_CRY", 0x13A2), ("TextSFX", 0x13AD),
    ("TextCommand_DOTS", 0x13C3), ("TextCommand_WAIT_BUTTON", 0x13E2),
    ("TextCommand_STRINGBUFFER", 0x13EA), ("TextCommand_DAY", 0x1402),
    ("WeekdayPointers", 0x1422), ("WeekdaySunday", 0x1430), ("TextEnd", 0x1458),
]

WESTERN_IDS = ("en", "de", "fr", "it", "es")


def load_manifest(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["releases"]


def load_banks(rom_dir: Path, releases: list[dict]) -> dict[str, bytes]:
    wanted = {r["id"]: r for r in releases if r["id"] in WESTERN_IDS}
    missing = set(WESTERN_IDS) - set(wanted)
    if missing:
        raise SystemExit(f"manifest missing western releases: {sorted(missing)}")
    banks = {}
    for rid in WESTERN_IDS:
        path = rom_dir / wanted[rid]["reference_filename"]
        if not path.is_file():
            raise SystemExit(f"missing reference ROM: {path}")
        banks[rid] = path.read_bytes()[:BANK_SIZE]
    return banks


def map_addr(addr: int, blocks):
    for block in blocks:
        if block.a <= addr < block.a + block.size:
            return block.b + (addr - block.a), "exact"
    prev = next((b for b in reversed(blocks) if b.a + b.size <= addr), None)
    nxt = next((b for b in blocks if b.a > addr), None)
    if prev and nxt:
        pd = prev.b - prev.a
        nd = nxt.b - nxt.a
        if pd == nd:
            return addr + pd, "inferred_same_delta"
        if addr - (prev.a + prev.size) <= 8:
            return addr + pd, "near_prev"
        if nxt.a - addr <= 8:
            return addr + nd, "near_next"
    return None, "unresolved"


def main() -> int:
    ap = argparse.ArgumentParser(description="Map English Bank 00 text symbols into western Gold ROMs.")
    ap.add_argument("--rom-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=Path("manifests/rom_baselines.json"))
    ap.add_argument("--out", type=Path, default=Path("analysis/bank00/text_symbol_candidates.csv"))
    args = ap.parse_args()

    banks = load_banks(args.rom_dir, load_manifest(args.manifest))
    reference = banks["en"]
    blocks = {
        rid: None if rid == "en" else SequenceMatcher(None, reference, banks[rid], autojunk=False).get_matching_blocks()
        for rid in WESTERN_IDS
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["symbol", "en"]
    for rid in WESTERN_IDS[1:]:
        fields += [rid, rid + "_confidence"]

    with args.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for name, addr in EN_SYMBOLS:
            row = [name, f"0x{addr:04X}"]
            for rid in WESTERN_IDS[1:]:
                mapped, confidence = map_addr(addr, blocks[rid])
                row += ["" if mapped is None else f"0x{mapped:04X}", confidence]
            w.writerow(row)

    print(f"wrote {args.out}")
    print("NOTE: repeated identical routines can produce ambiguous exact candidates; audit semantic labels against ROM control flow before finalizing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
