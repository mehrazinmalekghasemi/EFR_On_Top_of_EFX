#!/usr/bin/env python3
"""Independent cover verifier: imports neither search.py nor oracle.py.

Rebuilds every leaf's full EFX and EFR formulas from labeled allocation masks.
Checks all roots and every required child. UNKNOWN, missing, malformed, or
uncovered regions prevent a global theorem. Trust base still includes Z3;
these are replayable UNSAT instances, not formal proof objects.
"""
import argparse,itertools,json,time
from concurrent.futures import ProcessPoolExecutor,wait,FIRST_COMPLETED
import multiprocessing as mp
from pathlib import Path
import z3

def check_allocation(a,m,missing=None):
    assert isinstance(a,list) and len(a)==4
    seen=0
    for mask in a:
        assert isinstance(mask,int) and 0<=mask<(1<<m)
        assert not (mask&seen)
        seen |= mask
    assert seen==(((1<<m)-1) ^ (0 if missing is None else (1<<missing)))

def make_instance(node,goal,m):
    v=[[z3.Real(f'x{i}_{g}') for g in range(m)] for i in range(4)]
    constraints=[]
    for row in v:
        constraints += [x>=0 for x in row]+[sum(row)==1]
    constraints += [v[0][g]>=v[0][g+1] for g in range(m-1)]
    for i,order in enumerate(node['prefixes'],1):
        assert len(order)==len(set(order)) and all(type(g)==int and 0<=g<m for g in order)
        for p,g in enumerate(order):
            constraints += [v[i][g]>=v[i][h] for h in range(m) if h not in order[:p+1]]
    def value(i,mask):
        return sum((v[i][g] for g in range(m) if mask & (1<<g)), z3.RealVal(0))
    for w in node['witnesses']:
        a=w['allocation']; check_allocation(a,m)
        fair=[]
        if goal in ('extension','efx9'):
            if goal=='extension':
                g=w['deleted']; k=w['recipient']; b=w['predecessor']
                assert type(g)==int and 0<=g<m and type(k)==int and 0<=k<4
                check_allocation(b,m,g)
                expected=list(b); expected[k] |= 1<<g
                assert expected==a
            else: b=a
            for i in range(4):
                for j in range(4):
                    if i!=j:
                        for h in range(m):
                            if b[j] & (1<<h):
                                fair.append(value(i,b[i])>=value(i,b[j]^(1<<h)))
        if goal in ('extension','efr'):
            for i in range(4):
                for j in range(4):
                    if i!=j:
                        count=sum(1 for h in range(m) if a[j]&(1<<h))
                        if count:
                            fair.append(count*value(i,a[i]) >= (count-1)*value(i,a[j]))
        constraints.append(z3.Not(z3.And(fair)))
    return constraints

def solve_leaf(job):
    node,goal,m,timeout,deadline=job
    if time.time()>=deadline:return {'id':node['id'],'verdict':'NOT_CHECKED_DEADLINE'}
    s=z3.SolverFor('QF_LRA')
    s.add(*make_instance(node,goal,m))
    left=deadline-time.time()
    if left<=0:return {'id':node['id'],'verdict':'NOT_CHECKED_DEADLINE'}
    s.set(timeout=max(1,int(1000*min(timeout,left))))
    t=time.time();result=s.check()
    return {'id':node['id'],'verdict':str(result),'seconds':time.time()-t}

def verify(directory,timeout,shard=0,shards=1,workers=1,hours=24):
    directory=Path(directory); config=json.loads((directory/'config.json').read_text())
    goal=config['goal']; m=config['goods']
    assert config=={'schema':1,'goal':goal,'goods':m,'zero_tolerant_efx':True,
                    'normalized_row_sum':1,'agent0_sorted':True}
    assert goal in ('extension','efr','efx9') and m==(9 if goal=='efx9' else 10)
    log=[]; visiting=set(); jobs=[]; started=time.time(); deadline=started+hours*3600
    def visit(key,expected_prefixes,parent):
        assert key not in visiting
        visiting.add(key)
        path=directory/'nodes'/f'{key}.json'
        if not path.exists():
            log.append({'id':key,'verdict':'MISSING'}); return None
        node=json.loads(path.read_text())
        assert node['id']==key and node['prefixes']==expected_prefixes and node['parent']==parent
        if node['status']=='SPLIT':
            i=node['split_agent']-1
            assert 0<=i<3 and len(expected_prefixes[i])<m-1
            allowed=[g for g in range(m) if g not in expected_prefixes[i]]
            children=[key+f'_a{i+1}g{g}' for g in allowed]
            assert len(set(node['children']))==len(children) and set(node['children'])==set(children)
            answer=[];valid=True
            for g,c in zip(allowed,children):
                p=[list(x) for x in expected_prefixes];p[i].append(g)
                child=visit(c,p,key)
                if child is None:valid=False
                else:answer.extend(child)
            return answer if valid else None
        if node['status']!='COVERED':
            log.append({'id':key,'verdict':'UNCOVERED','status':node['status']}); return None
        jobs.append((node,goal,m,timeout,deadline))
        return [key]
    roots=list(itertools.combinations_with_replacement(range(m),3))
    chosen=[fav for idx,fav in enumerate(roots) if idx%shards==shard]
    dependencies=[]
    for fav in chosen:
        key='r_'+'_'.join(map(str,fav))
        dependencies.append(visit(key,[[g] for g in fav],None))
    solved=[]
    if workers==1:
        for job in jobs:
            solved.append(solve_leaf(job))
    elif jobs:
        pending=list(jobs);active={}
        with ProcessPoolExecutor(max_workers=workers,mp_context=mp.get_context('spawn')) as pool:
            while (pending or active) and time.time()<deadline:
                while pending and len(active)<workers:
                    job=pending.pop(0);active[pool.submit(solve_leaf,job)]=job[0]['id']
                done,_=wait(active,timeout=min(15,max(.01,deadline-time.time())),return_when=FIRST_COMPLETED)
                for f in done:
                    active.pop(f);solved.append(f.result())
            for f in active:solved.append(f.result())
            for job in pending:solved.append({'id':job[0]['id'],'verdict':'NOT_CHECKED_DEADLINE'})
    status={r['id']:r['verdict'] for r in solved}
    results=[dep is not None and all(status.get(key)=='unsat' for key in dep) for dep in dependencies]
    report={'goal':goal,'z3_version':z3.get_version_string(),'all_required_roots':len(roots),
            'roots_checked':len(chosen),'roots_verified':sum(results),'leaves_resolved':len(solved),
            'shard':shard,'shards':shards,'workers':workers,'seconds':time.time()-started,
            'checks':solved+log,
            'verdict':('VERIFIED_GLOBAL_COVER' if shards==1 else 'VERIFIED_SHARD_ONLY')
                      if all(results) else 'INCOMPLETE_NO_THEOREM'}
    return report

if __name__=='__main__':
    if not __debug__: raise SystemExit('Verification requires Python assertions; remove -O')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory')
    p.add_argument('--timeout',type=float,default=120)
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--hours',type=float,default=24)
    p.add_argument('--shard',type=int,default=0);p.add_argument('--shards',type=int,default=1)
    a=p.parse_args()
    if a.timeout<=0 or a.workers<1 or a.hours<=0 or a.shards<1 or not 0<=a.shard<a.shards:p.error('Invalid timeout/shard')
    try:r=verify(a.directory,a.timeout,a.shard,a.shards,a.workers,a.hours)
    except Exception as e:
        r={'verdict':'INVALID_NO_THEOREM','error':repr(e)}
    dest=Path(a.directory)/f'verification-{a.shard}-of-{a.shards}.json'
    dest.write_text(json.dumps(r,indent=2))
    print(json.dumps({k:v for k,v in r.items() if k!='checks'},indent=2))
    raise SystemExit(0 if r['verdict'].startswith('VERIFIED_') else 2)
