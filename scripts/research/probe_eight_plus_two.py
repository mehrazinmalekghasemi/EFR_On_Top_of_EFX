"""Reproduce fixed-instance EFX-8/EFR-10 bridge checks; no universal verdict."""
import json
from pathlib import Path
from efr.eight_plus_two import search,drop_one_bridges
from efr.oracle import is_efx,integer_rows

SOURCES=[
 'experiment-results/template-1125-041/witnesses.json',
 'experiment-results/restoration/obstruction-1125.json',
 'experiment-results/two-source/verified-obstruction.json',
 'experiment-results/restoration/obstruction-1224.json',
 'experiment-results/dangerous-items/sole-champion-witnesses.json',
]

def run():
    root=Path(__file__).resolve().parents[2];out=[]
    for source in SOURCES:
        data=json.loads((root/source).read_text())
        for index,w in enumerate(data if isinstance(data,list) else [data]):
            V=w['values'];A=w['initial'];g=w.get('omitted',9)
            local=drop_one_bridges(V,A,g);removable=[]
            for t,b in enumerate(A):
                for h in range(10):
                    if b>>h&1:
                        C=A.copy();C[t]^=1<<h
                        if is_efx(integer_rows(V),C):removable.append(h)
            narrow=[]
            if sorted(b.bit_count() for b in A)==[1,1,2,5]:
                donor=next(i for i,b in enumerate(A) if b.bit_count()==5)
                narrow=[x for x in local if A[donor]>>x['missing'][1]&1
                        and len(set(x['recipients']))==2 and donor not in x['recipients']]
            out.append(dict(source=source,index=index,profile=sorted(b.bit_count() for b in A),
                removable_goods=removable,local_count=len(local),
                local_witness=local[0] if local else None,narrow_menu_count=len(narrow),
                search=search(V,seconds=30)))
    bad=[[1]*8+[100,100] for _ in range(4)]
    return dict(scope='Fifteen retained rational instances; no family or universal certificate',
                instances=out,arbitrary_pair_counterexample=dict(values=bad,fixed=search(bad,[8,9]),free=search(bad)))

if __name__=='__main__':
    result=run();dest=Path(__file__).resolve().parents[2]/'experiment-results/eight-plus-two/results.json'
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,indent=2)+'\n')
    for w in result['instances']:
        print(w['profile'],w['index'],'removable',len(w['removable_goods']),'local',w['local_count'],'narrow',w['narrow_menu_count'],w['search']['status'])
