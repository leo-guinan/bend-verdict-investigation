import os,re,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
orig=open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/bend-src/tests/check/capture_soundness.bend').read()
# All variants retain the same intended bad proof; only binder names/scoping structure changes.
def ren(src,m):
 for a,b in m.items(): src=re.sub(r'(?<![A-Za-z0-9_])'+re.escape(a)+r'(?![A-Za-z0-9_])',b,src)
 return src
variants=[('original',orig),('alpha',ren(orig,{'s':'q','e':'w','a':'u','b':'v'})),('outer_only',ren(orig,{'s':'scope','e':'evid','a':'left','b':'right'})),('inner_names',orig.replace('a => b => b, a => b => {==}','x => y => y, x => y => {==}')),('motive_names',orig.replace('@s:','@scope:').replace('@e:','@evid:')),('all_distinct',orig.replace('s => e => e(Ob{}, Zb{})','scope => evid => evid(Ob{}, Zb{})').replace('@s:','@scope:').replace('@e:','@evid:').replace('s(b, a)','scope(b, a)').replace('s(Zb{}, Ob{})','scope(Zb{}, Ob{})'))]
rows=[]
for i,(tag,src) in enumerate(variants):
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/capture_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/capture-shadow-probes.json','w').write(json.dumps(rows,indent=2))
