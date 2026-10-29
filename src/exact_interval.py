"""Integer fixed-point outward intervals; no floating-point elementary functions."""
from fractions import Fraction as F
from math import isqrt,factorial
S=10**70
def floor(x):return x.numerator//x.denominator
def ceil(x):return -((-x.numerator)//x.denominator)
class I:
 def __init__(self,a,b=None):
  if isinstance(a,I):self.l,self.u=a.l,a.u;return
  if b is None:b=a
  a,b=F(a),F(b)
  if a>b:raise ValueError('REVERSED_INTERVAL')
  self.l=floor(a*S);self.u=ceil(b*S)
 @classmethod
 def raw(cls,l,u):
  v=object.__new__(cls);v.l,v.u=int(l),int(u);assert v.l<=v.u;return v
 def __add__(self,y):
  y=I(y);return I.raw(self.l+y.l,self.u+y.u)
 __radd__=__add__
 def __neg__(self):return I.raw(-self.u,-self.l)
 def __sub__(self,y):return self+-I(y)
 def __rsub__(self,y):return I(y)+-self
 def __mul__(self,y):
  y=I(y);v=[a*b for a in (self.l,self.u) for b in (y.l,y.u)]
  return I.raw(min(v)//S,-((-max(v))//S))
 __rmul__=__mul__
 def __truediv__(self,y):
  y=I(y)
  if y.l<=0<=y.u:raise ValueError('ZERO_DIVISOR')
  v=[F(a*S,b) for a in (self.l,self.u) for b in (y.l,y.u)]
  return I.raw(floor(min(v)),ceil(max(v)))
 def __rtruediv__(self,y):return I(y)/self
 def __pow__(self,n):
  assert isinstance(n,int) and n>=0
  if n==0:return I(1)
  if n%2==0:
   vals=[self.l**n,self.u**n];mn=0 if self.l<=0<=self.u else min(vals);mx=max(vals)
  else:mn,mx=self.l**n,self.u**n
  d=S**(n-1);return I.raw(mn//d,-((-mx)//d))
 def sqrt(self):
  if self.l<0:raise ValueError('NEGATIVE_SQRT')
  lo=isqrt(self.l*S);hi=isqrt(self.u*S)
  return I.raw(lo,hi if hi*hi==self.u*S else hi+1)
 def fractions(self):return F(self.l,S),F(self.u,S)
 def encoded(self):return dict(lower=str(F(self.l,S)),upper=str(F(self.u,S)))
 def decimal(self,n=18):
  d=10**n;l=(self.l*d)//S;u=-((-self.u*d)//S)
  def fmt(v):return ('-' if v<0 else '')+str(abs(v)//d)+'.'+str(abs(v)%d).zfill(n)
  return [fmt(l),fmt(u)]
def sincos_small(x):
 x=I(x);assert max(abs(x.l),abs(x.u))<=S//1000
 sn=sum(((-1)**k)*x**(2*k+1)/factorial(2*k+1) for k in range(6))
 cs=sum(((-1)**k)*x**(2*k)/factorial(2*k) for k in range(6))
 es=F(1,1000)**13/factorial(13);ec=F(1,1000)**12/factorial(12)
 return sn+I(-es,es),cs+I(-ec,ec)
def log_scalar(x):
 x=F(x)
 if x<=0:raise ValueError('NONPOSITIVE_LOG')
 k=0
 while x>=2:x/=2;k+=1
 while x<1:x*=2;k-=1
 def atanh_log(v):
  y=(I(v)-1)/(I(v)+1);out=I(0);power=y;yy=y*y
  for j in range(160):out+=2*power/(2*j+1);power*=yy
  # 0<=y<=1/3, geometric remainder independent of rounded power.
  tail=2*F(1,3)**321/(321*(1-F(1,9)))
  return out+I(0,tail)
 return atanh_log(x)+k*atanh_log(F(2))
def log(x):
 x=I(x);a=log_scalar(F(x.l,S));b=log_scalar(F(x.u,S));return I.raw(a.l,b.u)
def db(x):return -10*log(I(x)/2)/log(I(10))
