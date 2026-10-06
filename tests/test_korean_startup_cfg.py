import hashlib, json, unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class KoreanStartupCfgTests(unittest.TestCase):
    def test_cfg_is_publication_safe_and_split_at_shared_entry(self):
        cfg = json.loads((ROOT / "analysis/kin-ko-startup-cfg.json").read_text())
        self.assertEqual(cfg["source_sha256"], "9c273e86e6120c6a038160ccb0153b8b20425b84fc08a496281c1d1bcac492f6")
        self.assertEqual([b["start_address"] for b in cfg["blocks"]], [0x05CA, 0x05CE, 0x05D3, 0x05DB, 0x05DC, 0x0609])
        self.assertEqual(cfg["blocks"][3]["terminator"], "fallthrough $05dc")
        self.assertEqual(cfg["blocks"][4]["instructions"][17]["source"], "ld [$cec0], a")
        self.assertTrue(all("block_bytes" not in block for block in cfg["blocks"]))
        self.assertFalse(any("bytes" in instruction for block in cfg["blocks"] for instruction in block["instructions"]))

    def test_manifest_hashes_outputs(self):
        manifest = json.loads((ROOT / "manifests/korean-startup-cfg.json").read_text())
        self.assertFalse(manifest["raw_rom_bytes_included"])
        for output in manifest["outputs"]:
            self.assertEqual(hashlib.sha256((ROOT / output["path"]).read_bytes()).hexdigest(), output["sha256"])


if __name__ == "__main__": unittest.main()
