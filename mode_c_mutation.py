import sys,json,time,random,math
from pathlib import Path

from oracle import oracle
rng=random.Random(20260922)
records=[];hist={}; evaluations=0
start=time.time()
def common_least(v):
 return any(all(row[g]==min(row) for row in v) for g in range(10))
def evaluate(v):
 global evaluations
 q=oracle(v,scan_all=True,limit=1)
 assert q['complete']
 score=(sum(p['extension_count']>0 for p in q['profiles']),sum(p['extension_count'] for p in q['profiles']))
 evaluations+=1;hist[score[0]]=hist.get(score[0],0)+1
 return score,q
for seed in range(4):
 if seed==0:v=[[rng.randint(15,30) if g<4 else rng.randint(0,3) for g in range(10)] for i in range(4)]
 elif seed==1:
  base=[100,70,60,40,30,20,10,3,3,3];v=[[max(0,x+rng.randint(-3,3)) for x in base] for i in range(4)]
 elif seed==2:v=[[rng.choice([0,0,1,3,10,30]) for g in range(10)] for i in range(4)]
 else:v=[[rng.randint(1,10) for g in range(10)] for i in range(4)]
 while common_least(v):
  i=rng.randrange(4);g=min(range(10),key=lambda g:v[i][g]);v[i][g]+=1
 score,q=evaluate(v);best=(score,v,q)
 step=0
 while step<100:
  candidate=[row[:] for row in v]
  for change in range(rng.choice([1,1,2,4])):
   i,g=rng.randrange(4),rng.randrange(10)
   candidate[i][g]=max(0,candidate[i][g]+rng.choice([-10,-3,-1,1,3,10]))
  if common_least(candidate):continue
  step+=1
  ns,nq=evaluate(candidate)
  if ns<best[0]:best=(ns,candidate,nq)
  delta=4*(ns[0]-score[0])+math.log((ns[1]+1)/(score[1]+1))
  if delta<=0 or rng.random()<math.exp(-delta/0.15):v,score,q=candidate,ns,nq
  if ns[0]==0:break
 records.append({'seed_index':seed,'score':best[0],'values':best[1],'oracle':best[2]})
 print(json.dumps({'seed_index':seed,'best_score':best[0],'evaluations':evaluations}),flush=True)
 if best[0][0]==0:break
result={'no_common_least_good':True,'seed':20260922,'evaluations':evaluations,'seconds':time.time()-start,'successful_deletion_histogram':hist,'best_cases':records}
out=Path(__file__).resolve().parent/'experiment-results/mode-c-adversary/mutation.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='best_cases'}),flush=True)
