import csv,hashlib,json,unittest
from pathlib import Path
R=Path(__file__).parents[1];E={'kin-jp-rev0':(0x6AB0,0x6B10),'kin-jp-rev1':(0x6AB0,0x6B10),'gold-ko-rev0':(0x6898,0x68F8),'gold-en-rev0':(0x67BD,0x681D),'gold-de-rev0':(0x67F4,0x6854),'gold-es-rev0':(0x6805,0x6865),'gold-fr-rev0':(0x67F2,0x6852),'gold-it-rev0':(0x67EF,0x684F)};H='cfceda1a48a109a1b1e7df95eab6391c73dae4338c637ddf0f411779c60a75d4'
class T(unittest.TestCase):
 def test_releases(self):
  rows={x['id']:x for x in csv.DictReader((R/'research/releases.csv').read_text().splitlines())};self.assertEqual(set(rows),set(E))
  for k,(s,e) in E.items():
   m=json.loads((R/f'analysis/{k}-multiply-core.json').read_text());f=m['function'];w=json.loads((R/f'analysis/{k}-multiply-wrapper.json').read_text());d=json.loads((R/f'analysis/{k}-divide-wrapper.json').read_text());self.assertEqual(m['target']['sha256'],rows[k]['sha256']);self.assertEqual((f['bank'],f['address'],f['rom_offset'],f['range_end_exclusive'],f['length']),(1,s,s,e,96));self.assertEqual(f['code_sha256'],H);self.assertEqual(s,w['function']['far_call']['target']['rom_offset']);self.assertEqual(e,d['function']['home_call']['target']['rom_offset']);self.assertEqual(f['hram_layout']['multiplier'],0xFFB9);self.assertFalse(m['raw_rom_bytes_included'])
 def test_manifest(self):
  m=json.loads((R/'manifests/multiply-core-reconstruction.json').read_text());[self.assertEqual(hashlib.sha256((R/o['path']).read_bytes()).hexdigest(),o['sha256'])for o in m['outputs']]
if __name__=='__main__':unittest.main()
