"""Verified elementary moves for the restoration proof.

BCFF restoration is a cited theorem, not implemented in this module.
"""
from collections import deque
from oracle import integer_rows,tables,is_efx
from capacity import validate


def lift_preserving_start(values,A,g):
    """Integer nondegenerate refinement preserving the supplied EFX-nine start.

All EFX and EFR outputs for the lifted instance are valid for the input.
An empty starting bundle should instead receive g immediately.
"""
    rows=integer_rows(values);validate(rows,A,g)
    if any(b==0 for b in A):raise ValueError('Empty bundle: use direct insertion')
    m=len(rows[0]);C=1<<m
    bonus=[[C*int(bool(A[i]>>h&1))+(1<<h) for h in range(m)] for i in range(4)]
    K=2*(m+1)*max(map(sum,bonus))+1
    lifted=[[K*rows[i][h]+bonus[i][h] for h in range(m)] for i in range(4)]
    validate(lifted,A,g)
    return {'values':lifted,'scale':K,'bonus':bonus,'scaled_original':rows}


def source_analysis(values,A,g):
    rows=integer_rows(values);validate(rows,A,g)
    sums,mins,sizes,_=tables(rows)
    own=[int(sums[i,A[i]]) for i in range(4)]
    graph=[[j for j in range(4) if sums[i,A[j]]>own[i]] for i in range(4)]
    sources=[j for j in range(4) if not any(j in graph[i] for i in range(4))]
    options=[];moves=[]
    for k in sources:
        parent={k:None};queue=deque([k])
        while queue:
            i=queue.popleft()
            for j in graph[i]:
                if j not in parent:parent[j]=i;queue.append(j)
        candidates=[];mask=A[k]|(1<<g);T=mask
        while T:
            if all(sums[i,T]-mins[i,T]<=own[i] for i in range(4)):
                champions=[i for i in range(4) if sums[i,T]>own[i]]
                reachable=[i for i in champions if i in parent]
                if champions:candidates.append({'bundle':T,'champions':champions,'reachable':reachable})
                for i in reachable:
                    path=[];current=i
                    while current is not None:path.append(current);current=parent[current]
                    path.reverse();B=list(A)
                    for a,b in zip(path,path[1:]):B[a]=A[b]
                    B[i]=T
                    assert is_efx(rows,B)
                    assert all(sums[j,B[j]]>=own[j] for j in range(4))
                    assert all(sums[j,B[j]]>own[j] for j in path)
                    assert sum(b.bit_count() for b in B)==(B[0]|B[1]|B[2]|B[3]).bit_count()
                    moves.append({'allocation':B,'path':path,'source':k,'champion':i,
                                  'unallocated':((1<<len(rows[0]))-1)^(B[0]|B[1]|B[2]|B[3])})
            T=(T-1)&mask
        options.append({'source':k,'reachable_agents':sorted(parent),'candidates':candidates})
    return {'graph':graph,'sources':sources,'options':options,'moves':moves}


def improving_transfers(values,A,g):
    rows=integer_rows(values);validate(rows,A,g);out=[]
    for i in range(4):
        for j in range(i+1,4):
            for h in range(len(rows[0])):
                if A[j]>>h&1 and rows[i][h]>0:
                    B=list(A);B[i]|=1<<h;B[j]^=1<<h
                    if is_efx(rows,B):out.append({'predecessor':B,'from_agent':j,'to_agent':i,'good':h})
    return out
