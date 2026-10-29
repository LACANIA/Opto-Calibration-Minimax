"""Reading-only policy. Exact rational parameters; angles specified by cos squared."""
from fractions import Fraction as F
def rational(x):
 if isinstance(x,bool):raise ValueError('BOOLEAN_NOT_PARAMETER')
 try:return F(str(x)) if isinstance(x,float) else F(x)
 except (ValueError,TypeError,OverflowError,ZeroDivisionError) as e:raise ValueError('NONFINITE_OR_INVALID_INPUT') from e
def policy(Q,epsilon,hat_z):
 Q,epsilon,hat_z=map(rational,(Q,epsilon,hat_z))
 if not 0<Q<=F(1,10):raise ValueError('Q_OUTSIDE_PROVED_DOMAIN')
 if epsilon<0:raise ValueError('NEGATIVE_READING_ERROR')
 if not -epsilon<=hat_z<=Q+epsilon:raise ValueError('READING_OUTSIDE_ALLOWED_RANGE')
 r=Q*Q;K=1+r;u=min(Q,max(F(0),hat_z+epsilon))
 a=r if u<=r else u*K/(1+u)
 return dict(Q=Q,epsilon=epsilon,hat_z=hat_z,u=u,a=a,cos2=(a-r)/(1-r),epsilon0=r/K**2,sufficient_condition=epsilon<=r/K**2)
def consistent(Q,epsilon,hat_z,z):
 d=policy(Q,epsilon,hat_z);z=rational(z)
 if not 0<=z<=d['Q'] or abs(d['hat_z']-z)>d['epsilon']:raise ValueError('INCONSISTENT_TRUE_PARAMETER')
 return d
