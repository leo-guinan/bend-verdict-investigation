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
('route_g_h','''def f.g(n: N, rest: Unit2 -> N) -> N:
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
('swap_tags','''def f.g(n: N, rest: Unit2 -> N) -> N:
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
    case S{p}: f.h(Z{}, u => f.g(Z{}, v => f(p)))
'''),
('different_leads','''def f.g(n: N, rest: Unit2 -> N) -> N:
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
    case S{p}: f.g(p, u => f.h(Z{}, v => f(p)))
'''),
('partial_helper','''def f.g(n: N, rest: Unit2 -> N) -> N:
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
    case S{p}: f.g(Z{})
'''),
('three_members','''def f.g(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f.h(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f.k(n: N, rest: Unit2 -> N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: rest(U{})
def f(n: N) -> N:
  match n:
    case Z{}: Z{}
    case S{p}: f.g(Z{}, u => f.h(Z{}, v => f.k(Z{}, w => f(p))))
'''),
('eta_state','''def f.g(n: N, rest: Unit2 -> N) -> N:
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
    case S{p}: f.g(Z{}, u => (x => f.h(Z{}, v => f(p)))(u))
''')]
tail='''
def main() -> N:
  f(S{S{Z{}}})
'''
rows=[]
for i,(tag,body) in enumerate(vs):
 src=head+body+tail;p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/selector_probe_{i}.bend';open(p,'w').write(src);r=subprocess.run([B,p,'--verdict'],capture_output=True,text=True,timeout=20);rows.append({'tag':tag,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(src.encode()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(x['rc']==0 for x in rows),'rows':rows},indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/selector-state-probes.json','w').write(json.dumps(rows,indent=2))
