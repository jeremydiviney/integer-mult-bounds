"""Discovery-only literal owner swaps, retaining every call and helper width.

Prepared with OpenAI Codex assistance. Nomination is not admission; use the
unchanged source-bound physical replay and exact moment engines on any output.
"""
import argparse,copy,gzip,hashlib,json,math,random,time
from collections import Counter,defaultdict
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--data',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--trials',type=int,default=500000)
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--temperature',type=float,default=0)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False);rng=random.Random(a.seed)
    praw=(a.data/'PLAN.json').read_bytes();oraw=(a.data/'OWNERS.json.gz').read_bytes();plan=json.loads(praw);roles=json.loads(gzip.decompress(oraw))
    bins=[];index={}
    for key,(cap,ts)in plan['windows'].items():
        o,ch=map(int,key.split(','))
        for port in range(112):
            family=o*896+(2*plan['pairs'][str(ch)]+plan['sides'][str(ch)])*112+port
            index[o,ch,port]=len(bins);bins.append(dict(owner=o,child=ch,port=port,family=family,cap=cap,left=cap,window=set(ts),roles=[]))
    occupied=defaultdict(set);bywidth=defaultdict(list);loc=[]
    for i,r in enumerate(roles):
        k=index[r['owner_replica'],r['child'],r['port']];b=bins[k];loc.append(k);b['roles'].append(i);b['left']-=r['width'];bywidth[r['width']].append(i)
        assert r['time']not in occupied[b['family']];occupied[b['family']].add(r['time'])
    psi=[0]+[r*math.log(73/r)for r in range(1,49)];score=sum(psi[b['left']]for b in bins);original=score;best=score;bestloc=loc[:]
    partial={i for i,b in enumerate(bins)if 0<b['left']<b['cap']};accepted=0;strict=0;changes=[];start=time.monotonic()
    for trial in range(a.trials):
        i=rng.choice(tuple(partial));b=bins[i]
        ri=rng.choice(b['roles']);r=roles[ri];w=r['width'];t=r['time']
        ws=[v for v in bywidth if w<v<=w+b['left']]
        if not ws:continue
        sidx=rng.choice(bywidth[rng.choice(ws)]);s=roles[sidx];j=loc[sidx];d=bins[j];v=s['width'];u=s['time']
        if i==j or b['family']==d['family'] or d['left']+v-w>d['cap']:continue
        if u not in b['window'] or t not in d['window']:continue
        if u!=t and(u in occupied[b['family']]or t in occupied[d['family']]):continue
        lb=b['left']+w-v;ld=d['left']+v-w
        gain=psi[b['left']]+psi[d['left']]-psi[lb]-psi[ld]
        if gain< -1e-9 and(a.temperature<=0 or rng.random()>=math.exp(gain/a.temperature)):continue
        occupied[b['family']].remove(t);occupied[d['family']].remove(u);occupied[b['family']].add(u);occupied[d['family']].add(t)
        b['roles'].remove(ri);b['roles'].append(sidx);d['roles'].remove(sidx);d['roles'].append(ri)
        b['left']=lb;d['left']=ld;loc[ri]=j;loc[sidx]=i;score-=gain;accepted+=1;strict+=gain>1e-9
        for k in (i,j):
            z=bins[k]
            if 0<z['left']<z['cap']:partial.add(k)
            else:partial.discard(k)
        if score<best-1e-7:
            best=score;bestloc=loc[:];changes.append(dict(trial=trial,entropy_gain=original-best))
            print('BEST',trial,original-best,flush=True)
    # Only export the best incumbent, with independently recomputed intervals.
    used=defaultdict(list)
    for i,k in enumerate(bestloc):used[k].append(i)
    idle=Counter();newroles=copy.deepcopy(roles);seen=defaultdict(set)
    for k,b in enumerate(bins):
        off=0
        for i in sorted(used[k],key=lambda i:(roles[i]['time'],roles[i]['helper'])):
            r=newroles[i];assert r['time']in b['window']and r['time']not in seen[b['family']]
            seen[b['family']].add(r['time']);r.update(owner_replica=b['owner'],child=b['child'],port=b['port'],copy=b['owner']*112+b['port'],family=b['family'],offset=off);off+=r['width']
        assert off<=b['cap']
        if off<b['cap']:idle[b['cap']-off]+=1
    actual=sum(psi[r]*n for r,n in idle.items());assert abs(actual-best)<1e-6
    paid=idle.copy()
    for c in plan['provider_calls']:paid.update({int(k):n for k,n in plan['provider_registry'][c['provider']]['actual_paid_profile'].items()})
    assert 73*plan['live']-sum(r*n for r,n in paid.items())==plan['deficit']
    summary=dict(status='NOMINATION_REQUIRES_ADMISSION',seed=a.seed,trials=a.trials,temperature=a.temperature,accepted_swaps=accepted,improving_swaps=strict,entropy_gain=original-best,seconds=time.monotonic()-start,idle_profile=dict(sorted(idle.items())),best_history=changes,changed_owner_records=sum(x['family']!=y['family']for x,y in zip(roles,newroles)))
    (a.out/'SEARCH.json').write_text(json.dumps(summary,indent=2)+'\n')
    if original-best>1e-7:
        raw=json.dumps(newroles,sort_keys=True,separators=(',',':')).encode();packed=gzip.compress(raw,mtime=0)
        plan.update(profile={str(r):n for r,n in sorted(paid.items())},mode='literal-owner-width-swap-search',solver_status='FEASIBLE_NOT_OPTIMAL',gap=None,source_plan_sha256=hashlib.sha256(praw).hexdigest(),source_owners_sha256=hashlib.sha256(oraw).hexdigest(),assignment_sha256=hashlib.sha256(packed).hexdigest())
        (a.out/'PLAN.json').write_text(json.dumps(plan,indent=1)+'\n');(a.out/'OWNERS.json.gz').write_bytes(packed)
    print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
