import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
variants={
'inj_only':'''import Base
 type N is Data:
  Z{}
  S{p: N}
 def pred(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: p
 def inj(a: N, b: N, e: {S{a} == S{b} : N}) -> {a == b : N}:
  %x@e : {pred(S{a}) == pred(_) : N}
  {==}
'''.replace(' type','type').replace(' def','def'),
'use_no_call':open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/higher_evidence_base.bend').read(),
'use_call':open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/higher_evidence_base.bend').read().replace('def main() -> N:\n  Z{}','def main() -> N:\n  inj(Z{}, Z{}, {==})\n'),
}
rows=[]
for tag,src in variants.items():
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence_diff_{tag}.bend';open(p,'w').write(src);rr=[]
 for flag in ['--check-only','--verdict']:
  r=subprocess.run([B,p,flag],capture_output=True,text=True,timeout=20);rr.append({'flag':flag,'rc':r.returncode,'out':r.stdout+r.stderr})
 rows.append({'tag':tag,'sha256':hashlib.sha256(src.encode()).hexdigest(),'runs':rr})
print(json.dumps(rows,indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence-differential.json','w').write(json.dumps(rows,indent=2))
