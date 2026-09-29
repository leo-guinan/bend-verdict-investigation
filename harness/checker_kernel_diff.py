#!/usr/bin/env python3
import glob,os,subprocess,json
ROOT='/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/bend-src/tests'; BEND=os.path.expanduser('~/.bend/bin/bend')
rows=[]
for f in sorted(glob.glob(ROOT+'/**/*.bend',recursive=True)):
  try:
    p=subprocess.run([BEND,f,'--check-only'],capture_output=True,text=True,timeout=5)
    q=subprocess.run([BEND,f,'--verdict'],capture_output=True,text=True,timeout=5)
  except subprocess.TimeoutExpired:
    continue
  plain_ok=p.returncode==0 and 'ALL PROOFS CHECK' in p.stdout
  verdict_ok=q.returncode==0 and 'ALL PROOFS CHECK' in q.stdout
  if plain_ok != verdict_ok:
    rows.append({'file':os.path.relpath(f,ROOT),'plain_ok':plain_ok,'verdict_ok':verdict_ok,'plain':(p.stdout+p.stderr)[:400],'verdict':(q.stdout+q.stderr)[:400]})
print(json.dumps({'mismatches':len(rows),'rows':rows},indent=2))
open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/checker-kernel-mismatches.json','w').write(json.dumps(rows,indent=2))
