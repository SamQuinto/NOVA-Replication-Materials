"""Offline checks only: never call a model or require a key."""
import json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class ReplicationTests(unittest.TestCase):
    def call(self,script,*args):
        env=dict(os.environ);env.pop('OPENAI_API_KEY',None)
        p=subprocess.run([sys.executable,str(ROOT/script),*args],cwd=tempfile.gettempdir(),env=env,capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(p.returncode,0,p.stderr);return json.loads(p.stdout)
    def test_a1_job_preview_full_table(self):
        r=self.call('score_offer.py','--case-json',str(ROOT/'examples/job_offer.json'))
        self.assertFalse(r['api_called']);req=r['model_request'];self.assertEqual(req['model'],'gpt-6.1-sol')
        defs=json.loads(req['input'][2]['content'].split('\n',1)[1]);self.assertEqual(len(defs),215)
        self.assertFalse(any('payoff' in x for x in defs))
    def test_a1_tutorial_uses_identical_general_prompt(self):
        a=self.call('score_offer.py','--case-json',str(ROOT/'examples/job_offer.json'))
        b=self.call('score_tutorial_offer.py','--case-json',str(ROOT/'examples/tutorial_offer.json'))
        self.assertEqual(a['model_request']['input'][0],b['model_request']['input'][0])
        defs=json.loads(b['model_request']['input'][2]['content'].split('\n',1)[1]);self.assertEqual(len(defs),9)
    def test_a1_offline_job(self):
        r=self.call('score_offer.py','--case-json',str(ROOT/'examples/job_offer.json'),'--interpretation-json',str(ROOT/'examples/job_interpretation.json'))
        self.assertFalse(r['api_called']);self.assertEqual(len(r['response']['valid_pairs']),3)
        self.assertEqual(r['response']['decision'],'scorable')
        self.assertAlmostEqual(r['response']['total'],sum(x['points'] for x in r['response']['issue_breakdown']))
    def test_saved_appendix_example_retains_typos_and_both_role_values(self):
        case=json.loads((ROOT/'examples/appendix_a_offer.json').read_text(encoding='utf-8'))
        self.assertIn('6o vacations days',case['offer'])
        r=self.call('score_offer.py','--case-json',str(ROOT/'examples/appendix_a_offer.json'),'--interpretation-json',str(ROOT/'examples/appendix_a_interpretation.json'))
        self.assertFalse(r['api_called']);self.assertEqual(len(r['response']['issue_breakdown']),6)
        self.assertAlmostEqual(r['response']['total_for_proposer'],7.8)
        self.assertAlmostEqual(r['response']['total_for_receiver'],-5.3)
        self.assertEqual(r['response']['valid_pairs']['Remote Working Days'],'4 days per week')
    def test_a2_job_offline(self):
        r=self.call('score_offer.py','--architecture','A2','--case-json',str(ROOT/'examples/job_offer.json'),'--interpretation-json',str(ROOT/'examples/job_interpretation.json'))
        self.assertFalse(r['api_called']);self.assertEqual(r['response']['architecture'],'A2')
        self.assertEqual(len(r['response']['valid_pairs']),3)
    def test_a2_job_preview(self):
        r=self.call('score_offer.py','--architecture','A2','--case-json',str(ROOT/'examples/job_offer.json'))
        self.assertFalse(r['api_called']);self.assertEqual(r['model_request']['model'],'gpt-5.6-luna')
        user=json.loads(r['model_request']['messages'][1]['content']);self.assertIn('exercise_reading_rules',user)
    def test_a1_tutorial_offline(self):
        r=self.call('score_tutorial_offer.py','--case-json',str(ROOT/'examples/tutorial_offer.json'),'--interpretation-json',str(ROOT/'examples/tutorial_interpretation.json'))
        self.assertFalse(r['api_called']);self.assertEqual(len(r['response']['valid_pairs']),4)
        self.assertEqual(r['response']['decision'],'scorable')
    def test_a2_tutorial_preview(self):
        r=self.call('score_tutorial_offer.py','--architecture','A2','--case-json',str(ROOT/'examples/tutorial_offer.json'))
        self.assertFalse(r['api_called']);self.assertEqual(r['model_request']['model'],'gpt-5.6-luna')
    def test_a2_tutorial_offline(self):
        r=self.call('score_tutorial_offer.py','--architecture','A2','--case-json',str(ROOT/'examples/tutorial_offer.json'),'--interpretation-json',str(ROOT/'examples/tutorial_interpretation.json'))
        self.assertFalse(r['api_called']);self.assertEqual(len(r['response']['valid_pairs']),4)

    def test_named_a1_request_stage_matches_saved_request(self):
        r=self.call('A1-1.py','--case-json',str(ROOT/'examples/job_offer.json'))
        expected=json.loads((ROOT/'examples/A1_Job_Request.json').read_text(encoding='utf-8'))
        self.assertTrue(r==expected.get('model_request',expected),'A1 job request differs from the saved request')

    def test_named_a1_tutorial_request_stage_matches_saved_request(self):
        r=self.call('A1-1.py','--exercise','tutorial','--case-json',str(ROOT/'examples/tutorial_offer.json'))
        expected=json.loads((ROOT/'examples/A1_Tutorial_Request.json').read_text(encoding='utf-8'))
        self.assertTrue(r==expected.get('model_request',expected),'A1 tutorial request differs from the saved request')

    def test_named_a2_request_stage_matches_saved_request(self):
        r=self.call('A2-1.py','--case-json',str(ROOT/'examples/job_offer.json'))
        expected=json.loads((ROOT/'examples/A2_Job_Request.json').read_text(encoding='utf-8'))
        self.assertTrue(r==expected.get('model_request',expected),'A2 job request differs from the saved request')

    def test_named_a1_score_stage_matches_runner(self):
        args=['--case-json',str(ROOT/'examples/job_offer.json'),'--interpretation-json',str(ROOT/'examples/job_interpretation.json')]
        self.assertEqual(self.call('A1-2.py',*args),self.call('score_offer.py',*args)['response'])

    def test_named_a2_score_stage_matches_runner(self):
        args=['--case-json',str(ROOT/'examples/job_offer.json'),'--interpretation-json',str(ROOT/'examples/job_interpretation.json')]
        self.assertEqual(self.call('A2-2.py',*args),self.call('score_offer.py','--architecture','A2',*args)['response'])

if __name__=='__main__':unittest.main()
