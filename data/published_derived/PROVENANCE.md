# Published derived event contrasts: provenance and limitations

Source: de Paula, A. L., et al. (2026). Fine-scale erosion under soil conservation practices: selective sediment transport and runoff in terraced and non-terraced no-till hillslopes. Journal of Soils and Sediments, 26, 313. DOI: https://doi.org/10.1007/s11368-026-04517-0.

Official Supplementary Material 1, Table S1, retrieved 2026-10-29:
https://media.springernature.com/original/springer-static/esm/art%3A10.1007%2Fs11368-026-04517-0/MediaObjects/11368_2026_4517_MOESM1_ESM.docx

Source SHA256: eb6e8d5bfa74c1f039fb62b56601fbb6d764b5e393f28b7bd26e9d8c6172bee6.

The article's Rights and permissions section explicitly states Creative Commons Attribution 4.0 (https://creativecommons.org/licenses/by/4.0/). No different credit or restriction was found in this DOCX supplement. The CSV is an attributed extraction/reformatting of factual table values, not a new experiment. Original publisher DOCX need not be redistributed. Changes: decimal comma converted to dot; original event labels retained; ISO date and suffix split into additional fields; provenance columns added. Source_row is one-based data-row position, not DOCX row position.

Each value is a reported percentage contrast: 100 × (NT − NT+T) / NT. Positive values mean the reported variable is larger in the non-terraced plot; negative values mean it is larger in the terraced plot. The NT absolute values are not supplied in this supplement. A value of 100 is preserved as reported, not independently verified as exact absence. No missing values were inferred or replaced. Negative values are not errors by definition.

Metrics: SSCmed (mean suspended sediment concentration), SSCmax (maximum suspended sediment concentration), TRV (total runoff volume), TSY (total sediment yield). Four percentages are different response variables, not interchangeable measurements.

Event suffixes: T = afternoon; N = nighttime; T1/T2 = first/second events in close succession. Preserve the original label when matching other sources. There are 24 event rows, 20 distinct calendar dates, no duplicate complete labels. Rows include Mar 2, 2023_T; Mar 3, 2023_N; and Mar 3, 2023 (without suffix). A related 2025 article uses different March labeling; do not automatically join those records by date. Later author clarification or original timestamps would be needed.

These are repeated events from two management macroplots at one site, not 24 independent sites or replicated treatment assignments. Descriptive counts, ranges and unweighted medians do not estimate pooled percentage reductions, independent causal treatment effects or predictive performance. The table alone cannot train absolute runoff forecasts or validate within-field waterlogging maps. It lacks raw hydrographs, event rainfall predictors, absolute denominators and spatial inundation observations.

Reproduce from the official publisher download (not included in this repository):

```sh
python scripts/extract_springer_s1.py /path/to/official_supplement.docx --out outputs/s1
python -m unittest discover -s tests -v
```

The repository tests compare the published CSV's 96 numeric cells with an independent manual transcription and check event identity. During initial audit, the DOCX extraction also passed those same comparisons. Tests do not establish independence or causality.
