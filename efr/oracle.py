"""Exact additive EFX0/EFR oracle. Unlabeled partitions + labeled matchings.

Nonnegative rational input is scaled independently per row to primitive integers.
Numba int64 is used only under a proven overflow bound; otherwise Python bigints.
No floating point comparisons, tolerance, or heuristic negative verdicts.
"""
from functools import lru_cache
from fractions import Fraction
from itertools import permutations
from math import gcd, lcm
import time
import numpy as np
try:
    from numba import njit
except ImportError:
    def njit(*a, **kw):
        def deco(f):
            f.py_func = f
            return f
        return deco

PERMS = np.array(list(permutations(range(4))), dtype=np.int64)

@lru_cache(None)
def matching_tables():
    codes = np.arange(65536, dtype=np.int64)
    bits = np.zeros(65536, dtype=np.int64)
    counts = np.zeros(65536, dtype=np.int64)
    for p, perm in enumerate(PERMS):
        required = sum(1 << (4*i + int(perm[i])) for i in range(4))
        ok = (codes & required) == required
        bits[ok] |= 1 << p
        counts[ok] += 1
    return bits, counts

@lru_cache(None)
def partitions(m):
    """Every set partition into <=4 nonempty blocks once; pad with empties."""
    out = []
    def rec(g, blocks):
        if g == m:
            out.append(tuple(blocks + [0]*(4-len(blocks))))
            return
        for k in range(len(blocks)):
            blocks[k] |= 1 << g
            rec(g+1, blocks)
            blocks[k] ^= 1 << g
        if len(blocks) < 4:
            rec(g+1, blocks + [1 << g])
    rec(0, [])
    # Balanced cases first, but retain EVERY partition, including empty bundles.
    out.sort(key=lambda p: (sum((4*x.bit_count()-m)**2 for x in p), p))
    return np.asarray(out, dtype=np.int64)

def integer_rows(V):
    if len(V) != 4 or not V or not V[0]:
        raise ValueError('Expected four nonempty rows')
    m = len(V[0])
    rows = []
    for row in V:
        if len(row) != m:
            raise ValueError('Ragged valuation matrix')
        fs = [Fraction(str(x)) for x in row]
        if min(fs) < 0:
            raise ValueError('Only nonnegative additive goods are supported')
        den = lcm(*(x.denominator for x in fs))
        ints = [int(x*den) for x in fs]
        div = gcd(*ints) or 1
        rows.append([x//div for x in ints])
    return rows

def tables(rows):
    m = len(rows[0]); size = 1 << m
    # Every intermediate is nonnegative <=(m+1)*sum(row); differences, if any,
    # have absolute value at most the same bound. Use a conservative factor 32.
    fast = 32*max(map(sum, rows), default=0) <= np.iinfo(np.int64).max
    dtype = np.int64 if fast else object
    sums = np.zeros((4,size), dtype=dtype)
    mins = np.zeros((4,size), dtype=dtype)
    sizes = np.array([x.bit_count() for x in range(size)], dtype=np.int64)
    for mask in range(1,size):
        bit = mask & -mask; g = bit.bit_length()-1; rest = mask ^ bit
        for i in range(4):
            sums[i,mask] = sums[i,rest]+rows[i][g]
            mins[i,mask] = min(mins[i,rest],rows[i][g]) if rest else rows[i][g]
    return sums, mins, sizes, fast

@njit(cache=True)
def scan_kernel(parts, sums, mins, sizes, new_values, mode,
                matchbits, matchcounts, perms, limit, scan_all, max_recipient_size=10):
    """mode 0: EFX; 1: EFX+insertion; 2: direct EFR.
    Return local masks in agent order, target block owner, counts, completeness.
    """
    out = np.zeros((limit,5), dtype=np.int64)
    retained = 0; efx_total = 0; success_total = 0
    hist = np.zeros(11, dtype=np.int64)
    for index in range(len(parts)):
        B = parts[index]
        empty = 0
        for b in range(4):
            if B[b] == 0: empty += 1
        divisor = 1
        for e in range(2,empty+1): divisor *= e
        graph = 0
        for i in range(4):
            if mode != 2:
                threshold = 0
                for b in range(4):
                    r = sums[i,B[b]]-mins[i,B[b]]
                    if r > threshold: threshold = r
                for b in range(4):
                    if sums[i,B[b]] >= threshold:
                        graph |= 1 << (4*i+b)
            else:
                for b in range(4):
                    ok = True
                    for c in range(4):
                        s = int(sizes[B[c]])
                        if s > 1 and s*sums[i,B[b]] < (s-1)*sums[i,B[c]]:
                            ok = False
                            break
                    if ok: graph |= 1 << (4*i+b)
        if matchbits[graph] == 0: continue
        efx_total += matchcounts[graph]//divisor
        targets = 4 if mode == 1 else 1
        for target in range(targets):
            if mode == 1 and B[target] == 0 and target > 0 and B[target-1] == 0:
                continue  # indistinguishable empty targets
            code = graph
            s = int(sizes[B[target]])
            if mode == 1 and s > max_recipient_size: continue
            if mode == 1:
                for i in range(4):
                    rhs = s*(sums[i,B[target]]+new_values[i])
                    for b in range(4):
                        if b != target and (s+1)*sums[i,B[b]] < rhs:
                            code &= ~(1 << (4*i+b))
            matches = matchbits[code]
            if matches == 0: continue
            d = divisor
            if mode == 1 and s == 0 and empty > 0: d //= empty
            number = matchcounts[code]//d
            success_total += number
            if mode == 1: hist[s] += number
            if retained < limit:
                for p in range(24):
                    if matches & (1 << p):
                        owner = -1
                        for i in range(4):
                            b = perms[p,i]
                            out[retained,i] = B[b]
                            if b == target: owner = i
                        out[retained,4] = owner
                        retained += 1
                        # One representative per target partition. Still complete
                        # for existence: graph LUT tests all 24 assignments.
                        break
            if retained >= limit and not scan_all:
                return out, retained, efx_total, success_total, hist, index+1, False
    return out, retained, efx_total, success_total, hist, len(parts), True

def bundle_value(V,i,mask):
    return sum(V[i][g] for g in range(len(V[0])) if mask >> g & 1)

def valid_partition(A,m):
    return (len(A)==4 and all(isinstance(x,int) and 0<=x<(1<<m) for x in A)
            and sum(x.bit_count() for x in A)==m
            and (A[0]|A[1]|A[2]|A[3])==(1<<m)-1)

def is_efx(V,A):
    for i in range(4):
        own=bundle_value(V,i,A[i])
        for j in range(4):
            if j==i: continue
            for g in range(len(V[0])):
                if A[j] >> g & 1 and own < bundle_value(V,i,A[j]^(1<<g)):
                    return False
    return True

def is_efr(V,A):
    for i in range(4):
        for j in range(4):
            if j==i: continue
            s=A[j].bit_count()
            if s and s*bundle_value(V,i,A[i]) < (s-1)*bundle_value(V,i,A[j]):
                return False
    return True

def verify_witness(V,w,goal='extension'):
    A=tuple(w['allocation']); m=len(V[0])
    if not valid_partition(A,m): return False
    if goal=='efx9': return is_efx(V,A)
    if not is_efr(V,A): return False
    if goal=='efr': return True
    g=w['deleted']; k=w['recipient']; B=tuple(w['predecessor'])
    if not (0<=g<m and 0<=k<4 and len(B)==4): return False
    C=list(B); C[k] |= 1<<g
    return not any(x>>g&1 for x in B) and tuple(C)==A and is_efx(V,B)

def oracle(V, goal='extension', deleted=None, limit=8, scan_all=False,
           deadline=float('inf'), use_jit=True, predecessor_pattern=None, max_recipient_size=10):
    """Complete failure verdict only after exhaustive partitions/matchings.

    For extension: default all m deletions; deleted=g fixes the missing good.
    scan_all=True returns exact counts but stores only limit witnesses.
    Deadline interruption is UNKNOWN, never a counterexample.
    """
    if goal not in ('extension','efx9','efr') or limit<1 or not 0<=max_recipient_size<=10:
        raise ValueError('Invalid goal or witness limit')
    rows=integer_rows(V); m=len(rows[0])
    if (predecessor_pattern is not None or max_recipient_size != 10) and goal != 'extension':
        raise ValueError('Restrictions apply only to the extension oracle')
    if predecessor_pattern is not None:
        predecessor_pattern=tuple(sorted(predecessor_pattern))
        if len(predecessor_pattern)!=4 or min(predecessor_pattern)<0 or sum(predecessor_pattern)!=m-1:
            raise ValueError('Predecessor pattern must be four nonnegative sizes summing to m-1')
    if goal=='efx9' and m!=9: raise ValueError('efx9 requires nine goods')
    if goal!='efx9' and m!=10: raise ValueError('This engine targets ten goods')
    if deleted is not None and not 0<=deleted<m: raise ValueError('Invalid good')
    sums,mins,sizes,fast=tables(rows)
    kernel=scan_kernel if fast and use_jit else scan_kernel.py_func
    mb,mc=matching_tables(); witnesses=[]; profiles=[]; all_complete=True
    dels=(list(range(m)) if deleted is None else [deleted]) if goal=='extension' else [-1]
    # Try goods with small maximum normalized cross-value first. Ordering only.
    if deleted is None and goal=='extension':
        dels.sort(key=lambda g:max(Fraction(rows[i][g],sum(rows[i]) or 1) for i in range(4)))
    started=time.perf_counter()
    for g in dels:
        goods=[h for h in range(m) if h!=g]
        local=partitions(len(goods))
        if predecessor_pattern is not None:
            local=np.array([p for p in local if tuple(sorted(int(x).bit_count() for x in p))==predecessor_pattern],dtype=np.int64).reshape(-1,4)
        lift=np.array([sum((1<<h) for q,h in enumerate(goods) if mask>>q&1)
                       for mask in range(1<<len(goods))],dtype=np.int64)
        parts=lift[local]
        new=np.array([rows[i][g] if g>=0 else 0 for i in range(4)],dtype=np.int64 if fast else object)
        profile={'deleted':g,'efx_count':0,'extension_count':0,'recipient_size_counts':[0]*11,
                 'partitions_scanned':0,'complete':True}
        for start in range(0,len(parts),512):
            if time.time()>=deadline:
                profile['complete']=False; all_complete=False
                break
            cap=max(1,limit-len(witnesses))
            mode=1 if goal=='extension' else (0 if goal=='efx9' else 2)
            ans,n,ec,sc,hist,visited,complete=kernel(parts[start:start+512],sums,mins,sizes,new,
                mode,mb,mc,PERMS,cap,scan_all,max_recipient_size)
            profile['partitions_scanned']+=int(visited)
            profile['efx_count']+=int(ec) if mode!=2 else 0
            profile['extension_count']+=int(sc)
            profile['recipient_size_counts']=[x+int(y) for x,y in zip(profile['recipient_size_counts'],hist)]
            for a in ans[:n]:
                if len(witnesses)>=limit: break
                A=[int(x) for x in a[:4]]
                if goal=='extension':
                    k=int(a[4]); B=list(A); A[k] |= 1<<g
                    w={'deleted':g,'recipient':k,'predecessor':B,'allocation':A}
                    s=B[k].bit_count()
                    w['scaled_margins']=[None if i==k else str((s+1)*bundle_value(rows,i,B[i])
                        -s*(bundle_value(rows,i,B[k])+rows[i][g])) for i in range(4)]
                else: w={'allocation':A}
                if not verify_witness(rows,w,goal):
                    raise AssertionError('Kernel witness failed independent exact check')
                witnesses.append(w)
            if not complete:
                profile['complete']=False; all_complete=False
                break
        profiles.append(profile)
        if not profile['complete'] or (len(witnesses)>=limit and not scan_all):
            all_complete=False
            break
    return {'status':'FOUND' if witnesses else ('ABSENT' if all_complete else 'UNKNOWN'),
            'goal':goal,'restrictions':{'predecessor_pattern':predecessor_pattern,'max_recipient_size':max_recipient_size},'witnesses':witnesses,'profiles':profiles,'complete':all_complete,
            'arithmetic':'int64' if fast else 'python-bigint','seconds':time.perf_counter()-started}

if __name__=='__main__':
    import argparse,json
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('matrix',help='JSON 4x10 matrix; rational strings accepted')
    p.add_argument('--goal',choices=['extension','efr','efx9'],default='extension')
    p.add_argument('--deleted',type=int)
    p.add_argument('--all',action='store_true',help='Full counts, no early success exit')
    p.add_argument('--out',default='oracle-result.json')
    p.add_argument('--pattern',help='Restrict predecessor sizes, e.g. 2,2,2,3; diagnostic only')
    p.add_argument('--max-recipient-size',type=int,default=10)
    a=p.parse_args()
    r=oracle(json.load(open(a.matrix)),a.goal,a.deleted,scan_all=a.all,
             predecessor_pattern=tuple(map(int,a.pattern.split(','))) if a.pattern else None,
             max_recipient_size=a.max_recipient_size)
    from pathlib import Path
    Path(a.out).write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))
