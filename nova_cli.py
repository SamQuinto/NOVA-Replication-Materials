"""Request preview, saved-interpretation replay, and explicit live scoring.

No API call is made unless --live is supplied. This is a replication runner,
not a drop-in replacement for the separate Empirica deployment package.
"""
from pathlib import Path
import argparse,copy,io,json,os,sys,types,urllib.request,urllib.error
import common1225 as c
ROOT=Path(__file__).resolve().parent

def data_dir(exercise):return ROOT/'frozen/tutorial' if exercise=='tutorial' else ROOT/'frozen'
def a1_setup(exercise):
    sys.path.insert(0,str(ROOT/'runtime/app/a1/backend'))
    from scorer import Scorer
    return Scorer(data_dir(exercise)/'Scoring_Table.json',helper=False,model='gpt-6.1-sol')
def a1_request(case,exercise,reasoning):
    folder=data_dir(exercise);schema=c.load(folder/('OUTPUT_FORMAT.json' if exercise=='tutorial' else 'SOURCE_FIRST_FORMAT.json'))
    return dict(model='gpt-6.1-sol',store=False,reasoning=dict(effort=reasoning),max_output_tokens=32768,input=[dict(role='developer',content=(ROOT/'prompts/A1_Final.txt').read_text(encoding='utf-8')),*[dict(role='developer',content=name+'\n'+json.dumps(c.load(folder/file),ensure_ascii=False,separators=(',',':'))) for name,file in [('EXERCISE_INFORMATION','A1_Exercise.json'),('SCORING_TABLE','A1_Scoring_Definitions.json'),('ROLE_MATERIALS','Role_Materials.json')]],dict(role='user',content=json.dumps(dict(CURRENT_OFFER=dict(proposer_role=case['role'],text=case['offer']),PREVIOUS_OFFER=dict(text=case.get('previous_offer',''))),ensure_ascii=False,separators=(',',':')))],text=dict(format=dict(type='json_schema',name='offer_interpretation',strict=True,schema=schema)))

class PreviewReady(Exception):
    def __init__(self,request):self.request=request

def a2_setup(exercise,preview=False):
    os.environ.update(NEGOTIATOR_SCENARIO_FILE=str(data_dir(exercise)/'Scoring_Table.json'),NEGOTIATOR_PROVIDER='openai',NEGOTIATOR_MODEL='gpt-5.6-luna',NEGOTIATOR_SCORER_ROUTING='single')
    os.environ.pop('NEGOTIATOR_API_LEDGER',None)
    if exercise=='job':
        # Final evaluated job rules used the generic A1 validation/scoring core.
        a1_setup(exercise)
    else:
        for name in ['scenario','scenario_rules','offer_engine','api_budget']:sys.modules.pop(name,None)
    sys.path.insert(0,str(ROOT/'runtime/app/backend'));import stream
    if exercise=='tutorial':
        if preview:stream._api_key=lambda:'REQUEST_PREVIEW_ONLY'
        def post(request,timeout=45):
            req=json.loads(request.data.decode());req['store']=False
            if preview:raise PreviewReady(req)
            c.api(req,'A2_tutorial');return io.BytesIO(json.dumps(c.LAST_BODY).encode())
        stream.urllib=types.SimpleNamespace(request=types.SimpleNamespace(Request=urllib.request.Request,urlopen=post),error=urllib.error)
    return stream

def run(case,architecture,exercise,reasoning,interpretation=None,live=False):
    c.RECEIPTS.clear()
    if architecture=='A1':
        scorer=a1_setup(exercise);scorer.reasoning=reasoning;request=a1_request(case,exercise,reasoning)
        if interpretation is None and not live:return dict(model_request=request,api_called=False)
        if interpretation is None:interpretation,_=c.api(request,'A1_'+reasoning)
        result=scorer.for_empirica(scorer.finalize(case['offer'],interpretation,case['role'],case.get('previous_offer','')))
    elif exercise=='job':
        stream=a2_setup(exercise,preview=not live);import a2_extract,a2_finalize
        a2_extract.STREAM=stream;a2_extract.ROLE=case['role'];a2_extract.RUN_ID=None;a2_extract.RECEIPTS.clear();a2_extract.TRACE.clear()
        if interpretation is None and not live:
            original=c.api
            def capture(request,stage):raise PreviewReady(request)
            c.api=capture
            try:a2_extract.extract(case['offer'],case.get('previous_offer',''),model='gpt-5.6-luna')
            except PreviewReady as e:return dict(model_request=e.request,api_called=False)
            finally:c.api=original
        if interpretation is None:interpretation=a2_extract.extract(case['offer'],case.get('previous_offer',''),model='gpt-5.6-luna')
        result=a2_finalize.finalize(case,interpretation)
    else:
        stream=a2_setup(exercise,preview=not live)
        if interpretation is None and not live:
            try:stream._llm_extract_once(case['offer'],case.get('previous_offer',''))
            except PreviewReady as e:return dict(model_request=e.request,api_called=False,note='A dense offer can receive a second existing completeness call in live mode.')
        if interpretation is None:interpretation=stream.llm_extract(case['offer'],case.get('previous_offer',''))
        result=stream.score(case['offer'],case['role'],copy.deepcopy(interpretation),case.get('previous_offer',''))
    return dict(response=result,interpretation=interpretation,receipts=c.RECEIPTS,api_called=bool(c.RECEIPTS))

def main(default_exercise='job'):
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--architecture',choices=['A1','A2'],default='A1');p.add_argument('--exercise',choices=['job','tutorial'],default=default_exercise);p.add_argument('--reasoning',choices=['low','high'],default='low');p.add_argument('--offer');p.add_argument('--case-json',type=Path);p.add_argument('--role',default='Candidate',choices=['Candidate','Recruiter']);p.add_argument('--previous-offer',default='');p.add_argument('--interpretation-json',type=Path);p.add_argument('--live',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
    if a.case_json:case=c.load(a.case_json)
    elif a.offer:case=dict(role=a.role,offer=a.offer,previous_offer=a.previous_offer)
    else:p.error('Supply --offer or --case-json.')
    case.setdefault('previous_offer','')
    if a.architecture=='A2' and a.reasoning!='low':p.error('The evaluated A2 setting is low reasoning.')
    interpretation=c.load(a.interpretation_json) if a.interpretation_json else None
    value=run(case,a.architecture,a.exercise,a.reasoning,interpretation,a.live);text=json.dumps(value,ensure_ascii=False,indent=2)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text,encoding='utf-8')
    else:print(text)
if __name__=='__main__':main()
