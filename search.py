#!/usr/bin/env python3
"""Resumable exact QF_LRA region-cover search; a deadline is NOT a theorem.

Default goal: every nonnegative additive 4x10 instance has some deleted good,
complete EFX0 predecessor, and EFR insertion. Alternative goals efr / efx9.
All proof claims require verify.py, with a fresh solve and full coverage check.
"""
import os
for _v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ.setdefault(_v,'1')
import argparse
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from fractions import Fraction
from itertools import combinations_with_replacement
import json
import multiprocessing as mp
from pathlib import Path
import time
import z3
from oracle import oracle, verify_witness

SCHEMA=1

def atomic(path,obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2)); tmp.replace(path)

def variables(m):
    return [[z3.Real(f'v_{i}_{g}') for g in range(m)] for i in range(4)]

def base_constraints(v,prefixes):
    m=len(v[0]); cs=[]
    for row in v:
        cs.extend(x>=0 for x in row); cs.append(z3.Sum(row)==1)
    cs.extend(v[0][g]>=v[0][g+1] for g in range(m-1))
    for i,pref in enumerate(prefixes,1):
        used=set()
        for g in pref:
            used.add(g)
            cs.extend(v[i][g]>=v[i][h] for h in range(m) if h not in used)
    return cs

def sv(row,mask):
    return z3.Sum([row[g] for g in range(len(row)) if mask>>g&1]) if mask else z3.RealVal(0)

def efx_constraints(v,A):
    cs=[]
    for i in range(4):
        own=sv(v[i],A[i])
        for j in range(4):
            if i==j or A[j].bit_count()<2: continue
            for g in range(len(v[0])):
                if A[j]>>g&1: cs.append(own>=sv(v[i],A[j]^(1<<g)))
    return cs

def witness_constraints(v,w,goal):
    A=w['allocation']
    if goal=='efx9': return efx_constraints(v,A)
    if goal=='extension':
        B=w['predecessor']; k=w['recipient']; g=w['deleted']; s=B[k].bit_count()
        cs=efx_constraints(v,B)
        for i in range(4):
            if i!=k: cs.append((s+1)*sv(v[i],B[i])>=s*(sv(v[i],B[k])+v[i][g]))
        return cs
    cs=[]
    for i in range(4):
        for j in range(4):
            if i!=j and A[j].bit_count()>1:
                s=A[j].bit_count(); cs.append(s*sv(v[i],A[i]) >= (s-1)*sv(v[i],A[j]))
    return cs

def witness_key(w,goal):
    if goal=='extension': return tuple(w['predecessor'])+(w['deleted'],w['recipient'])
    return tuple(w['allocation'])

def extract(s,v):
    model=s.model(); ans=[]
    for row in v:
        vals=[]
        for x in row:
            q=model.eval(x,model_completion=True)
            vals.append(str(Fraction(q.numerator_as_long(),q.denominator_as_long())))
        ans.append(vals)
    return ans

def build_solver(v,node,goal,seed):
    s=z3.SolverFor('QF_LRA'); s.set(random_seed=seed, **{'smt.arith.solver':2})
    s.add(*base_constraints(v,node['prefixes']))
    for w in node['witnesses']:
        s.add(z3.Not(z3.And(*witness_constraints(v,w,goal))))
    return s

def work_node(path,config,deadline,opts):
    node=json.loads(Path(path).read_text()); goal=config['goal']; m=config['goods']
    start=time.time(); local_end=min(deadline,start+opts['slice_seconds'])
    node['status']='OPEN'; node.pop('reason',None)
    v=variables(m); s=build_solver(v,node,goal,opts['seed'])
    seen={witness_key(w,goal) for w in node['witnesses']}
    added=0; calls=0; solver_seconds=0.; oracle_seconds=0.
    def finish(status,reason):
        node['status']=status; node['reason']=reason
        node['solver_calls']=node.get('solver_calls',0)+calls
        node['worker_seconds']=node.get('worker_seconds',0)+time.time()-start
        node['solver_seconds']=node.get('solver_seconds',0)+solver_seconds
        node['oracle_seconds']=node.get('oracle_seconds',0)+oracle_seconds
        node['last_added']=added
        atomic(path,node)
        return {'id':node['id'],'status':status,'menu':len(node['witnesses']),
                'seconds':time.time()-start,'reason':reason}
    for _ in range(opts['rounds']):
        remaining=local_end-time.time()
        if remaining<=0: return finish('OPEN','time slice ended')
        s.set(timeout=max(1,int(1000*min(opts['smt_seconds'],remaining))))
        t=time.time(); result=s.check(); solver_seconds+=time.time()-t; calls+=1
        if result==z3.unsat:
            # Export a replayable UNSAT instance, NOT a proof object.
            Path(path).with_suffix('.smt2').write_text(s.to_smt2())
            return finish('COVERED','exact UNSAT; independent verification still required')
        if result!=z3.sat:
            return finish('OPEN','solver unknown: '+s.reason_unknown())
        V=extract(s,v); node['last_model']=V
        t=time.time()
        target='efx9' if goal=='efx9' else 'extension'
        found=oracle(V,goal=target,limit=opts['batch'],deadline=local_end)
        oracle_seconds+=time.time()-t
        if found['status']=='UNKNOWN': return finish('OPEN','oracle deadline; no negative inference')
        if found['status']=='ABSENT' and goal!='efx9':
            node['mode_c_failure']={'matrix':V,'profile':found}
            t=time.time()
            fallback=oracle(V,goal='efr',limit=opts['batch'],deadline=local_end)
            oracle_seconds+=time.time()-t
            node['direct_efr_at_mode_c_failure']=fallback
            if goal=='extension':
                node['counterexample']=V
                return finish('REFUTED','all deletion/predecessor/insertion choices failed exactly')
            found=fallback
            if found['status']=='UNKNOWN': return finish('OPEN','direct EFR oracle deadline')
        if found['status']=='ABSENT':
            node['counterexample']=V; node['negative_oracle']=found
            return finish('REFUTED','exhaustive exact allocation search failed')
        fresh=0
        for w in found['witnesses']:
            key=witness_key(w,goal)
            if key in seen: continue
            # Rational strings -> Fractions; preserve all agent labels.
            if not verify_witness([[Fraction(x) for x in row] for row in V],w,goal):
                raise AssertionError('Invalid point witness')
            seen.add(key); node['witnesses'].append(w)
            s.add(z3.Not(z3.And(*witness_constraints(v,w,goal))))
            fresh+=1; added+=1
        if not fresh:
            raise AssertionError('SAT model had only already-excluded witnesses')
        atomic(path,node)  # every batch survives interruption
    return finish('OPEN','round limit for this slice')

def root_nodes(m):
    for fav in combinations_with_replacement(range(m),3):
        rid='r_'+'_'.join(map(str,fav))
        yield {'id':rid,'prefixes':[[x] for x in fav], 'witnesses':[],
               'status':'OPEN','parent':None}

def split_node(node,m):
    choices=[i for i in range(3) if len(node['prefixes'][i])<m-1]
    if not choices: return None
    i=min(choices,key=lambda i:len(node['prefixes'][i]))
    children=[]
    for g in range(m):
        if g in node['prefixes'][i]: continue
        prefs=[list(x) for x in node['prefixes']]; prefs[i].append(g)
        cid=node['id']+f'_a{i+1}g{g}'
        children.append({'id':cid,'prefixes':prefs,'witnesses':node['witnesses'],
                         'status':'OPEN','parent':node['id']})
    return i,children

def summarize(out,config):
    nodes=[json.loads(p.read_text()) for p in (out/'nodes').glob('*.json')]
    byid={n['id']:n for n in nodes}; memo={}
    def covered(key):
        if key in memo: return memo[key]
        n=byid.get(key,{})
        ans=n.get('status')=='COVERED'
        if n.get('status')=='SPLIT':
            ans=bool(n.get('children')) and all(covered(c) for c in n['children'])
        memo[key]=ans; return ans
    roots=list(root_nodes(config['goods']))
    summary={'goal':config['goal'],'required_roots':len(roots),
        'covered_roots':sum(covered(n['id']) for n in roots),
        'nodes':len(nodes),'covered_leaves':sum(n['status']=='COVERED' for n in nodes),
        'open_leaves':sum(n['status'] in ('OPEN','ERROR') for n in nodes),
        'refuted':sum(n['status']=='REFUTED' for n in nodes),
        'worker_seconds':sum(n.get('worker_seconds',0) for n in nodes),
        'verdict':'INCOMPLETE'}
    if summary['refuted']: summary['verdict']='CONJECTURE_REFUTED_BY_ORACLE_REQUIRES_RECHECK'
    elif summary['covered_roots']==len(roots): summary['verdict']='SEARCH_COVERED_REQUIRES_VERIFY_PY'
    atomic(out/'summary.json',summary)
    return summary

def run(args):
    out=Path(args.out); (out/'nodes').mkdir(parents=True,exist_ok=True)
    config={'schema':SCHEMA,'goal':args.goal,'goods':9 if args.goal=='efx9' else 10,
            'zero_tolerant_efx':True,'normalized_row_sum':1,'agent0_sorted':True}
    config_path=out/'config.json'
    if config_path.exists():
        if json.loads(config_path.read_text())!=config:
            raise ValueError('Output directory belongs to a different goal/configuration')
    else:
        atomic(config_path,config)
    roots=list(root_nodes(config['goods']))
    for n in roots:
        p=out/'nodes'/f"{n['id']}.json"
        if not p.exists(): atomic(p,n)
    # Deterministic root sharding allows independent machines/directories.
    root_index={n['id']:i for i,n in enumerate(roots)}
    def in_shard(n):
        root=n['id'].split('_a')[0]
        return root_index[root]%args.shards==args.shard
    pending=[]
    for p in sorted((out/'nodes').glob('*.json')):
        n=json.loads(p.read_text())
        if n['status'] in ('OPEN','ERROR') and in_shard(n): pending.append(p)
    deadline=time.time()+args.hours*3600
    opts=vars(args).copy(); active={}; last=time.time(); processed=0
    # Warm compilation/cache once before worker launch. Included in wall budget.
    oracle([[1]*config['goods'] for _ in range(4)],
           goal='efx9' if args.goal=='efx9' else 'extension',limit=1,deadline=deadline)
    with ProcessPoolExecutor(max_workers=args.workers,mp_context=mp.get_context('spawn')) as pool:
        while (pending or active) and time.time()<deadline:
            while pending and len(active)<args.workers and time.time()<deadline:
                p=pending.pop(0)
                active[pool.submit(work_node,str(p),config,deadline,opts)]=p
            if not active: break
            done,_=wait(active,timeout=min(15,max(.01,deadline-time.time())),return_when=FIRST_COMPLETED)
            for future in done:
                p=active.pop(future); processed+=1
                try: result=future.result()
                except Exception as e:
                    node=json.loads(p.read_text()); node['status']='ERROR'; node['error']=repr(e)
                    atomic(p,node); print(json.dumps({'id':node['id'],'error':repr(e)}),flush=True)
                    continue
                print(json.dumps(result),flush=True)
                node=json.loads(p.read_text())
                if node['status']=='OPEN' and time.time()<deadline:
                    children=None if args.no_split else split_node(node,config['goods'])
                    if children is not None:
                        i,kids=children
                        for kid in kids:
                            cp=out/'nodes'/f"{kid['id']}.json"
                            # Child-before-parent writes are crash safe; orphan children
                            # are not used for coverage and may only duplicate search.
                            atomic(cp,kid); pending.append(cp)
                        node['status']='SPLIT'; node['split_agent']=i+1
                        node['children']=[k['id'] for k in kids]; atomic(p,node)
                    elif args.no_split:
                        pending.append(p)
                if node['status']=='REFUTED' and args.stop_on_refutation:
                    pending.clear(); deadline=time.time()
            if time.time()-last>=30:
                print(json.dumps({'progress':summarize(out,config),'queued':len(pending),
                                  'running':len(active)}),flush=True); last=time.time()
        # Workers receive the same global deadline and save their last batch.
        # Normal exit can overrun by bounded kernel/solver shutdown overhead.
        for future,p in list(active.items()):
            try: future.result()
            except Exception as e:
                n=json.loads(p.read_text()); n['status']='ERROR'; n['error']=repr(e); atomic(p,n)
    print(json.dumps(summarize(out,config),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',default='run')
    p.add_argument('--goal',choices=['extension','efr','efx9'],default='extension')
    p.add_argument('--workers',type=int,default=max(1,(os.cpu_count() or 2)-1))
    p.add_argument('--hours',type=float,default=1)
    p.add_argument('--slice-seconds',type=float,default=60)
    p.add_argument('--smt-seconds',type=float,default=10)
    p.add_argument('--rounds',type=int,default=64)
    p.add_argument('--batch',type=int,default=8)
    p.add_argument('--seed',type=int,default=42)
    p.add_argument('--no-split',action='store_true')
    p.add_argument('--shards',type=int,default=1)
    p.add_argument('--shard',type=int,default=0)
    p.add_argument('--stop-on-refutation',action='store_true')
    a=p.parse_args()
    if min(a.workers,a.rounds,a.batch,a.shards)<=0 or not 0<=a.shard<a.shards or min(a.hours,a.slice_seconds,a.smt_seconds)<=0:
        p.error('Budgets must be positive and 0 <= shard < shards')
    run(a)
