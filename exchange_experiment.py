#!/usr/bin/env python3
"""Seeded, bounded experiments; samples are not a universal theorem."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time
from exchange_search import ExchangeSearch,verify_trap
from oracle import oracle,partitions,verify_witness


def run(seed,count,budget,out):
    rng=random.Random(seed); started=time.monotonic();deadline=started+budget
    records=[]; skipped=0
    # Warm the old oracle separately; initialization is recorded in total time.
    oracle([[1]*9 for _ in range(4)],goal='efx9',limit=1)
    def record(name,v,a,g,kind):
        nonlocal skipped
        remaining=deadline-time.monotonic()
        if remaining<=0:skipped+=1;return
        r=ExchangeSearch(v).solve(a,g,max_states=1000,seconds=min(3,remaining))
        item={'name':name,'kind':kind,'values':v,'initial':a,'deleted':g,'result':r}
        if r['status']=='TRAPPED':
            item['closure_verified']=verify_trap(v,a,g,r['closed_component'])
            if not item['closure_verified']:raise AssertionError('Invalid closed component')
            # Separate complete oracle, with its own bounded diagnostic budget.
            q=oracle(v,limit=1,deadline=time.time()+min(5,max(0,deadline-time.monotonic())))
            item['unrestricted_status']=q['status'];item['unrestricted_witnesses']=q['witnesses']
        elif r['status']=='FOUND':
            if not verify_witness(v,r['witness']):raise AssertionError('Invalid witness')
        records.append(item)
    for h in [6,7,10,20,35,36,100]:
        record(f'four-large-H{h}',[[h]*4+[1]*6 for _ in range(4)],[1,2,4,1008],3,'regression')
    record('fixed-deletion',[[1]*9+[2] for _ in range(4)],[7,24,96,384],9,'regression')
    case=json.loads(Path('examples/least-good-fixed-predecessor.json').read_text())
    record('ownership-only',case['values'],case['predecessor'],case['deleted'],'regression')
    local=partitions(9)
    for t in range(count):
        if time.monotonic()>=deadline:skipped+=2*(count-t);break
        family=t%4
        if family==0:v=[[rng.randrange(21) for _ in range(10)] for _ in range(4)]
        elif family==1:
            base=[rng.randrange(1,21) for _ in range(10)]
            v=[[max(0,x+rng.randrange(-1,2)) for x in base] for _ in range(4)]
        elif family==2:v=[[rng.choice([0,0,1,2,10,30]) for _ in range(10)] for _ in range(4)]
        else:
            base=[rng.choice([1,1,1,5,10,20]) for _ in range(10)];v=[base[:] for _ in range(4)]
        g=rng.randrange(10);goods=[h for h in range(10) if h!=g]
        reduced=[[row[h] for h in goods] for row in v]
        q=oracle(reduced,goal='efx9',limit=1,deadline=time.time()+max(0,deadline-time.monotonic()))
        if q['status']!='FOUND':skipped+=2;continue
        def lift(mask):return sum(1<<h for b,h in enumerate(goods) if mask>>b&1)
        a=[lift(x) for x in q['witnesses'][0]['allocation']]
        record(f'family{family}-profile{t}-oracle-start',v,a,g,'sample')
        engine=ExchangeSearch(v);candidate=None
        # A second start sampled from partition candidates, not chosen for insertability.
        for idx in rng.sample(range(len(local)),min(128,len(local))):
            b=tuple(sorted(lift(int(x)) for x in local[idx]));owners=engine.assignments(b)
            if owners:candidate=list(rng.choice(owners));break
        if candidate is None:skipped+=1
        else:record(f'family{family}-profile{t}-partition-start',v,candidate,g,'sample')
    def summarize(items):
        stages=Counter()
        for x in items:
            r=x['result']
            stages[r['status'] if r['status']!='FOUND' else
                   ('direct' if r['direct'] else 'ownership' if r['exchange_depth']==0 else 'exchange')]+=1
        return {'cases':len(items),'stages':dict(stages),
                'exchange_depths':dict(Counter(str(x['result']['exchange_depth']) for x in items if x['result']['status']=='FOUND')),
                'verified_traps':sum(x.get('closure_verified',False) for x in items),
                'traps_with_unrestricted_extension':sum(x.get('unrestricted_status')=='FOUND' for x in items)}
    report={'seed':seed,'requested_profiles':count,'budget_seconds':budget,'seconds':time.monotonic()-started,
            'skipped_starts':skipped,'regressions':summarize([x for x in records if x['kind']=='regression']),
            'samples':summarize([x for x in records if x['kind']=='sample']),
            'scope':'Finite seeded samples and exact restricted-graph certificates; no universal claim.',
            'records':records}
    Path(out).parent.mkdir(parents=True,exist_ok=True);Path(out).write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2),flush=True)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seed',type=int,default=42);p.add_argument('--profiles',type=int,default=40)
    p.add_argument('--seconds',type=float,default=180);p.add_argument('--out',default='exchange-results.json')
    a=p.parse_args()
    if a.profiles<0 or a.seconds<=0:p.error('Invalid budget')
    run(a.seed,a.profiles,a.seconds,a.out)
