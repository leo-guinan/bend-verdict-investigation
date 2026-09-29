import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
base='''import Base

def f(n: Nat) -> Nat:
  match n:
    case 0n:
      0n
    case 1n+p:
      ((1n + f(p)) : Nat)

def main() -> Nat:
  f({arg})
'''
vs=[('zero','0n'),('one','1n'),('succ','2n'),('large','1000n'),('nested','Nat.add(100n, 1n)')]
rows=[]
for i,(tag,arg) in enumerate(vs):
 src=base.replace('{arg}',arg);p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/numeric_probe_{i}.bend';open(p,'w').write(src);rr=[]
 for flag in ['--check-only','--verdict']:
  r=subprocess.run([B,p,flag],capture_output=True,text=True,timeout=20);rr.append({'flag':flag,'rc':r.returncode,'out':r.stdout+r.stderr})
 rows.append({'tag':tag,'sha256':hashlib.sha256(src.encode()).hexdigest(),'runs':rr})
print(json.dumps(rows,indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/numeric-match-probes.json','w').write(json.dumps(rows,indent=2))
