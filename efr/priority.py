"""Exact priority-decorated graph catalog; no solver or valuation enumeration."""
import argparse,json
from collections import Counter
from pathlib import Path
from efr.structural_reductions import PERMUTATIONS
from efr.case_status import classify


def automorphisms(case):
    sizes=case['profile'];edges={tuple(e) for e in case['edges']}
    return [p for p in PERMUTATIONS if all(sizes[i]==sizes[p[i]] for i in range(4))
            and {(p[i],p[j]) for i,j in edges}==edges]


def priority_representatives(case):
    group=automorphisms(case)
    representatives=sorted({min(tuple(p[i] for i in order) for p in group)
                            for order in PERMUTATIONS})
    assert len(representatives)*len(group)==24
    return representatives


def report():
    rows=[]
    for case in classify():
        if case['status']!='OPEN':continue
        orders=priority_representatives(case)
        rows.append(dict(id=case['id'],profile=case['profile'],edges=case['edges'],
                         sources=case['sources'],automorphism_count=len(automorphisms(case)),
                         priorities=orders,count=len(orders)))
    counts=Counter()
    for row in rows:counts[str(len(row['sources']))]+=row['count']
    return dict(scope='Priority-decorated OPEN templates, not new valuation exclusions',
                graph_templates=len(rows),priority_decorated_templates=sum(r['count'] for r in rows),
                by_sources=dict(counts),cases=rows)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out');args=parser.parse_args()
    result=report()
    if args.out:
        path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
