"""Check role-material loading without using an API key or making model calls."""
import importlib.util
import json
from pathlib import Path
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('nova_demo',ROOT/'demo/Start_Demo.py')
demo=importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)

class DemoMaterialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=demo.ThreadingHTTPServer(('127.0.0.1',0),demo.Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def test_every_role_matches_its_exercise_file(self):
        for exercise in ['job','tutorial']:
            folder=ROOT/'code/frozen'/('tutorial' if exercise=='tutorial' else '')
            source=json.loads((folder/'Scoring_Table.json').read_text(encoding='utf-8'))
            for role in ['Candidate','Recruiter']:
                with self.subTest(exercise=exercise,role=role):
                    with urlopen(self.url+f'/api/materials?exercise={exercise}&role={role}') as response:
                        material=json.load(response)
                    self.assertEqual(material['text'],source['roles'][role]['full_text'])
                    self.assertNotIn('blocks',material)
                    self.assertNotIn('OPENAI_API_KEY',material)
                    self.assertNotIn('issues',material)

    def test_invalid_exercise_and_role_are_rejected(self):
        for query in ['exercise=other','role=other','exercise=../../private']:
            with self.assertRaises(HTTPError) as error:
                urlopen(self.url+'/api/materials?'+query)
            self.assertEqual(error.exception.code,400)

    def test_page_has_scrollable_material_panel_and_original_scoring_area(self):
        with urlopen(self.url) as response:page=response.read().decode('utf-8')
        self.assertIn('id="role-materials"',page)
        self.assertIn('overflow-y:auto',page)
        self.assertIn('id="scoring-demo"',page)
        self.assertIn('loadMaterials()',page)

if __name__=='__main__':unittest.main()
