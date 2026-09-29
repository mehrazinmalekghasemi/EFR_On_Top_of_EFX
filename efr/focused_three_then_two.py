"""D21-D23 constructive subcases; no global nonexistence verdict."""
from itertools import combinations
from efr.dangerous_moves import _context,_certificate
from efr.oracle import is_efx


def _paths(val,A,u,s):
    paths={s:[s]};todo=[s]
    for i in todo:
        for j in range(4):
            if j not in paths and val(i,A[j])>u[i]:paths[j]=paths[i]+[j];todo.append(j)
    return paths


def singleton_pair_mutual(values,A,g,p,q,r):
    """D21: singleton blocks pair insertion; mutual triple dangers permit escape."""
    rows,items,val,R,u=_context(values,A,g)
    if len({p,q,r})!=3 or not {p,q,r}<=set(range(4)):raise ValueError('Invalid roles')
    o=next(j for j in range(4) if j not in (p,q,r));z=[row[g] for row in rows]
    checks=[ [A[j].bit_count() for j in (o,p,q,r)]==[1,2,3,3],
      all(z[j]<=u[j] for j in range(4)),
      all(val(j,A[k])<=u[j] for j in range(4) for k in (p,q,r)),
      all(val(k,A[o])>u[k] for k in (q,r)),
      all(z[k]+rows[k][x]<=u[k] for k in (p,q,r) for x in items(A[k])),
      all(z[o]+rows[o][x]<=u[o] for k in (q,r) for x in items(A[k])),
      2*(val(o,A[p])+z[o])>3*u[o]]
    if not all(checks):raise ValueError('D21 guards required')
    Dq=[x for x in items(A[r]) if z[q]+rows[q][x]>u[q]]
    Dr=[x for x in items(A[q]) if z[r]+rows[r][x]>u[r]]
    if len(Dq)!=2 or len(Dr)!=2:raise ValueError('Mutual two-item danger required')
    c,d=Dr[0],Dq[0];B=list(A)
    B[q]=(A[q]^(1<<c))|(1<<d);B[r]=(A[r]^(1<<d))|(1<<c)
    if is_efx(rows,B):return _certificate(rows,A,B,'singleton_champion_mutual_exchange')
    x,y=next((x,y) for x in items(A[q]) for y in items(A[r]) if rows[p][x]+rows[p][y]>u[p])
    c=next(c for c in Dr if c!=x)
    h=next(h for h in items(A[p]) if z[o]+rows[o][h]>u[o])
    B=list(A);B[p]=(1<<x)|(1<<y);B[o]=(1<<g)|(1<<h);B[q]=A[o];B[r]=(A[r]^(1<<y))|(1<<c)
    return _certificate(rows,A,B,'singleton_champion_four_agent_repair')


def single_observer_quad_escape(values,A,g,s):
    """D22: one observer supplies all forbidden pairs and is reachable from s."""
    rows,items,val,R,u=_context(values,A,g)
    if s not in range(4) or A[s].bit_count()!=4:raise ValueError('Four-good source required')
    if any(val(j,A[s])>u[j] or rows[j][g]>u[j] for j in range(4)):raise ValueError('Source and pool bounds required')
    for x in items(A[s]):
        if rows[s][g]+rows[s][x]>u[s]:
            B=list(A);B[s]=(1<<g)|(1<<x)
            return _certificate(rows,A,B,'quad_self_pair_escape')
    edges=[(j,Y) for j in range(4) if j!=s for pair in combinations(items(A[s]),2)
           for Y in [sum(1<<x for x in pair)] if rows[j][g]+val(j,Y)>u[j]]
    if len({j for j,Y in edges})!=1:return None
    j,Y=edges[0];paths=_paths(val,A,u,s)
    if j not in paths:return None
    T=Y|(1<<g);B=list(A);path=paths[j]
    for a,b in zip(path,path[1:]):B[a]=A[b]
    B[j]=T
    return _certificate(rows,A,B,'single_observer_quad_champion',path=path)


def reverse_dangerous_transfer(values,A,g,s,t,x):
    """D23: compensate s for x; t strictly prefers {g,x}. Try all 16 Y subsets."""
    rows,items,val,R,u=_context(values,A,g)
    if s==t or s not in range(4) or t not in range(4):raise ValueError('Invalid sources')
    singles=[j for j in range(4) if j not in (s,t)]
    if A[s].bit_count()!=3 or A[t].bit_count()!=4 or any(A[j].bit_count()!=1 for j in singles):raise ValueError('Requires (1,1,3,4)')
    if x not in items(A[s]) or rows[t][g]+rows[t][x]<=u[t]:raise ValueError('Dangerous source item required')
    if any(rows[j][g]>u[j] for j in range(4)) or any(val(j,A[k])>u[j] for j in range(4) for k in (s,t)):raise ValueError('Source and pool bounds required')
    paths=_paths(val,A,u,s)
    if any(j not in paths for j in singles):raise ValueError('Both singleton owners must be reachable')
    for n in range(5):
        for ys in combinations(items(A[t]),n):
            Y=sum(1<<y for y in ys)
            if val(s,Y)<rows[s][x] or val(t,Y)>u[t]-rows[t][g]:continue
            C=(A[s]^(1<<x))|Y;B=list(A);B[s]=C;B[t]=(1<<g)|(1<<x)
            if is_efx(rows,B):return _certificate(rows,A,B,'reverse_dangerous_compensation',compensation=Y)
            E,j=next((E,j) for k in range(1,C.bit_count()+1) for es in combinations(items(C),k)
                     for E in [sum(1<<e for e in es)] for j in range(4) if val(j,E)>u[j])
            assert j!=t
            B=list(A);B[t]=(1<<g)|(1<<x)
            if j==s:B[s]=E
            else:
                path=paths[j]
                for a,b in zip(path,path[1:]):B[a]=A[b]
                B[j]=E
            return _certificate(rows,A,B,'reverse_dangerous_blocker_escape',compensation=Y,champion=j)
    return None
