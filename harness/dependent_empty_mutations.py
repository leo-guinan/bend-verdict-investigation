import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
base=open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/dependent_empty_result_probe.bend').read()
variants=[
('direct',base),
('match_a',base.replace('  F(a,b,e)','  match a:\n    case Z{}: F(a,b,e)\n    case S{p}: F(a,b,e)')),
('match_b',base.replace('  F(a,b,e)','  match b:\n    case Z{}: F(a,b,e)\n    case S{p}: F(a,b,e)')),
('let_result',base.replace('  F(a,b,e)','  x = F(a,b,e)\n  x')),
('annotated_result',base.replace('  F(a,b,e)','  (F(a,b,e) : Out(a))')),
('rewrite_result',base.replace('  F(a,b,e)','  %h@e : {a == _ : N}\n  F(a,b,e)'))]
rows=[]
for i,(tag,src) in enumerate(variants):
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/dependent_empty_mut_{i}.bend';open(p,'w').write(src);rr=[]
 for flag in ['--check-only','--verdict']:
  r=subprocess.run([B,p,flag],capture_output=True,text=True,timeout=20);rr.append({'flag':flag,'rc':r.returncode,'out':r.stdout+r.stderr})
 rows.append({'tag':tag,'sha256':hashlib.sha256(src.encode()).hexdigest(),'runs':rr})
print(json.dumps(rows,indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/dependent-empty-mutations.json','w').write(json.dumps(rows,indent=2))
