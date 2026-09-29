import os, subprocess, json, hashlib
B=os.path.expanduser('~/.bend/bin/bend')
base=open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/higher_evidence_base.bend').read()
variants=[]
def add(tag, src): variants.append((tag, src))
add('direct', base)
add('eta_call', base.replace('F(a, b, e)', 'F(a)(b)(e)'))
add('let_fn', base.replace('F(a, b, e)', 'g = F(a, b)\n  g(e)'))
add('annotated_fn', base.replace('F(a, b, e)', '(F(a, b) : @e: {S{a} == S{b} : N} -> {a == b : N})(e)'))
add('template_eta', base.replace('F(a, b, e)', '(x => F(a, b, x))(e)'))
add('result_empty', base.replace(') -> {a == b : N}:\n  F(a, b, e)', ') -> Empty:\n  F(a, b, e)'))
apply_src='''\ndef apply_e(~F: @a: N -> @b: N -> {S{a} == S{b} : N} -> {a == b : N}, a: N, b: N, e: {S{a} == S{b} : N}) -> {a == b : N}:\n  F(a,b,e)\n'''
add('evidence_template', base.replace('  F(a, b, e)', '  apply_e(~F, a, b, e)') + apply_src)
rows=[]
for i,(tag,src) in enumerate(variants):
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence_mut_{i}.bend'
 open(p,'w').write(src)
 rr=[]
 for flag in ['--check-only','--verdict']:
  r=subprocess.run([B,p,flag],capture_output=True,text=True,timeout=20)
  rr.append({'flag':flag,'rc':r.returncode,'out':r.stdout+r.stderr})
 rows.append({'tag':tag,'sha256':hashlib.sha256(src.encode()).hexdigest(),'runs':rr})
print(json.dumps(rows,indent=2))
open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence-mutations.json','w').write(json.dumps(rows,indent=2))
