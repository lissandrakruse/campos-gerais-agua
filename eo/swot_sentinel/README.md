# SWOT–Sentinel-2 quality-gated comparison

**Primary good-quality sample: n = 0. Reliable agreement/accuracy cannot be estimated for this fixed AOI/date.** Actual satellite-derived subsets, not simulated data.

Sensitivity admitting suspect quality has 495 pairs (all suspect): MAE 0.0184255601 in fraction units, Pearson r 0.5511087464. These describe exploratory differences, not accuracy, agronomic validation or regional generalization. 39 negative SWOT estimates remain unaltered; missing values never become dry-land zeros. Optical threshold fractions and SWOT estimates are different quantities. Time separation is about 17.05 hours.

## Run

```bash
python -m pip install -r eo/swot_sentinel/requirements_comparison.txt
python eo/swot_sentinel/compare_actual.py
python eo/swot_sentinel/test_comparison.py
```

The fixed inputs are a derived 55 × 51 native-100 m SWOT subset (not the full granule) and the corrected Sentinel MNDWI raster. Source filename and original full-file SHA-256 remain in NetCDF attributes; attribution files apply. No private download link or credentials are included. Public source DOI: https://doi.org/10.5067/SWOT-RASTER-D . Sentinel calibration and source are documented in ../sentinel2.

The script regenerates small GeoTIFFs, metrics and bilingual panels; test_comparison.py runs offline geometry/missingness/count/metric assertions and writes paired_cells.csv and an output hash manifest. These are software QA, not field validation. Gray pixels mean missing data, not zero water. Signed SWOT values are shown with an asymmetric color scale. Published results came from the included local subset; no claim of contemporaneous ground reference.

The earlier Sentinel-only module recorded SWOT as pending at that version. This separate module supersedes that status, not its source calibration. See comparison/comparison_metrics.json for all caveats and quality flags. No full article is stored here.

## Published executed notebook

[Kaggle saved run 363627480](https://www.kaggle.com/code/lissandrakruse/campos-gerais-swot-sentinel-quality-audit?scriptVersionId=363627480): successful execution in 38.3 seconds, 10 focused checks passed. The notebook installs netCDF4 if needed and uses embedded public subsets; no Earthdata or Drive credentials. Source notebook is included alongside the local CLI. Package installation requires internet, while the scientific inputs are embedded.
