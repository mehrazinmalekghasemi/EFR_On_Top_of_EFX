"""Constructive dangerous-item proofs. No valuation-space search."""
from efr.capacity import validate
from efr.oracle import is_efx
from efr.compensation import check_priority


def _context(values,A,g):
    rows=validate(values,A,g)
    if len(rows)!=4 or len(rows[0])!=10:raise ValueError('Requires four agents and ten goods')
    items=lambda mask:[h for h in range(10) if mask>>h&1]
    value=lambda j,mask:sum(rows[j][h] for h in items(mask))
    deletion=lambda j,mask:max((value(j,mask)-rows[j][h] for h in items(mask)),default=0)
    own=[value(j,A[j]) for j in range(4)]
    return rows,items,value,deletion,own


def _certificate(rows,A,B,kind,priority=None,**details):
    assert sum(b.bit_count() for b in B)==(B[0]|B[1]|B[2]|B[3]).bit_count()
    assert is_efx(rows,B)
    val=lambda j,b:sum(rows[j][h] for h in range(10) if b>>h&1)
    old=[val(j,A[j]) for j in range(4)];new=[val(j,B[j]) for j in range(4)]
    if priority is None:
        assert all(a>=b for a,b in zip(new,old)) and any(a>b for a,b in zip(new,old))
    else:assert tuple(new[j] for j in priority)>tuple(old[j] for j in priority)
    return dict(kind=kind,allocation=B,old_utilities=list(map(str,old)),
                new_utilities=list(map(str,new)),**details)


def both_champions_progress(values,A,g,p,q,r):
    """Proved both-champions branch in the all-envious-source star.

    Raises ValueError outside the stated elementary extremal assumptions.
    Returns a Pareto-improving partial EFX allocation. Restoration is not run.
    See research/DANGEROUS_ITEM_PROGRESS.md, Theorem D4.
    """
    rows,items,val,R,u=_context(values,A,g)
    if len({p,q,r})!=3 or not {p,q,r}<=set(range(4)):raise ValueError('Invalid agent identities')
    o=next(j for j in range(4) if j not in {p,q,r})
    def require(condition,message):
        if not condition:raise ValueError(message)
    require([A[j].bit_count() for j in (o,p,q,r)]==[1,2,3,3],'Requires singleton, pair, triple, triple')
    z=[rows[j][g] for j in range(4)]
    require(all(z[j]<=u[j] for j in range(4)),'Pool bound required')
    require(all(val(j,A[k])<=u[j] for j in range(4) for k in (p,q,r)),'Three source bundles required')
    require(all(val(k,A[o])>u[k] for k in (p,q,r)),'All sources must envy the singleton')
    require(all(z[k]+rows[k][h]<=u[k] for k in (p,q,r) for h in items(A[k])), 'No self-pair improvement required')
    require(all(z[o]+rows[o][h]<=u[o] for k in (p,q,r) for h in items(A[k])), 'Singleton reachability cuts required')
    champions={k:[h for h in items(A[p]) if z[k]+rows[k][h]>u[k]] for k in (q,r)}
    require(all(champions.values()),'Both triples must champion the pair')
    require(all(rows[p][y]<rows[p][h] for k in (q,r) for h in champions[k] for y in items(A[k])), 'Pair compensation already available')
    require(any(2*(val(k,A[p])+z[k])>3*u[k] for k in (q,r)), 'Insertion into pair must be blocked')

    # At least one triple is high-pool. Exhaust just its three replacements,
    # and those of any other high-pool triple, as in the proof.
    for k in (q,r):
        if 2*z[k]<=u[k]:continue
        for h in items(A[k]):
            B=list(A);B[k]=(A[k]^(1<<h))|(1<<g)
            if is_efx(rows,B):return _certificate(rows,A,B,'triple_replacement',agent=k,removed=h)
    assert all(2*z[k]>u[k] and 3*z[k]<=2*u[k] for k in (q,r))
    danger_q=[h for h in items(A[r]) if z[q]+rows[q][h]>u[q]]
    danger_r=[h for h in items(A[q]) if z[r]+rows[r][h]>u[r]]
    assert len(danger_q)==len(danger_r)==2
    c,d=danger_r[0],danger_q[0]
    B=list(A);B[q]=(A[q]^(1<<c))|(1<<d);B[r]=(A[r]^(1<<d))|(1<<c)
    if is_efx(rows,B):return _certificate(rows,A,B,'dangerous_exchange',goods=[c,d])

    # An external blocker envies a mixed pair in one changed triple. Orient
    # Q,R so its R item is dangerous to Q's owner.
    blocker=None
    for j in (o,p):
        for a in items(A[q]^(1<<c)):
            if rows[j][a]+rows[j][d]>u[j]:blocker=(j,q,r,a,d);break
        if blocker is not None:break
        for b in items(A[r]^(1<<d)):
            if rows[j][c]+rows[j][b]>u[j]:blocker=(j,r,q,b,c);break
        if blocker is not None:break
    assert blocker is not None
    j,Q,Rowner,a,b=blocker
    E=(1<<a)|(1<<b)
    remaining_R=A[Rowner]^(1<<b)
    danger=[h for h in items(A[Q]) if z[Rowner]+rows[Rowner][h]>u[Rowner]]
    if a in danger:
        other=next(h for h in danger if h!=a)
        C=(1<<other)|remaining_R
    else:
        e=max(items(remaining_R),key=lambda h:rows[Rowner][h])
        C=sum(1<<h for h in danger)|(1<<e)
    assert not C&E and val(Rowner,C)>u[Rowner]
    assert R(Q,C)<=u[Q] and R(j,C)<=u[j]
    k=p if j==o else o
    B=list(A);B[j]=E;B[Rowner]=C
    B[Q]=A[o] if j==o else (1<<g)|(1<<champions[Q][0])
    if R(k,C)<=u[k]:
        return _certificate(rows,A,B,'three_agent_mixed_repair',blocker=j,mixed_pair=E,compensation=C)
    # A second mixed pair is disjoint from E, since it lies in C.
    F=None
    for x in items(C&A[Q]):
        for y in items(C&A[Rowner]):
            if rows[k][x]+rows[k][y]>u[k]:F=(1<<x)|(1<<y);break
        if F is not None:break
    assert F is not None and not E&F
    B=list(A);B[j]=E;B[k]=F;B[Q]=A[o];B[Rowner]=(1<<g)|(1<<champions[Rowner][0])
    return _certificate(rows,A,B,'four_agent_disjoint_pairs',mixed_pairs=[E,F])


def residual_singleton_relay(values,A,g,s,i,t,h,priority=(0,1,2,3)):
    """Theorem R1: keep the donor's remainder; two other targets are singletons.

    None means the theorem's hypotheses fail, not that no repair exists.
    """
    priority=check_priority(priority)
    rows,items,val,R,u=_context(values,A,g)
    if len({s,i,t})!=3 or not {s,i,t}<=set(range(4)):raise ValueError('Invalid agent identities')
    r=next(j for j in range(4) if j not in {s,i,t})
    if not 0<=h<10 or not A[t]>>h&1:return None
    if A[i].bit_count()!=1 or A[r].bit_count()!=1 or min(A[s].bit_count(),A[t].bit_count())<2:return None
    if any(rows[j][g]>u[j] for j in range(4)):return None
    if val(s,A[i])<u[s] or rows[i][g]+rows[i][h]<=u[i]:return None
    if rows[t][g]+rows[t][h]>u[t] or 2*rows[t][h]>u[t]:return None
    B=list(A);B[s]=A[i];B[i]=(1<<g)|(1<<h);B[t]=A[t]^(1<<h)
    new=[val(j,B[j]) for j in range(4)]
    if tuple(new[j] for j in priority)<=tuple(u[j] for j in priority):return None
    return _certificate(rows,A,B,'residual_singleton_relay',priority=priority,agent_priority=list(priority))


def full_star_progress(values,A,g,p,q,r):
    """T11: complete all-envious-source (1,2,3,3) extremal branch.

    Requires the same elementary reductions as the earlier both-champion
    theorem. Handles one or two pair champions without a priority assumption.
    Returns Pareto-improving EFX; fixed-priority restoration is not run.
    """
    rows,items,val,R,u=_context(values,A,g)
    if len({p,q,r})!=3 or not {p,q,r}<=set(range(4)):raise ValueError('Invalid agents')
    o=next(j for j in range(4) if j not in {p,q,r})
    def require(ok,msg):
        if not ok:raise ValueError(msg)
    z=[rows[j][g] for j in range(4)]
    require([A[j].bit_count() for j in (o,p,q,r)]==[1,2,3,3],'Wrong size profile')
    require(all(z[j]<=u[j] for j in range(4)),'Pool bound required')
    require(all(val(j,A[k])<=u[j] for j in range(4) for k in (p,q,r)),'Source bounds required')
    require(all(val(k,A[o])>u[k] for k in (p,q,r)),'All sources must envy singleton')
    require(all(z[k]+rows[k][h]<=u[k] for k in (p,q,r) for h in items(A[k])),'Self-pair cuts required')
    require(all(z[o]+rows[o][h]<=u[o] for k in (p,q,r) for h in items(A[k])),'Singleton reachability cuts required')
    champions={k:[h for h in items(A[p]) if z[k]+rows[k][h]>u[k]] for k in (q,r)}
    require(any(2*(val(k,A[p])+z[k])>3*u[k] for k in (q,r)),'Pair insertion must be blocked')
    require(all(rows[p][y]<rows[p][h] for k in (q,r) for h in champions[k] for y in items(A[k])),'Pair compensation already available')
    if all(champions.values()):return both_champions_progress(values,A,g,p,q,r)
    require(any(champions.values()),'At least one pair champion is necessary')
    if not champions[q]:q,r=r,q  # Role names only; agent identities and priorities do not change.
    h=champions[q][0]
    for k in (q,r):
        if 2*z[k]<=u[k]:continue
        for removed in items(A[k]):
            B=list(A);B[k]=(A[k]^(1<<removed))|(1<<g)
            if is_efx(rows,B):return _certificate(rows,A,B,'sole_triple_replacement',agent=k)
    assert all(2*z[k]>u[k] and 3*z[k]<=2*u[k] for k in (q,r))
    Dq=[x for x in items(A[r]) if z[q]+rows[q][x]>u[q]]
    Dr=[x for x in items(A[q]) if z[r]+rows[r][x]>u[r]]
    assert len(Dr)==2 and len(Dq) in (1,2)
    if len(Dq)==2:
        # Every mixed Q/R pair is safe to both triple owners. Keep the sole
        # pair champion q in that role even when the external violation changes.
        c,d=Dr[0],Dq[0]
        B=list(A);B[q]=(A[q]^(1<<c))|(1<<d);B[r]=(A[r]^(1<<d))|(1<<c)
        if is_efx(rows,B):return _certificate(rows,A,B,'sole_mutual_exchange')
        bad=None
        for j in (o,p):
            for x in items(A[q]):
                for y in items(A[r]):
                    if rows[j][x]+rows[j][y]>u[j]:bad=(j,x,y);break
                if bad is not None:break
            if bad is not None:break
        assert bad is not None
        j,x,y=bad;k=p if j==o else o;E=(1<<x)|(1<<y)
        c=next(a for a in Dr if a!=x)
        C=(A[r]^(1<<y))|(1<<c)
        assert val(r,C)>u[r] and R(q,C)<=u[q] and R(j,C)<=u[j]
        B=list(A);B[j]=E;B[r]=C;B[q]=A[o] if j==o else (1<<g)|(1<<h)
        if R(k,C)<=u[k]:return _certificate(rows,A,B,'sole_mutual_three_agent')
        F=next((1<<x2)|(1<<y2) for x2 in items(C&A[q]) for y2 in items(C&A[r]) if rows[k][x2]+rows[k][y2]>u[k])
        B=list(A);B[j]=E;B[k]=F;B[q]=(1<<g)|(1<<h);B[r]=A[o]
        return _certificate(rows,A,B,'sole_mutual_four_agent')
    # Split danger: q and p block different items of R.
    d=Dq[0];Dp=[x for x in items(A[r]) if z[p]+rows[p][x]>u[p]]
    assert len(Dp)==1 and Dp[0]!=d
    e=Dp[0];ell=next(x for x in items(A[p]) if x!=h);c,c2=Dr
    C=(A[r]^(1<<e))|(1<<c)
    B=list(A);B[p]=(1<<ell)|(1<<e);B[q]=(1<<g)|(1<<h);B[r]=C
    assert val(p,B[p])>u[p] and val(r,C)>u[r] and R(p,C)<=u[p]
    if R(q,C)>val(q,B[q]):
        assert rows[q][c]+rows[q][d]>val(q,B[q])
        B[q]=(1<<c)|(1<<d);B[r]=(1<<g)|(1<<c2)
        return _certificate(rows,A,B,'sole_split_champion_blocker')
    if R(o,C)>u[o]:
        x=next(x for x in items(A[r]^(1<<e)) if rows[o][c]+rows[o][x]>u[o])
        B[o]=(1<<c)|(1<<x);B[q]=A[o];B[r]=(1<<g)|(1<<c2)
        return _certificate(rows,A,B,'sole_split_singleton_blocker')
    return _certificate(rows,A,B,'sole_split_three_agent')


def repair_pair_blocker(values,A,g,t,j,h,b,y):
    """F4: a blocking pair yields a safe exchange without using the pool good.

    t receives {h,b}; pair owner j replaces b by y. Return None outside
    the sufficient conditions; no global repair failure is inferred.
    """
    rows,items,val,R,u=_context(values,A,g)
    if t==j or t not in range(4) or j not in range(4):raise ValueError('Invalid agents')
    if min(h,b,y)<0 or max(h,b,y)>=10:return None
    if A[t].bit_count()<2 or A[j].bit_count()!=2:return None
    if h==y or not A[t]>>h&1 or not A[t]>>y&1 or not A[j]>>b&1:return None
    if rows[t][h]+rows[t][b]<=u[t] or rows[j][y]<rows[j][b]:return None
    B=list(A);B[t]=(1<<h)|(1<<b);B[j]=(A[j]^(1<<b))|(1<<y)
    return _certificate(rows,A,B,'pool_free_pair_blocker_repair')
