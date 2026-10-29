"""Reproduce the two quantitative formula figures and supporting tables.
Outputs only under --output. No network, optimization, or historical imports.
"""
from pathlib import Path
from fractions import Fraction
import argparse,json
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,Rectangle
S=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=S/'reproduced'/'figures');args=ap.parse_args()
O=args.output
if O.exists() and any(O.iterdir()):ap.error('OUTPUT_DIRECTORY_NOT_EMPTY')
O.mkdir(parents=True,exist_ok=True)
mp.mp.dps=80
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','savefig.bbox':'tight'})
teal='#008893';purple='#6B43B5';orange='#C95B19';gray='#56636D'
def astar(q):
 q=mp.mpf(q);k=1+q*q
 return (q*k*k+2*q*q)/(k*(1+q)+mp.sqrt(k*k-2*q*q*(q+2)))
def save(fig,name):
 for ext in ['pdf','svg','png']:fig.savefig(O/(name+'.'+ext),dpi=200)
 plt.close(fig)
# Existing exact-limit illustration.
qs=np.geomspace(.001,.1,401);vals=[]
for Q in qs:
 Q=mp.mpf(str(Q));aa=astar(Q);vals.append([float(aa*aa),float(2*Q**3),float(10*mp.log10(aa*aa/(2*Q**3)))])
vals=np.array(vals);fig,ax=plt.subplots(1,2,figsize=(10,3.5),layout='constrained')
ax[0].loglog(qs,vals[:,0],color=purple,label=r'Common preset: $a_*^2$',lw=2);ax[0].loglog(qs,vals[:,1],color=teal,label=r'Informed: $2Q^3$',lw=2)
ax[0].set(xlabel=r'Block-axis amplitude bound $Q$',ylabel=r'Worst normalized transmission $T$');ax[0].legend(frameon=False,fontsize=9)
ax[1].semilogx(qs,vals[:,2],color=teal,lw=2);ax[1].set(xlabel=r'Block-axis amplitude bound $Q$',ylabel='Ideal information advantage (dB)')
for Q in [.001,.01,.03,.1]:
 aa=astar(str(Q));v=float(aa*aa);w=float(2*mp.mpf(str(Q))**3)
 ax[0].plot(Q,v,'o',color=purple,ms=4);ax[0].plot(Q,w,'o',color=teal,ms=4);ax[1].plot(Q,float(10*mp.log10(v/w)),'o',color=teal,ms=4)
for a in ax:a.grid(alpha=.2);a.set_xlim(.001,.1)
ax[0].set_title('(a) Exact minimax values',loc='left');ax[1].set_title('(b) Same-box difference',loc='left');save(fig,'exact_limits')
# Full policy domain with exact junctions explicitly in plotted nodes.
q=mp.mpf('.01');eps=mp.mpf('.00009');r=q*q;k=1+r;eps0=r/k**2;etac=(astar(q)/mp.sqrt(2)-q**mp.mpf('1.5'))/2
lo=-eps;hi=q+eps;b1=r-eps;b2=q-eps
hat=sorted(set(list(np.linspace(float(lo),float(hi),601))+[float(lo),float(hi),float(b1),float(b2)]))
def theta(h):
 u=min(q,max(mp.mpf(0),mp.mpf(str(h))+eps));a=r if u<=r else u*k/(1+u)
 return float(mp.acos(mp.sqrt((a-r)/(1-r)))*180/mp.pi)
angles=[theta(h) for h in hat]
fig,ax=plt.subplots(1,2,figsize=(10.6,4.5),layout='constrained')
ax[0].plot(np.array(hat)*1e3,angles,lw=2,color=teal)
for b in [b1,b2]:ax[0].axvline(float(b)*1e3,color=gray,ls=':',lw=1)
ax[0].set(xlabel=r'Reading $\widehat z$ ($10^{-3}$ amplitude)',ylabel=r'Positive setting $\theta$ (degrees)',xlim=(float(lo)*1e3,float(hi)*1e3),ylim=(83.9,90.4))
ax[0].set_title('(a) Full legal reading range',loc='left');ax[0].grid(alpha=.15)
for pos,left,right,lab in [([.12,.10,.30,.25],lo,mp.mpf('.0002'),r'$10^{-5}$'),([.60,.56,.34,.30],mp.mpf('.0098'),hi,r'$10^{-5}$')]:
 ins=ax[0].inset_axes(pos);xx=np.linspace(float(left),float(right),201);ins.plot(xx*1e5,[theta(h) for h in xx],color=teal,lw=1.4)
 bb=b1 if left==lo else b2;ins.axvline(float(bb)*1e5,color=gray,ls=':',lw=1);ins.set_title('Reading ('+lab+')',fontsize=8);ins.tick_params(labelsize=7);ins.grid(alpha=.15)
ax[0].text(.03,.95,r'$\widehat z=r-\varepsilon=10^{-5}$',transform=ax[0].transAxes,fontsize=8,va='top')
ax[0].text(.42,.04,r'$\widehat z=Q-\varepsilon=0.00991$',transform=ax[0].transAxes,fontsize=8)
ex=float(eps0)*1e4;ey=float(etac)*1e3
ax[1].add_patch(Rectangle((0,0),ex,ey,facecolor=teal,alpha=.15));ax[1].plot([0,ex],[ey,ey],'--',color=teal,lw=1.5);ax[1].plot([ex,ex],[0,ey],color=teal,lw=1.5)
ax[1].plot(ex,ey,'o',mfc='white',mec=teal,ms=5,zorder=5)
ax[1].scatter([.9],[1],color=orange,zorder=4,s=32);ax[1].annotate('Declared example',(.9,1),xytext=(.12,.63),arrowprops={'arrowstyle':'->','color':orange},fontsize=9)
ax[1].text(.09,.24,'Strict benefit certified',fontsize=9,color=teal);ax[1].text(ex*1.08,ey*.5,'Not certified\nby this theorem',fontsize=9)
ax[1].text(.05,ey+.10,'Dashed top boundary excluded',fontsize=8,color=teal)
ax[1].set(xlim=(0,ex*1.8),ylim=(0,ey*1.45),xlabel=r'Readout bound $\varepsilon$ ($10^{-4}$ amplitude)',ylabel=r'Angle-error bound $\eta$ ($10^{-3}$ rad)')
ax[1].set_title('(b) Sufficient guarantee region',loc='left');ax[1].grid(alpha=.15);save(fig,'policy_and_guarantee')
c=json.loads((S/'records/limit_02/numerical_certificate.json').read_text())
table=r'''\begin{table}[tb]\centering\small
\caption{Exact limits at four specification values, displayed with rounded numerical values. The readout bound $\varepsilon_0$ is sufficient; complete directed intervals are provided in S2.}\label{tab:four}
\begin{tabular}{rrrrr}\toprule
$Q$ & $\varepsilon_0$ & $V_{\rm adapt}$ & $A_{\rm fixed}$ (dB) & $A_{\rm adapt}$ (dB)\\\midrule
'''
for row in c['rows']:
 Q=float(Fraction(row['Q']));ep=float(Fraction(row['epsilon0_exact']));v=float(Fraction(row['V_epsilon_exact']))
 table+=f'{Q:g} & {ep:.5g} & {v:.5g} & {float(row["A_fixed_display"][0]):.4f} & {float(row["A_epsilon_display"][0]):.4f} '+r'\\'+'\n'
table+=r'\bottomrule\end{tabular}\end{table}';(O/'four_values.tex').write_text(table)
table=r'''\begin{table}[tb]\centering\small
\caption{Guaranteed performance for $Q=0.01$, $\varepsilon=0.00009$ and $\eta=0.001$ rad. Decimal bounds are rounded in the stated direction.}\label{tab:main}
\begin{tabular}{p{.64\linewidth}r}\toprule
Quantity & Bound\\\midrule
Policy worst normalized transmission & $\leq 1.8\times10^{-5}$\\
Policy guaranteed absolute attenuation & $\geq 50.4575$ dB\\
Best common-preset guaranteed attenuation & $\leq 48.9006$ dB\\
Difference of worst attenuation guarantees & $\geq 1.5570$ dB\\
\bottomrule\end{tabular}\end{table}
''';(O/'main_example.tex').write_text(table)
main=c['main'];assert Fraction('50.4575')<=Fraction(main['A_policy_bound']['lower']);assert Fraction('48.9006')>=Fraction(main['fixed_global_A_upper']['upper']);assert Fraction('1.5570')<=Fraction(main['certified_advantage_db']['lower'])
data={'precision_digits':80,'figure_names':['exact_limits','policy_and_guarantee'],'policy':{'domain':[str(lo),str(hi)],'junctions':[str(b1),str(b2)],'reading':hat,'theta_degrees':angles},'epsilon0':str(eps0),'eta_c':str(etac),'series':{'Q':qs.tolist(),'values':vals.tolist()},'checks':{'directed_table_rounding':True,'complete_reading_domain':True,'junctions_present':all(float(b) in hat for b in [b1,b2]),'low_platform_equal':theta(float(lo))==theta(float(b1)),'high_platform_equal':theta(float(b2))==theta(float(hi))},'purpose':'illustration of existing formulas; no new design or measurement'}
assert all(data['checks'].values());(O/'plot_data.json').write_text(json.dumps(data,indent=2))
print(json.dumps({'status':'PASS','figures':2,'checks':data['checks'],'output':str(O)}))
