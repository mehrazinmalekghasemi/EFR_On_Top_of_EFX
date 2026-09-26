"""Bounded real-valued EFR proof search over necessary extremal-state regions.

This searches EFR existence, not universal direct EFX-nine insertion (Mode C).
Timeout is OPEN. No agent-priority-dependent cuts are used after canonicalization.
"""
import argparse,json,time,hashlib
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import z3
from search import variables,sv,efx_constraints,witness_constraints,extract
from oracle import oracle,integer_rows,verify_witness,valid_partition
from structural_reductions import catalog


def build(case,simplify_pairs=True):
    v=variables(10);A=case['initial'];own=[sv(v[i],A[i]) for i in range(4)]
    s=z3.SolverFor('QF_LRA');s.set(**{'smt.arith.solver':2})
    for row in v:s.add(*[x>=0 for x in row],z3.Sum(row)==1)
    s.add(*efx_constraints(v,A))
    edges={tuple(e) for e in case['edges']}
    for i in range(4):
        s.add(v[i][9]<=own[i])
        for j in range(4):
            if i!=j:s.add(own[i]<sv(v[i],A[j]) if (i,j) in edges else own[i]>=sv(v[i],A[j]))
        if A[i].bit_count()>=2:
            for h in range(9):
                if A[i]>>h&1:s.add(v[i][9]+v[i][h]<=own[i])
    # Only one simultaneous goods relabeling INSIDE each fixed initial bundle.
    for block in A:
        goods=[h for h in range(9) if block>>h&1]
        for h,h2 in zip(goods,goods[1:]):s.add(v[0][h]>=v[0][h2])
    for k,block in enumerate(A):
        size=block.bit_count()
        blockers=[i for i in range(4) if i!=k]
        if simplify_pairs and size==2 and k in case['sources']:
            blockers=[i for i in blockers if case['profile'][i]!=2 and not case['reach'][k][i]]
        s.add(z3.Or(*[(size+1)*own[i]<size*(sv(v[i],block)+v[i][9]) for i in blockers]))
        if simplify_pairs and size>=2:
            for i in range(4):
                if case['reach'][k][i]:
                    for h in range(9):
                        if block>>h&1:s.add(v[i][9]+v[i][h]<=own[i])
        # Every safe champion closing an envy path yields a Pareto improvement.
        subset=block
        while True:
            if subset!=block and (not simplify_pairs or subset.bit_count()>=2):
                T=subset|512
                safe=z3.And(*[sv(v[j],T^(1<<h))<=own[j]
                              for j in range(4) for h in range(10) if T>>h&1])
                for i in range(4):
                    if case['reach'][k][i]:s.add(z3.Not(z3.And(sv(v[i],T)>own[i],safe)))
            if subset==0:break
            subset=(subset-1)&block
    return s,v


def run(task):
    case,seconds,query_seconds,outdir,seed_directory,simplify_pairs=task
    started=time.monotonic();deadline=time.time()+seconds
    s,v=build(case,simplify_pairs);build_seconds=time.monotonic()-started
    witnesses=[]
    if seed_directory:
        seed_file=Path(seed_directory)/(case['id']+'.json')
        if seed_file.exists():
            previous=json.loads(seed_file.read_text())
            for w in previous.get('witnesses',[]):
                if not valid_partition(w['allocation'],10):raise ValueError('Invalid imported complete allocation')
                witnesses.append(w);s.add(z3.Not(z3.And(*witness_constraints(v,w,'efr'))))
    seeded_count=len(witnesses)
    status='OPEN';reason='wall budget';calls=0;solver_seconds=0;oracle_seconds=0;last=None
    while time.time()<deadline:
        s.set(timeout=max(1,int(1000*min(query_seconds,deadline-time.time()))))
        t=time.monotonic();check=s.check();solver_seconds+=time.monotonic()-t;calls+=1
        if check==z3.unsat:status='UNSAT_REPLAY_PENDING';reason='region covered or infeasible';break
        if check!=z3.sat:reason='solver '+s.reason_unknown();break
        last=extract(s,v)
        t=time.monotonic();q=oracle(last,limit=1,deadline=deadline)
        if q['status']=='ABSENT':q=oracle(last,goal='efr',limit=1,deadline=deadline)
        oracle_seconds+=time.monotonic()-t
        if q['status']=='ABSENT':status='EFR_COUNTEREXAMPLE_CANDIDATE';reason='exact point oracle exhausted all complete allocations';break
        if q['status']!='FOUND':reason='point oracle deadline';break
        w=q['witnesses'][0]
        assert verify_witness(integer_rows(last),w,'efr')
        witnesses.append(w)
        # An EFR witness covers a larger region than its EFX-predecessor certificate.
        s.add(z3.Not(z3.And(*witness_constraints(v,w,'efr'))))
    directory=Path(outdir);directory.mkdir(parents=True,exist_ok=True)
    result={'case':case,'status':status,'reason':reason,'seconds':time.monotonic()-started,
            'build_seconds':build_seconds,'solver_seconds':solver_seconds,'oracle_seconds':oracle_seconds,
            'solver_calls':calls,'seeded_witness_count':seeded_count,'witness_count':len(witnesses),'witnesses':witnesses,'last_model':last,
            'pair_simplification':simplify_pairs,'scope':'EFR existence over this necessary extremal region; NOT a Mode C certificate'}
    if status=='UNSAT_REPLAY_PENDING':
        smt=s.to_smt2();(directory/(case['id']+'.smt2')).write_text(smt)
        result['smt2_sha256']=hashlib.sha256(smt.encode()).hexdigest()
    (directory/(case['id']+'.json')).write_text(json.dumps(result,indent=2))
    return {k:x for k,x in result.items() if k not in ('witnesses','last_model')}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=15)
    p.add_argument('--query-seconds',type=float,default=10);p.add_argument('--workers',type=int,default=3)
    p.add_argument('--legacy-pairs',action='store_true');p.add_argument('--pilot',action='store_true');p.add_argument('--case');p.add_argument('--seed-directory');p.add_argument('--out',default='run/structural-pilot')
    a=p.parse_args();cases,summary=catalog()
    if a.pilot:
        selected={}
        for c in cases:selected.setdefault((tuple(c['profile']),len(c['sources'])),c)
        cases=list(selected.values())
    if a.case:cases=[c for c in cases if c['id']==a.case]
    if not cases:raise ValueError('No matching structural case')
    results=[]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for r in pool.map(run,[(c,a.seconds,a.query_seconds,a.out,a.seed_directory,not a.legacy_pairs) for c in cases]):
            results.append(r);print(json.dumps({'id':r['case']['id'],'status':r['status'],'witnesses':r['witness_count'],'seconds':r['seconds']}),flush=True)
    Path(a.out,'summary.json').write_text(json.dumps({'catalog':summary,'seconds_per_case':a.seconds,
        'pair_simplification':not a.legacy_pairs,'query_seconds':a.query_seconds,'workers':a.workers,'pilot':a.pilot,'results':results},indent=2))
