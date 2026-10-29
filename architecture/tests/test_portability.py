"""Check that the architecture folder works without its outer repository."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]

class PortabilityTests(unittest.TestCase):
    def test_four_stages_in_a_renamed_folder(self):
        env=dict(os.environ);env.pop('OPENAI_API_KEY',None)
        with tempfile.TemporaryDirectory(prefix='nova-portability-') as directory:
            relocated=Path(directory)/'Another supplement'/'Renamed scorer folder'
            shutil.copytree(ROOT,relocated,ignore=shutil.ignore_patterns('__pycache__','local-output'))
            for stage in ['A1-1','A1-2','A2-1','A2-2']:
                args=['--case-json','examples/job_offer.json']
                if stage.endswith('-2'):args+=['--interpretation-json','examples/job_interpretation.json']
                completed=subprocess.run([sys.executable,str(relocated/(stage+'.py')),*args],cwd=directory,env=env,capture_output=True,text=True,encoding='utf-8',timeout=30)
                self.assertEqual(completed.returncode,0,completed.stderr)
                result=json.loads(completed.stdout)
                if stage.endswith('-1'):self.assertIn('model',result)
                else:self.assertEqual(result['decision'],'scorable')

    def test_a2_live_orchestration_calls_prepared_model_once_with_a_fake_api(self):
        program='''import json,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import nova_cli,common1225 as client
root=Path(sys.argv[1]); calls=[]
def fake(request,stage):
 calls.append(request)
 return json.loads((root/'examples/job_interpretation.json').read_text()),dict(input_tokens=1,output_tokens=1)
client.api=fake
case=json.loads((root/'examples/job_offer.json').read_text())
result=nova_cli.run(case,'A2','job','low',None,True)
assert len(calls)==1
assert calls[0]['model']=='gpt-5.6-luna'
assert result['response']['decision']=='scorable'
print(json.dumps({'fake_calls':len(calls),'real_api_calls':0}))
'''
        completed=subprocess.run([sys.executable,'-c',program,str(ROOT)],capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(completed.returncode,0,completed.stderr)
        self.assertEqual(json.loads(completed.stdout)['real_api_calls'],0)

if __name__=='__main__':unittest.main()
