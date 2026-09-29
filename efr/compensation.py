"""Certified local relay moves; no valuation search or universal coverage claim."""
from itertools import permutations
from efr.oracle import integer_rows, is_efx
from efr.capacity import validate


def check_priority(priority):
    priority=tuple(priority)
    if len(priority)!=4 or set(priority)!=set(range(4)):
        raise ValueError('priority must order all four agent identities exactly once')
    return priority


def compensated_relay(values,A,g,s,i,t,T,priority=(0,1,2,3)):
    """Certify s<-A_i, i<-T, t<-best safe pair from A_s union (A_t minus T).

    Conditions and exact optimality within this compensation class are proved
    in research/SOURCE_COMPENSATION.md. Return None if the sufficient conditions
    fail; this is NOT failure of EFR existence, Mode C, or all three-agent moves.
    T is a bit mask. The priority belongs to physical agent identities and must
    be carried through every relabeling and restoration step.
    """
    priority=check_priority(priority)
    rows=integer_rows(values);validate(rows,A,g)
    if len(rows)!=4 or len({s,i,t})!=3 or not {s,i,t}<=set(range(4)):
        raise ValueError('three distinct valid agents are required')
    if not is_efx(rows,A):return None
    m=len(rows[0]);goods=lambda mask:[h for h in range(m) if mask>>h&1]
    value=lambda j,mask:sum(rows[j][h] for h in goods(mask))
    deletion=lambda j,mask:max((value(j,mask)-rows[j][h] for h in goods(mask)),default=0)
    own=[value(j,A[j]) for j in range(4)]
    if any(rows[j][g]>own[j] for j in range(4)):return None
    if A[s].bit_count()<2 or A[t].bit_count()<2:return None
    if T<0 or not T>>g&1 or T & ~(A[t]|(1<<g)):return None
    if value(i,T)<=own[i] or value(s,A[i])<own[s]:return None
    if any(deletion(j,T)>own[j] for j in range(4)):return None
    r=next(j for j in range(4) if j not in {s,i,t})
    available=A[s]|(A[t]&~T)
    selected=sorted(goods(available),key=lambda h:(-rows[t][h],h))[:2]
    C=sum(1<<h for h in selected)
    fairness_floor=max(deletion(t,T),deletion(t,A[i]),deletion(t,A[r]))
    rank={j:k for k,j in enumerate(priority)}
    gains={i}|({s} if value(s,A[i])>own[s] else set())
    earlier_gain=any(rank[j]<rank[t] for j in gains)
    threshold=fairness_floor if earlier_gain else max(fairness_floor,own[t])
    if value(t,C)<threshold:return None
    B=list(A);B[s]=A[i];B[i]=T;B[t]=C
    new=[value(j,B[j]) for j in range(4)]
    assert is_efx(rows,B)
    assert tuple(new[j] for j in priority)>tuple(own[j] for j in priority)
    return dict(kind='safe_compensation_relay',allocation=B,priority=list(priority),
                path_start=s,champion=i,donor=t,champion_bundle=T,
                compensation_goods=selected,fairness_floor=fairness_floor,
                required_value=threshold,compensation_value=value(t,C),
                old_utilities=own,new_utilities=new)


def pair_relays(values,A,g,priority=(0,1,2,3)):
    """Try only the proved relay with T={g,h}; at most 24*m proposals."""
    check_priority(priority)
    out=[]
    for s,i,t in permutations(range(4),3):
        for h in range(len(values[0])):
            if A[t]>>h&1:
                result=compensated_relay(values,A,g,s,i,t,(1<<g)|(1<<h),priority)
                if result is not None:out.append(result)
    return out
