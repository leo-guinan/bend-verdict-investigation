import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
head='''import Base

type N is Data:
  Z{}
  S{p: N}

type Unit2 is Data:
  U{}

'''
vs=[
('baseline','''def f.g(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})

def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(Z{}, u => f(p))
'''),
('helper_default','''def f.g(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: rest(U{})
    case _: Z{}

def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(Z{}, u => f(p))
'''),
('nested_helper','''def f.g(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{Z{}}: rest(U{})
    case S{S{p}}: rest(U{})

def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(Z{}, u => f(p))
'''),
('two_helpers','''def f.g(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})

def f.h(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})

def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(Z{}, u => f.h(Z{}, v => f(p)))
'''),
('empty_tail','''type E2 is Data:

def f.g(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: rest(U{})

def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(Z{}, u => f(p))
'''),
]
tail='''
def main() -> N:
  f(S{S{Z{}}})
'''
rows=[]
for i,(tag,body) in enumerate(vs):
 src=head+body+tail;p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/group_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/group-emission-probes.json','w').write(json.dumps(rows,indent=2))
