# Capão da Onça satellite comparison: bounded exploratory pilot

## Scientific question
Do a quality-screened SWOT water-fraction raster and a near-date Sentinel-2 optical water-index mask exhibit spatial consistency in a roughly 5 × 5 km context window near Capão da Onça, Ponta Grossa? This is **not** field-scale runoff validation, irrigation prescription, soil-moisture estimation, or a crop-damage experiment.

## Status and evidence boundary
`candidate_pair.json` describes actual public-catalog granules, not processed SWOT observations. SWOT NetCDF access currently requires an Earthdata-authenticated user download; the existing browser was not signed in. No authentication bypass, account creation, token creation, or TLS-verification disabling was performed. Sentinel processing status must be judged by actual output `manifest.json` and GeoTIFF existence, not the STAC catalog alone.

## Selected pair
SWOT 100 m Raster Version D, cycle 034/pass 227/tile 055F, 2025-06-16 20:26:30 UTC. Sentinel-2B L2A 22JET, 2025-06-17 13:29:20 UTC. Separation about 17.05 h, not simultaneous. The actual CMR polygon contains the context point; neighboring tile 056F was excluded by polygon check even though the point search returned it. Catalog polygons do not guarantee usable science measurements.

## Planned comparison after both data sources are available
1. Read native CRS, coordinate axes, variable units and fill/quality flags from SWOT NetCDF; verify point/AOI intersections and valid-pixel count. Retain provenance and file hashes. Do not infer non-water from missing measurements.
2. Start with `water_area_qual == 0` for `water_frac`; report results allowing suspect quality (`<=1`) separately as sensitivity analysis. Inspect bitwise flags and uncertainty; do not silently cap unusual fraction values. Report WSE only with independent `wse_qual` screening, never compare WSE numerically against NDWI.
3. Use actual Sentinel-2 scaled/offset surface-reflectance B03, B08, B11 and SCL. Mask cloud, cirrus, shadow, snow, no-data and uncertain classification. Preserve per-pixel missingness. Calculate NDWI and MNDWI; MNDWI > 0 is a provisional unvalidated classification, not ground truth. Show alternative thresholds -0.1/0/+0.1 as sensitivity, not post-hoc optimization.
4. Align to the **native SWOT 100 m grid**, aggregating valid 20 m optical pixels to water fraction, with the optical valid-coverage fraction per coarse pixel. Require at least 80% optical valid coverage for the primary comparison, and report retained sample counts. Do not upsample SWOT to pretend 10 m information.
5. Report fraction differences/MAE and scatter only over mutually valid cells; correlation only if enough variation and samples. Compare masks with agreement metrics only after explicit thresholds. Spatial dependence and the 17 h time offset limit inferential claims. Rainfall or operational changes between observations remain unmeasured confounders.
6. If there are too few valid water cells, report non-feasibility for this AOI/date instead of moving the area or inventing comparisons. Additional dates/nearby verified water bodies require an explicit scientific rationale.

## Scale and interpretation
A 100 × 100 m pixel is one hectare nominally. Published experimental plots around 1.5 ha cannot be resolved as independent, pure SWOT sampling units. This pilot concerns landscape context; surveyed plot polygons and independent field observations are absent. Raster is an aggregation of SWOT pixel-cloud measurements, not the original PIXC-level analysis. Similarity across two satellite products is cross-sensor consistency, **not ground-truth agronomic validation**.

## Primary documentation
- Product: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_Raster_100m_D
- Raster Product Description Rev C, 24 February 2025: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/pdd/D-56416_SWOT_Product_Description_L2_HR_Raster_20250224a_RevC_clean_sig_final.pdf
- Public metadata API: https://cmr.earthdata.nasa.gov/search/granules.json
- Sentinel catalog: https://earth-search.aws.element84.com/v1

Keep downloaded documentation for verification only; do not assume its copyright permits republication with a public Kaggle dataset. Public code, catalog references, and imagery subsets require their respective attribution/license records.
