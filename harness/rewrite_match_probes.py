import os, subprocess, json, hashlib
B=os.path.expanduser('~/.bend/bin/bend')
head='''import Base

type N is Data:
  Z{}
  S{p: N}

law pred:
  for n: N
  N

def pred(n):
  match n:
    case Z{}:
      Z{}
    case S{p}:
      p

'''
variants=[
('plain','''law q:\n  for a: N\n  for b: N\n  for e: {S{a} == S{b} : N}\n  {a == b : N}\n\ndef q(a,b,e):\n  %x@e : {pred(S{a}) == pred(_) : N}\n  {==}\n'''),
('nested_match','''law q:\n  for a: N\n  for b: N\n  for e: {S{a} == S{b} : N}\n  {a == b : N}\n\ndef q(a,b,e):\n  match a:\n    case Z{}:\n      %x@e : {pred(S{a}) == pred(_) : N}\n      {==}\n    case S{ap}:\n      %x@e : {pred(S{ap}) == pred(_) : N}\n      {==}\n'''),
('endpoint_swap','''law q:\n  for a: N\n  for b: N\n  for e: {S{a} == S{b} : N}\n  {a == b : N}\n\ndef q(a,b,e):\n  %x@e : {pred(_) == pred(S{b}) : N}\n  {==}\n'''),
('double_rewrite','''law q:\n  for a: N\n  for b: N\n  for e: {S{a} == S{b} : N}\n  {a == b : N}\n\ndef q(a,b,e):\n  %x@e : {pred(S{a}) == pred(_) : N}\n  %y@x : {pred(S{a}) == pred(_) : N}\n  {==}\n'''),
('empty_claim','''type EmptyQ is Data:\n\nlaw q:\n  for a: N\n  for b: N\n  for e: {S{a} == S{b} : N}\n  EmptyQ\n\ndef q(a,b,e):\n  %x@e : {pred(S{a}) == pred(_) : N}\n  {==}\n'''),
]
tail='''\nlaw main:\n  N\n\ndef main():\n  Z{}\n'''
rows=[]
for i,(tag,body) in enumerate(variants):
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/rewrite_probe_{i}.bend';open(p,'w').write(head+body+tail)
 r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20)
 rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(open(p,'rb').read()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2))
open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/rewrite-match-probes.json','w').write(json.dumps(rows,indent=2))
