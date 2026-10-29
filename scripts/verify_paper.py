"""Portable read-only check of paper formulas and copied rational certificates.
Run from any directory. Requires Python and SymPy; no historical paths/imports.
Writes no files. Output can be redirected to a new receipt by the caller.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,sys
import sympy as s
sys.set_int_max_str_digits(0)
P=Path(__file__).resolve().parents[1]
c=json.loads((P/'records/limit_02/numerical_certificate.json').read_text())
checks=[]
def check(name,ok):
 checks.append({'name':name,'passed':bool(ok)})
 if not ok:raise AssertionError(name)
q,a,z,u,eta=s.symbols('q a z u eta',positive=True)
r=q*q;k=1+r
t=a*a+z*z*(k-a)**2-2*z*(a-r)*(1-a)
sq=((1+z)*a-z*k)**2+2*r*z
check('completed_square',s.expand(t-sq)==0)
au=u*k/(1+u)
check('finite_readout_identity',s.factor(t.subs(a,au)-2*r*u-(u-z)*(k*k*(u-z)/(1+u)**2-2*r))==0)
check('small_u',s.factor(t.subs(a,r)-(r*r+z*z))==0)
check('junction',s.factor(au.subs(u,r)-r)==0)
astar=(k*(1+q)-s.sqrt(k*k-2*q*q*(q+2)))/(q+2)
check('asymptotic',s.series(astar,q,0,4).removeO()==q/2+3*q*q/4+5*q**3/8)
check('benefit_boundary',s.simplify((2*(q**s.Rational(3,2)+2*eta)**2).subs(eta,(astar/s.sqrt(2)-q**s.Rational(3,2))/2)-astar**2)==0)
def root(x,n=90):
 d=10**n;t=isqrt(x.numerator*d*d//x.denominator)
 return F(t,d),F(t+1,d)
def logbound(x,N=180):
 x=F(x)
 if x<=0:raise ValueError('NONPOSITIVE_LOG')
 e=0
 while x>=2:x/=2;e+=1
 while x<1:x*=2;e-=1
 def series(y):
  base=2*sum((y**(2*j+1)/F(2*j+1) for j in range(N)),F(0))
  tail=2*y**(2*N+1)/(F(2*N+1)*(1-y*y))
  return base,base+tail
 l,h=series((x-1)/(x+1));l2,h2=series(F(1,3))
 return (l+e*l2,h+e*h2) if e>=0 else (l+e*h2,h+e*l2)
def dbbound(lo,hi):
 ll,_=logbound(lo/2);_,hh=logbound(hi/2);dlo,dhi=logbound(10)
 vals=[-10*v/d for v in (ll,hh) for d in (dlo,dhi)]
 return min(vals),max(vals)
def overlap(x,record):return x[0]<=F(record['upper']) and F(record['lower'])<=x[1]
for row in c['rows']:
 Q=F(row['Q']);R=Q*Q;K=1+R;dl,dh=root(K*K-2*Q*Q*(Q+2));num=Q*K*K+2*Q*Q
 al,ah=num/(K*(1+Q)+dh),num/(K*(1+Q)+dl)
 check('root_domain_'+str(Q),R<al<=ah<Q*K/(1+Q))
 check('Vfixed_'+str(Q),overlap((al*al,ah*ah),row['V_fixed']))
 check('A_fixed_'+str(Q),overlap(dbbound(al*al,ah*ah),row['A_fixed_db']))
 check('epsilon0_'+str(Q),F(row['epsilon0_exact'])==R/(K*K))
 check('adaptive_'+str(Q),F(row['V_epsilon_exact'])==2*Q**3)
m=c['main'];B=F(m['T_error_upper_exact']);check('main_B',B==F(9,500000))
bp=dbbound(B,B);check('policy_db',overlap(bp,m['A_policy_bound']))
check('readout_budget',F(9,100000)<F(10000,100020001))
for key,record in [('A_policy_display','A_policy_bound'),('fixed_global_A_upper_display','fixed_global_A_upper'),('certified_advantage_display','certified_advantage_db')]:
 check('outward_display_'+key,F(m[key][0])<=F(m[record]['lower'])<=F(m[record]['upper'])<=F(m[key][1]))
mc=json.loads((P/'records/limit_02/metadata_correction.json').read_text())
check('symbolic_count_correction',mc['corrected']==7 and len(mc['actual_names'])==7)
for stage in ['01','02']:
 audit=json.loads((P/f'records/limit_{stage}/independent_audit.json').read_text());check('historical_audit_'+stage,audit['status']=='PASS')
try:logbound(0)
except ValueError:check('illegal_log',True)
else:check('illegal_log',False)
print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'root_digits':90,'log_terms':180,'scope':'paper-specific exact formula and certificate cross-check; not a new optical experiment'},indent=2))
