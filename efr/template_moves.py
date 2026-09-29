"""Small proof-backed moves used while probing template 1125_041."""
from efr.dangerous_moves import _context,_certificate


def weak_pair_path(values,A,g,path,h):
    """D24: a strict old envy path needs only weak acceptance of its final pair."""
    rows,items,val,R,u=_context(values,A,g)
    if len(path)<2 or len(set(path))!=len(path) or not set(path)<=set(range(4)):raise ValueError('Simple nonempty path required')
    if A[path[0]].bit_count()<2 or h not in items(A[path[0]]):return None
    if any(rows[j][g]>u[j] for j in range(4)):return None
    if any(val(a,A[b])<=u[a] for a,b in zip(path,path[1:])):return None
    j=path[-1]
    if rows[j][g]+rows[j][h]<u[j]:return None
    B=list(A)
    for a,b in zip(path,path[1:]):B[a]=A[b]
    B[j]=(1<<g)|(1<<h)
    return _certificate(rows,A,B,'weak_pair_path',path=list(path))


def exchange_pool_and_release(values,A,g,s,t,h,Y,Z):
    """D25: two source owners improve; check only the two unchanged observers."""
    rows,items,val,R,u=_context(values,A,g)
    if s==t or s not in range(4) or t not in range(4):raise ValueError('Invalid owners')
    if h not in items(A[s]) or Y<0 or Z<0 or Y&Z or (Y|Z)&~A[t]:return None
    if any(val(i,A[j])>u[i] for i in range(4) for j in (s,t)):return None
    if val(s,Y)+rows[s][g]<rows[s][h] or val(t,Y|Z)>rows[t][h]:return None
    if val(s,Y|Z)<rows[s][h] or val(t,Y)+rows[t][g]>rows[t][h]:return None
    B=list(A);B[s]=(A[s]^(1<<h))|Y|(1<<g);B[t]=(A[t]&~(Y|Z))|(1<<h)
    if val(s,B[s])==u[s] and val(t,B[t])==u[t]:return None
    if any(R(k,B[j])>u[k] for k in range(4) if k not in (s,t) for j in (s,t)):return None
    return _certificate(rows,A,B,'exchange_pool_and_release',released=Z)
