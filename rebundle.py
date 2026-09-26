#!/usr/bin/env python3
"""Nearest extendable EFX predecessor under simultaneous rebundling.

Distance counts changed memberships among four physical blocks and the omitted
slot, minimizing over block matchings. Whole-block ownership changes are free;
the final insertion is excluded. No EFX requirement on intermediate microsteps.
"""
from functools import lru_cache
from itertools import permutations
import time
import numpy as np
from oracle import (njit,PERMS,partitions,integer_rows,tables,matching_tables,
                    scan_kernel,verify_witness)
from capacity import validate

@lru_cache(None)
def lifted_partitions(g):
    goods=[h for h in range(10) if h!=g]
    lift=np.array([sum(1<<h for b,h in enumerate(goods) if mask>>b&1)
                   for mask in range(512)],dtype=np.int64)
    return lift[partitions(9)]

@njit(cache=True)
def distances(parts,initial,sizes,pool_match):
    out=np.empty(len(parts),dtype=np.int64)
    for n in range(len(parts)):
        best=0
        for q in range(24):
            retained=0
            for i in range(4):retained+=sizes[initial[i]&parts[n,PERMS[q,i]]]
            if retained>best:best=retained
        out[n]=10-pool_match-best
    return out


def movement(initial,old_g,target,new_g):
    # Explicit best block matching, independent of the compiled distance kernel.
    best=max(permutations(range(4)),key=lambda p:sum((initial[i]&target[p[i]]).bit_count() for i in range(4)))
    aligned=[target[best[i]] for i in range(4)]
    def slots(blocks,g):
        return [4 if h==g else next(i for i,b in enumerate(blocks) if b>>h&1) for h in range(10)]
    before=slots(initial,old_g);after=slots(aligned,new_g)
    changed=[{'good':h,'from_slot':before[h],'to_slot':after[h]} for h in range(10) if before[h]!=after[h]]
    return {'distance':len(changed),'target_agent_by_initial_block':list(best),
            'changed_goods':changed,'omitted_slot':4}


def nearest(values,initial,old_g,max_radius=10,seconds=60):
    started=time.monotonic();deadline=started+seconds
    if not 0<=max_radius<=10 or seconds<0:raise ValueError('Invalid budget')
    rows=integer_rows(values)
    if len(rows[0])!=10:raise ValueError('Requires ten goods')
    validate(rows,initial,old_g)
    sums,mins,sizes,fast=tables(rows);mb,mc=matching_tables()
    kernel=scan_kernel if fast else scan_kernel.py_func
    initial_array=np.array(initial,dtype=np.int64)
    cache=[];counts=[];visited=0
    def result(status,**kw):
        return {'status':status,'max_radius':max_radius,'completed_radii':counts,
                'partitions_checked':visited,'seconds':time.monotonic()-started,**kw}
    for g in range(10):
        if time.monotonic()>=deadline:return result('UNKNOWN',reason='geometry preparation deadline')
        parts=lifted_partitions(g);d=distances(parts,initial_array,sizes,int(g==old_g))
        cache.append((parts,d))
    for radius in range(max_radius+1):
        checked=0
        for g,(parts,d) in enumerate(cache):
            selected=parts[d==radius]
            new=np.array([row[g] for row in rows],dtype=np.int64 if fast else object)
            for start in range(0,len(selected),512):
                if time.monotonic()>=deadline:return result('UNKNOWN',reason='scan deadline')
                found,n,_,_,_,seen,_=kernel(selected[start:start+512],sums,mins,sizes,new,1,mb,mc,PERMS,1,False)
                visited+=int(seen);checked+=int(seen)
                if n:
                    B=[int(x) for x in found[0,:4]];k=int(found[0,4]);A=B.copy();A[k]|=1<<g
                    w={'predecessor':B,'deleted':g,'recipient':k,'allocation':A}
                    if not verify_witness(rows,w):raise AssertionError('Invalid extension')
                    moves=movement(initial,old_g,B,g)
                    if moves['distance']!=radius:raise AssertionError('Incorrect distance')
                    return result('FOUND',minimum_radius=radius,witness=w,movement=moves,
                                  minimum_certified=True)
        counts.append({'radius':radius,'partitions_checked':checked})
    return result('MODE_C_ABSENT' if max_radius==10 else 'ABSENT_WITHIN_RADIUS',
                  minimum_certified=False)
