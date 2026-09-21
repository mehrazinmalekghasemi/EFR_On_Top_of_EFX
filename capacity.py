#!/usr/bin/env python3
"""Exact insertion diagnostics and a sufficient bundle-rotation repair.

Input JSON: {"values": [[...],...], "predecessor": [mask,...], "deleted": index}.
Works for any number of agents. CLI: python capacity.py input.json
"""
import argparse
from fractions import Fraction
import json


def value(row, mask):
    return sum((x for g,x in enumerate(row) if mask>>g&1), Fraction(0))


def validate(V,A,g):
    V=[[Fraction(str(x)) for x in row] for row in V]
    if not V or len(A)!=len(V) or not V[0]: raise ValueError('Invalid dimensions')
    m=len(V[0]); union=0
    if type(g)!=int or not 0<=g<m: raise ValueError('Invalid deleted good')
    for row in V:
        if len(row)!=m or any(x<0 for x in row): raise ValueError('Invalid valuations')
    for b in A:
        if type(b)!=int or b<0 or b>>m or union&b or b>>g&1:
            raise ValueError('Invalid predecessor partition')
        union|=b
    if union != ((1<<m)-1)^(1<<g): raise ValueError('Predecessor must allocate every other good')
    for i,row in enumerate(V):
        for j,b in enumerate(A):
            if i!=j and any(value(row,A[i])<value(row,b^(1<<h)) for h in range(m) if b>>h&1):
                raise ValueError('Predecessor is not EFX0')
    return V


def diagnostics(V,A,g):
    V=validate(V,A,g); targets=[]
    for k,b in enumerate(A):
        s=b.bit_count(); comparisons=[]
        for i,row in enumerate(V):
            if i==k: continue
            margin=(s+1)*value(row,A[i])-s*(value(row,b)+row[g])
            comparisons.append({'agent':i,'scaled_margin':str(margin),
                'capacity':str(Fraction(s+1,s)*value(row,A[i])-value(row,b)) if s else None})
        targets.append({'recipient':k,'feasible':all(Fraction(c['scaled_margin'])>=0 for c in comparisons),
                        'comparisons':comparisons})
    return targets


def envy_cycle(V,A):
    graph=[[j for j in range(len(A)) if value(row,A[j])>value(row,A[i])]
           for i,row in enumerate(V)]
    state=[0]*len(A); stack=[]
    def dfs(i):
        state[i]=1;stack.append(i)
        for j in graph[i]:
            if state[j]==1: return stack[stack.index(j):]
            if state[j]==0:
                c=dfs(j)
                if c: return c
        stack.pop();state[i]=2
        return None
    for i in range(len(A)):
        if state[i]==0:
            c=dfs(i)
            if c:return c
    return None


def repair(V,A,g):
    V=validate(V,A,g); A=list(A); rotations=[]
    while True:
        targets=diagnostics(V,A,g)
        for t in targets:
            if t['feasible']:
                B=A.copy();B[t['recipient']]|=1<<g
                return {'status':'FOUND','predecessor':A,'allocation':B,
                        'recipient':t['recipient'],'deleted':g,'rotations':rotations,'targets':targets}
        cycle=envy_cycle(V,A)
        if not cycle:
            return {'status':'NO_INSERTION_AFTER_THIS_REPAIR','predecessor':A,
                    'rotations':rotations,'targets':targets,
                    'note':'This does not exclude other EFX predecessors or other deleted goods.'}
        old=A.copy()
        for p,i in enumerate(cycle): A[i]=old[cycle[(p+1)%len(cycle)]]
        rotations.append(cycle)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    with open(a.input) as f:d=json.load(f)
    print(json.dumps(repair(d['values'],d['predecessor'],d['deleted']),indent=2))
