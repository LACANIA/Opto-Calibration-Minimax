"""Read-only payload integrity check; no implicit research-tree dependencies."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[1]
m=json.loads((P/'MANIFEST.json').read_text(encoding='utf-8'))
expected={v['path']:v for v in m['files']}
excluded={'.git','.venv','venv','__pycache__','reproduced'}
seen={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(P).parts) and p.name!='MANIFEST.json' and p.suffix not in {'.pyc','.pyo'}}
assert seen==set(expected),{'missing':sorted(set(expected)-seen),'unexpected':sorted(seen-set(expected))}
for rel,v in expected.items():
    p=(P/rel).resolve();assert p.is_relative_to(P.resolve())
    assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],rel
print(json.dumps({'status':'PASS','files':len(seen),'writes':0},indent=2))
