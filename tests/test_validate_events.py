import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_events.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class ValidatorTests(unittest.TestCase):
    def check_row(self, **changes):
        row = dict(zip(v.FIELDS, ["e1", "s1", "site", "plot", "2023-01-01T00:00:00Z", "2023-01-01T01:00:00Z", "10", "2", "50", "example", "observed"]))
        row.update(changes)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.csv"
            with p.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=v.FIELDS)
                w.writeheader(); w.writerow(row)
            return v.validate(p)

    def test_valid(self):
        self.assertEqual(self.check_row(), [])
    def test_missing_is_not_zero(self):
        self.assertEqual(self.check_row(runoff_mm="", cover_pct=""), [])
    def test_missing_rain(self):
        self.assertTrue(self.check_row(rainfall_mm=""))
    def test_nonfinite_and_negative(self):
        for value in ["nan", "inf", "-1", "abc"]:
            with self.subTest(value=value):
                self.assertTrue(self.check_row(runoff_mm=value))
    def test_cover_range(self):
        self.assertTrue(self.check_row(cover_pct="101"))
    def test_times(self):
        self.assertTrue(self.check_row(end_utc="2022-01-01T00:00:00Z"))
        self.assertTrue(self.check_row(start_utc="2023-01-01T00:00:00"))
    def test_synthetic_gate(self):
        path = ROOT / "examples/eventos_sinteticos.csv"
        self.assertTrue(v.validate(path))
        self.assertEqual(v.validate(path, True), [])
    def test_empty_template_rejected(self):
        self.assertTrue(v.validate(ROOT / "data/templates/eventos.csv"))

if __name__ == "__main__":
    unittest.main()
