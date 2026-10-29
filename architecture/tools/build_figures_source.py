"""Build editable black-and-white architecture diagrams and their text source."""
from pathlib import Path
import json,html,textwrap
W=Path(__file__).resolve().parents[1];OUT=W/'figures'

MAIN={
 'A1':dict(header=['A1  Flexible','Higher API cost'],boxes=[
  ('Offer data and exercise files',[
   'Offer text entered in the free-text box',
   'Negotiator’s assigned role',
   'Role materials and scoring table (JSON files)',
   'General-purpose prompt containing the main instructions (text file)',
   'Optional: Previous offer text, when referenced—for example, “Keep everything from the previous offer, but change the salary to $60,000.”']),
  ('Python script A1-1',['Combines the inputs above, including all issues and options from the scoring table, into one JSON request sent to the LLM.']),
  ('Advanced LLM',['(e.g., OpenAI GPT-6.1 Sol)',
   'Processes the JSON request prepared above',
   'Identifies the proposed issues and matches them to available options in the scoring table',
   'Returns its interpretation as JSON']),
  ('Interpretation (JSON)',[
   'Identified issues and their interpreted options',
   'Words quoted from the offer to support each interpretation',
   'Clarification questions and ideas retained without scores, if needed']),
  ('Python script A1-2',[
   'Checks the interpretation above for supporting quotations, valid issues and options, and allowable values',
   'Looks up researcher-defined scores in the scoring table and calculates totals',
   'Returns the scored offer as JSON']),
  ('Scored offer (JSON)',[
   'Interpreted issues and options, with their individual scores',
   'Each negotiator’s total score when the offer is complete and valid',
   'Clarification questions and unscored ideas, if any'])]),
 'A2':dict(header=['A2  Customized','Higher setup effort, lower API cost'],boxes=[
  ('Offer data and exercise files',[
   'Offer text entered in the free-text box',
   'Negotiator’s assigned role',
   'Role materials, scoring table and matching vocabulary (JSON files)',
   'Main instructions (text file) and exercise-specific reading instructions (JSON file)',
   'Optional: Previous offer text, when the current offer refers to it']),
  ('Python script A2-1',[
   'Uses matching rules to select relevant issues and options from the scoring table',
   'Combines these entries with the offer, role materials and instructions into one JSON request sent to the LLM']),
  ('Economical LLM',['(e.g., OpenAI GPT-5.6 Luna)',
   'Processes the JSON request prepared above',
   'Identifies the proposed issues and matches them to the selected scoring-table options',
   'Returns its interpretation as JSON']),
  ('Interpretation (JSON)',[
   'Identified issues and their interpreted options',
   'Words quoted from the offer to support each interpretation',
   'Clarification questions and ideas retained without scores, if needed']),
  ('Python script A2-2',[
   'Applies exercise-specific Python rules to the interpretation above',
   'Checks quotations, issues, options and values, then looks up assigned scores and calculates totals',
   'Returns the scored offer as JSON']),
  ('Scored offer (JSON)',[
   'Interpreted issues and options, with their individual scores',
   'Each negotiator’s total score when the offer is complete and valid',
   'Clarification questions and unscored ideas, if any'])])}

def esc(s):return html.escape(s)
def text(x,y,lines,size=28,bold=False,anchor='middle'):
 return '<text x="'+str(x)+'" y="'+str(y)+'" text-anchor="'+anchor+'" font-family="Arial, sans-serif" font-size="'+str(size)+'"'+(' font-weight="bold"' if bold else '')+'>'+''.join('<tspan x="'+str(x)+'" dy="'+('0' if i==0 else str(size*1.26))+'">'+esc(v)+'</tspan>' for i,v in enumerate(lines))+'</text>'
def box(x,y,w,h,title,body,core=False):
 parts=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="black" stroke-width="{3 if core else 1.8}"/>',text(x+w/2,y+42,[title],31,True)]
 ypos=y+85
 for line in body:
  model=line.startswith('(e.g.,')
  wrapped=textwrap.wrap(line,width=int((w-70)/14.5),break_long_words=False)
  plain=model or title=='Python script A1-1'
  lines=wrapped if plain else ['• '+wrapped[0]]+['  '+s for s in wrapped[1:]]
  parts.append(text(x+27,ypos,lines,27,anchor='start'));ypos+=34*len(wrapped)+8
 assert ypos<=y+h+5,(title,ypos,y+h)
 return ''.join(parts)
def arrow(x1,y1,x2,y2,label=None):
 s=f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="black" stroke-width="2.3" marker-end="url(#arrow)"/>'
 if label:s+=text(x1+18,(y1+y2)/2,[label],24,anchor='start')
 return s
def svg(width,height,body):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="black"/></marker></defs><rect width="100%" height="100%" fill="white"/>'+body+'</svg>'
def main():
 global MAIN
 content=OUT/'Figure_Content.json'
 if content.exists():MAIN=json.loads(content.read_text(encoding='utf-8'))['main']
 OUT.mkdir(exist_ok=True)
 heights=[]
 for step in range(6):
  sizes=[]
  for col in MAIN.values():
   body=col['boxes'][step][1]
   sizes.append(110+sum(34*len(textwrap.wrap(line,width=42,break_long_words=False))+8 for line in body))
  heights.append(max(sizes))
 ys=[];y=85
 for height in heights:ys.append(y);y+=height+45
 parts=[]
 for i,(key,col) in enumerate(MAIN.items()):
  x=35+i*750;cx=x+345;parts.append(text(cx,40,col['header'],31,True))
  for j,((title,body),top,height) in enumerate(zip(col['boxes'],ys,heights)):
   parts.append(box(x,top,690,height,title,body,core=j==5))
   if j<5:parts.append(arrow(cx,top+height+3,cx,ys[j+1]-5))
 (OUT/'Figure_B1_NOVA_Architectures.svg').write_text(svg(1510,y-10,''.join(parts)),encoding='utf-8')
 # Separate the old tutorial's optional completeness path from the job design.
 parts=[text(540,40,['A2 tutorial','Existing interpretation and scoring path'],31,True)]
 nodes=[(110,285,'Offer data and tutorial files',['Offer text, recorded role and relevant context','Tutorial issue definitions and response format','Existing tutorial interpretation instructions']),
 (440,205,'Python script A2-T1',['Retrieves relevant tutorial issues and options','Builds the first model request (JSON)']),
 (690,205,'Economical LLM',['OpenAI GPT-5.6 Luna at low reasoning','Returns the first interpretation (JSON)']),
 (940,185,'Python script A2-T2',['Checks the existing dense-offer signal','If not dense, skips the second reading']),
 (1170,205,'Optional second Luna call',['Independently rereads the original offer','Checks completeness without seeing answer 1']),
 (1420,220,'Python script A2-T3',['Merges readings and flags disagreements','Applies existing tutorial checks and scores']),
 (1685,205,'Scored offer (JSON)',['Interpreted terms and role-specific scores','Questions and ideas retained without points'])]
 for i,(top,height,title,body) in enumerate(nodes):
  parts.append(box(145,top,790,height,title,body,core=i==6))
  if i<len(nodes)-1:parts.append(arrow(540,top+height+3,540,nodes[i+1][0]-5,'Dense offer' if i==3 else None))
 parts.append('<path d="M935,1030 L1045,1030 L1045,1530 L935,1530" fill="none" stroke="black" stroke-width="2.3" marker-end="url(#arrow)"/>')
 parts.append(text(1060,1260,['Skip','second','call'],24,anchor='start'))
 (OUT/'Figure_B2_Tutorial_Path.svg').write_text(svg(1170,1930,''.join(parts)),encoding='utf-8')
 (OUT/'Figure_Content.json').write_text(json.dumps(dict(main=MAIN,tutorial_nodes=nodes,script_numbering='The main labels map to A1-1.py, A1-2.py, A2-1.py and A2-2.py. Tutorial labels map separately to existing functions.'),ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'README.md').write_text('''# Architecture figures

`Figure_B1_NOVA_Architectures.svg` compares the latest evaluated job A1 and A2 configurations. `Figure_B2_Tutorial_Path.svg` shows the existing tutorial A2 path separately. SVG text and boxes can be edited in a vector editor. PNG copies are ready to inspect or insert into a manuscript.

Suggested caption: **Figure B1. NOVA scorer architecture templates.**

Suggested note: The language model identifies the proposed issues and options; Python scripts apply researcher-defined scores. A1 receives every active issue definition. A2 retrieves possible issues and uses fitted reading rules. The four main numbered script boxes correspond to `A1-1.py`, `A1-2.py`, `A2-1.py` and `A2-2.py`. The optional second tutorial reading is shown separately, not as part of the fitted one-call A2 job scorer.

`Architecture_Figure_Editable.docx` is the editable text-and-box master. Run `python tools/sync_figure_from_word.py` after editing it, then `python tools/build_figures_source.py` to update the SVG from `Figure_Content.json`. Rasterizing the SVG is a separate optional image step. `tools/build_word_figure_source.py` can build a fresh editable Word layout from the JSON, but should not be used to overwrite unsynchronized Word edits. The images contain no embedded figure number or caption.
''',encoding='utf-8')
 print(str(OUT))
if __name__=='__main__':main()
