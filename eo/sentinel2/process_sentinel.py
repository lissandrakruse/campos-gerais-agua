"""Clip public Sentinel-2 L2A COGs; exploratory water indices, not field truth."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/matplotlib_satellite')
import json, argparse, hashlib, math, datetime
from pathlib import Path
import numpy as np
import rasterio
from rasterio.windows import from_bounds, Window
from rasterio.warp import transform_bounds,reproject,Resampling
from rasterio.transform import from_origin
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(item_id,bbox):
 root=Path(__file__).parent
 items=json.load(open(root/'catalog_2025.json'))['features']
 item=next(x for x in items if x['id']==item_id)
 out=root/item_id;out.mkdir(exist_ok=True)
 (out/'stac_item.json').write_text(json.dumps(item,indent=2))
 crs='EPSG:32722';bb=transform_bounds('EPSG:4326',crs,*bbox)
 left,bottom,right,top=[math.floor(bb[0]/20)*20,math.floor(bb[1]/20)*20,math.ceil(bb[2]/20)*20,math.ceil(bb[3]/20)*20]
 width,height=int(round((right-left)/20)),int(round((top-bottom)/20));tx=from_origin(left,top,20,20)
 profile={'driver':'GTiff','height':height,'width':width,'count':1,'crs':crs,'transform':tx,'compress':'deflate'}
 arrays={};manifest={'item_id':item_id,'datetime':item['properties']['datetime'],'aoi_bbox_wgs84':bbox,'output_bounds_utm22s':[left,bottom,right,top],'grid_resolution_m':20,'assets':{},'method':{'reflectance':'EarthSearch harmonized COG: boa_offset_applied=true so effective offset=0, scale=0.0001; conflicting declared offset retained for audit; v1 superseded','resampling':'10m reflectance averaged to 20m; 20m SWIR nearest for alignment; SCL nearest','mask':'SCL 4,5,6 only; excludes shadow/cloud/snow/unclassified/dark/notdata','classification':'MNDWI>0 illustrative unvalidated threshold; not ground truth'},'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',CPL_VSIL_CURL_ALLOWED_EXTENSIONS='.tif',GDAL_HTTP_TIMEOUT='120'):
  for name in ['green','nir','swir16','scl','red','blue']:
   a=item['assets'][name];url=a['href'];print('READ',name,url,flush=True)
   with rasterio.open(url) as src:
    win=from_bounds(left,bottom,right,top,src.transform).round_offsets().round_lengths()
    raw=src.read(1,window=win,boundless=False)
    meta=a.get('raster:bands',[{}])[0];scale=meta.get('scale',1);declared_offset=meta.get('offset',0);offset=0 if name!='scl' and item['properties'].get('earthsearch:boa_offset_applied') is True else declared_offset
    srcarr=raw.astype('float32')
    srcarr[raw==0]=np.nan
    if name!='scl':srcarr=srcarr*scale+offset
    dst=np.full((height,width),np.nan,dtype='float32')
    reproject(srcarr,dst,src_transform=src.window_transform(win),src_crs=src.crs,dst_transform=tx,dst_crs=crs,src_nodata=np.nan,dst_nodata=np.nan,resampling=Resampling.nearest if name=='scl' or src.res[0]>=20 else Resampling.average)
    arrays[name]=dst
    p=out/(name+'.tif')
    with rasterio.open(p,'w',**profile,dtype='float32',nodata=np.nan) as d:d.write(dst,1)
    manifest['assets'][name]={'source':url,'source_resolution_m':list(src.res),'scale':scale,'effective_offset':offset,'declared_stac_offset':declared_offset,'clip_sha256':sha(p)}
 valid=np.isin(arrays['scl'],[4,5,6])
 for name,a,b in [('ndwi','green','nir'),('mndwi','green','swir16')]:
  denom=arrays[a]+arrays[b]
  z=np.where(valid & np.isfinite(denom)&(denom>1e-6),(arrays[a]-arrays[b])/denom,np.nan).astype('float32')
  arrays[name]=z
  with rasterio.open(out/(name+'.tif'),'w',**profile,dtype='float32',nodata=np.nan) as d:d.write(z,1)
 manifest['qa']={'band_percentiles_0_5_50_95_100':{k:[float(v) for v in np.nanpercentile(arrays[k],[0,5,50,95,100])] for k in ['green','nir','swir16','red','blue']},'index_valid_counts':{k:int(np.isfinite(arrays[k]).sum()) for k in ['ndwi','mndwi']},'total_pixels':width*height,'valid_scl_pixels':int(valid.sum()),'valid_fraction':float(valid.mean()),'scl_counts':{str(int(k)):int((arrays['scl']==k).sum()) for k in np.unique(arrays['scl'][np.isfinite(arrays['scl'])])},'mndwi_positive_pixels':int((arrays['mndwi']>0).sum()),'mndwi_positive_area_ha':float((arrays['mndwi']>0).sum()*400/10000),'warning':'Area is exploratory threshold-selected area over whole AOI, not crop-specific or validated flooding.'}
 extent=[left/1000,right/1000,bottom/1000,top/1000]
 fig,ax=plt.subplots(1,3,figsize=(15,5),layout='constrained')
 rgb=np.stack([arrays[x] for x in ['red','green','blue']],axis=-1);rgb=np.clip(rgb/0.25,0,1);rgb[~valid]=0.8
 ax[0].imshow(rgb,extent=extent);ax[0].set_title('Sentinel-2 surface reflectance (RGB)')
 for j,name in enumerate(['ndwi','mndwi'],1):
  im=ax[j].imshow(arrays[name],extent=extent,cmap='BrBG',vmin=-1,vmax=1);ax[j].set_title(name.upper()+' (valid SCL only)');fig.colorbar(im,ax=ax[j],shrink=.75)
 for x in ax:x.set_xlabel('UTM 22S easting (km)');x.set_ylabel('Northing (km)')
 fig.suptitle(item_id+'\nExploratory image analysis; not validated inundation or crop damage')
 fig.savefig(out/'sentinel_preview.png',dpi=180);plt.close(fig)
 manifest['data_attribution']='Contains modified Copernicus Sentinel data [2025]';manifest['calibration_reference']='https://github.com/Element84/earth-search/discussions/26';manifest['metadata_conflict_reference']='https://github.com/Element84/earth-search/issues/71';manifest['all_output_hashes']={p.name:sha(p) for p in out.glob('*') if p.is_file() and p.name!='manifest.json'}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest['qa'],indent=2),flush=True)

if __name__=='__main__':
 run('S2B_22JET_20250617_0_L2A',[-50.07,-25.12,-50.02,-25.07])
