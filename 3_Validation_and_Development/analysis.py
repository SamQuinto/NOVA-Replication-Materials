"""Reproduce NOVA's reported measures from the de-identified pilot data.

No API calls are made. All paths are relative to this file, not to a user's
OneDrive folder. The notebook uses the supplied scoring-review decisions;
it does not ask a model to judge those responses again.
"""
from pathlib import Path
import json,math,collections,re
import numpy as np
import pandas as pd
from scipy import stats
ROOT=Path(__file__).resolve().parent
REQUIRED={'Salary','Personal Budget','Starting Date'}
def read(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))
def wilson(k,n):
    z=stats.norm.ppf(.975);p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return max(0,c-h),min(1,c+h)
def mean_ci(values):
    x=np.array([v for v in values if v is not None and pd.notna(v)],dtype=float);n=len(x)
    if not n:return dict(n=0,mean=None,sd=None,ci_low=None,ci_high=None)
    sd=x.std(ddof=1) if n>1 else None;h=stats.t.ppf(.975,n-1)*sd/math.sqrt(n) if n>1 else float('nan')
    return dict(n=n,mean=x.mean(),sd=sd,ci_low=x.mean()-h,ci_high=x.mean()+h)
def validation():
    usage=pd.DataFrame(read('api_usage.json'));result=[]
    for dataset in ['main','tutorial']:
        book=pd.read_csv(ROOT/'data'/f'{dataset}_review.csv',keep_default_na=False)
        a=next(c for c in book if c.startswith('Type A'));b=next(c for c in book if c.startswith('Type B'))
        for scorer,rows in book.groupby('Scorer Architecture',sort=False):
            assert rows['Offer ID'].is_unique
            assert set(rows[a])<=set(['Y','N']) and set(rows[b])<=set(['Y','N'])
            passed=((rows[a]=='N')&(rows[b]=='N'));k=int(passed.sum());n=len(rows);lo,hi=wilson(k,n)
            u=usage[(usage.dataset==dataset)&(usage.scorer==scorer)]
            assert len(u)==n and set(u.offer_id)==set(rows['Offer ID'])
            result.append(dict(dataset=dataset,scorer=scorer,passed=k,offers=n,accuracy=k/n,ci_low=lo,ci_high=hi,type_a=int((rows[a]=='Y').sum()),type_b=int((rows[b]=='Y').sum()),both=int(((rows[a]=='Y')&(rows[b]=='Y')).sum()),api_cost_per_1000_low=u.cost_lower_usd.mean()*1000,api_cost_per_1000_high=u.cost_upper_usd.mean()*1000,mean_scoring_seconds=u.api_seconds.mean(),calls=int(u.model_calls.sum())))
    return pd.DataFrame(result)
def recompute_behavior():
    records=[];events=[];frequency=collections.defaultdict(lambda:collections.Counter())
    source=read('negotiations.json');sent=read('sent_offers.json')
    for d in source:
        offers=sorted([o for o in sent if o['trial_id']==d['trial_id']],key=lambda o:o['offer_number'])
        latest={};ever=set();last={};explore=introduce=exploit=0;opening=set()
        for j,o in enumerate(offers):
            choices=o['choices'];current=set(choices);before=set().union(*latest.values()) if latest else set();new=current-ever
            def canonical(value):
                text=re.sub(r'\s+',' ',str(value).lower()).strip().replace('$','').replace(',','')
                try:return float(text)
                except ValueError:return text
            revised={k for k,v in choices.items() if k in last and canonical(v)!=canonical(last[k])}
            if j==0:opening=set(current)
            else:explore+=int(current!=before);introduce+=int(bool(new));exploit+=int(bool(revised))
            events.append(dict(trial_id=d['trial_id'],offer_number=o['offer_number'],eligible=j>0,issue_count=len(current),introduction=int(bool(new)) if j else None,exploration=int(current!=before) if j else None,exploitation=int(bool(revised)) if j else None,new_issue_count=len(new) if j else None))
            latest[o['role']]=current;ever|=current;last.update(choices)
        n=len(offers)-1
        row={**d,'offer_count':len(offers),'issue_diversity':len(ever),'nonrequired_issue_diversity':len(ever-REQUIRED),'introduced_issue_after_opening':int(bool(ever-opening)),'new_distinct_issues_after_opening':len(ever-opening),'exploration_rate':explore/n if n else None,'introduction_rate':introduce/n if n else None,'exploitation_rate':exploit/n if n else None,'all_issue_names':sorted(ever)}
        for field in ['offer_count','issue_diversity','nonrequired_issue_diversity','introduced_issue_after_opening']:
            assert row[field]==d[field],(d['trial_id'],field,row[field],d[field])
        records.append(row)
        if d['condition']=='NOVA' and not d['early_quit']:
            for issue in ever-REQUIRED:frequency[issue]['opening' if issue in opening else 'later']+=1
    f=pd.DataFrame([dict(issue=k,opening=v['opening'],introduced_later=v['later'],total=sum(v.values())) for k,v in frequency.items()]).sort_values(['total','issue'],ascending=[False,True])
    return pd.DataFrame(records),pd.DataFrame(events),f
def behavioral_comparisons(dyads):
    result=[];complete=dyads[dyads.early_quit==0]
    measures=['offer_count','issue_diversity','nonrequired_issue_diversity','exploration_rate','introduction_rate','exploitation_rate','negotiation_minutes','preparation_minutes','joint_agreement_points','realized_joint_points']
    for measure in measures:
        groups={c:pd.to_numeric(complete[complete.condition==c][measure],errors='coerce').dropna() for c in ['NOVA','Fixed 9']}
        p=stats.ttest_ind(groups['NOVA'],groups['Fixed 9'],equal_var=False).pvalue
        for c,x in groups.items():result.append(dict(measure=measure,condition=c,**mean_ci(x),p_value=p))
    return pd.DataFrame(result)
def agreement_rates(dyads):
    result=[]
    for population,df in [('Valid reciprocal negotiations',dyads),('Completed negotiations',dyads[dyads.early_quit==0])]:
        counts=[(int(g.agreement.sum()),len(g)-int(g.agreement.sum())) for _,g in df.groupby('condition')]
        p=stats.fisher_exact(counts).pvalue
        for c,g in df.groupby('condition'):
            k=int(g.agreement.sum());n=len(g);lo,hi=wilson(k,n);result.append(dict(population=population,condition=c,agreements=k,negotiations=n,rate=k/n,ci_low=lo,ci_high=hi,p_value=p))
    return pd.DataFrame(result)
def rating(v):
    if v is None:return None
    freq={'Never':1,'Rarely':2,'Occasionally':3,'Frequently':4,'Very frequently':5}
    if v in freq:return freq[v]
    import re
    m=re.match(r'^\s*([1-7])\b',str(v));return float(m[1]) if m else None
def average(a):
    a=[x for x in a if x is not None];return sum(a)/len(a) if a else None
def surveys():
    people=[]
    labels={'subjective_value':'Subjective value (Q1–Q16)','creative_engagement':'Creative engagement (Q20–Q24)','creative_confidence':'Creative confidence (Q25–Q27)','realism':'Q18: The negotiation was realistic','role_imagination':'Q17: Imagine being in the role','role_seriousness':'Q19: Took the role seriously','felt_stuck':'Q29: Felt stuck at least once (not a validated impasse measure)'}
    schema=json.loads((ROOT.parent/'2_Exercise_Materials/questionnaires/Post_Negotiation_Analysis_Schema.json').read_text(encoding='utf-8'))
    questions=schema.get('questions',[])
    if isinstance(questions,list):labels.update({q['id']:q['id'].upper()+': '+q.get('label','') for q in questions})
    for r in read('post_negotiation_responses.json'):
        answers=r['responses'];q={i:rating(answers.get('q'+str(i))) for i in range(1,28)}
        for i in [3,5]:q[i]=8-q[i] if q[i] is not None else None
        p={k:r[k] for k in ['trial_id','pilot','condition','role']}
        p.update(subjective_value=average([q[i] for i in range(1,17)]),creative_engagement=average([q[i] for i in range(20,25)]),creative_confidence=average([q[i] for i in range(25,28)]),realism=q[18],role_imagination=q[17],role_seriousness=q[19])
        p['felt_stuck']=None if 'q29' not in answers else float(str(answers['q29']).lower().startswith('yes'))
        for i in range(1,28):p['q'+str(i)]=q[i]
        people.append(p)
    people=pd.DataFrame(people);measures=['subjective_value','creative_engagement','creative_confidence','realism','role_imagination','role_seriousness','felt_stuck']+['q'+str(i) for i in range(1,28)]
    # Both people must answer a measure; compare dyad means to avoid treating
    # two partners as independent observations.
    paired=people.groupby(['trial_id','condition'])[measures].agg(['mean','count'])
    rows=[]
    for measure in measures:
        samples={}
        for c in ['NOVA','Fixed 9']:
            g=paired.xs(c,level='condition');samples[c]=g.loc[g[(measure,'count')]==2,(measure,'mean')]
        p=stats.ttest_ind(samples['NOVA'],samples['Fixed 9'],equal_var=False).pvalue
        for c,x in samples.items():rows.append(dict(measure=labels.get(measure,measure),condition=c,**mean_ci(x),p_value=p))
    return people,pd.DataFrame(rows)
def figures(dyads,frequency):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'normal','savefig.facecolor':'white'})
    out=ROOT/'figures';out.mkdir(exist_ok=True)
    nova=dyads[(dyads.condition=='NOVA')&(dyads.early_quit==0)]
    fig,ax=plt.subplots(figsize=(6.4,4.2));x=nova.issue_diversity
    ax.hist(x,bins=np.arange(x.min()-.5,x.max()+1.5),color='#ccc',edgecolor='black',linewidth=1)
    ax.set(xlabel='Number of distinct issues per negotiation',ylabel='Number of negotiations',xticks=np.arange(x.min(),x.max()+1));ax.yaxis.get_major_locator().set_params(integer=True);fig.tight_layout();fig.savefig(out/'Issue_Diversity.png',dpi=250);fig.savefig(out/'Issue_Diversity.svg');plt.close(fig)
    hidden={'Remote Working Days','Vacation Days','Probation Length','Contract Length'}
    labels={'Remote Working Days':'Remote working days','Vacation Days':'Vacation days','Professional Training Program':'Professional development or training','Role in Recruitment Fair':'Recruitment-fair assistance'}
    f=frequency.iloc[::-1];fig,ax=plt.subplots(figsize=(8.6,7.4));y=np.arange(len(f))
    ax.barh(y,f.opening,color='white',edgecolor='black',label='In opening offer',linewidth=.8)
    ax.barh(y,f.introduced_later,left=f.opening,color='#999',edgecolor='black',label='Introduced after opening offer',linewidth=.8)
    ax.set_yticks(y,[labels.get(s,s)+('*' if s in hidden else '') for s in f.issue]);ax.tick_params(axis='y',length=0)
    for i,v in enumerate(f.total):ax.text(v+.25,i,str(v),va='center',fontsize=11)
    ax.set_xlabel('Number of negotiations');ax.set_xlim(0,max(f.total)+3);ax.xaxis.get_major_locator().set_params(integer=True)
    ax.legend(loc='upper left',bbox_to_anchor=(0,-.1),frameon=False,fontsize=11)
    fig.text(.02,.015,'* Issues made explicit to one party only',fontsize=11);fig.subplots_adjust(left=.43,right=.96,top=.98,bottom=.17)
    fig.savefig(out/'Nonrequired_Issues.png',dpi=250);fig.savefig(out/'Nonrequired_Issues.svg');plt.close(fig)
def reproduction_checks(v,d):
    n=d[(d.condition=='NOVA')&(d.early_quit==0)]
    assert len(n)==38;assert n.introduced_issue_after_opening.sum()==22
    assert abs(n.nonrequired_issue_diversity.mean()-3.736842105263158)<1e-12
    expected={('main','A1-low'):1224,('main','A1-high'):1225,('main','A2'):1225,('tutorial','A1-low'):731,('tutorial','A1-high'):731,('tutorial','A2'):640}
    for _,r in v.iterrows():assert r.passed==expected[(r.dataset,r.scorer)]
    return pd.DataFrame([{'check':'Main and tutorial accuracy counts','result':'Match reviewed workbook'}, {'check':'Completed NOVA negotiations','result':'38'}, {'check':'Mean additional issues','result':f'{n.nonrequired_issue_diversity.mean():.6f}'}, {'check':'New issues after opening','result':'22/38'}, {'check':'Coffee scoring-table entry','result':'Absent from frozen 215-issue snapshot; manuscript statement about a later addition is not reproduced here.'}, {'check':'Agreement eligibility','result':'Analysis uses both scores >= 0. Historical JSON includes contradictory legacy > 0 metadata; it is preserved as a snapshot.'}, {'check':'Primary accuracy scope','result':'Type A and Type B. Historical option-mapping flags are not independently verified by this measure.'}])
def main():
    v=validation();d,e,f=recompute_behavior();people,s=surveys();figures(d,f)
    outputs={'Accuracy_and_Costs.csv':v,'Behavioral_Comparisons.csv':behavioral_comparisons(d),'Agreement_Rates.csv':agreement_rates(d),'Survey_Comparisons.csv':s,'Issue_Frequency.csv':f,'Recomputed_Offer_Events.csv':e,'Reproduction_Checks.csv':reproduction_checks(v,d)}
    for name,frame in outputs.items():frame.to_csv(ROOT/'results'/name,index=False)
    return outputs
if __name__=='__main__':
    (ROOT/'results').mkdir(exist_ok=True);main();print('Analysis complete. Results and figures saved; no API calls made.')
