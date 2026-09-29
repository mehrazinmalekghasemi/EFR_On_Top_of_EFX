"""Exact EFX-8 to EFR-10 bridge. Fixed-instance exhaustion is not a universal proof."""
from functools import lru_cache
from itertools import combinations,product
import time
import numpy as np
from efr.oracle import integer_rows,tables,is_efx,is_efr
from efr.capacity import validate as validate_nine


def validate_eight(values,A,missing):
    rows=integer_rows(values)
    if len(rows[0])!=10 or len(A)!=4 or len(missing)!=2 or len(set(missing))!=2 or any(type(g)!=int or not 0<=g<10 for g in missing):raise ValueError('Four agents, ten goods, two distinct missing goods required')
    union=0
    for b in A:
        if type(b)!=int or b<0 or b>>10 or union&b:raise ValueError('Invalid disjoint bundles')
        union|=b
    if union!=1023^sum(1<<g for g in missing):raise ValueError('Must allocate exactly the other eight goods')
    if not is_efx(rows,A):raise ValueError('Predecessor must be EFX0')
    return rows


def extensions(values,A,missing):
    rows=validate_eight(values,A,missing);g,h=missing;out=[]
    for p,q in product(range(4),repeat=2):
        B=list(A);B[p]|=1<<g;B[q]|=1<<h
        if is_efr(rows,B):out.append(dict(missing=list(missing),recipients=[p,q],predecessor=list(A),allocation=B))
    return out


def drop_one_bridges(values,A,g):
    rows=validate_nine(values,A,g);out=[]
    for j,b in enumerate(A):
        for h in range(10):
            if b>>h&1:
                C=list(A);C[j]^=1<<h
                if is_efx(rows,C):out.extend(extensions(rows,C,[g,h]))
    return out


@lru_cache(None)
def ownerships():
    return (np.arange(65536,dtype=np.int64)[:,None] >> (2*np.arange(8,dtype=np.int64))) & 3


def search(values,missing_pair=None,seconds=30):
    """All 4^8 assignments for each of 45 pairs; stop on first certified witness.

    NO_BRIDGE is exhaustive only for this instance and the requested pair scope.
    A time limit returns UNKNOWN. Includes empty and unbalanced bundles.
    """
    start=time.monotonic();rows=integer_rows(values)
    if len(rows[0])!=10:raise ValueError('Ten goods required')
    if missing_pair is not None and (len(missing_pair)!=2 or len(set(missing_pair))!=2 or any(type(g)!=int or not 0<=g<10 for g in missing_pair)):raise ValueError('Invalid omitted pair')
    pairs=[tuple(missing_pair)] if missing_pair is not None else list(combinations(range(10),2))
    sums,mins,sizes,fast=tables(rows);owners=ownerships();scanned=0;efx_count=0
    def report(status,**extra):
        return dict(status=status,scope='One fixed valuation instance; '+('fixed omitted pair' if missing_pair is not None else 'all omitted pairs'),
                    pairs_scanned=scanned,efx_predecessors=efx_count,seconds=time.monotonic()-start,**extra)
    for g,h in pairs:
        if time.monotonic()-start>=seconds:return report('UNKNOWN',complete=False)
        goods=[x for x in range(10) if x not in (g,h)]
        B=np.stack([np.sum((owners==i)*(1<<np.array(goods,dtype=np.int64)),axis=1) for i in range(4)],axis=1)
        ok=np.ones(len(B),dtype=bool)
        for i in range(4):
            for j in range(4):
                if i!=j:ok &= sums[i,B[:,i]]>=sums[i,B[:,j]]-mins[i,B[:,j]]
        B=B[ok];efx_count+=len(B);scanned+=1
        for p,q in product(range(4),repeat=2):
            if time.monotonic()-start>=seconds:return report('UNKNOWN',complete=False)
            C=B.copy();C[:,p]|=1<<g;C[:,q]|=1<<h
            ok=np.ones(len(C),dtype=bool)
            for i in range(4):
                for j in range(4):
                    if i!=j:
                        n=sizes[C[:,j]]
                        ok &= n*sums[i,C[:,i]]>=np.maximum(n-1,0)*sums[i,C[:,j]]
            ids=np.flatnonzero(ok)
            if len(ids):
                k=int(ids[0]);a=list(map(int,B[k]));c=list(map(int,C[k]))
                validate_eight(rows,a,[g,h]);assert is_efr(rows,c)
                return report('FOUND',complete=False,witness=dict(missing=[g,h],recipients=[p,q],predecessor=a,allocation=c))
    return report('NO_BRIDGE',complete=True)
