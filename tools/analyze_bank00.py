#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha1, sha256
import csv, json, itertools

ROOT=Path('/mnt/data')
RELEASES=[
 ('jp-rev0','Pocket Monsters Kin (Japan).gbc'),
 ('jp-revA','Pocket Monsters Kin (Japan) (Rev A).gbc'),
 ('kr','Pocket Monsters Geum (Korea).gbc'),
 ('en','Pokemon - Gold Version (USA, Europe).gbc'),
 ('de','Pokemon - Goldene Edition (Germany).gbc'),
 ('fr','Pokemon - Version Or (France).gbc'),
 ('it','Pokemon - Versione Oro (Italy).gbc'),
 ('es','Pokemon - Edicion Oro (Spain).gbc'),
]
BANK=0x4000
roms={rid:(ROOT/fn).read_bytes() for rid,fn in RELEASES}
banks={rid:data[:BANK] for rid,data in roms.items()}

def ranges(indices):
    if not indices:return []
    out=[]; s=p=indices[0]
    for x in indices[1:]:
        if x==p+1:p=x;continue
        out.append((s,p));s=p=x
    out.append((s,p));return out

def clusters_vs(ref, other):
    idx=[i for i,(a,b) in enumerate(zip(banks[ref],banks[other])) if a!=b]
    return idx,ranges(idx)

summary=[]
for rid,_ in RELEASES:
    b=banks[rid]
    summary.append({
        'release':rid,'bank':'00','size':len(b),'sha1':sha1(b).hexdigest(),'sha256':sha256(b).hexdigest(),
        'entry_0100_0103':b[0x100:0x104].hex().upper(),
        'title_raw':b[0x134:0x143].hex().upper(),
        'title_ascii':''.join(chr(x) if 32<=x<127 else '.' for x in b[0x134:0x143]),
        'game_code':bytes(b[0x13F:0x143]).decode('ascii','replace'),
        'cgb_flag':f'{b[0x143]:02X}','sgb_flag':f'{b[0x146]:02X}',
        'cart_type':f'{b[0x147]:02X}','rom_size_code':f'{b[0x148]:02X}','ram_size_code':f'{b[0x149]:02X}',
        'destination':f'{b[0x14A]:02X}','version':f'{b[0x14C]:02X}','header_checksum':f'{b[0x14D]:02X}',
        'global_checksum':f'{b[0x14E]:02X}{b[0x14F]:02X}',
    })

pairwise=[]
for (a,_),(b,__) in itertools.combinations(RELEASES,2):
    idx,rs=clusters_vs(a,b)
    pairwise.append({'a':a,'b':b,'different_bytes':len(idx),'different_ranges':len(rs),'first_diff':f'0x{idx[0]:04X}' if idx else '', 'last_diff':f'0x{idx[-1]:04X}' if idx else ''})

variable=[]
for i in range(BANK):
    vals={banks[r][i] for r,_ in RELEASES}
    if len(vals)>1: variable.append(i)
var_ranges=ranges(variable)
range_rows=[]
for s,e in var_ranges:
    range_rows.append({'start':f'0x{s:04X}','end':f'0x{e:04X}','length':e-s+1,'distinct_patterns':len({banks[r][s:e+1] for r,_ in RELEASES})})

hash_groups={}
for rid,_ in RELEASES:
    h=sha1(banks[rid]).hexdigest(); hash_groups.setdefault(h,[]).append(rid)

out={'summary':summary,'pairwise':pairwise,'variable_byte_count':len(variable),'variable_ranges':range_rows,'bank_hash_groups':list(hash_groups.values())}
(ROOT/'bank00_analysis.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'bank00_summary.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys());w.writeheader();w.writerows(summary)
with (ROOT/'bank00_pairwise.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=pairwise[0].keys());w.writeheader();w.writerows(pairwise)
with (ROOT/'bank00_variable_ranges.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=range_rows[0].keys());w.writeheader();w.writerows(range_rows)

print(json.dumps(out,ensure_ascii=False,indent=2))
