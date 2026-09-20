#!/usr/bin/env python3
"""Measure point-oracle throughput. Never extrapolate this to a full SMT proof."""
import argparse,json,os,platform,time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from pathlib import Path
from statistics import median
import numpy as np
import z3
from oracle import oracle

def trial(job):
    index,V,full=job
    t=time.perf_counter()
    r=oracle(V,limit=1,scan_all=full)
    return {'index':index,'seconds':time.perf_counter()-t,'kernel_and_scan_seconds':r['seconds'],
            'status':r['status'],'complete':r['complete'],'arithmetic':r['arithmetic']}

def benchmark(count,workers,seed):
    rng=np.random.default_rng(seed)
    uniform=[rng.integers(0,21,size=(4,10)).tolist() for _ in range(count)]
    near=[]
    for _ in range(count):
        base=rng.integers(100,1000,size=(1,10))
        near.append((base+rng.integers(0,4,size=(4,10))).tolist())
    t=time.perf_counter();oracle([[1]*10 for _ in range(4)],limit=1)
    startup=time.perf_counter()-t
    report={'machine':platform.platform(),'processor':platform.processor(),'logical_cpus':os.cpu_count(),
            'workers':workers,'z3':z3.get_version_string(),'startup_seconds':startup,
            'scope':'point oracle only; not time to prove the whole real valuation domain','runs':{}}
    for name,matrices,full in [('random_first',uniform,False),('near_identical_first',near,False),
                                ('random_all_deletions',uniform,True),('near_identical_all_deletions',near,True)]:
        jobs=[(i,V,full) for i,V in enumerate(matrices)]
        t=time.perf_counter()
        if workers==1:rs=list(map(trial,jobs))
        else:
            with ProcessPoolExecutor(max_workers=workers,mp_context=mp.get_context('spawn')) as pool:
                rs=list(pool.map(trial,jobs,chunksize=max(1,count//(workers*4))))
        elapsed=time.perf_counter()-t
        ts=sorted(x['seconds'] for x in rs)
        report['runs'][name]={'count':count,'wall_seconds':elapsed,'profiles_per_second':count/elapsed,
            'median_seconds':median(ts),'p95_seconds':ts[min(len(ts)-1,int(.95*len(ts)))],
            'max_seconds':max(ts),'found':sum(r['status']=='FOUND' for r in rs),
            'complete':sum(r['complete'] for r in rs)}
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--count',type=int,default=100)
    p.add_argument('--workers',type=int,default=1)
    p.add_argument('--seed',type=int,default=42)
    p.add_argument('--out',default='benchmark.json')
    a=p.parse_args()
    if a.count<1 or a.workers<1:p.error('positive count/workers required')
    r=benchmark(a.count,a.workers,a.seed)
    Path(a.out).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
