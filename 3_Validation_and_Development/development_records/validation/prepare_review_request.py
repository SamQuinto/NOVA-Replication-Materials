"""Prepare a reference/checklist request. No API call unless --live is supplied."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
CODE=HERE.parents[2]/'1_Architecture_and_Demonstration/code'
sys.path.insert(0,str(CODE))
import common1225 as c
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--task',choices=['reference','checklist','reference-correction'],required=True);p.add_argument('--exercise',choices=['job','tutorial'],default='tutorial');p.add_argument('--input-json',type=Path,required=True);p.add_argument('--advanced',action='store_true');p.add_argument('--live',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
    folder=CODE/'frozen/tutorial' if a.exercise=='tutorial' else CODE/'frozen'
    prompt={'reference':'Reference.txt','checklist':'Checklist_Review.txt','reference-correction':'Reference_Correction.txt'}[a.task]
    schema=c.load(HERE/('Checklist_Format.json' if a.task=='checklist' else 'Reference_Format.json'))
    if a.task!='checklist':schema['properties']['references']['items']['properties']['ideas']['items']['properties']['issue']['enum']=[x['name'] for x in c.load(folder/'Scoring_Table.json')['issues']]+['Outside table']
    body=c.load(a.input_json)
    request=dict(model='gpt-6.1-sol' if a.advanced else 'gpt-5.6-luna',store=False,reasoning=dict(effort='high' if a.advanced else 'low'),max_output_tokens=18000 if a.task!='checklist' else 9000,input=[dict(role='developer',content=(HERE/prompt).read_text(encoding='utf-8')),dict(role='developer',content=json.dumps(dict(EXERCISE_INFORMATION=c.load(folder/'A1_Exercise.json'),SCORING_TABLE=c.load(folder/'A1_Scoring_Definitions.json'),ROLE_MATERIALS=c.load(folder/'Role_Materials.json')),ensure_ascii=False,separators=(',',':'))),dict(role='user',content=json.dumps(body,ensure_ascii=False,separators=(',',':')))],text=dict(format=dict(type='json_schema',name='checklist_review' if a.task=='checklist' else 'reference_key',strict=True,schema=schema)))
    if a.live:
        result,receipt=c.api(request,'validation_'+a.task);value=dict(result=result,receipt=receipt)
    else:value=dict(model_request=request,api_called=False)
    text=json.dumps(value,ensure_ascii=False,indent=2)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text,encoding='utf-8')
    else:
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        print(text)
if __name__=='__main__':main()
