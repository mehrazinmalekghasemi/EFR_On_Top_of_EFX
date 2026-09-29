"""Exact bounded SAT probe of template 1125_041, excluding all drop-one bridges."""
import json,time
from pathlib import Path
from itertools import product
import z3
from efr.eight_plus_two import drop_one_bridges,search
from efr.oracle import is_efx,integer_rows

def run():
    A=[1,2,12,496];edges={(0,1),(2,0)}
    v=[[z3.Real(f'v_{i}_{g}') for g in range(10)] for i in range(4)]
    goods=lambda b:[g for g in range(10) if b>>g&1]
    val=lambda i,b:z3.Sum([v[i][g] for g in goods(b)])
    efx=lambda B:z3.And([val(i,B[i])>=val(i,B[j]^(1<<h)) for i,j in product(range(4),repeat=2) if i!=j for h in goods(B[j])])
    efr=lambda B:z3.And([B[j].bit_count()*val(i,B[i])>=max(B[j].bit_count()-1,0)*val(i,B[j]) for i,j in product(range(4),repeat=2) if i!=j])
    s=z3.Solver();s.set(timeout=20000)
    s.add(*[x>=0 for row in v for x in row],efx(A))
    for i in range(4):
        s.add(val(i,A[i])==100,v[i][9]<=100)
        for j in range(4):
            if i!=j:s.add(val(i,A[j])>100 if (i,j) in edges else val(i,A[j])<=100)
    for p in range(4):
        B=A.copy();B[p]|=512;s.add(z3.Not(efr(B)))
    for t,b in enumerate(A):
        for h in goods(b):
            C=A.copy();C[t]^=1<<h
            for p,q in product(range(4),repeat=2):
                B=C.copy();B[p]|=512;B[q]|=1<<h
                s.add(z3.Not(z3.And(efx(C),efr(B))))
    start=time.monotonic();status=s.check()
    out=dict(status=str(status),seconds=time.monotonic()-start,initial=A,omitted=9,
             scope='Normalized template 1125_041; excludes only direct insertion and all local drop-one EFX8 bridges')
    if status==z3.sat:
        m=s.model();V=[[str(m.eval(x)) for x in row] for row in v];out['values']=V
        assert is_efx(integer_rows(V),A) and not drop_one_bridges(V,A,9)
        out['unrestricted_bridge']=search(V)
    elif status==z3.unknown:out['reason']=s.reason_unknown()
    return out

if __name__=='__main__':
    out=run();p=Path(__file__).resolve().parents[2]/'experiment-results/eight-plus-two/no-local-1125.json'
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
