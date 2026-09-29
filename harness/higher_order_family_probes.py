import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
head='''import Base

def Payload(b: Bool) -> Type:
  match b:
    case False{}: Unit
    case True{}: Empty

def Apply(~F: @b: Bool -> Type, b: Bool) -> Type:
  F(b)

def Alias(~F: @b: Bool -> Type, b: Bool) -> Type:
  Apply(~F, b)

def BoolId(b: Bool) -> Bool:
  b

def BoolNot(b: Bool) -> Bool:
  match b:
    case False{}: True{}
    case True{}: False{}

type Packet<b: Bool> is Type:
  P{payload: Payload(b)}

def seed() -> Packet<False{}>:
  P{Unit{}}

'''
vs=[('direct','Apply(~Payload, True{})'),('alias','Alias(~Payload, True{})'),('id_true','Apply(~Payload, BoolId(True{}))'),('not_false','Apply(~Payload, BoolNot(False{}))'),('double_not','Alias(~Payload, BoolNot(BoolNot(True{})))'),('packet_alias','Apply(~(b => Packet<b>), True{})')]
rows=[]
for i,(tag,target) in enumerate(vs):
 src=head+f'def contradiction() -> {target}:\n  seed\n'
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/family_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/higher-order-family-probes.json','w').write(json.dumps(rows,indent=2))
