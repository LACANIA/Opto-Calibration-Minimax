"""Regenerate the primary numerical quantities from the fixed theoretical inputs."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,argparse
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'src'))
from exact_interval import I,db
ap=argparse.ArgumentParser()
ap.add_argument('--output',type=Path,default=P/'reproduced/tables')
args=ap.parse_args();out=args.output
if out.exists() and any(out.iterdir()):ap.error('OUTPUT_DIRECTORY_NOT_EMPTY')
spec=json.loads((P/'inputs/spec.json').read_text())
expected=json.loads((P/'records/limit_02/numerical_certificate.json').read_text())
rows=[]
for qs in spec['Q_checks']:
    q=F(qs);r=q*q;eps=r/(1+r)**2;qi=I(q);k=1+qi**2
    a=(k*(1+qi)-(k**2-2*qi**2*(qi+2)).sqrt())/(qi+2)
    vf=a**2;va=I(2*q**3)
    rows.append(dict(Q=qs,epsilon0_exact=str(eps),epsilon0_display=I(eps).decimal(18),V_epsilon_exact=str(2*q**3),A_epsilon_db=db(va).encoded(),A_epsilon_display=db(va).decimal(15),V_fixed=vf.encoded(),A_fixed_db=db(vf).encoded(),A_fixed_display=db(vf).decimal(15)))
assert rows==expected['rows'],'PRIMARY_ROWS_DIFFER'
Q=F(spec['main']['Q']);epsilon=F(spec['main']['epsilon']);eta=F(spec['main']['eta_rad'])
qi=I(Q);k=1+qi**2;a=(k*(1+qi)-(k**2-2*qi**2*(qi+2)).sqrt())/(qi+2);vf=a**2
assert Q==F(1,100) and eta==F(1,1000),'FIXED_MAIN_EXAMPLE_REQUIRED'
B=2*(F(1,1000)+2*eta)**2
generic=((2*qi**3).sqrt()+2*I(2).sqrt()*I(eta))**2
main=dict(Q=str(Q),epsilon=str(epsilon),eta=str(eta),epsilon0=str(Q*Q/(1+Q*Q)**2),T_error_upper_exact=str(B),T_error_upper_display=I(B).decimal(18),A_policy_lower_expression='-10 log10(9/1000000)',A_policy_bound=db(I(B)).encoded(),A_policy_display=db(I(B)).decimal(15),fixed_global_A_upper=db(vf).encoded(),fixed_global_A_upper_display=db(vf).decimal(15),certified_advantage_db=(db(I(B))-db(vf)).encoded(),certified_advantage_display=(db(I(B))-db(vf)).decimal(15),Vfixed_over_policy_bound=(vf/I(B)).encoded(),comparison_direction='actual policy worst attenuation >= A_policy_bound; optimal fixed with same angle error <= A_fixed(no error)',general_norm_formula=generic.encoded())
assert main==expected['main'],'PRIMARY_MAIN_QUANTITIES_DIFFER'
out.mkdir(parents=True,exist_ok=True)
result={'rows':rows,'main':main,'arithmetic':{'decimal_digits':70,'log_terms':160},'saved_primary_quantities_match':True,'scope':'numerical table regeneration, not a rerun of all historical auxiliary controls'}
(out/'numerical_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','rows':len(rows),'primary_records_match':True,'output':str(out)},indent=2))
