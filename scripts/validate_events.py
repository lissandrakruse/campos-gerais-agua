"""Validate a minimal event CSV; not a hydrological or scientific validation."""
import argparse
import csv
import math
from datetime import datetime
from pathlib import Path

FIELDS = ["event_id", "storm_group_id", "site_id", "plot_id", "start_utc", "end_utc", "rainfall_mm", "runoff_mm", "cover_pct", "source_id", "data_kind"]

def validate(path, allow_synthetic=False):
    errors = []
    seen = set()
    count = 0
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            return ["Header must match the documented schema exactly."]
        for number, row in enumerate(reader, 2):
            count += 1
            prefix = f"line {number}: "
            if None in row or any(v is None for v in row.values()):
                errors.append(prefix + "wrong number of CSV fields")
                continue
            row = {k: v.strip() for k, v in row.items()}
            for field in FIELDS:
                if field not in {"runoff_mm", "cover_pct"} and not row[field]:
                    errors.append(prefix + field + " is required")
            if row["event_id"] in seen:
                errors.append(prefix + "duplicate event_id")
            seen.add(row["event_id"])
            if row["data_kind"] not in {"observed", "synthetic"}:
                errors.append(prefix + "data_kind must be observed or synthetic")
            if row["data_kind"] == "synthetic" and not allow_synthetic:
                errors.append(prefix + "synthetic data require --allow-synthetic")
            times = []
            for field in ["start_utc", "end_utc"]:
                try:
                    if not row[field].endswith("Z"):
                        raise ValueError()
                    times.append(datetime.fromisoformat(row[field].replace("Z", "+00:00")))
                except ValueError:
                    errors.append(prefix + field + " must be an ISO UTC timestamp ending in Z")
            if len(times) == 2 and times[1] <= times[0]:
                errors.append(prefix + "end_utc must be after start_utc")
            for field in ["rainfall_mm", "runoff_mm", "cover_pct"]:
                if not row[field]:
                    continue
                try:
                    value = float(row[field])
                    if not math.isfinite(value) or value < 0 or (field == "cover_pct" and value > 100):
                        raise ValueError()
                except ValueError:
                    errors.append(prefix + field + " is outside documented numeric bounds")
    if not count:
        errors.append("No observations: header-only template is not an analysis dataset.")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path")
    parser.add_argument("--allow-synthetic", action="store_true")
    args = parser.parse_args()
    try:
        errors = validate(args.csv_path, args.allow_synthetic)
    except (OSError, UnicodeError, csv.Error) as exc:
        parser.exit(2, f"Cannot read input: {exc}\n")
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Schema checks passed. This is not scientific validation or evidence of model performance.")

if __name__ == "__main__":
    main()
