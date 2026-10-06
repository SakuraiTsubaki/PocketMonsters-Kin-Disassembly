import hashlib, json, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
EXPECTED={'de':'542f275f8632ef5265e5cde80a8ba1f0ec11ce714ef9d773088a92680bd17d73','fr':'6103cadf2ae505f4b489a8a414c8db27a2307d797ddf8a3a848659b591dd4023','it':'367e606f82b9e2e16d0cc8011c5ba2df1862da574e57ffd66e786a82af5b6e22','es':'7b78e33a348a0729e38ee0fd778cf49b3e07c35d2175ebc74d8f9be41f41455b'}
class Tests(unittest.TestCase):
 def test_languages(self):
  for lang,digest in EXPECTED.items():
   c=json.loads((ROOT/f'analysis/kin-{lang}-startup-cfg.json').read_text());self.assertEqual(c['source_sha256'],digest);self.assertEqual([b['start_address'] for b in c['blocks']],[0x5c6,0x5ca,0x5cd,0x5cf,0x5fc]);self.assertTrue(all('block_bytes' not in b for b in c['blocks']))
 def test_manifests(self):
  for lang in EXPECTED:
   m=json.loads((ROOT/f'manifests/{lang}-startup-cfg.json').read_text());self.assertFalse(m['raw_rom_bytes_included']);[self.assertEqual(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest(),o['sha256']) for o in m['outputs']]
if __name__=='__main__':unittest.main()
