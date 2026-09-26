"""Independent literal enumeration and cross-solver replay for two-source work.

The enumeration uses Python sets and direct integer sums, not the bitmask
suballocation enumerator in two_source_moves.py. cvc5 is optional for --replay.
"""
import argparse,json,itertools,hashlib,time
from pathlib import Path


def literal_verification(V,A,g):
    n=len(V);m=len(V[0]);old=[{h for h in range(m) if b>>h&1} for b in A]
    def value(i,S):return sum(V[i][h] for h in S)
    own=[value(i,old[i]) for i in range(n)]
    def efx(B):return all(value(i,B[i])>=value(i,B[j]-{h}) for i in range(n) for j in range(n) if i!=j for h in B[j])
    def efr(B):return all(len(B[j])*value(i,B[i])>=(len(B[j])-1)*value(i,B[j]) for i in range(n) for j in range(n) if i!=j)
    assert efx(old)
    reports=[]
    for a,b in itertools.combinations(range(n),2):
        pool=sorted(old[a]|old[b]|{g});counts={'assignments':0,'efx_states':0,'lex_improvements':0,'pareto_improvements':0,'complete_efr':0}
        for dest in itertools.product(range(3),repeat=len(pool)):
            B=[set(x) for x in old];B[a]={h for h,k in zip(pool,dest) if k==1};B[b]={h for h,k in zip(pool,dest) if k==2}
            counts['assignments']+=1
            if 0 not in dest and efr(B):counts['complete_efr']+=1
            if efx(B):
                counts['efx_states']+=1;new=[value(i,B[i]) for i in range(n)]
                if tuple(new)>tuple(own):counts['lex_improvements']+=1
                if new!=own and all(x>=y for x,y in zip(new,own)):counts['pareto_improvements']+=1
        reports.append({'agents':[a,b],**counts})
    return {'by_pair':reports,'totals':{k:sum(r[k] for r in reports) for k in counts},'subset_value_counts':[len({sum(row[h] for h in range(m) if mask>>h&1) for mask in range(1<<m)}) for row in V]}


def three_agent_completion(V,A):
    m=len(V[0]);old=[{h for h in range(m) if b>>h&1} for b in A]
    for fixed in range(4):
        active=[i for i in range(4) if i!=fixed];pool=sorted(set(range(m))-old[fixed])
        for dest in itertools.product(active,repeat=len(pool)):
            B=[set() for _ in range(4)];B[fixed]=old[fixed]
            for h,i in zip(pool,dest):B[i].add(h)
            if all(len(B[j])*sum(V[i][h] for h in B[i])>=(len(B[j])-1)*sum(V[i][h] for h in B[j]) for i in range(4) for j in range(4) if i!=j):
                return {'fixed_agent':fixed,'allocation':[sum(1<<h for h in x) for x in B]}
    return None


def replay(output_directory='run/verification'):
    import cvc5,z3
    from structural_efr_search import build
    from two_source_probe import compensation_cuts
    directory=Path('experiment-results/two-source');records=[]
    source_files=[]
    for x in json.loads((directory/'all-compensation.json').read_text()):
        if x['status']!='unsat':continue
        s,v=build(x['case']);compensation_cuts(s,v,x['case']['initial'])
        source_files.append((x['case']['id']+'-compensation',list(s.assertions())))
    for f in directory.glob('*-pareto.smt2'):source_files.append((f.stem,list(z3.parse_smt2_file(str(f)))))
    output=Path(output_directory);portable=output/'portable';portable.mkdir(parents=True,exist_ok=True)
    for name,assertions in source_files:
        # Normalize unary (+ x), which cvc5's parser rejects, to x.
        q=z3.Solver();q.add(*[z3.simplify(x) for x in assertions]);source=q.to_smt2()
        f=portable/(name+'.smt2');f.write_text(source)
        s=cvc5.Solver();s.setLogic('QF_LRA');s.setOption('tlimit-per','30000');s.setOption('produce-proofs','true');s.setOption('check-proofs','true')
        p=cvc5.InputParser(s);p.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,source,str(f));sm=p.getSymbolManager();replies=[];started=time.monotonic()
        while True:
            c=p.nextCommand()
            if c.isNull():break
            answer=c.invoke(s,sm).strip()
            if answer:replies.append(answer)
        version=s.getVersion();version=version.decode() if isinstance(version,bytes) else version
        records.append({'file':str(Path('portable')/f.name),'sha256':hashlib.sha256(source.encode()).hexdigest(),'replies':replies,'seconds':time.monotonic()-started,'solver':version,'check_proofs':True})
        print(name,replies,flush=True)
    (output/'cvc5-replay.json').write_text(json.dumps(records,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true')
    p.add_argument('--out',default='run/verification');a=p.parse_args()
    if a.replay:replay(a.out)
    else:
        from restoration_moves import lift_preserving_start
        from oracle import oracle,verify_witness
        from two_source_moves import compensated_path
        x=json.loads(Path('experiment-results/two-source/verified-obstruction.json').read_text());V=x['values'];A=x['initial']
        lifted=lift_preserving_start(V,A,9)
        result={'values':V,'initial':A,'omitted':9,'fixed_priority':[0,1,2,3],
                'base_verification':literal_verification(V,A,9),'lift':lifted,
                'nondegenerate_verification':literal_verification(lifted['values'],A,9),
                'three_agent_completion':three_agent_completion(lifted['values'],A),
                'three_agent_efx_progress':compensated_path(lifted['values'],A,9),
                'base_three_agent_efx_progress':compensated_path(V,A,9),
                'mode_c':oracle(lifted['values'],limit=1,deadline=time.time()+30)}
        assert result['mode_c']['status']=='FOUND'
        assert verify_witness(lifted['values'],result['mode_c']['witnesses'][0])
        output=Path(a.out);output.mkdir(parents=True,exist_ok=True)
        (output/'verified-obstruction.json').write_text(json.dumps(result,indent=2))
        print(json.dumps({k:result[k] for k in ['base_verification','nondegenerate_verification','three_agent_completion']},indent=2))
