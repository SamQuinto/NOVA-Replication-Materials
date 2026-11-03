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
                    self.assertEqual(demo.normalise_material(material['html']),demo.normalise_material(demo.without_narrative_label(material['text'])))
                    self.assertNotIn('ROLE NARRATIVE:',material['html'])
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

    def test_materials_take_just_under_half_the_desktop_width(self):
        with urlopen(self.url) as response:page=response.read().decode('utf-8')
        self.assertIn('grid-template-columns:minmax(0,46fr) minmax(0,54fr)',page)
        self.assertNotIn('grid-template-columns:280px minmax(0,1fr)',page)
        self.assertIn('@media(max-width:760px)',page)

    def test_job_materials_keep_the_existing_formatting(self):
        for role in ['Candidate','Recruiter']:
            material=demo.role_materials('job',role)
            self.assertIn('<strong>',material['html'])
            self.assertIn('<em>',material['html'])
            self.assertIn('<u>',material['html'])
            self.assertIn('•',material['html'])
            self.assertIn('color:#',material['html'])
            self.assertIn('<h3>Background Information</h3>',material['html'])

    def test_display_html_drops_scripts_events_and_external_content(self):
        html=demo.material_html('**ROLE NARRATIVE:** <strong>Read this</strong><script>alert(1)</script><img src="https://example.com/a" onerror="alert(2)"><span onclick="alert(3)" style="color:#166534;background-image:url(https://example.com)">Safely</span>',formatted=True)
        self.assertNotIn('ROLE NARRATIVE:',html)
        self.assertNotIn('script',html)
        self.assertNotIn('alert',html)
        self.assertNotIn('<img',html)
        self.assertNotIn('onclick',html)
        self.assertNotIn('url(',html)
        self.assertIn('<strong>Read this</strong>',html)
        self.assertIn('color:#166534',html)

if __name__=='__main__':unittest.main()
