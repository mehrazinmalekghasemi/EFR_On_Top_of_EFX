"""Bounded exact-rational SAT probes; install z3-solver==5.1.0.0 to rerun."""
import z3,json,time,argparse
from itertools import combinations
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,choices=range(1,5),default=4);args=parser.parse_args()
A=[1,2,12,496];goods=lambda b:[g for g in range(10) if b>>g&1]
v=[[z3.Real(f'v_{i}_{g}') for g in range(10)] for i in range(4)]
val=lambda i,b:z3.Sum([v[i][g] for g in goods(b)])
s=z3.Solver();s.set(timeout=20000)
for row in v:
 for x in row:s.add(x>=0)
edges={(0,1),(2,0)}
for i in range(4):
 s.add(val(i,A[i])==100,v[i][9]<=100)
 for j in range(4):
  if i!=j:s.add(val(i,A[j])>100 if (i,j) in edges else val(i,A[j])<=100)
  if i!=j:
   for h in goods(A[j]):s.add(val(i,A[j]^(1<<h))<=100)
for i in (2,3):
 for h in goods(A[i]):s.add(v[i][9]+v[i][h]<=100)
for i in (0,1):
 for h in goods(A[2]):s.add(v[i][9]+v[i][h]<=100)
for k in range(4):
 n=A[k].bit_count();s.add(z3.Or([n*(val(i,A[k])+v[i][9])>(n+1)*100 for i in range(4) if i!=k]))
s.add(v[3][9]>50)
for h in goods(A[3]):
 C=(A[3]^(1<<h))|(1<<9)
 s.add(z3.Or([val(i,C^(1<<x))>100 for i in (0,1,2) for x in goods(C)]))
for h in goods(A[2]):
 for n in range(6):
  for ys in combinations(goods(A[3]),n):
   Y=sum(1<<y for y in ys)
   s.add(z3.Implies(v[3][9]+v[3][h]>100,z3.Or(val(3,Y)>100-v[3][9],val(2,Y)<v[2][h])))

if args.stage>=2:
 s.add(*[v[i][9]<100 for i in range(4)])
 for n in range(6):
  for hs in combinations(goods(A[3]),n):
   C=sum(1<<h for h in hs)|(1<<9)
   s.add(z3.Implies(val(3,C)>100,z3.Or([val(i,C^(1<<x))>100 for i in (0,1,2) for x in goods(C)])))
if args.stage>=3:
 for i in (2,3):
  for h in goods(A[i]):s.add(v[i][9]+v[i][h]<100)
 for i in (0,1):
  for h in goods(A[2]):s.add(v[i][9]+v[i][h]<100)
if args.stage>=4:
 for h in goods(A[2]):
  for n in range(6):
   for ys in combinations(goods(A[3]),n):
    Y=sum(1<<y for y in ys)
    B=list(A);B[2]=(A[2]^(1<<h))|Y;B[3]=(A[3]^Y)|(1<<h)
    pareto=z3.And(val(2,B[2])>=100,val(3,B[3])>=100,z3.Or(val(2,B[2])>100,val(3,B[3])>100))
    safe=z3.And([val(i,B[i])>=val(i,B[j]^(1<<x)) for i in range(4) for j in range(4) if i!=j for x in goods(B[j])])
    s.add(z3.Not(z3.And(pareto,safe)))
t=time.time();status=s.check();out={'stage':args.stage,'status':str(status),'seconds':time.time()-t,
 'scope':'Counterexample to the specified move menu in one normalized template; not to EFR existence'}
if status==z3.sat:
 m=s.model();out['values']=[[str(m.eval(x)) for x in row] for row in v];out['initial']=A
print(json.dumps(out,indent=2))
