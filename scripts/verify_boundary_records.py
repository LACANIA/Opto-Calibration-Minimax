"""Read-only exact checks of the saved finite boundary controls."""
from pathlib import Path
from fractions import Fraction as F
import sys,json
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'src'))
from bounded_policy import consistent
rows=json.loads((P/'records/limit_02/boundary_records.json').read_text())
for row in rows:
    Q,epsilon,hat,z=map(F,(row['Q'],row['epsilon'],row['hat_z'],row['z']))
    out=consistent(Q,epsilon,hat,z)
    for key in ['u','a','cos2']:assert out[key]==F(row[key]),key
    a=out['a'];r=Q*Q;K=1+r
    val=((1+z)*a-z*K)**2+2*r*z
    assert val==F(row['worst_external_T'])
    assert out['sufficient_condition']==row['sufficient_condition']
    if out['sufficient_condition']:assert val<=2*Q**3
print(json.dumps({'status':'PASS','records':len(rows),'arithmetic':'exact rational','scope':'finite controls, not a new full-domain proof'},indent=2))
