import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
head='''import Base

type Box<A: Type> is Type:
  MkBox{x: A}

def make(n: Nat) -> Box<Nat>:
  MkBox{n}

def make_any(~A: Type, x: A) -> Box<A>:
  MkBox{x}

def get(b: Box<Nat>) -> Nat:
  match b:
    case MkBox{x}: x

'''
vs=[('direct','''def main() -> Nat:
  get(make(3n))
'''),('specialized','''def main() -> Nat:
  get(make_any(~Nat, 3n))
'''),('lambda_ctor','''def ctor() -> Nat -> Box<Nat>:
  x => MkBox{x}
def main() -> Nat:
  get(ctor()(3n))
'''),('let_ctor','''def make_let(n: Nat) -> Box<Nat>:
  x = n
  MkBox{x}
def main() -> Nat:
  get(make_let(3n))
'''),('wrong_specialization','''def main() -> Nat:
  get(make_any(~Bool, 3n))
'''),('omitted_template','''def main() -> Nat:
  get(make_any(3n))
''')]
rows=[]
for i,(tag,body) in enumerate(vs):
 src=head+body;p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/partial_ctor_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/partial-constructor-probes.json','w').write(json.dumps(rows,indent=2))
