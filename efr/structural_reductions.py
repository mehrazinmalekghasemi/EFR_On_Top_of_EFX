"""Exact structural catalog for extremal EFR obstructions, not Mode C witnesses."""
from itertools import permutations
from collections import Counter

PROFILES=((1,1,1,6),(1,1,2,5),(1,1,3,4),(1,2,2,4),(1,2,3,3),(2,2,2,3))
PERMUTATIONS=tuple(permutations(range(4)))
PAIRS=tuple((i,j) for i in range(4) for j in range(4) if i!=j)


def graph_data(code):
    edges=tuple((i,j) for b,(i,j) in enumerate(PAIRS) if code>>b&1)
    sources=tuple(j for j in range(4) if not any(b==j for a,b in edges))
    remaining=set(range(4))
    while remaining:
        roots={j for j in remaining if not any(b==j and a in remaining for a,b in edges)}
        if not roots:return None
        remaining-=roots
    reach=[[i==j or (i,j) in edges for j in range(4)] for i in range(4)]
    for k in range(4):
        for i in range(4):
            for j in range(4):reach[i][j]=reach[i][j] or (reach[i][k] and reach[k][j])
    return edges,sources,reach


def canonical_edges(edges,stabilizer):
    return min(tuple(sorted((p[i],p[j]) for i,j in edges)) for p in stabilizer)


def catalog():
    cases=[];counts=[]
    dags=[graph_data(code) for code in range(4096)]
    dags=[d for d in dags if d is not None]
    for sizes in PROFILES:
        stabilizer=[p for p in PERMUTATIONS if all(sizes[i]==sizes[p[i]] for i in range(4))]
        all_patterns={canonical_edges(e,stabilizer) for e,s,r in dags}
        unique_removed={canonical_edges(e,stabilizer) for e,s,r in dags if len(s)>=2}
        basic={canonical_edges(e,stabilizer) for e,s,r in dags
               if len(s)>=2 and all(sizes[i]>=2 for i in s)}
        triple={e for e in basic if sizes!=(2,2,2,3) or not any(j==3 for i,j in e)}
        final=set()
        for e in triple:
            code=sum(1<<PAIRS.index(edge) for edge in e)
            _,sources,reach=graph_data(code)
            if all(any(sizes[i]!=2 and not reach[k][i] for i in range(4))
                   for k in sources if sizes[k]==2):final.add(e)
        counts.append({'profile':list(sizes),'acyclic_patterns':len(all_patterns),'after_unique_source_lemma':len(unique_removed),
                       'after_source_lemmas':len(basic),'after_triple_source_lemma':len(triple),'after_pair_lemma':len(final)})
        A=[];pos=0
        for size in sizes:A.append(((1<<size)-1)<<pos);pos+=size
        for edges in sorted(final):
            code=sum(1<<PAIRS.index(e) for e in edges)
            _,sources,reach=graph_data(code)
            cases.append({'id':''.join(map(str,sizes))+'_'+format(code,'03x'),
                          'profile':list(sizes),'initial':A,'omitted':9,
                          'edges':[list(e) for e in edges],'sources':list(sources),'reach':reach})
    summary={'labeled_dags':dict(Counter(len(s) for e,s,r in dags)),
             'profile_counts':counts,'before':sum(c['acyclic_patterns'] for c in counts),
             'after_unique_source_lemma':sum(c['after_unique_source_lemma'] for c in counts),
             'after_source_lemmas':sum(c['after_source_lemmas'] for c in counts),
             'after_triple_source_lemma':sum(c['after_triple_source_lemma'] for c in counts),'after_pair_lemma':len(cases),
             'by_sources':dict(Counter(len(c['sources']) for c in cases))}
    return cases,summary

if __name__=='__main__':
    import json
    print(json.dumps(catalog()[1],indent=2))
