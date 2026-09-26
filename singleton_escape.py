"""Exact singleton-source exchange lemma, without a common-least-good assumption."""
from collections import deque
from capacity import validate, value, diagnostics
from rebundle import movement


def escape(values, allocation, omitted, source):
    V=validate(values,allocation,omitted)
    A=list(allocation); n=len(A)
    if not 0<=source<n or A[source].bit_count()!=1:
        return {'status':'NOT_APPLICABLE','reason':'source must hold a singleton'}
    graph=[[j for j in range(n) if value(V[i],A[j])>value(V[i],A[i])] for i in range(n)]
    if any(source in graph[i] for i in range(n)):
        return {'status':'NOT_APPLICABLE','reason':'agent is envied'}
    parent={source:None};queue=deque([source])
    while queue:
        i=queue.popleft()
        for j in graph[i]:
            if j not in parent:parent[j]=i;queue.append(j)
    blockers=[c['agent'] for c in diagnostics(V,A,omitted)[source]['comparisons']
              if 2*value(V[c['agent']],A[c['agent']]) < value(V[c['agent']],A[source])+V[c['agent']][omitted]]
    eligible=[i for i in blockers if i in parent]
    if not eligible:
        return {'status':'NOT_APPLICABLE','reason':'no reachable insertion blocker'}
    last=eligible[0];path=[];i=last
    while i is not None:path.append(i);i=parent[i]
    path.reverse();B=A.copy()
    for a,b in zip(path,path[1:]):B[a]=A[b]
    B[last]=1<<omitted
    new_omitted=A[source].bit_length()-1
    validate(V,B,new_omitted)
    before=[value(V[i],A[i]) for i in range(n)]
    after=[value(V[i],B[i]) for i in range(n)]
    assert all(after[i]>before[i] for i in path)
    assert all(after[i]>=before[i] for i in range(n))
    result={'status':'IMPROVED_EFX_PREDECESSOR','predecessor':B,'deleted':new_omitted,
            'path':path,'utilities_before':list(map(str,before)),'utilities_after':list(map(str,after))}
    if n==4 and len(V[0])==10:
        result['movement']=movement(A,omitted,B,new_omitted)
        assert result['movement']['distance']==2
    return result
