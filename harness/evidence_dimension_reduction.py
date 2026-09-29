import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
pre='''import Base

type N is Data:
  Z{}
  S{p: N}

def use(~F: __FT__, a: N, b: N, e: __ET__) -> __RT__:
  __BODY__

def main() -> N:
  Z{}
'''
cases=[('plain','@a: N -> @b: N -> N','N','N','F(a,b,e)'),('eq_arg_only','@a: N -> @b: N -> {S{a} == S{b} : N} -> N','{S{a} == S{b} : N}','N','F(a,b,e)'),('eq_result_only','@a: N -> @b: N -> N -> {a == b : N}','N','{a == b : N}','F(a,b,Z{})'),('eq_both_affine','@a: N -> @b: N -> {S{a} == S{b} : N} -> {a == b : N}','{S{a} == S{b} : N}','{a == b : N}','F(a,b,e)'),('eq_both_template_removed','@a: N -> @b: N -> {S{a} == S{b} : N} -> {a == b : N}','{S{a} == S{b} : N}','{a == b : N}','F(a,b,e)')]
rows=[]
for i,(tag,ft,et,rt,body) in enumerate(cases):
 src=pre.replace('__FT__',ft).replace('__ET__',et).replace('__RT__',rt).replace('__BODY__',body)
 if tag=='eq_both_template_removed': src=src.replace('def use(~F:', 'def use(F:')
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence_dim_{i}.bend';open(p,'w').write(src);rr=[]
 for flag in ['--check-only','--verdict']:
  r=subprocess.run([B,p,flag],capture_output=True,text=True,timeout=20);rr.append({'flag':flag,'rc':r.returncode,'out':r.stdout+r.stderr})
 rows.append({'tag':tag,'sha256':hashlib.sha256(src.encode()).hexdigest(),'runs':rr})
print(json.dumps(rows,indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence-dimension-reduction.json','w').write(json.dumps(rows,indent=2))
