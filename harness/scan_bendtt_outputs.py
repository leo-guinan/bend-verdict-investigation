#!/usr/bin/env python3
import json,os,subprocess,re,tempfile
j=json.load(open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/verdict-scan.json'))
root='/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/bend-src/tests'; bend=os.path.expanduser('~/.bend/bin/bend')
hits=[]; emitted=0
with tempfile.TemporaryDirectory(prefix='bendtt-scan-') as d:
 for r in j['rows']:
  if not r.get('ok'): continue
  src=os.path.join(root,r['file']); out=os.path.join(d,str(emitted)+'.bendtt')
  try:
   p=subprocess.run([bend,src,'-o',out],capture_output=True,text=True,timeout=8)
  except subprocess.TimeoutExpired: continue
  if p.returncode!=0 or not os.path.exists(out): continue
  emitted+=1
  lines=open(out,encoding='utf8').read().splitlines()
  # A closed top-level Empty type is <>. Keep exact line evidence.
  for no,line in enumerate(lines,1):
   if re.search(r':\s*<>\s*=\s*$',line) or re.search(r'^\S+\s*:\s*<>\s*=',line):
    hits.append({'source':r['file'],'line':no,'text':line})
print(json.dumps({'emitted':emitted,'closed_empty_type_lines':hits},indent=2))
