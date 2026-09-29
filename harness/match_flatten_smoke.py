import os, subprocess, json, tempfile, hashlib
B=os.path.expanduser('~/.bend/bin/bend')
base='''import Base\n\ntype N is Data:\n  Z{}\n  S{p: N}\n\ndef f(n: N) -> N:\n  match n:\n__BODY__\n\nlaw main:\n  N\n\ndef main():\n  f(S{Z{}})\n'''
variants=[
'''    case Z{}:
      Z{}
    case S{p}:
      S{f(p)}''',
'''    case S{p}:
      S{f(p)}
    case Z{}:
      Z{}''',
'''    case Z{}:
      Z{}
    case S{Z{}}:
      S{Z{}}
    case S{S{p}}:
      S{f(S{p})}''',
'''    case Z{}:
      Z{}
    case S{p}:
      S{f(p)}
    case _:
      Z{}''',
'''    case S{Z{}}:
      S{Z{}}
    case S{p}:
      S{f(p)}
    case Z{}:
      Z{}''',
'''    case Z{}:
      Z{}
    case S{p}:
      S{f(p)}
    case S{p}:
      Z{}''',
]
rows=[]
for i,b in enumerate(variants):
 p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/bend_match_{i}.bend'; open(p,'w').write(base.replace('__BODY__',b))
 r=subprocess.run([B,p,'--verdict'],text=True,capture_output=True,timeout=20)
 rows.append({'i':i,'rc':r.returncode,'out':r.stdout+r.stderr,'sha256':hashlib.sha256(open(p,'rb').read()).hexdigest()})
print(json.dumps({'variants':len(rows),'passes':sum(r['rc']==0 for r in rows),'rows':rows},indent=2))
open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/match-flatten-smoke.json','w').write(json.dumps(rows,indent=2))
