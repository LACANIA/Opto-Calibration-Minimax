"""Read-only reproduction of the stated sufficient angle-boundary enclosure."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
P=Path(__file__).resolve().parents[1]
record=json.loads((P/'checks/angle_boundary.json').read_text(encoding='utf-8'))
D=10**80
def root(x):
    n=isqrt(x.numerator*D*D//x.denominator)
    lo,hi=F(n,D),F(n+1,D)
    assert lo*lo<=x<=hi*hi
    return lo,hi
Q=F(record['Q']);r=Q*Q;K=1+r
dl,dh=root(K*K-2*Q*Q*(Q+2));sl,sh=root(F(2))
num=Q*K*K+2*Q*Q
al=num/(K*(1+Q)+dh);ah=num/(K*(1+Q)+dl)
lo=(al/sh-F(1,1000))/2;hi=(ah/sl-F(1,1000))/2
checks={
 'rational_endpoints_reproduced':lo==F(record['eta_c_rad']['lower']) and hi==F(record['eta_c_rad']['upper']),
 'ordered_positive_enclosure':0<lo<=hi,
 'one_mrad_strictly_below':F(record['eta_main_rad'])<lo,
 'rounded_display':F('1.29445')<=1000*lo<=1000*hi<F('1.29455'),
}
assert all(checks.values()),checks
print(json.dumps({'status':'PASS','checks':checks,'scope':'existing sufficient boundary only; no optimal setting-error result'},indent=2))
