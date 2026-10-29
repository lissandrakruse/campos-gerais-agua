import csv,itertools,statistics,tempfile,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from analyze_sensitivity import analyze,box_extrema,weighted_mean
SOURCE=ROOT/'data/published_derived/de_paula_2026_s1_derived_event_contrasts.csv'
class Audit(unittest.TestCase):
 def test_extrema_against_exhaustive_corners(self):
  for v in [[-3.,1.,2.,5.],[25.89,100.,60.],[-347.22,100.,64.72,-9.66]]:
   for k in [1,2,5,6,10]:
    values=[weighted_mean(v,w) for w in itertools.product([1,k],repeat=len(v))]
    lo,hi=box_extrema(v,k);self.assertAlmostEqual(lo,min(values));self.assertAlmostEqual(hi,max(values))
 def test_extrema_enclose_interior(self):
  v=[-7.,3.,10.]
  lo,hi=box_extrema(v,5)
  for w in itertools.product([1,2,3,4,5],repeat=3):self.assertTrue(lo-1e-12<=weighted_mean(v,w)<=hi+1e-12)
 def test_data_results_and_witness(self):
  with tempfile.TemporaryDirectory() as d:
   a=analyze(SOURCE,Path(d));self.assertEqual(a['records'],24);self.assertEqual(a['dates'],20)
   m={x['metric']:x for x in a['metrics']}
   self.assertEqual(m['trv_difference_pct']['n_positive'],24)
   self.assertEqual(m['tsy_difference_pct']['n_negative'],3)
   self.assertAlmostEqual(m['tsy_difference_pct']['row_mean_pct'],64.10958333333333)
   self.assertAlmostEqual(m['tsy_difference_pct']['date_balanced_mean_pct'],70.54025)
   self.assertAlmostEqual(m['tsy_difference_pct']['denominator_ratio_sign_threshold'],5.284087428650981)
   w=a['constructed_witness_summary'];self.assertGreater(w[0]['constructed_pooled_contrast_pct'],0);self.assertLess(w[1]['constructed_pooled_contrast_pct'],0)
   self.assertTrue(all(x['recovered_percentages_max_absolute_error']<1e-10 for x in w))
   self.assertEqual(len(list(csv.DictReader((Path(d)/'published_descriptions/leave_one_date_out.csv').read_text().splitlines()))),80)
 def test_deterministic(self):
  with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
   analyze(SOURCE,Path(a));analyze(SOURCE,Path(b))
   for f in Path(a).rglob('*'):
    if f.is_file():self.assertEqual(f.read_bytes(),(Path(b)/f.relative_to(a)).read_bytes())
 def test_sign_threshold(self):
  rows=list(csv.DictReader(SOURCE.read_text().splitlines()));v=[float(r['tsy_difference_pct']) for r in rows]
  k=sum(x for x in v if x>0)/(-sum(x for x in v if x<0))
  self.assertAlmostEqual(box_extrema(v,k)[0],0,places=10)
  self.assertGreater(box_extrema(v,5)[0],0);self.assertLess(box_extrema(v,6)[0],0)
if __name__=='__main__':unittest.main()
