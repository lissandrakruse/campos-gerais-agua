"""Independent manual transcription checks, 96 published numeric cells."""
import unittest
from pathlib import Path
import csv, importlib.util
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("extractor", ROOT / "scripts/extract_springer_s1.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
describe, METRICS = module.describe, module.METRICS
def load_rows():
 with (ROOT / "data/published_derived/de_paula_2026_s1_derived_event_contrasts.csv").open(encoding="utf-8", newline="") as f:
  rows = list(csv.DictReader(f))
 for row in rows:
  row["source_row"] = int(row["source_row"])
  for key in METRICS: row[key] = float(row[key])
 return rows
class SourceTableTests(unittest.TestCase):
 def test_all_published_numbers(self):
  expected=[*[ [100.,100.,100.,100.] for _ in range(8)], [88.04,87.80,57.14,99.82],[100.,100.,100.,100.],[100.,100.,100.,100.],[5.19,35.60,64.29,80.],[100.,100.,96.55,100.],[-18.24,-27.82,60.09,42.5],[67.51,98.5,85.24,95.65],[100.,100.,100.,100.],[100.,100.,100.,100.],[46.38,-62.28,81.44,87.87],[100.,100.,100.,100.],[-118.93,-14.72,41.35,-9.66],[13.68,-30.68,35.99,64.72],[41.62,55.94,25.89,-347.22],[-35.46,-8.63,44.17,27.22],[-53.43,-172.21,30.74,-2.27]]
  rows=load_rows()
  self.assertEqual(len(rows),len(expected))
  for row,values in zip(rows,expected):
   for key,value in zip(METRICS,values):
    with self.subTest(row=row['source_row'],metric=key):self.assertEqual(row[key],value)
 def test_event_identity_preserved(self):
  rows=load_rows();s=describe(rows)
  self.assertEqual(s['n_distinct_dates'],20)
  self.assertEqual([rows[i]['event_suffix'] for i in [1,2,3,21,22]],['T','N','','T1','T2'])
  self.assertEqual(s['year_counts'],{'2023':19,'2024':4,'2025':1})
  self.assertEqual(s['metrics']['trv_difference_pct']['n_equal_100_reported'],13)
  self.assertEqual(s['metrics']['tsy_difference_pct']['n_negative'],3)
if __name__=='__main__':unittest.main()
