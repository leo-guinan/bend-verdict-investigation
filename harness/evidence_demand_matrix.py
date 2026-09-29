import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
base=open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/dependent_empty_result_probe.bend').read()
F='@a: N -> @b: N -> {a == b : N} -> Out(a)'
variants=[('unused',base),('demanded_template',base+f'''\ndef demand(~G: {F}) -> N:\n  use(~G, S{{Z{{}}}}, S{{Z{{}}}}, {{==}})\n\n'''),('demanded_alias',base+f'''\ndef route(~G: {F}) -> Out(S{{Z{{}}}}):\n  use(~G, S{{Z{{}}}}, S{{Z{{}}}}, {{==}})\n\ndef demand(~G: {F}) -> N:\n  route(~G)\n  Z{{}}\n\n'''),('called_template',base+f'''\ndef demand(~G: {F}) -> N:\n  use(~G, S{{Z{{}}}}, S{{Z{{}}}}, {{==}})\n\ndef main2() -> N:\n  Z{{}}\n''')]
rows=[]
for i,(tag,src) in enumerate(variants):
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/demand_probe_{i}.bend';open(p,'w').write(src);rr=[]
 for flag in ['--check-only','--verdict']:
  r=subprocess.run([B,p,flag],capture_output=True,text=True,timeout=20);rr.append({'flag':flag,'rc':r.returncode,'out':r.stdout+r.stderr})
 rows.append({'tag':tag,'sha256':hashlib.sha256(src.encode()).hexdigest(),'runs':rr})
print(json.dumps(rows,indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/evidence-demand-matrix.json','w').write(json.dumps(rows,indent=2))
