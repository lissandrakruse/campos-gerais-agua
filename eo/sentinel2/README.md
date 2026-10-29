# Sentinel-2 exploratory water indices — corrected v2

Contains modified Copernicus Sentinel data [2025]. This EO module is separate from the runoff-table audit and does not validate it.

## Verified execution

[Kaggle v2, pinned](https://www.kaggle.com/code/lissandrakruse/campos-gerais-sentinel-2-water-indices?scriptVersionId=363624325) completed successfully in 41.3 seconds. `execution_provenance.json` records the downloaded executed notebook hash and the source-only notebook stored here. Outputs were cleared only to avoid embedding imagery; code cells are unchanged. `verified_run_manifest.json` records original scene URLs, calibration, reprojection, raster hashes and QA. Bands are not duplicated in GitHub.

Scene `S2B_22JET_20250617_0_L2A`, 2025-06-17 13:29:20 UTC. AOI `[-50.07,-25.12,-50.02,-25.07]` (WGS84) is a regional context rectangle, **not surveyed crop or experimental plot boundaries**. The 20 m UTM22S grid has 71,145 finite NDWI/MNDWI pixels. 24 pixels meet MNDWI > 0 (0.96 ha). This is threshold-selected area, **not validated water extent, flooding, soil moisture, runoff or crop damage**. No field-reference observations were used.

## Calibration correction

Version 1 double-applied an offset and is superseded; do not use its maps or 0.12 ha value. In this Earth Search COG, `earthsearch:boa_offset_applied=true` means the provider already applied the BOA offset. Corrected v2 applies scale 0.0001 and **effective offset 0**, preserving contradictory declared STAC offset -0.1 in the audit. This is provider/product-specific, not a universal Sentinel rule. See attribution and references in the manifest.

10 m bands are averaged to 20 m; SWIR/SCL aligned with nearest neighbor. SCL 4/5/6 retained. SCL cloud screening does not establish cloud-free ground truth. Additional threshold sensitivity is planned, not reported as completed.

## Run

```bash
# Python with numpy, rasterio, matplotlib installed; network access to public COGs
python eo/sentinel2/process_sentinel.py
```

The adjacent catalog deliberately contains only the executed scene. The script writes new output under its scene-ID folder and downloads/clips public COGs. No credentials are required. Dependencies are not version-pinned: the manifest verifies the archived Kaggle run, not a promise of byte-identical future GDAL results. The included notebook is the source of the executed Kaggle v2 (Kaggle filesystem paths). Repository tests validate code/metadata/units, **not independently rerun satellite processing or field accuracy**.

## SWOT status

SWOT science data have **not** been downloaded or processed. A candidate observation roughly 17.05 h earlier exists in the catalog, but no cross-sensor agreement result exists. Authorized acquisition of the science file, variable/quality inspection and valid overlap checks remain necessary. See [comparison protocol](../COMPARISON_PROTOCOL.md).
