"""Two-source/two-singleton structural escapes. No global failure claim."""
from itertools import combinations
from efr.dangerous_moves import _context,_certificate
from efr.compensation import check_priority
from efr.capacity import diagnostics
from efr.oracle import is_efx,is_efr


def pair_source_escape(values,A,g,s,t):
    """D19: pair source reaches both singletons; other source has z_t<=u_t/2."""
    rows,items,val,R,u=_context(values,A,g)
    if s==t or s not in range(4) or t not in range(4):raise ValueError('Invalid sources')
    singles=[j for j in range(4) if j not in (s,t)]
    if A[s].bit_count()!=2 or A[t].bit_count()!=5 or any(A[j].bit_count()!=1 for j in singles):raise ValueError('Requires (1,1,2,5)')
    if any(val(j,A[k])>u[j] for j in range(4) for k in (s,t)):raise ValueError('Unenvied sources required')
    if any(rows[j][g]>u[j] for j in range(4)) or 2*rows[t][g]>u[t]:raise ValueError('Pool bounds required')
    graph=[[j for j in range(4) if val(i,A[j])>u[i]] for i in range(4)]
    paths={s:[s]};todo=[s]
    for i in todo:
        for j in graph[i]:
            if j not in paths:paths[j]=paths[i]+[j];todo.append(j)
    if any(j not in paths for j in singles):raise ValueError('Both singletons must be reachable')
    for h in items(A[s]):
        if rows[s][g]+rows[s][h]>u[s]:
            B=list(A);B[s]=(1<<g)|(1<<h)
            return _certificate(rows,A,B,'pair_source_self_improvement')
    target=diagnostics(values,A,g)[s]
    if target['feasible']:
        B=list(A);B[s]|=1<<g
        assert is_efr(rows,B)
        return dict(kind='pair_source_efr_insertion',allocation=B)
    j=next(j for j in singles if 2*(val(j,A[s])+rows[j][g])>3*u[j])
    h=next(h for h in items(A[s]) if rows[j][g]+rows[j][h]>u[j])
    path=paths[j];B=list(A)
    for k,l in zip(path,path[1:]):B[k]=A[l]
    B[j]=(1<<g)|(1<<h)
    return _certificate(rows,A,B,'pair_source_reachable_champion',path=path)


def retain_dominant_rotation(values,A,g,s,i,t,h,priority=(0,1,2,3)):
    """Try the new frame: i keeps its singleton plus g, s gets the other singleton.

    Redistribute all source goods between the other singleton owner and t,
    keeping h at t. At most 64 assignments; failure is only for this frame.
    """
    priority=check_priority(priority);rows,items,val,R,u=_context(values,A,g)
    if len({s,i,t})!=3 or not {s,i,t}<=set(range(4)):raise ValueError('Invalid identities')
    r=next(j for j in range(4) if j not in (s,i,t))
    if A[i].bit_count()!=1 or A[r].bit_count()!=1 or min(A[s].bit_count(),A[t].bit_count())<2:raise ValueError('Two singletons required')
    if h not in items(A[t]):raise ValueError('Donor item required')
    if val(s,A[r])<u[s]:return None
    available=A[s]|(A[t]^(1<<h));goods=items(available)
    for n in range(7):
        for chosen in combinations(goods,n):
            E=sum(1<<x for x in chosen)
            if val(r,E)<u[r]:continue
            B=list(A);B[i]=A[i]|(1<<g);B[s]=A[r];B[r]=E;B[t]=(available^E)|(1<<h)
            new=[val(j,B[j]) for j in range(4)]
            if tuple(new[j] for j in priority)<=tuple(u[j] for j in priority):continue
            if is_efx(rows,B):return _certificate(rows,A,B,'retain_dominant_singleton_rotation',priority=priority)
    return None
