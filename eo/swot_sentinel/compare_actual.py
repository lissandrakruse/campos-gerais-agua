"""Actual native-grid SWOT/Sentinel comparison; no authentication required for local inputs."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/mpl_compare')
from pathlib import Path
import json,hashlib
import numpy as np
from netCDF4 import Dataset
import rasterio
from rasterio.warp import transform_bounds,reproject,Resampling
from rasterio.transform import from_origin
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).parent; OUT=ROOT/'comparison';OUT.mkdir(exist_ok=True)
S2=ROOT/'kaggle_outputs_v2/sentinel/S2B_22JET_20250617_0_L2A'
SW=ROOT/'input/swot_055F_20250616.nc'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def serial(x):
 if isinstance(x,np.ndarray):return x.tolist()
 if isinstance(x,np.generic):return x.item()
 return x
with Dataset(SW) as d:
 x=np.asarray(d['x'][:]);y=np.asarray(d['y'][:]);b=transform_bounds('EPSG:4326','EPSG:32722',-50.07,-25.12,-50.02,-25.07)
 ix=np.where((x>=b[0])&(x<=b[2]))[0];iy=np.where((y>=b[1])&(y<=b[3]))[0];xs=x[ix];ys=y[iy][::-1]
 tx=from_origin(xs[0]-50,ys[0]+50,100,100);shape=(len(ys),len(xs))
 def read(k):return np.ma.filled(d[k][iy[0]:iy[-1]+1,ix[0]:ix[-1]+1].astype('float64'),np.nan)[::-1,:]
 wf=read('water_frac');qual=read('water_area_qual');unc=read('water_frac_uncert');bits=read('water_area_qual_bitwise')
 flags={n:int(np.sum((bits[np.isfinite(wf)].astype('uint32')&m)>0)) for n,m in zip(d['water_area_qual_bitwise'].flag_meanings.split(),d['water_area_qual_bitwise'].flag_masks)}
 attrs={k:serial(v) for k,v in d.__dict__.items() if not k.startswith('xref')}
with rasterio.open(S2/'mndwi.tif') as s:
 index=s.read(1);valid=np.isfinite(index);src_tx=s.transform;src_crs=s.crs;sb=s.bounds
 def agg(a):
  dst=np.full(shape,np.nan,dtype='float32');reproject(a.astype('float32'),dst,src_transform=src_tx,src_crs=src_crs,dst_transform=tx,dst_crs='EPSG:32722',dst_nodata=np.nan,resampling=Resampling.average);return dst
 coverage=agg(valid)
 # Exclude partial edge cells because averaging excludes beyond-source pixels.
 full=(xs[None,:]-50>=sb.left)&(xs[None,:]+50<=sb.right)&(ys[:,None]-50>=sb.bottom)&(ys[:,None]+50<=sb.top)
 coverage=np.where(full,coverage,np.nan)
 fractions={str(t):np.divide(agg(valid&(index>t)),coverage,out=np.full(shape,np.nan,dtype='float32'),where=coverage>0) for t in [-.1,0.,.1]}
 optical=fractions['0.0'];mutual=np.isfinite(wf)&np.isfinite(optical)&(coverage>=.8)
 strict=mutual&(qual==0);suspect=mutual&(qual<=1)
 def metric(mask,opt):
  a=wf[mask];z=opt[mask];delta=a-z
  return {'n':int(mask.sum()),'mae_fraction':float(np.mean(abs(delta))) if len(a) else None,'mean_difference_swot_minus_optical_fraction':float(np.mean(delta)) if len(a) else None,'rmse_fraction':float(np.sqrt(np.mean(delta**2))) if len(a) else None,'pearson_r':float(np.corrcoef(a,z)[0,1]) if len(a)>2 and np.std(a)>0 and np.std(z)>0 else None,'swot_mean_fraction':float(a.mean()) if len(a) else None,'optical_mean_fraction':float(z.mean()) if len(a) else None,'optical_nonzero_cells':int(np.sum(z>0)),'swot_negative_cells':int(np.sum(a<0))}
 report={'status':'actual_both_sources_processed_strict_primary_no_eligible_cells','aoi_bbox_wgs84':[-50.07,-25.12,-50.02,-25.07],'grid':'native SWOT 100 m EPSG:32722; cells selected by centers inside transformed AOI bounding rectangle','shape_rows_cols':shape,'grid_bounds_utm22s':[tx.c,tx.f-shape[0]*100,tx.c+shape[1]*100,tx.f],'swot_input_sha256':sha(SW),'swot_input_bytes':SW.stat().st_size,'swot_attributes':attrs,'sentinel_manifest_sha256':sha(S2/'manifest.json'),'temporal_separation_hours':17.047184444444444,'swot_finite_water_fraction_cells':int(np.isfinite(wf).sum()),'swot_quality_counts_all_cells':{str(int(q)):int((qual==q).sum()) for q in np.unique(qual[np.isfinite(qual)])},'quality_flags_over_finite_water_fraction_cells':flags,'optical_coverage_ge80_and_complete_cell_count':int(np.sum(coverage>=.8)),'primary_quality0':metric(strict,optical),'sensitivity_quality_le1':metric(suspect,optical),'threshold_sensitivity_quality_le1':{t:metric(suspect,o) for t,o in fractions.items()},'water_fraction_uncertainty_suspect_quantiles_5_50_95':np.quantile(unc[suspect&np.isfinite(unc)],[.05,.5,.95]).tolist(),'limitations':['No good-quality water-fraction cells: strict primary comparison cannot be estimated.','Suspect-only differences are exploratory cross-sensor consistency, not accuracy or agronomic validation.','MNDWI binary threshold fraction is not equivalent to SWOT water-fraction estimator.','Approximately17h temporal mismatch; no independent contemporaneous ground truth.','Negative SWOT fractions retained, not clipped; missing SWOT is never interpreted as zero water.','Fixed context AOI, not surveyed crop plots; no post-hoc geographic expansion.']}
 (OUT/'comparison_metrics.json').write_text(json.dumps(report,indent=2,default=serial)+'\n')
 profile={'driver':'GTiff','height':shape[0],'width':shape[1],'count':1,'dtype':'float32','crs':'EPSG:32722','transform':tx,'nodata':np.nan,'compress':'deflate'}
 for name,a in {'swot_water_fraction':wf,'swot_water_area_quality':qual,'swot_water_fraction_uncertainty':unc,'sentinel_valid_coverage':coverage,'sentinel_mndwi_water_fraction':optical,'exploratory_difference':np.where(suspect,wf-optical,np.nan)}.items():
  with rasterio.open(OUT/(name+'.tif'),'w',**profile) as dst:dst.write(a.astype('float32'),1)
 extent=[tx.c/1000,(tx.c+shape[1]*100)/1000,(tx.f-shape[0]*100)/1000,tx.f/1000]
 fig,axs=plt.subplots(2,2,figsize=(11,9),layout='constrained')
 for ax,a,title,vmin,vmax,cmap in [(axs[0,0],np.where(qual<=1,wf,np.nan),'SWOT water fraction: suspect observations only',0,.65,'Blues'),(axs[0,1],np.where(coverage>=.8,optical,np.nan),'Sentinel-2 MNDWI > 0 fraction (100 m)',0,.65,'Blues'),(axs[1,0],np.where(suspect,wf-optical,np.nan),'Exploratory difference: SWOT minus optical',-.65,.65,'RdBu')]:
  cm=plt.get_cmap('RdBu' if title.startswith('SWOT water fraction') else cmap).copy();cm.set_bad('#bdbdbd');
  from matplotlib.colors import TwoSlopeNorm
  opts={'norm':TwoSlopeNorm(vmin=-.005,vcenter=0,vmax=.65)} if title.startswith('SWOT water fraction') else {'vmin':vmin,'vmax':vmax}
  im=ax.imshow(a,extent=extent,cmap=cm,**opts);cb=fig.colorbar(im,ax=ax,shrink=.8);
  if title.startswith('SWOT water fraction'):cb.set_ticks([-.005,0,.1,.3,.5,.65]);cb.set_label('Signed fraction; asymmetric color scale')
  ax.set_title(title,fontsize=10);ax.set_xlabel('UTM22S easting (km)');ax.set_ylabel('Northing (km)')
 ax=axs[1,1];ax.scatter(optical[suspect],wf[suspect],s=9,alpha=.4);ax.plot([0,.65],[0,.65],'k--',lw=1);ax.set_xlim(-.02,.65);ax.set_ylim(-.02,.65);ax.set_xlabel('Optical threshold-selected fraction');ax.set_ylabel('SWOT estimated water fraction');ax.set_title(f'Suspect-only exploratory pairs: n={suspect.sum()}')
 fig.suptitle('Capão da Onça context pilot: 16–17 June 2025\nStrict good-quality sample n=0; Gray = unavailable/excluded, not dry land',fontsize=12)
 fig.savefig(OUT/'comparison_panels.png',dpi=300);
 titles=['Fração de água SWOT: somente observações suspeitas','Fração óptica MNDWI > 0 (100 m)','Diferença exploratória: SWOT menos óptico',f'Pares exploratórios suspeitos: n={suspect.sum()}']
 for ax,title in zip(axs.flat,titles):ax.set_title(title,fontsize=10)
 for ax in [axs[0,0],axs[0,1],axs[1,0]]:ax.set_xlabel('UTM22S leste (km)');ax.set_ylabel('Norte (km)')
 axs[1,1].set_xlabel('Fração óptica selecionada pelo limiar');axs[1,1].set_ylabel('Fração de água estimada pelo SWOT')
 fig.suptitle('Piloto no entorno de Capão da Onça: 16–17 de junho de 2025\nAmostra principal de boa qualidade n=0; cinza = indisponível/excluído, não solo seco',fontsize=12)
 fig.savefig(OUT/'comparison_panels_pt.png',dpi=300);plt.close(fig)
 print(json.dumps({k:report[k] for k in ['swot_finite_water_fraction_cells','quality_flags_over_finite_water_fraction_cells','primary_quality0','sensitivity_quality_le1','threshold_sensitivity_quality_le1']},indent=2))
