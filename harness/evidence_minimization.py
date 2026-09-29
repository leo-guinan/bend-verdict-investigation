import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
base=open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/higher_evidence_base.bend').read()
vs=[('F_affine',base.replace('~F: @a:', 'F: @a:')),('F_erased',base.replace('~F: @a:', '-F: @a:')),('simple_F',base.replace('@a: N -> @b: N -> {S{a} == S{b} : N} -> {a == b : N}','@a: N -> N')),('no_template','''import Base

type N is Data:
  Z{}
  S{p: N}

def use(F: @a: N -> @b: N -> {S{a} == S{b} : N} -> {a == b : N}, a: N, b: N, e: {S{a} == S{b} : N}) -> {a == b : N}:
  F(a, b, e)

def main() -> N:
  Z{}
''')]
rows=[]
for i,(tag,src) in enumerate(vs):
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence_min_{i}.bend';open(p,'w').write(src);rr=[]
 for flag in ['--check-only','--verdict']:
  r=subprocess.run([B,p,flag],capture_output=True,text=True,timeout=20);rr.append({'flag':flag,'rc':r.returncode,'out':r.stdout+r.stderr})
 rows.append({'tag':tag,'sha256':hashlib.sha256(src.encode()).hexdigest(),'runs':rr})
print(json.dumps(rows,indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence-minimization.json','w').write(json.dumps(rows,indent=2))
