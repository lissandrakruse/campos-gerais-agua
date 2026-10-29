"""Reproducibility/geometry checks on this fixed pilot; no statistical validation claim."""
import json,hashlib,csv
from pathlib import Path
import numpy as np,rasterio
from netCDF4 import Dataset
R=Path(__file__).parent;O=R/'comparison';m=json.load(open(O/'comparison_metrics.json'))
def read(n):
 with rasterio.open(O/(n+'.tif')) as s:return s.read(1),s.transform,s.crs
wf,t,c=read('swot_water_fraction');q,_,_=read('swot_water_area_quality');cov,_,_=read('sentinel_valid_coverage');op,_,_=read('sentinel_mndwi_water_fraction');delta,_,_=read('exploratory_difference')
assert c.to_epsg()==32722 and t.a==100 and t.e==-100
assert wf.shape==(55,51) and np.isfinite(wf).sum()==508
assert ((q==0)&np.isfinite(wf)).sum()==0
mask=np.isfinite(delta)
assert mask.sum()==495 and np.all(cov[mask]>=.8) and np.all(q[mask]==1)
assert np.allclose(delta[mask],wf[mask]-op[mask],atol=1e-7)
assert np.isclose(np.mean(abs(delta[mask])),m['sensitivity_quality_le1']['mae_fraction'])
assert np.all((op[np.isfinite(op)]>=0)&(op[np.isfinite(op)]<=1))
assert np.sum(wf[mask]<0)==39
with Dataset(R/'input/swot_055F_20250616.nc') as d:
 ix=int(np.where(d['x'][:]==t.c+50)[0][0]);iy=int(np.where(d['y'][:]==t.f-50)[0][0])
 native=np.ma.filled(d['water_frac'][iy-54:iy+1,ix:ix+51],np.nan)[::-1,:]
 assert np.allclose(wf,native,equal_nan=True)
with open(O/'paired_cells.csv','w') as f:
 w=csv.writer(f);w.writerow(['row','col','easting_m','northing_m','water_area_quality','optical_valid_fraction','swot_water_fraction','optical_threshold_fraction','swot_minus_optical'])
 for row,col in zip(*np.where(mask)):
  w.writerow([int(row),int(col),t.c+(col+.5)*100,t.f-(row+.5)*100,int(q[row,col]),float(cov[row,col]),float(wf[row,col]),float(op[row,col]),float(delta[row,col])])
files={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in O.iterdir() if p.suffix in ['.tif','.png','.csv','.json'] and p.name!='output_manifest.json'}
(O/'output_manifest.json').write_text(json.dumps({'checks_passed':10,'artifacts':files},indent=2)+'\n')
print('PASS: 10 geometry, missingness, count and metric checks; paired_cells.csv and hashes written')
