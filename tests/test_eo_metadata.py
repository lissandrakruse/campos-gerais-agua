"""Offline source/metadata checks, not image reruns or ground validation."""
import ast, hashlib, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'eo/sentinel2'
class EOMetadataTests(unittest.TestCase):
 def test_calibration_manifest(self):
  item=json.loads((ROOT/'catalog_2025.json').read_text())['features'][0]
  self.assertIs(item['properties']['earthsearch:boa_offset_applied'],True)
  m=json.loads((ROOT/'verified_run_manifest.json').read_text())
  for name in ['green','nir','swir16','red','blue']:
   self.assertEqual(m['assets'][name]['scale'],0.0001)
   self.assertEqual(m['assets'][name]['effective_offset'],0)
   self.assertEqual(m['assets'][name]['declared_stac_offset'],-0.1)
 def test_conditional_offset_code(self):
  tree=ast.parse((ROOT/'process_sentinel.py').read_text())
  assignments=[x for x in ast.walk(tree) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='offset' for t in x.targets)]
  self.assertEqual(len(assignments),1)
  expr=ast.Expression(assignments[0].value); code=compile(expr,'offset','eval')
  for flag,expected in [(True,0),(False,-0.1),(None,-0.1)]:
   self.assertEqual(eval(code,{},dict(name='green',item={'properties':{'earthsearch:boa_offset_applied':flag}},declared_offset=-0.1)),expected)
 def test_manifest_pixel_units_and_limits(self):
  m=json.loads((ROOT/'verified_run_manifest.json').read_text());q=m['qa']
  self.assertEqual(m['grid_resolution_m'],20)
  self.assertEqual(q['index_valid_counts']['mndwi'],71145)
  self.assertEqual(q['mndwi_positive_pixels'],24)
  self.assertAlmostEqual(q['mndwi_positive_area_ha'],24*20*20/10000)
  self.assertIn('not crop-specific or validated flooding',q['warning'])
 def test_source_notebook_and_provenance(self):
  p=json.loads((ROOT/'execution_provenance.json').read_text())
  for file,key in [('sentinel2_water_indices_v2.ipynb','published_source_notebook_sha256'),('process_sentinel.py','processing_script_sha256')]:
   self.assertEqual(hashlib.sha256((ROOT/file).read_bytes()).hexdigest(),p[key])
  n=json.loads((ROOT/'sentinel2_water_indices_v2.ipynb').read_text())
  for c in n['cells']:
   if c['cell_type']=='code':
    self.assertEqual(c['outputs'],[]);compile(''.join(c['source']),'notebook','exec')
  self.assertIn('363624325',p['kaggle_url'])
if __name__=='__main__':unittest.main()
