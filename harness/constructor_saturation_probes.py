import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
head='''import Base

type N is Data:
  Z{}
  S{p: N}

type Uni is Data:
  U{}

type Emp is Data:

def isZ(n: N) -> Data:
  match n:
    case Z{}: Uni
    case S{k}: Emp

def isZeta(n: N) -> Data:
  isZ(n)

type DPair<a, b, -T: Kind(a), -p: @x: T -> Kind(b)> is Kind(a <&> b):
  MkP{fst: T, snd: p(fst)}

'''
vs=[('correct','''def packed() -> DPair<&2, &2, N, isZ>:
  MkP{Z{}, U{}}
'''),('explicit_ann','''def packed() -> DPair<&2, &2, N, isZ>:
  ({MkP{Z{}, U{}}} : DPair<&2, &2, N, isZ>)
'''),('wrong_index','''def packed() -> DPair<&2, &2, N, isZ>:
  MkP{S{Z{}}, U{}}
'''),('wrong_field','''def packed() -> DPair<&2, &2, N, isZ>:
  MkP{Z{}, Emp}
'''),('eta_family','''def packed() -> DPair<&2, &2, N, isZeta>:
  MkP{Z{}, U{}}
'''),('nested_pair','''def packed() -> DPair<&2, &2, N, isZ>:
  MkP{Z{}, (U{} : Uni)}
''')]
tail='''\ndef get(d: DPair<&2, &2, N, isZ>) -> N:\n  match d:\n    case MkP{a, b}: a\n\ndef main() -> N:\n  get(packed())\n'''
rows=[]
for i,(tag,body) in enumerate(vs):
 src=head+body+tail;p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/ctor_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/constructor-saturation-probes.json','w').write(json.dumps(rows,indent=2))
