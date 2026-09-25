"""Targeted CEGAR for failure of a stated two-bundle repair rule.

Not an exhaustive EFR existence search. A SAT obstruction is independently
enumerated by two_source_moves; complete EFR may still exist elsewhere.
"""
import argparse,json,time
from pathlib import Path
import z3
from structural_reductions import catalog
from structural_efr_search import build
from search import sv,efx_constraints,witness_constraints,extract
from oracle import integer_rows,oracle
from two_source_moves import local_moves


def compensation_cuts(s,v,A):
    own=[sv(v[i],A[i]) for i in range(4)]
    count=0
    for k in range(4):
        if A[k].bit_count()!=2:continue
        for i in range(4):
            if i==k or A[i].bit_count()<2:continue
            for h in range(9):
                if not A[k]>>h&1:continue
                for y in range(9):
                    if A[i]>>y&1:
                        s.add(z3.Or(v[i][9]+v[i][h]<=own[i],v[k][y]<v[k][h]));count+=1
    return count


def run(case_id,seconds=60,dominance='pareto'):
    case=next(c for c in catalog()[0] if c['id']==case_id)
    s,v=build(case);A=case['initial'];own=[sv(v[i],A[i]) for i in range(4)]
    for row in v:s.add(*[x>0 for x in row])
    compensation_count=compensation_cuts(s,v,A)
    deadline=time.monotonic()+seconds;cuts=[];status='OPEN';values=None;diagnostic=None
    while time.monotonic()<deadline:
        s.set(timeout=max(1,int(1000*min(10,deadline-time.monotonic()))));r=s.check()
        if r==z3.unsat:status='UNSAT_REPLAY_PENDING';break
        if r!=z3.sat:break
        values=extract(s,v);diagnostic=local_moves(values,A,9,dominance=dominance)
        if diagnostic['status']=='ABSENT':status='TWO_BUNDLE_OBSTRUCTION';break
        move=diagnostic['moves'][0];B=move['allocation']
        if move['kind']=='complete_efr':good=z3.And(*witness_constraints(v,{'allocation':B},'efr'))
        else:
            new=[sv(v[i],B[i]) for i in range(4)]
            if dominance=='pareto':better=z3.And(*[new[i]>=own[i] for i in range(4)],z3.Or(*[new[i]>own[i] for i in range(4)]))
            else:better=z3.Or(*[z3.And(*[new[j]==own[j] for j in range(i)],new[i]>own[i]) for i in range(4)])
            good=z3.And(*efx_constraints(v,B),better)
        s.add(z3.Not(good));cuts.append(move)
    result={'case':case,'status':status,'dominance':dominance,'seconds_budget':seconds,'compensation_cuts':compensation_count,'cuts':cuts,'values':values,'diagnostic':diagnostic,'scope':'Failure of two-bundle repair only; NOT an EFR or Mode C counterexample'}
    if values is not None:result['integer_values']=integer_rows(values)
    if status=='TWO_BUNDLE_OBSTRUCTION':result['unrestricted_oracle']=oracle(values,limit=1,deadline=time.time()+30)
    directory=Path('experiment-results/two-source');directory.mkdir(parents=True,exist_ok=True)
    (directory/(case_id+'-'+dominance+'.json')).write_text(json.dumps(result,indent=2))
    if status=='UNSAT_REPLAY_PENDING':(directory/(case_id+'-'+dominance+'.smt2')).write_text(s.to_smt2())
    return {k:result[k] for k in ['status','dominance','integer_values'] if k in result}|{'cut_count':len(cuts)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',default='2223_000');p.add_argument('--seconds',type=float,default=60);p.add_argument('--dominance',choices=['pareto','lex'],default='pareto');a=p.parse_args()
    print(json.dumps(run(a.case,a.seconds,a.dominance)),flush=True)
