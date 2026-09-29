import os,subprocess,json,hashlib
B=os.path.expanduser('~/.bend/bin/bend')
base='''import Base

def f(x: U32) -> U32:
  match x:
    case 0: 0
    case 1: 1
    case 4294967295: 2
    case _: 3

def main() -> U32:
  f({arg})
'''
vs=[('zero','0'),('one','1'),('max','4294967295'),('mid','2147483648'),('overflow','4294967296'),('negative','-1')]
rows=[]
for i,(tag,arg) in enumerate(vs):
 src=base.replace('{arg}',arg);p=f'/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/u32_probe_{i}.bend';open(p,'w').write(src);rr=[]
 for flag in ['--check-only','--verdict']:
  r=subprocess.run([B,p,flag],capture_output=True,text=True,timeout=20);rr.append({'flag':flag,'rc':r.returncode,'out':r.stdout+r.stderr})
 rows.append({'tag':tag,'sha256':hashlib.sha256(src.encode()).hexdigest(),'runs':rr})
print(json.dumps(rows,indent=2));open('/Users/leoguinan/.hermes/profiles/quainance/cache/scratch/u32-boundary-probes.json','w').write(json.dumps(rows,indent=2))
