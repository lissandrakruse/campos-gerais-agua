#!/usr/bin/env python3
"""Deterministic descriptive pipeline for the published S1 contrasts only."""
import argparse, csv, datetime, hashlib, json, math
from pathlib import Path
from extract_springer_s1 import describe, METRICS, DOI, URL
from analyze_sensitivity import analyze
EXPECTED_CSV_SHA256 = "52ff69ca53da06c2bd2d441629b79efe64a5435973d9c1957f97096cfbf10215"
DEFAULT_INPUT = Path(__file__).resolve().parents[1] / "data/published_derived/de_paula_2026_s1_derived_event_contrasts.csv"
CAVEAT = "Published rounded percentage contrasts, not raw measurements. Unweighted medians are not pooled reductions. No predictive model, causal inference, or regional validation. These 24 selected runoff-event records cover 20 dates of one experiment, not 24 independent sites or all eligible storms. Reported 100% is not independently verified absence. Outlet runoff is not within-field waterlogging. Occurrence classification requires all eligible storms, including verified zero-runoff events."
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def validate(path):
    # Exact bytes pin all 96 numeric cells, event labels and attribution to audited version.
    if sha(path) != EXPECTED_CSV_SHA256:
        raise ValueError("CSV differs from the audited published table; re-audit required")
    with Path(path).open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 24:
        raise ValueError("Expected 24 source rows")
    for i, row in enumerate(rows, 1):
        if int(row["source_row"]) != i or row["source_doi"] != DOI:
            raise ValueError("Invalid source provenance")
        datetime.date.fromisoformat(row["event_date"])
        row["source_row"] = i
        for m in METRICS:
            row[m] = float(row[m])
            if not math.isfinite(row[m]):
                raise ValueError("Nonfinite source value")
    return rows

def run(input_path=DEFAULT_INPUT, out=Path("outputs/published")):
    input_path, out = Path(input_path), Path(out)
    rows = validate(input_path)
    summary = describe(rows)
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    fields = ["metric"] + list(summary["metrics"][METRICS[0]])
    with (out / "metrics.csv").open("w", encoding="utf-8", newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for m in METRICS: writer.writerow({"metric":m, **summary["metrics"][m]})
    lines=["# Descriptive reproduction of Supplementary Table S1", "", CAVEAT, "", f"Source: https://doi.org/{DOI} (Supplementary Table S1; CC BY 4.0).", "", "24 event rows, 20 dates, 96 percentage values checked against the audited version.", "", "| Metric | Minimum (%) | Maximum (%) | Unweighted median (%) | Negative values |", "|---|---:|---:|---:|---:|"]
    for m in METRICS:
        s=summary["metrics"][m]
        lines.append(f"| {m} | {s['min_pct']} | {s['max_pct']} | {s['median_pct_unweighted']} | {s['n_negative']} |")
    lines += ["", "No observed pooled reduction is calculated: absolute denominators are missing. Constructed denominator scenarios are explicitly hypothetical. No confidence intervals or machine-learning performance are calculated. Original extraction and limitations are documented in data/published_derived/PROVENANCE.md and docs/dados.md.", "", "Row counts do not measure spatial replication. Date inconsistencies between papers are not automatically reconciled. Future limited models may use audited event aggregates and predictors; minute-level hydrographs are not required for every model."]
    (out / "report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    analyze(input_path, out / "sensitivity")
    output_names=["summary.json","metrics.csv","report.md"] + sorted(str(p.relative_to(out)) for p in (out/"sensitivity").rglob("*") if p.is_file())
    manifest={"pipeline_version":"2.0.0", "input_sha256":sha(input_path), "source_doi":DOI,"source_url":URL,"license_derived_table":"CC BY 4.0", "mode":"published_derived_and_separate_constructed_scenarios", "outputs":{n:sha(out/n) for n in output_names}}
    # No wall-clock timestamps or absolute paths: same bytes in every output directory.
    (out / "manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--out", type=Path, default=Path("outputs/published"))
    a=p.parse_args(); s=run(a.input,a.out)
    print(f"Validated {s['n_event_rows']} event rows; descriptive outputs: {a.out}")
if __name__ == "__main__": main()
