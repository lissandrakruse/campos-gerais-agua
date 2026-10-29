#!/usr/bin/env python3
"""Descriptive weighting audit; no causal/predictive inference or observed denominators."""
import argparse,csv,hashlib,json,statistics
from collections import defaultdict
from pathlib import Path
METRICS=['ssc_med_difference_pct','ssc_max_difference_pct','trv_difference_pct','tsy_difference_pct']
def weighted_mean(v,w):return sum(x*y for x,y in zip(v,w))/sum(w)
def box_extrema(v,k):
    """Exact fractional-linear extrema for independently bounded positive weights [1,k].
    An optimum has boundary weights; ordered thresholds suffice by exchange argument.
    Endpoints allowing all 1/all k include the constant-weight case.
    """
    if k<1:raise ValueError('k must be >= 1')
    s=sorted(v);n=len(s)
    lo=min(weighted_mean(s,[k if i<j else 1 for i in range(n)]) for j in range(n+1))
    hi=max(weighted_mean(s,[1 if i<j else k for i in range(n)]) for j in range(n+1))
    return lo,hi

def analyze(path,out):
    raw=path.read_bytes();rows=list(csv.DictReader(raw.decode().splitlines()))
    groups=defaultdict(list)
    for r in rows:groups[r['event_date']].append(r)
    summaries=[];lodo=[];bounds=[];date_rows=[]
    for m in METRICS:
        v=[float(r[m]) for r in rows]
        dm={d:statistics.mean(float(r[m]) for r in rr) for d,rr in groups.items()}
        for d,x in dm.items():date_rows.append({'metric':m,'date':d,'record_count':len(groups[d]),'within_date_mean_pct':x})
        p=sum(x for x in v if x>0);a=-sum(x for x in v if x<0)
        for d in sorted(groups):
            kept=[float(r[m]) for r in rows if r['event_date']!=d]
            lodo.append({'metric':m,'excluded_date':d,'remaining_records':len(kept),'row_mean_pct':statistics.mean(kept),'row_median_pct':statistics.median(kept),'date_balanced_mean_pct':statistics.mean(x for dd,x in dm.items() if dd!=d)})
        lm=[x for x in lodo if x['metric']==m]
        summaries.append({'metric':m,'n_records':len(v),'n_dates':len(dm),'n_positive':sum(x>0 for x in v),'n_negative':sum(x<0 for x in v),'row_mean_pct':statistics.mean(v),'row_median_pct':statistics.median(v),'date_balanced_mean_pct':statistics.mean(dm.values()),'date_balanced_median_pct':statistics.median(dm.values()),'date_minus_row_mean_pp':statistics.mean(dm.values())-statistics.mean(v),'lodo_row_mean_min_pct':min(x['row_mean_pct'] for x in lm),'lodo_row_mean_max_pct':max(x['row_mean_pct'] for x in lm),'unknown_weight_closure_min_pct':min(v) if m.startswith(('trv','tsy')) else None,'unknown_weight_closure_max_pct':max(v) if m.startswith(('trv','tsy')) else None,'denominator_ratio_sign_threshold':p/a if a and m=='tsy_difference_pct' else None})
        for k in ([1,2,5,6,10,100] if m.startswith(('trv','tsy')) else []):
            lo,hi=box_extrema(v,k);bounds.append({'metric':m,'assumed_max_to_min_denominator_ratio':k,'lower_weighted_contrast_pct':lo,'upper_weighted_contrast_pct':hi,'interpretation':'hypothetical independently bounded denominators; not estimated physical values'})
    witnesses=[]
    for scenario in ['equal','negative_tsy_weight_6']:
        for r in rows:
            d=float(r['tsy_difference_pct']);a=6.0 if scenario=='negative_tsy_weight_6' and d<0 else 1.0
            witnesses.append({'scenario':scenario,'source_row':r['source_row'],'event_date':r['event_date'],'reported_tsy_contrast_pct':d,'constructed_nt_arbitrary_units':a,'constructed_terraced_arbitrary_units':a*(1-d/100),'status':'constructed compatibility witness, NOT observed sediment yields'})
    witness_summaries=[]
    for scenario in ['equal','negative_tsy_weight_6']:
        rr=[r for r in witnesses if r['scenario']==scenario];a=sum(r['constructed_nt_arbitrary_units'] for r in rr);b=sum(r['constructed_terraced_arbitrary_units'] for r in rr)
        witness_summaries.append({'scenario':scenario,'constructed_pooled_contrast_pct':100*(a-b)/a,'recovered_percentages_max_absolute_error':max(abs(100*(r['constructed_nt_arbitrary_units']-r['constructed_terraced_arbitrary_units'])/r['constructed_nt_arbitrary_units']-r['reported_tsy_contrast_pct']) for r in rr)})
    out.mkdir(parents=True,exist_ok=True)
    for name,data in [('metric_sensitivity.csv',summaries),('leave_one_date_out.csv',lodo),('date_balanced_inputs.csv',date_rows),('denominator_bound_scenarios.csv',bounds),('constructed_tsy_witnesses.csv',witnesses)]:
        target = out / ('constructed_scenarios' if name in ['denominator_bound_scenarios.csv','constructed_tsy_witnesses.csv'] else 'published_descriptions') / name
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator="\n");w.writeheader();w.writerows(data)
    result={'source_sha256':hashlib.sha256(raw).hexdigest(),'source_doi':'10.1007/s11368-026-04517-0','records':len(rows),'dates':len(groups),'same_date_multiple_records':{d:len(rr) for d,rr in groups.items() if len(rr)>1},'metrics':summaries,'constructed_witness_summary':witness_summaries,'scope':'Published rounded contrasts, selected records at one paired site; no p-values, confidence intervals, generalization or observed absolute denominators.'}
    (out/'sensitivity_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();print(json.dumps(analyze(a.input,a.out),indent=2))
