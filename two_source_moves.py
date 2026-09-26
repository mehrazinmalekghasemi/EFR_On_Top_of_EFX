"""Exact two-bundle diagnostics; failure is NOT EFR nonexistence.

The pool may be repartitioned between two agents and the unallocated pool.
Other agents retain their bundles. Integer arithmetic only.
"""
from itertools import combinations,permutations
from oracle import integer_rows, tables, is_efx


def subsets(mask):
    t=mask
    while True:
        yield t
        if not t:break
        t=(t-1)&mask


def compensated_pair(values,A,g):
    """Safe pair compensation for a two-good donor; no source assumption needed."""
    rows=integer_rows(values);sums,mins,sizes,_=tables(rows)
    own=[int(sums[i,A[i]]) for i in range(4)]
    if not is_efx(rows,A) or any(rows[i][g]>own[i] for i in range(4)):return []
    out=[]
    for k in range(4):
        if A[k].bit_count()!=2:continue
        for i in range(4):
            if i==k or A[i].bit_count()<2:continue
            for h in range(len(rows[0])):
                if not A[k]>>h&1 or rows[i][g]+rows[i][h]<=own[i]:continue
                for y in range(len(rows[0])):
                    if not A[i]>>y&1 or rows[k][y]<rows[k][h]:continue
                    B=A.copy();B[k]=(A[k]^(1<<h))|(1<<y);B[i]=(1<<g)|(1<<h)
                    assert is_efx(rows,B)
                    assert all(sums[j,B[j]]>=own[j] for j in range(4))
                    out.append({'kind':'compensated_pair','donor':k,'champion':i,'taken':h,'compensation':y,'allocation':B})
    return out


def four_source_progress(values,A,g):
    """Construct the four-source theorem's EFR completion or EFX improvement.

    BCFF restoration after this move is a theorem dependency, not implemented.
    """
    from capacity import validate,diagnostics
    rows=integer_rows(values);validate(rows,A,g)
    assert len(rows[0])==10 and sum(x.bit_count() for x in A)==9
    sums,mins,sizes,_=tables(rows);own=[int(sums[i,A[i]]) for i in range(4)]
    assert all(sums[i,A[j]]<=own[i] for i in range(4) for j in range(4)), 'Requires four sources'
    for target in diagnostics(rows,A,g):
        if target['feasible']:
            # diagnostics lists recipients in agent order.
            k=target['recipient'];B=A.copy();B[k]|=1<<g
            return {'kind':'complete_efr','allocation':B}
    for i in range(4):
        if rows[i][g]>own[i]:
            B=A.copy();B[i]=1<<g
            return {'kind':'pool_singleton','allocation':B}
    assert sorted(x.bit_count() for x in A)==[2,2,2,3]
    for i in range(4):
        for h in range(10):
            if A[i]>>h&1 and rows[i][g]+rows[i][h]>own[i]:
                B=A.copy();B[i]=(1<<g)|(1<<h)
                assert is_efx(rows,B)
                return {'kind':'self_pair','allocation':B}
    moves=compensated_pair(rows,A,g)
    if moves:return moves[0]
    t=next(i for i in range(4) if A[i].bit_count()==3)
    for h in range(10):
        if A[t]>>h&1:
            B=A.copy();B[t]=(A[t]^(1<<h))|(1<<g)
            if sums[t,B[t]]>own[t] and is_efx(rows,B):return {'kind':'triple_replacement','allocation':B}
    raise AssertionError('Contradicts the proved four-source progress lemma')


def compensated_path(values,A,g):
    """Three-agent path: s takes old A_i, i takes {g,h}, t takes old A_s.

    Agent t may lose utility, but remains EFX. Requiring i<t makes the
    improvement strict for the fixed lexicographic order 0,1,2,3.
    """
    rows=integer_rows(values);sums,mins,sizes,_=tables(rows)
    own=[int(sums[i,A[i]]) for i in range(4)]
    if not is_efx(rows,A) or any(rows[i][g]>own[i] for i in range(4)):return []
    result=[]
    for s,i,t in permutations(range(4),3):
        if i>=t or A[t].bit_count()<2 or sums[s,A[i]]<own[s]:continue
        for h in range(len(rows[0])):
            if not A[t]>>h&1 or rows[i][g]+rows[i][h]<=own[i]:continue
            B=A.copy();B[s]=A[i];B[i]=(1<<g)|(1<<h);B[t]=A[s]
            if any(sums[t,B[t]]<sums[t,B[j]]-mins[t,B[j]] for j in range(4) if j!=t):continue
            assert is_efx(rows,B)
            new=[int(sums[j,B[j]]) for j in range(4)]
            assert tuple(new)>tuple(own)
            result.append({'path_start':s,'champion':i,'donor':t,'good':h,'allocation':B,'old_utilities':own,'new_utilities':new})
    return result


def local_moves(values,A,g,agents=None,limit=1,dominance='pareto'):
    """Exhaust ALL repartitions for each selected pair, including partial states.

    Return complete EFR outcomes or partial EFX improvements. lex uses fixed
    agent order 0,1,2,3. A negative result covers only this two-bundle move class.
    """
    rows=integer_rows(values);sums,mins,sizes,_=tables(rows)
    own=[int(sums[i,A[i]]) for i in range(4)]
    assert is_efx(rows,A)
    pairs=list(combinations(range(4) if agents is None else agents,2))
    out=[];checked=0;by_pair=[]
    def fair(B,goal):
        vals=[int(sums[i,B[i]]) for i in range(4)]
        for i in range(4):
            for j in range(4):
                if i==j:continue
                if goal=='efx':
                    if vals[i]<int(sums[i,B[j]]-mins[i,B[j]]):return False
                elif sizes[B[j]]*vals[i]<(sizes[B[j]]-1)*sums[i,B[j]]:return False
        return True
    for a,b in pairs:
        pool=A[a]|A[b]|(1<<g);count=0
        for X in subsets(pool):
            for Y in subsets(pool^X):
                checked+=1;count+=1
                B=A.copy();B[a]=X;B[b]=Y
                complete=(X|Y)==pool
                if complete and fair(B,'efr'):kind='complete_efr'
                else:
                    new=[int(sums[i,B[i]]) for i in range(4)]
                    better=(all(x>=y for x,y in zip(new,own)) and new!=own) if dominance=='pareto' else tuple(new)>tuple(own)
                    if not better or not fair(B,'efx'):continue
                    kind=dominance+'_efx'
                out.append({'kind':kind,'agents':[a,b],'allocation':B,'old_utilities':own,'new_utilities':[int(sums[i,B[i]]) for i in range(4)]})
                if limit and len(out)>=limit:return {'status':'FOUND','moves':out,'checked':checked,'complete':False}
        by_pair.append({'agents':[a,b],'assignments':count})
    return {'status':'FOUND' if out else 'ABSENT','moves':out,'checked':checked,'complete':True,'by_pair':by_pair,'dominance':dominance}
