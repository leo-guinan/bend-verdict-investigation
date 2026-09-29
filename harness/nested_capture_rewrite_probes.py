import os,re,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
base=open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/nested_capture_rewrite.bend').read()
variants=[('baseline',base),('motive_a',base.replace('%e@e :','%a@e :')),('motive_b',base.replace('%e@e :','%b@e :')),('motive_Q',base.replace('%e@e :','%Q@e :')),('nested_outer',base.replace('def main() -> N:', 'def outer(~R: Type, a: N, b: N, e: {S{a} == S{b} : N}) -> {a == b : N}:\n  wrap(~R, a, b, e)\n\ndef main() -> N:')),('swap_call',base.replace('lift(~Q, a, b, e)','lift(~Q, b, a, e)'))]
rows=[]
for i,(tag,src) in enumerate(variants):
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/nested_capture_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/nested-capture-rewrite-probes.json','w').write(json.dumps(rows,indent=2))
