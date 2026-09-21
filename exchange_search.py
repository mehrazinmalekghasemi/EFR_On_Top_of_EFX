#!/usr/bin/env python3
"""Exact graph search: arbitrary EFX ownership changes and omitted-good swaps.

Nodes are UNLABELED bundle partitions; ownership is reconstructed by all 24
permutations. Sorting a node never sorts a labeled allocation witness.
TRAPPED certifies only exhaustion of this restricted move graph. UNKNOWN is a cap.
"""
from collections import deque
from itertools import permutations
import time
from oracle import integer_rows, verify_witness

class ExchangeSearch:
    def __init__(self, values):
        self.V=integer_rows(values)
        self.m=len(self.V[0]); self.full=(1<<self.m)-1
        if len(self.V)!=4 or self.m!=10:raise ValueError('Requires 4 agents and 10 goods')
        self.sums=[]
        for row in self.V:
            s=[0]*(1<<self.m)
            for b in range(1,len(s)):
                bit=b&-b;s[b]=s[b^bit]+row[bit.bit_length()-1]
            self.sums.append(s)
        self.cache={}

    def assignments(self, blocks):
        if blocks not in self.cache:
            threshold=[max((self.sums[i][b]-min(self.V[i][h] for h in range(self.m) if b>>h&1))
                           if b else 0 for b in blocks) for i in range(4)]
            self.cache[blocks]=tuple(a for a in sorted(set(permutations(blocks)))
                                    if all(self.sums[i][a[i]]>=threshold[i] for i in range(4)))
        return self.cache[blocks]

    def insertion(self,a,g):
        for k,b in enumerate(a):
            s=b.bit_count()
            if all(i==k or (s+1)*self.sums[i][a[i]]>=s*(self.sums[i][b]+self.V[i][g]) for i in range(4)):
                final=list(a);final[k]|=1<<g
                w={'predecessor':list(a),'deleted':g,'recipient':k,'allocation':final}
                if not verify_witness(self.V,w):raise AssertionError('Invalid extension')
                return w
        return None

    def solve(self,initial,g,max_states=2000,seconds=5):
        start=time.monotonic();end=start+seconds
        initial=tuple(initial);blocks=tuple(sorted(initial))
        if max_states<1 or seconds<0:raise ValueError('Invalid budget')
        union=0
        for b in initial:
            if type(b)!=int or b<0 or b&union or b&~self.full:raise ValueError('Invalid partition')
            union|=b
        if not 0<=g<self.m or union!=self.full^(1<<g):raise ValueError('Invalid deletion')
        if initial not in self.assignments(blocks):raise ValueError('Initial allocation is not EFX')
        direct=self.insertion(initial,g)
        moves={blocks:None}; parents={blocks:None}; omitted={blocks:g};depth={blocks:0};queue=deque([blocks]);closed=[]
        examined=0;edges=0
        def finish(status, witness=None, target=None, reason=None):
            path=[]
            if target is not None:
                p=target
                while p is not None:
                    path.append({'blocks':list(p),'deleted':omitted[p],'incoming_exchange':moves[p]})
                    p=parents[p]
                path.reverse()
            return {'status':status,'direct':direct is not None,'states_discovered':len(parents),
                    'states_expanded':examined,'valid_neighbor_checks':edges,
                    'exchange_depth':depth[target] if target is not None else None,
                    'witness':witness,'path':path,'reason':reason,'seconds':time.monotonic()-start,
                    'closed_component':[list(p) for p in closed] if status=='TRAPPED' else None}
        while queue:
            if time.monotonic()>=end:return finish('UNKNOWN',reason='time budget')
            b=queue.popleft();g=omitted[b];examined+=1
            for a in self.assignments(b):
                w=self.insertion(a,g)
                if w:return finish('FOUND',w,b)
            for k,mask in enumerate(b):
                for h in range(self.m):
                    if not mask>>h&1:continue
                    if time.monotonic()>=end:return finish('UNKNOWN',reason='time budget')
                    c=list(b);c[k]=(mask^(1<<h))|(1<<g);c=tuple(sorted(c))
                    target_owners=self.assignments(c)
                    transition=None
                    for old in self.assignments(b):
                        owner=old.index(mask);new=list(old);new[owner]=(mask^(1<<h))|(1<<g)
                        if tuple(new) in target_owners:
                            transition={'before':list(old),'after':new,'removed':h,'inserted':g}
                            break
                    if transition is None:continue
                    edges+=1
                    if c in parents:continue
                    if len(parents)>=max_states:return finish('UNKNOWN',reason='state budget')
                    moves[c]=transition;parents[c]=b;omitted[c]=h;depth[c]=depth[b]+1;queue.append(c)
            closed.append(b)
        return finish('TRAPPED',reason='Every reachable partition and all EFX ownerships exhausted')


def verify_trap(values,initial,g,component):
    """Separate, slow definition-based verification of a closed graph component."""
    from oracle import is_efx,is_efr
    V=integer_rows(values);m=len(V[0]);full=(1<<m)-1
    states={tuple(x) for x in component}
    if tuple(sorted(initial)) not in states:return False
    if (full ^ sum(initial)) != 1<<g:return False
    for b in states:
        if len(b)!=4 or b!=tuple(sorted(b)):return False
        union=0
        for x in b:
            if type(x)!=int or x<0 or x&~full or x&union:return False
            union|=x
        missing=full^union
        if missing.bit_count()!=1:return False
        good=missing.bit_length()-1
        owners=[a for a in set(permutations(b)) if is_efx(V,a)]
        if not owners:return False
        for a in owners:
            for k in range(4):
                final=list(a);final[k]|=missing
                if is_efr(V,final):return False
        for k,mask in enumerate(b):
            for h in range(m):
                if mask>>h&1:
                    c=list(b);c[k]=(mask^(1<<h))|(1<<good);c=tuple(sorted(c))
                    for a in owners:
                        owner=a.index(mask);new=list(a);new[owner]=(mask^(1<<h))|(1<<good)
                        if is_efx(V,new) and c not in states:return False
    return True
