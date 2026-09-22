"""Bounded adversarial search for failure of all EFX-nine insertion constructions.

Every point uses the unrestricted exact oracle. Solver timeout is UNKNOWN.
No initial partition, locality radius, or predecessor-size restriction is imposed.
"""
import argparse, json, time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import z3
from search import variables, witness_constraints, extract
from oracle import oracle, verify_witness, integer_rows


def run(task):
    domain, seconds, directory = task
    v=variables(10)
    s=z3.SolverFor('QF_LRA');s.set(**{'smt.arith.solver':2})
    for row in v:s.add(*[x>=0 for x in row],z3.Sum(row)==1)
    # One simultaneous goods permutation, never independent row sorting.
    s.add(*[v[0][g]>=v[0][g+1] for g in range(9)])
    if domain=='near_identical':
        for i in range(1,4):
            for g in range(10):s.add(v[i][g]-v[0][g]<=z3.RealVal('1/100'),v[0][g]-v[i][g]<=z3.RealVal('1/100'))
    elif domain=='four_large':
        for row in v:
            s.add(*[row[g]>=z3.RealVal('1/8') for g in range(4)])
            s.add(*[row[g]<=z3.RealVal('1/32') for g in range(4,10)])
    elif domain!='general':raise ValueError(domain)
    # A common least good is already a provable positive case (given EFX-nine).
    # Therefore target the complementary region, including ties correctly.
    for g in range(10):
        s.add(z3.Or(*[v[i][h]<v[i][g] for i in range(4) for h in range(10) if h!=g]))
    start=time.time(); end=start+seconds; cases=[];status='UNKNOWN'; reason='wall budget'; last=None
    while time.time()<end:
        s.set(timeout=max(1,int(min(15,end-time.time())*1000)))
        r=s.check()
        if r==z3.unsat:status='COVERED_DOMAIN';reason='UNSAT';break
        if r!=z3.sat:reason=s.reason_unknown();break
        last=extract(s,v)
        q=oracle(last,limit=1,deadline=end)
        if q['status']=='ABSENT':status='MODE_C_COUNTEREXAMPLE';reason='all deletions and EFX ownership assignments exhausted';break
        if q['status']!='FOUND':reason='point oracle deadline';break
        w=q['witnesses'][0]
        assert verify_witness(integer_rows(last),w)
        cases.append({'values':last,'witness':w})
        s.add(z3.Not(z3.And(*witness_constraints(v,w,'extension'))))
    result={'domain':domain,'status':status,'reason':reason,'seconds':time.time()-start,
            'witness_count':len(cases),'last_model':last,'cases':cases,
            'scope':'all nonnegative additive normalized rows within stated domain; no common least good; row zero sorted by simultaneous goods relabeling'}
    Path(directory).mkdir(parents=True,exist_ok=True)
    Path(directory,domain+'.json').write_text(json.dumps(result,indent=2))
    return {k:x for k,x in result.items() if k not in ('last_model','cases')}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=120)
    p.add_argument('--out',default='experiment-results/mode-c-adversary');a=p.parse_args()
    with ProcessPoolExecutor(max_workers=3) as pool:
        for result in pool.map(run,[(d,a.seconds,a.out) for d in ['general','near_identical','four_large']]):print(json.dumps(result),flush=True)
