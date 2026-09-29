#!/usr/bin/env python3
import glob, os, subprocess, json, re, time
ROOT='/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/bend-src/tests'
BEND=os.path.expanduser('~/.bend/bin/bend')
files=sorted(glob.glob(ROOT+'/**/*.bend', recursive=True))
rows=[]
for f in files:
    text=open(f,encoding='utf-8').read()
    suspicious=bool(re.search(r'(?m)^\s*law\s+(?:main|boom|false)\s*:\s*\n\s*Empty\s*$', text) or re.search(r'(?m)^\s*def\s+(?:main|boom|false)\([^)]*\)\s*->\s*Empty\s*:', text))
    try:
        p=subprocess.run([BEND,f,'--verdict'],capture_output=True,text=True,timeout=5)
        out=(p.stdout+p.stderr).strip()
        ok=p.returncode==0 and 'ALL PROOFS CHECK' in p.stdout
        rows.append({'file':os.path.relpath(f,ROOT),'ok':ok,'suspicious':suspicious,'out':out[:500]})
    except subprocess.TimeoutExpired:
        rows.append({'file':os.path.relpath(f,ROOT),'timeout':True,'suspicious':suspicious})
result={'total':len(rows),'passing':sum(r.get('ok',False) for r in rows),'timeouts':sum(r.get('timeout',False) for r in rows),'suspicious_passes':[r for r in rows if r.get('ok') and r.get('suspicious')],'rows':rows}
path='/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/verdict-scan.json'
open(path,'w').write(json.dumps(result,indent=2,sort_keys=True))
print(json.dumps({k:result[k] for k in ('total','passing','timeouts','suspicious_passes')},indent=2))
