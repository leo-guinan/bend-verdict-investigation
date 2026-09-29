import os, subprocess, json, hashlib
B=os.path.expanduser('~/.bend/bin/bend')
head='''type Empty is Data:

type Unit is Data:
  Unit{}

type Array<-T: Type> is Type:
  ALeaf{value: T}
  ANode{xs: Array<T>, ys: Array<T>}

def EmptyIfLeftIsNode(xs: Array<Unit>) -> Type:
  match xs:
    case ALeaf{x}: Unit
    case ANode{ALeaf{x}, r}: Unit
    case ANode{ANode{a, b}, r}: Empty

def Pick(~xs: Array<Unit>) -> Type:
  EmptyIfLeftIsNode(xs)

def Id(~xs: Array<Unit>) -> Array<Unit>:
  xs

def Eta(~xs: Array<Unit>) -> Array<Unit>:
  Id(~xs)

def Wrap(~T: Type) -> Type:
  T
'''
S='ANode{ALeaf{Unit{}}, ANode{ALeaf{Unit{}}, ALeaf{Unit{}}}}'; D='ANode{ANode{ALeaf{Unit{}}, ALeaf{Unit{}}}, ALeaf{Unit{}}}'
vs=[('direct',f'Pick(~{S})',f'Pick(~{D})'),('id',f'Pick(~Id(~{S}))',f'Pick(~Id(~{D}))'),('eta',f'Pick(~Eta(~{S}))',f'Pick(~Eta(~{D}))'),('wrap',f'Pick(~Wrap(~{S}))',f'Pick(~Wrap(~{D}))'),('nested_alias',f'Pick(~Eta(~Id(~{S})))',f'Pick(~Id(~Eta(~{D})))'),('same_runtime_alias',f'Pick(~Id(~{S}))',f'Pick(~Eta(~{S}))')]
rows=[]
for i,(tag,st,dt) in enumerate(vs):
 src=head+f'''\ndef seed() -> {st}:\n  Unit{{}}\n\ndef contradiction() -> {dt}:\n  seed\n'''
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/alias_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/alias-normalization-probes.json','w').write(json.dumps(rows,indent=2))
