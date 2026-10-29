#!/usr/bin/env python3
"""Extract published derived contrasts, NOT raw runoff, from de Paula et al. S1.
Input: official DOCX; output: sourced CSV and descriptive audit (no inference).
"""
import argparse,csv,datetime,hashlib,json,re,statistics,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
DOI='10.1007/s11368-026-04517-0'
URL='https://media.springernature.com/original/springer-static/esm/art%3A10.1007%2Fs11368-026-04517-0/MediaObjects/11368_2026_4517_MOESM1_ESM.docx'
METRICS=['ssc_med_difference_pct','ssc_max_difference_pct','trv_difference_pct','tsy_difference_pct']
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def extract(path):
 root=ET.fromstring(zipfile.ZipFile(path).read('word/document.xml'))
 tables=root.findall('.//w:tbl',NS)
 assert len(tables)==1, 'Review changed source: expected one table'
 rows=[]
 for tr in tables[0].findall('w:tr',NS)[3:]:
  cells=[''.join(t.itertext()).strip() for t in tr.findall('w:tc',NS)]
  assert len(cells)==5
  label=cells[0];datepart,_,suffix=label.partition('_')
  date=datetime.datetime.strptime(datepart,'%b %d, %Y').date().isoformat()
  row={'source_row':len(rows)+1,'event_label_original':label,'event_date':date,'event_suffix':suffix}
  for name,value in zip(METRICS,cells[1:]): row[name]=float(value.replace(',','.'))
  row['source_doi']=DOI;row['source_table']='Supplementary Table S1';rows.append(row)
 assert len(rows)==24
 return rows
def describe(rows):
 dates={r['event_date'] for r in rows}
 out={'n_event_rows':len(rows),'n_distinct_dates':len(dates),'duplicate_full_event_labels':len(rows)-len({r['event_label_original'] for r in rows}), 'multiple_events_same_date':{d:sum(r['event_date']==d for r in rows) for d in sorted(dates) if sum(r['event_date']==d for r in rows)>1},'year_counts':{y:sum(r['event_date'][:4]==y for r in rows) for y in sorted({r['event_date'][:4] for r in rows})},'metrics':{}}
 for m in METRICS:
  a=[r[m] for r in rows];out['metrics'][m]={'n':len(a),'min_pct':min(a),'max_pct':max(a),'median_pct_unweighted':statistics.median(a),'n_negative':sum(x<0 for x in a),'n_zero':sum(x==0 for x in a),'n_positive':sum(x>0 for x in a),'n_equal_100_reported':sum(x==100 for x in a)}
 out['interpretation']='Published rounded relative contrasts only. No absolute runoff volumes, rainfall predictors or sampling denominators. Unweighted descriptions are not pooled reductions, confidence intervals or independent treatment effects. 100% is as reported, not independently verified absence.'
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('docx',type=Path);p.add_argument('--out',type=Path,default=Path('.'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 rows=extract(a.docx)
 with (a.out/'de_paula_2026_s1_derived_event_contrasts.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
 summary=describe(rows);summary['source_sha256']=hashlib.sha256(a.docx.read_bytes()).hexdigest();summary['source_url']=URL
 (a.out/'de_paula_2026_s1_audit.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
