import sys, tempfile, unittest, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_pipeline as p
class PipelineTests(unittest.TestCase):
 def test_deterministic_outputs(self):
  with tempfile.TemporaryDirectory() as tmp:
   a,b=Path(tmp)/'a',Path(tmp)/'b';s=p.run(out=a);p.run(out=b)
   self.assertEqual(s['n_event_rows'],24)
   self.assertEqual(s['n_distinct_dates'],20)
   self.assertEqual(sorted(x.name for x in a.iterdir()),['manifest.json','metrics.csv','report.md','summary.json'])
   for x in a.iterdir():self.assertEqual(x.read_bytes(),(b/x.name).read_bytes())
   manifest=json.loads((a/'manifest.json').read_text())
   for n,h in manifest['outputs'].items():self.assertEqual(p.sha(a/n),h)
 def test_altered_value_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   f=Path(tmp)/'bad.csv';f.write_bytes(p.DEFAULT_INPUT.read_bytes().replace(b'100.0',b'99.0',1))
   with self.assertRaises(ValueError):p.run(f,Path(tmp)/'out')
   self.assertFalse((Path(tmp)/'out').exists())
 def test_synthetic_rejected(self):
  with self.assertRaises(ValueError):p.validate(ROOT/'examples/eventos_sinteticos.csv')
if __name__=='__main__':unittest.main()
