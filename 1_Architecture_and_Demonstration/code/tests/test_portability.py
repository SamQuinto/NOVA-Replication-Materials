"""Check that the architecture folder works without its outer repository."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile,unittest
import urllib.request
ROOT=Path(__file__).resolve().parents[1]

class PortabilityTests(unittest.TestCase):
    def test_whole_architecture_folder_and_demo_work_after_renaming(self):
        env=dict(os.environ);env.pop('OPENAI_API_KEY',None)
        with tempfile.TemporaryDirectory(prefix='nova-demo-portability-') as directory:
            relocated=Path(directory)/'Another supplement'/'Renamed architecture'
            shutil.copytree(ROOT.parent,relocated,ignore=shutil.ignore_patterns('__pycache__','local-output','.env','.env.local'))
            server=subprocess.Popen([sys.executable,str(relocated/'demo/Start_Demo.py'),'--port','0','--no-browser'],cwd=directory,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            try:
                url=server.stdout.readline().strip().split('demonstration: ',1)[1]
                with urllib.request.urlopen(url+'api/status',timeout=10) as response:status=json.load(response)
                self.assertFalse(status['key_ready']);self.assertEqual(len(status['examples']),6)
                for exercise in ['job','tutorial']:
                    for architecture in ['A1','A2']:
                        request=urllib.request.Request(url+'api/score',data=json.dumps(dict(live=False,exercise=exercise,architecture=architecture,reasoning='low')).encode(),headers={'Content-Type':'application/json'})
                        with urllib.request.urlopen(request,timeout=40) as response:result=json.load(response)
                        self.assertFalse(result['api_called']);self.assertEqual(result['response']['decision'],'scorable')
                        self.assertEqual(result['saved_configuration'],{'architecture':'A1','reasoning':'low'})
                        if exercise=='job':self.assertAlmostEqual(result['response']['total'],7.8)
                for example in status['examples']:
                    request=urllib.request.Request(url+'api/score',data=json.dumps(dict(live=False,example_id=example['id'],exercise='job',architecture='A2',reasoning='high')).encode(),headers={'Content-Type':'application/json'})
                    with urllib.request.urlopen(request,timeout=40) as response:result=json.load(response)
                    self.assertFalse(result['api_called'])
                    self.assertEqual(result['saved_example_id'],example['id'])
                    self.assertEqual(result['saved_exercise'],example['exercise'])
                    expected='clarification_needed' if example['id']=='clarification' else 'scorable'
                    self.assertEqual(result['response']['decision'],expected)
                    if example['id']=='unpriced':self.assertIn('free coffee',result['response']['novel_terms'])
            finally:server.terminate();server.communicate(timeout=10)

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
