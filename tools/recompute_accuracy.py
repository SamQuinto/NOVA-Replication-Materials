"""Recompute aggregate A/B results from authorized saved checks. No API calls."""
import argparse,json,math
from collections import defaultdict
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--checks',type=Path,required=True);a=p.parse_args()
data=json.loads(a.checks.read_text(encoding='utf-8-sig'));groups=defaultdict(list)
for r in data:
    x=r.get('check',r);groups[x.get('scorer',x.get('configuration','Unknown'))].append(x)
for scorer,rows in groups.items():
    def flag(r,new,old):return bool(r.get(new,r.get(old,False)))
    n=len(rows);k=sum(not(flag(r,'type_a','type1') or flag(r,'type_b','type2') or r.get('technical_error',False)) for r in rows)
    z=1.959963984540054;prop=k/n;d=1+z*z/n;mid=(prop+z*z/(2*n))/d;half=z*math.sqrt(prop*(1-prop)/n+z*z/(4*n*n))/d
    print(json.dumps(dict(scorer=scorer,n=n,passes=k,accuracy=prop,ci95=[mid-half,min(1,mid+half)],type_a=sum(flag(r,'type_a','type1') for r in rows),type_b=sum(flag(r,'type_b','type2') for r in rows))))
