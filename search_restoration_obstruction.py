"""Bounded integer search for failure of specific local repair rules, NOT EFR nonexistence."""
import sys,json,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

import z3
from search import variables,sv,efx_constraints,extract,witness_constraints
from itertools import permutations
from restoration_moves import source_analysis as analyze
from capacity import diagnostics

def work(profile):
 a=[];p=0
 for n in profile:a.append(((1<<n)-1)<<p);p+=n
 v=[[z3.Int(f'v_{i}_{g}') for g in range(10)] for i in range(4)];s=z3.Solver();s.set(timeout=45000)
 for row in v:s.add(*[z3.And(x>=1,x<=30) for x in row])
 for g in range(10):s.add(z3.Or(*[v[i][h]<v[i][g] for i in range(4) for h in range(10) if h!=g]))
 s.add(*efx_constraints(v,a)); own=[sv(v[i],a[i]) for i in range(4)]
 edge=[[own[i]<sv(v[i],a[j]) if i!=j else z3.BoolVal(False) for j in range(4)] for i in range(4)]
 # Acyclicity without restricting which agent labels precede others.
 ranks=[z3.Real('rank_'+str(i)) for i in range(4)]
 for r in ranks:s.add(r>=0,r<=3)
 for i in range(4):
  for j in range(4):s.add(z3.Implies(edge[i][j],ranks[j]>=ranks[i]+1))
 # Keep comparisons strict to make the envy graph locally stable.
 for i in range(4):
  for j in range(4):
   if i!=j:s.add(own[i]!=sv(v[i],a[j]))
 reach=[[z3.Or(z3.BoolVal(i==j),edge[i][j]) for j in range(4)] for i in range(4)]
 for k in range(4):
  for i in range(4):
   for j in range(4):reach[i][j]=z3.Or(reach[i][j],z3.And(reach[i][k],reach[k][j]))
 for k in range(4):
  n=profile[k]
  s.add(z3.Or(*[(n+1)*own[i]<n*(sv(v[i],a[k])+v[i][9]) for i in range(4) if i!=k]))
  source=z3.And(*[z3.Not(edge[i][k]) for i in range(4)])
  mask=a[k]|512;T=mask
  while T:
   safe=z3.And(*[sv(v[j],T^(1<<h))<=own[j] for j in range(4) for h in range(10) if T>>h&1])
   for i in range(4):s.add(z3.Not(z3.And(source,reach[k][i],sv(v[i],T)>own[i],safe)))
   T=(T-1)&mask
 for perm in permutations(range(4)):
  B=[a[j] for j in perm]
  efx=z3.And(*efx_constraints(v,B))
  better=z3.Or(*[z3.And(*[sv(v[j],B[j])==own[j] for j in range(i)],sv(v[i],B[i])>own[i]) for i in range(4)])
  s.add(z3.Not(z3.And(efx,better)))
  for k in range(4):
   C=B.copy();C[k]|=512
   s.add(z3.Not(z3.And(*witness_constraints(v,{'predecessor':B,'allocation':C,'deleted':9,'recipient':k},'extension'))))
 r=s.check();out={'profile':profile,'status':str(r)}
 if r==z3.sat:
  V=[[str(s.model().eval(x).as_long()) for x in row] for row in v];analysis=analyze(V,a,9)
  assert not analysis['moves'];assert not any(t['feasible'] for t in diagnostics(V,a,9))
  out.update(values=V,initial=a,omitted=9,analysis=analysis)
 elif r==z3.unknown:out['reason']=s.reason_unknown()
 directory=Path(__file__).resolve().parent/'experiment-results/restoration'
 directory.mkdir(parents=True,exist_ok=True)
 (directory/('search-obstruction-'+''.join(map(str,profile))+'.json')).write_text(json.dumps(out,indent=2))
 return {'profile':profile,'status':str(r), 'sources':out.get('analysis',{}).get('sources')}
if __name__=='__main__':
 with ProcessPoolExecutor(max_workers=3) as pool:
  for x in pool.map(work,[(1,1,2,5),(1,2,2,4),(2,2,2,3)]):print(json.dumps(x),flush=True)
