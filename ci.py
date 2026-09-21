#!/usr/bin/env python3
"""GitHub orchestration. No GitHub credentials are needed by this module."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tarfile
import time

ROOT=Path(__file__).resolve().parent
CORE=('oracle.py','search.py','verify.py','requirements.txt','ci.py')

def fingerprint():
    h=hashlib.sha256()
    for name in CORE:
        h.update(name.encode()+b'\0'+(ROOT/name).read_bytes()+b'\0')
    return h.hexdigest()

def save(path,data):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(data,indent=2));t.replace(p)

def identity(goal,shards,shard):
    return {'schema':1,'goal':goal,'shards':shards,'shard':shard,'code_sha256':fingerprint()}

def check_identity(actual,expected):
    for k,v in expected.items():
        if actual.get(k)!=v:raise ValueError(f'Checkpoint mismatch: {k}; expected {v!r}, got {actual.get(k)!r}')

def pack(checkpoint,destination):
    checkpoint=Path(checkpoint);destination=Path(destination)
    destination.parent.mkdir(parents=True,exist_ok=True)
    tmp=destination.with_suffix('.tmp')
    with tarfile.open(tmp,'w:gz',compresslevel=6) as t:
        for p in sorted(checkpoint.rglob('*')):
            if p.is_file() and p.suffix in ('.json','.smt2'):
                t.add(p,arcname=str(Path('checkpoint')/p.relative_to(checkpoint)),recursive=False)
    tmp.replace(destination)

def restore(archive,destination,expected):
    destination=Path(destination)
    if destination.exists() and any(destination.iterdir()):raise ValueError('Restore destination must be empty')
    with tarfile.open(archive,'r:gz') as t:
        members=t.getmembers();names=[]
        for m in members:
            p=Path(m.name)
            if not m.isfile() or p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0]!='checkpoint':
                raise ValueError('Invalid checkpoint archive member')
            names.append(m.name)
        if len(names)!=len(set(names)):raise ValueError('Duplicate archive members')
        info=t.extractfile('checkpoint/campaign.json')
        if info is None:raise ValueError('Checkpoint lacks campaign metadata')
        check_identity(json.load(info),expected)
        # Only checked regular files are extracted, with the fixed outer prefix removed.
        for m in members:
            rel=Path(m.name).relative_to('checkpoint');p=destination/rel
            p.parent.mkdir(parents=True,exist_ok=True)
            with t.extractfile(m) as src,p.open('wb') as dst:
                import shutil
                shutil.copyfileobj(src,dst)
    if not (destination/'config.json').exists():raise ValueError('Checkpoint lacks engine config')

def supervised(command,seconds):
    print('Executing:', ' '.join(map(str,command)),flush=True)
    proc=subprocess.Popen(command,cwd=ROOT,start_new_session=True)
    try:return proc.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        print('Time budget reached; stopping this process group and preserving completed checkpoint writes.',flush=True)
        try:os.killpg(proc.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        try:proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            proc.wait()
        return 124

def shard_progress(checkpoint,goal,shards,shard):
    m=9 if goal=='efx9' else 10
    roots=['r_'+'_'.join(map(str,p)) for p in itertools.combinations_with_replacement(range(m),3)]
    owned=[r for i,r in enumerate(roots) if i%shards==shard]
    nodes={}
    for p in (Path(checkpoint)/'nodes').glob('*.json'):
        n=json.loads(p.read_text())
        if n['id'].split('_a')[0] in owned:nodes[n['id']]=n
    visited=set()
    def covered(k,trail):
        if k in trail:raise ValueError('Cycle in checkpoint tree')
        visited.add(k);n=nodes.get(k,{})
        if n.get('status')=='COVERED':return True
        if n.get('status')=='SPLIT':
            children=n.get('children',[])
            states=[covered(c,trail|{k}) for c in children]
            return bool(children) and all(states)
        return False
    closed=sum(covered(r,set()) for r in owned)
    return {'owned_roots':len(owned),'search_covered_roots':closed,'nodes':len(nodes),
            'open_nodes':sum(n.get('status') in ('OPEN','ERROR') for n in nodes.values()),
            'covered_leaves':sum(n.get('status')=='COVERED' for n in nodes.values()),
            'witnesses_added':sum(n.get('witnesses_added',0) for n in nodes.values()),
            'unknown_visits':sum(n.get('unknown_visits',0) for n in nodes.values()),
            'solver_seconds':sum(n.get('solver_seconds',0) for n in nodes.values()),
            'oracle_seconds':sum(n.get('oracle_seconds',0) for n in nodes.values()),
            'errors':sum(n.get('status')=='ERROR' for n in nodes.values()),
            'refuted':sum(n.get('status')=='REFUTED' for n in nodes.values())}

def run_shard(a):
    if not 1<=a.shards<=20 or not 0<=a.shard<a.shards or not 0<a.minutes<=270:
        raise ValueError('Invalid shard or time budget')
    if a.goal not in ('extension','efr','efx9') or a.mode not in ('search','verify'):
        raise ValueError('Invalid goal or mode')
    if a.mode=='verify' and not a.resume:raise ValueError('Verify mode requires a previous run checkpoint')
    if not 1<=a.split_after<=10 or not 1<=a.smt_seconds<=120:raise ValueError('Invalid search tuning')
    if not 1<=a.workers<=4:raise ValueError('Use 1 to 4 workers per standard runner')
    checkpoint=Path(a.checkpoint).resolve(); payload=Path(a.payload).resolve()
    expected=identity(a.goal,a.shards,a.shard)
    if a.resume:
        restore(a.resume,checkpoint,expected)
    else:
        if checkpoint.exists() and any(checkpoint.iterdir()):raise ValueError('Fresh run would overwrite a checkpoint')
        checkpoint.mkdir(parents=True,exist_ok=True)
        save(checkpoint/'campaign.json',expected)
    # A new round must never reuse the preceding round's verification verdict.
    for p in checkpoint.glob('verification-*.json'):p.unlink()
    started=time.time()
    report={**expected,'run_id':os.environ.get('GITHUB_RUN_ID','local'),'mode':a.mode,
            'split_after':a.split_after,'smt_seconds':a.smt_seconds,'restored':bool(a.resume),'minutes':a.minutes,'workers':a.workers,'status':'ERROR'}
    exit_code=0
    try:
        if a.mode=='search':
            cmd=[sys.executable,'search.py','--goal',a.goal,'--shards',str(a.shards),'--shard',str(a.shard),
                 '--workers',str(a.workers),'--hours',str(a.minutes/60),'--out',str(checkpoint),
                 '--split-after',str(a.split_after),'--smt-seconds',str(a.smt_seconds)]
            report['search_exit']=supervised(cmd,a.minutes*60+45)
            if report['search_exit'] not in (0,124):raise RuntimeError('Search process failed; inspect job logs')
        cmd=[sys.executable,'verify.py',str(checkpoint),'--workers',str(a.workers),
             '--shards',str(a.shards),'--shard',str(a.shard),'--hours',str((a.minutes if a.mode=='verify' else 5)/60),
             '--timeout','60']
        report['verify_exit']=supervised(cmd,(a.minutes if a.mode=='verify' else 5)*60+45)
        if report['verify_exit'] not in (0,2,124):raise RuntimeError('Verification process failed')
        vp=checkpoint/f'verification-{a.shard}-of-{a.shards}.json'
        report['verification']=json.loads(vp.read_text()) if vp.exists() else {'verdict':'NOT_COMPLETED'}
        report['progress']=shard_progress(checkpoint,a.goal,a.shards,a.shard)
        verdict=report['verification']['verdict']
        if verdict=='INVALID_NO_THEOREM':raise RuntimeError('Independent verifier rejected the checkpoint')
        if report['progress']['errors']:raise RuntimeError('Search contains ERROR nodes; inspect job logs')
        report['status']='VERIFIED' if verdict in ('VERIFIED_GLOBAL_COVER','VERIFIED_SHARD_ONLY') else 'INCOMPLETE'
        if report['progress']['refuted']:report['status']='COUNTEREXAMPLE_REQUIRES_RECHECK'
    except Exception as e:
        report['error']=str(e);report['status']='ERROR';exit_code=1
    finally:
        report['elapsed_seconds']=time.time()-started
        save(checkpoint/'last-round.json',report)
        save(payload/'result.json',report)
        pack(checkpoint,payload/'checkpoint.tar.gz')
        summary=os.environ.get('GITHUB_STEP_SUMMARY')
        if summary:
            with open(summary,'a') as f:
                f.write(f"## Shard {a.shard} of {a.shards}\n\nStatus: **{report['status']}**\n\n")
                f.write('```json\n'+json.dumps({k:v for k,v in report.items() if k!='verification'},indent=2)+'\n```\n')
        print(json.dumps({k:v for k,v in report.items() if k!='verification'},indent=2),flush=True)
    return exit_code

def plan():
    goal=os.environ['GOAL'];mode=os.environ['MODE'];shards=int(os.environ['SHARDS']);minutes=float(os.environ['MINUTES'])
    resume=os.environ.get('RESUME_RUN','').strip()
    if goal not in ('extension','efr','efx9') or mode not in ('search','verify'):raise ValueError('Invalid mode or goal')
    if not 1<=shards<=20 or not 1<=minutes<=270:raise ValueError('Choose 1..20 shards and 1..270 minutes')
    if resume and (not resume.isdigit() or int(resume)<=0):raise ValueError('Resume run must be a numeric run ID, not a URL')
    if mode=='verify' and not resume:raise ValueError('Verify mode needs a previous run ID')
    output={'matrix':json.dumps({'shard':list(range(shards))},separators=(',',':'))}
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a') as f:
            for k,v in output.items():f.write(k+'='+v+'\n')
    print(json.dumps(output))

def combine_reports(reports,goal,shards,run_id):
    indexed={}
    expected_total=165 if goal=='efx9' else 220
    for r in reports:
        i=r.get('shard')
        if type(i)!=int or not 0<=i<shards or i in indexed:raise ValueError('Invalid or duplicate shard report')
        check_identity(r,identity(goal,shards,i))
        if str(r.get('run_id'))!=str(run_id):raise ValueError('Report belongs to another workflow run')
        indexed[i]=r
    missing=sorted(set(range(shards))-set(indexed))
    all_verified=not missing
    for i,r in indexed.items():
        v=r.get('verification',{})
        required=len(range(i,expected_total,shards))
        all_verified &= (r.get('status')=='VERIFIED' and v.get('verdict') in ('VERIFIED_SHARD_ONLY','VERIFIED_GLOBAL_COVER')
                         and v.get('goal')==goal and v.get('shard')==i and v.get('shards')==shards
                         and v.get('roots_checked')==required and v.get('roots_verified')==required
                         and v.get('all_required_roots')==expected_total)
    return {'goal':goal,'run_id':str(run_id),'shards':shards,'received_shards':len(indexed),'missing_shards':missing,
            'required_roots':expected_total,'verdict':'ALL_SHARDS_VERIFIED' if all_verified else 'INCOMPLETE_NO_THEOREM',
            'reports':[indexed[i] for i in sorted(indexed)]}

def collect(a):
    reports=[json.loads(p.read_text()) for p in Path(a.directory).rglob('result.json')]
    result=combine_reports(reports,a.goal,a.shards,os.environ.get('GITHUB_RUN_ID','local'))
    save('campaign-summary.json',result)
    lines=['# EFR search results','',f"**{result['verdict']}**",'',
           f"Received {result['received_shards']}/{a.shards} shard checkpoints.", '',
           '| Shard | Status | Search-covered roots | Required roots | Covered leaves | New witnesses | Unknown visits |', '|---:|---|---:|---:|---:|---:|---:|']
    for r in result['reports']:
        p=r.get('progress',{})
        lines.append(f"| {r['shard']} | {r['status']} | {p.get('search_covered_roots','?')} | {p.get('owned_roots','?')} | {p.get('covered_leaves',0)} | {p.get('witnesses_added',0)} | {p.get('unknown_visits',0)} |")
    if result['missing_shards']:lines += ['',f"Missing shards: {result['missing_shards']}. Inspect failed jobs before resuming."]
    else:lines += ['',f"To continue: run this workflow again with resume_run = {result['run_id']}, goal = {a.goal}, shards = {a.shards}."]
    lines += ['','Download checkpoint artifacts before they expire. A green workflow only means execution completed; it does not mean a theorem was proved.']
    text='\n'.join(lines)+'\n';Path('campaign-summary.md').write_text(text)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as f:f.write(text)
    print(text)
    return 1 if result['missing_shards'] or any(r['status']=='ERROR' for r in result['reports']) else 0

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);subs=p.add_subparsers(dest='command',required=True)
    subs.add_parser('plan')
    s=subs.add_parser('shard');s.add_argument('--mode',default='search');s.add_argument('--goal',default='extension')
    s.add_argument('--shards',type=int,required=True);s.add_argument('--shard',type=int,required=True)
    s.add_argument('--split-after',type=int,default=2);s.add_argument('--smt-seconds',type=float,default=10)
    s.add_argument('--minutes',type=float,default=15);s.add_argument('--workers',type=int,default=2)
    s.add_argument('--resume',default='');s.add_argument('--checkpoint',default='checkpoint');s.add_argument('--payload',default='payload')
    c=subs.add_parser('collect');c.add_argument('directory');c.add_argument('--goal',required=True);c.add_argument('--shards',type=int,required=True)
    a=p.parse_args()
    if a.command=='plan':plan()
    elif a.command=='shard':raise SystemExit(run_shard(a))
    else:raise SystemExit(collect(a))
