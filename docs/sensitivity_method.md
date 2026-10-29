# Event-weighting and denominator-identifiability audit

## Scope and provenance

This is a new secondary computation using the 96 reported two-decimal percentage contrasts in Supplementary Table S1 of de Paula et al. (2026), DOI https://doi.org/10.1007/s11368-026-04517-0. The source CSV SHA256 is recorded in the output. It is not a new field experiment, new predictive model, new mathematical theorem, or correction of the source authors' findings. The source study has additional measurements and aggregate results that are not encoded in Table S1. Our non-identifiability statement concerns reuse of **Table S1 alone**, not everything known by the authors or reported elsewhere.

24 records have 20 calendar dates: four dates each contain two labeled records. Labels are retained. The two macroplots at one site are not independent treatment replicates. Grouping by date is a weighting sensitivity and minimum anti-leakage precaution, not proof that the remaining dates are independent storms. Consecutive-day storms and carry-over sediment can require broader grouping; metadata are insufficient to define that grouping here.

## Reproducible computations

1. Unweighted record means and medians for each of four variables.
2. Date-balanced mean: first calculate an unweighted mean within date, then average those 20 means equally. This changes the descriptive estimand, not the physical water/sediment accounting.
3. Leave-one-date-out: remove all rows sharing one date and recompute summaries. Report the range across 20 exclusions. These ranges are influence diagnostics, **not confidence intervals** or predictive validation.
4. Counts of positive/negative contrasts and their conditional relationship to aggregate direction.
5. For additive TRV and TSY only, independently bounded-denominator scenarios and a constructed non-identifiability witness. Do not interpret sums of event SSC maxima or means as cumulative sediment concentration, so these aggregate scenarios are deliberately not calculated for SSC.

## Conditional aggregation identity

For selected, non-overlapping event records with the same units/normalization basis and strictly positive non-terraced quantities A_i, let B_i be the terraced quantity and d_i = 100(A_i-B_i)/A_i. Then the corresponding selected-event pooled contrast is D = 100(sum A_i - sum B_i)/sum A_i = sum(w_i d_i), where w_i = A_i/sum A_i. This is an elementary weighted-mean identity.

If all that is known is d_i, the scale and weights are unavailable. The closure of admissible D values is [min d_i, max d_i]; with all weights strictly positive and heterogeneous d, the endpoints are limits rather than attainable extrema. This is not an annual budget or a population interval. The reported percentages are rounded; all numerical bounds here use the published values as input. They are not exact bounds on unknown unrounded physical quantities.

For TRV all 24 reported contrasts are positive, ranging 25.89–100%. Consequently any admissible positive weighting preserves the direction for these selected records, although it does not identify the magnitude. For TSY there are 21 positives and three negatives, ranging -347.22–100%; therefore direction is not identified by these percentages alone.

## Bounded-denominator scenarios

Assume, for sensitivity analysis only, 1 <= A_i <= k after arbitrary common rescaling, without additional constraints across records. No observed or literature-based k is claimed. Fractional-linear extrema occur at bounds. Ordering d_i allows checking n+1 threshold allocations for minimum and maximum: give weight k to a prefix of the smallest contrasts (minimum) or a suffix of largest contrasts (maximum). Exhaustive corner tests on small vectors and interior checks independently verify implementation.

For TSY, the smallest denominator ratio permitting a nonpositive pooled contrast is k* = sum(d_i>0 d_i) / [-sum(d_i<0 d_i)] = 5.284087428650981. At k*, assigning k* to negative rows and 1 to positive rows gives zero numerator; below k*, no allocation within the independent box gives a negative numerator. This is an algebraic stress-test threshold, **not an estimate of the actual denominator ratio**.

At k=5, exact box bounds are 2.8342–90.0058%; at k=6, -7.2285–91.4998%. These are assumed-weight scenario ranges, not statistical uncertainty intervals. The specific simple witness below is compatible but not necessarily the minimum at k=6.

## Constructed witnesses, NOT observed sediment yields

- Assign every A_i=1 arbitrary unit: recover every reported percentage with B_i=A_i(1-d_i/100), pooled TSY contrast +64.1096%.
- Assign A_i=6 to the three negative-TSY rows and A_i=1 to other rows: same 24 reported percentages, pooled TSY contrast -6.5928%.

All constructed B_i are nonnegative. The maximum recovered-percentage error is <6e-14 percentage points. These examples demonstrate why those percentages alone do not determine a pooled total. They do not assert that either denominator configuration occurred, that the configurations fit all information in the full paper, or that the source study's aggregate conclusion is wrong. No synthetic value is included in the observed-data CSV.

## Observed descriptive results

| Variable | Record mean (%) | Date-balanced mean (%) | Change (percentage points) | Leave-one-date-out record-mean range (%) |
|---|---:|---:|---:|---:|
| SSCmed |59.8483|59.8465|-0.0018|56.1982–67.6213|
| SSCmax |56.7292|53.5398|-3.1894|52.7955–66.6830|
| TRV |80.1204|80.6548|+0.5343|78.3132–84.2195|
| TSY |64.1096|70.5403|+6.4307|60.8468–84.4832|

Medians of the 24 records are 100% for all four metrics, illustrating that a median is not a pooled reduction. Date-balanced TRV median is98.275%; this statistic also is not a pooled budget.

## Scientific value and novelty boundary

The credible contribution is a tested, source-linked **data-reuse audit** exposing which directions survive missing denominator weights, how grouping changes summaries, and which metadata must be recovered before a stronger hydrological model can be evaluated. This is more substantive than simply reprinting percentages, but it does not establish broad novelty or guarantee publication.

Temporal aggregation and sediment weighting are established issues. Primary examples checked:
- Lu, H., Moran, C. J., and Sivapalan, M. (2005), *A theoretical exploration of catchment-scale sediment delivery*, Water Resources Research, DOI https://doi.org/10.1029/2005WR004018. The paper explicitly treats different temporal averaging windows; two corrections are linked by the publisher. We do not reproduce or rely on its corrected equations.
- Skålevåg, A., Korup, O., and Bronstert, A. (2024), *Inferring sediment-discharge event types in an Alpine catchment from sub-daily time series*, HESS28,4771ff, DOI https://doi.org/10.5194/hess-28-4771-2024. It calculates event sediment yield by integrating concentration×discharge, illustrating why individual concentration percentages cannot replace loads.

This was a focused prior-art check, not a systematic or exhaustive novelty search. An extension to other independent published sites/tables would be needed to assess transferability; the current study is a single-data-source case study.

## Run

python scripts/run_pipeline.py --out outputs/published
python -m unittest discover -s tests -v

Five tests pass, including exact comparison with exhaustive bound corners, interior-value enclosure, source-summary checks, witness recovery, sign threshold and byte-identical repeated outputs. Tests establish software properties, not field validity.
