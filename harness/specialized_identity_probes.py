import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
head='''import Base

type N is Data:
  Z{}
  S{p: N}

type Unit2 is Data:
  U{}

type Box is Type:
  B{}

'''
vs=[
('one','''def f.g(~T: Type, n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(~Unit2, Z{}, u => f(p))
'''),
('two_types','''def f.g(~T: Type, n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f.h(~T: Type, n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(~Unit2, Z{}, u => f.h(~N, Z{}, v => f(p)))
'''),
('swap_specialized','''def f.g(~T: Type, n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f.h(~T: Type, n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.h(~Unit2, Z{}, u => f.g(~N, Z{}, v => f(p)))
'''),
('same_tag_diff_type','''def f.g(~T: Type, n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f.h(~T: Type, n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(~Unit2, Z{}, u => f.h(~Box, Z{}, v => f(p)))
'''),
('partial_spec','''def f.g(~T: Type, n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(Z{}, u => f(p))
''')]
tail='''
def main() -> N:
  f(S{S{Z{}}})
'''
rows=[]
for i,(tag,body) in enumerate(vs):
 src=head+body+tail;p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/special_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/specialized-identity-probes.json','w').write(json.dumps(rows,indent=2))
