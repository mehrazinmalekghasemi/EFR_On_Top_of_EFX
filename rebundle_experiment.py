#!/usr/bin/env python3
"""Measure exact coordinated-rebundling distance on previously certified traps."""
import argparse
from collections import Counter
import json
import random
from pathlib import Path
from rebundle import nearest,movement
from oracle import verify_witness


def run(source,out,stress=0):
    cases=json.loads(Path(source).read_text())['cases'];records=[]
    rng=random.Random(2026)
    for t in range(stress):
        v=[[rng.randrange(14,31) for _ in range(4)]+[rng.randrange(1,3) for _ in range(6)] for _ in range(4)]
        g=rng.randrange(4)
        cases.append({'name':f'heterogeneous-stress-{t}','seed':2026,'kind':'stress',
                      'values':v,'initial':[1<<h for h in range(4) if h!=g]+[1008],'deleted':g})
    for case in cases:
        r=nearest(case['values'],case['initial'],case['deleted'],max_radius=10,seconds=90)
        if r['status']=='FOUND':
            assert verify_witness(case['values'],r['witness'])
            assert movement(case['initial'],case['deleted'],r['witness']['predecessor'],r['witness']['deleted'])['distance']==r['minimum_radius']
        record={'name':case['name'],'seed':case['seed'],'kind':case['kind'],
                'values':case['values'],'initial':case['initial'],'deleted':case['deleted'],'result':r}
        records.append(record)
        print(json.dumps({'case':case['name'],'seed':case['seed'],'status':r['status'],
                          'radius':r.get('minimum_radius'),'seconds':r['seconds']}),flush=True)
    report={'cases':len(records),'statuses':dict(Counter(x['result']['status'] for x in records)),
            'minimum_radius_histogram':dict(Counter(str(x['result'].get('minimum_radius')) for x in records)),
            'by_kind':{kind:dict(Counter(str(x['result'].get('minimum_radius',x['result']['status'])) for x in records if x['kind']==kind)) for kind in sorted({x['kind'] for x in records})},
            'definition':'Minimum changed memberships between physical blocks and omitted slot, modulo whole-block ownership; final insertion excluded.',
            'scope':'Finite trap and stress starts, not a universal proof. Intermediate microsteps need not be EFX.',
            'records':records}
    Path(out).parent.mkdir(parents=True,exist_ok=True);Path(out).write_text(json.dumps(report,indent=2))
    print('SUMMARY '+json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',default='experiment-results/run-35576951293/verified-traps.json')
    p.add_argument('--out',default='rebundle-results.json');p.add_argument('--stress',type=int,default=0)
    a=p.parse_args()
    if not 0<=a.stress<=100:p.error('Stress count must be 0..100')
    run(a.source,a.out,a.stress)
