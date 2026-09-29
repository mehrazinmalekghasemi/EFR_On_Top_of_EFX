"""Separate local strategies by source structure; no global failure verdict."""
from itertools import combinations, product
from efr.dominant import dominant_relay
from efr.dangerous_moves import _context, _certificate
from efr.compensation import check_priority
from efr.oracle import is_efx


def surplus_lift(values,A,g,s,i,t,h,priority=(0,1,2,3)):
    """D16: allocate leftover goods jointly to blocker, donor, or pool."""
    priority=check_priority(priority)
    base=dominant_relay(values,A,g,s,i,t,h,priority)
    if base['move']:return dict(move=base['move'],assignments_checked=0)
    rows,items,val,R,u=_context(values,A,g)
    H=A[s]|(A[t]^(1<<h));K=list(A);K[s]=A[i];K[i]=(1<<g)|(1<<h)
    seen=set();checked=0
    for ob in base['obstructions']:
        for block in ob['blockers']:
            j,E=block['agent'],block['subset']
            if (j,E) in seen:continue
            seen.add((j,E));left=items(H&~E)
            assert len(left)<=4
            for choices in product(range(3),repeat=len(left)):
                checked+=1
                X=sum(1<<x for x,c in zip(left,choices) if c==1)
                F=sum(1<<x for x,c in zip(left,choices) if c==2)
                B=list(K);B[j]=E|X;B[t]=K[j]|F
                new=[val(k,B[k]) for k in range(4)]
                if tuple(new[k] for k in priority)<=tuple(u[k] for k in priority):continue
                if not is_efx(rows,B):continue
                return dict(move=_certificate(rows,A,B,'blocker_surplus_lift',priority=priority,
                                               blocker=j,envied_subset=E,surplus_goods=X,top_up=F),
                            assignments_checked=checked)
    return dict(move=None,assignments_checked=checked,
                scope='Only joint splits of the recorded D12-D13 blocker leftovers')


def quad_replacement(values,A,g,s):
    """D18: forbidden-pair intersection criterion for an unenvied 4-good source."""
    rows,items,val,R,u=_context(values,A,g)
    if s not in range(4) or A[s].bit_count()!=4:raise ValueError('Four-good source required')
    if any(val(j,A[s])>u[j] for j in range(4)):raise ValueError('Bundle must be unenvied')
    edges=[]
    for j in range(4):
        if j==s:continue
        for pair in combinations(items(A[s]),2):
            Y=sum(1<<x for x in pair)
            if rows[j][g]+val(j,Y)>u[j]:edges.append(dict(observer=j,pair=Y))
    common=A[s]
    for edge in edges:common &= edge['pair']
    profitable=[x for x in items(common) if rows[s][g]>rows[s][x]]
    move=None
    if profitable:
        x=profitable[0];B=list(A);B[s]=(A[s]^(1<<x))|(1<<g)
        move=_certificate(rows,A,B,'quad_safe_replacement',removed=x)
    obstruction=[]
    if not common:
        for a,b in combinations(edges,2):
            if not a['pair']&b['pair']:obstruction=[a,b];break
        if not obstruction:
            for a,b,c in combinations(edges,3):
                if not a['pair']&b['pair']&c['pair']:
                    obstruction=[a,b,c];break
        assert obstruction
    return dict(move=move,forbidden_pairs=edges,common_items=items(common),
                profitable_common_items=profitable,intersection_obstruction=obstruction,
                scope='Exact strict Pareto replacement test, not all possible moves')
