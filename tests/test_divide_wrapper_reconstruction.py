import csv,hashlib,json,unittest
from pathlib import Path
R=Path(__file__).parents[1];E={'kin-jp-rev0':(0x3185,0x6B10),'kin-jp-rev1':(0x3185,0x6B10),'gold-ko-rev0':(0x3267,0x68F8),'gold-en-rev0':(0x31C9,0x681D),'gold-de-rev0':(0x31F6,0x6854),'gold-es-rev0':(0x31ED,0x6865),'gold-fr-rev0':(0x31DB,0x6852),'gold-it-rev0':(0x31EE,0x684F)}
class T(unittest.TestCase):
 def test_releases(self):
  rows={x['id']:x for x in csv.DictReader((R/'research/releases.csv').read_text().splitlines())};self.assertEqual(set(rows),set(E))
  for k,(a,t) in E.items():
   m=json.loads((R/f'analysis/{k}-divide-wrapper.json').read_text());f=m['function'];d=json.loads((R/f'analysis/{k}-multiply-wrapper.json').read_text());self.assertEqual(m['target']['sha256'],rows[k]['sha256']);self.assertEqual((f['bank'],f['address'],f['length']),(0,a,18));self.assertEqual(f['rom_offset'],d['function']['range_end_exclusive']);self.assertEqual(f['home_call']['target']['bank'],1);self.assertEqual(f['home_call']['target']['address'],t);self.assertEqual(f['home_call']['saved_rom_bank_hram_address'],0xFF9F);self.assertEqual(f['preserved_registers'],['AF','BC','DE','HL']);self.assertFalse(m['raw_rom_bytes_included'])
 def test_manifest(self):
  m=json.loads((R/'manifests/divide-wrapper-reconstruction.json').read_text());[self.assertEqual(hashlib.sha256((R/o['path']).read_bytes()).hexdigest(),o['sha256'])for o in m['outputs']]
if __name__=='__main__':unittest.main()
