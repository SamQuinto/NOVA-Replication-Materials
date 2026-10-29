"""Build editable black-and-white architecture diagrams from one content file."""
from pathlib import Path
import json,html,textwrap
W=Path(__file__).resolve().parents[1];OUT=W/'figures'

MAIN={
 'A1':dict(header=['A1  Flexible','Higher API cost'],boxes=[
  ('Offer data and exercise files',['Offer text and negotiator role (JSON)','Optional prior-offer context','Role materials and full table definitions','General prompt and response format']),
  ('Python script A1-1',['Builds one model request (JSON)','Includes every active issue and option','Keeps score calculation in Python']),
  ('Advanced LLM',['e.g., OpenAI GPT-6.1 Sol','Selects issues and options from the offer','Returns supporting words and questions']),
  ('Interpretation (JSON)',['Issues, options and quoted evidence','Clarification questions','Ideas retained without points']),
  ('Python script A1-2',['Checks evidence, options and values','Looks up researcher-defined scores','Prepares totals and follow-up messages']),
  ('Scored offer (JSON)',['Scores by issue and option','Role-specific totals when complete','Clarifications and unpriced ideas'])]),
 'A2':dict(header=['A2  Customized','Higher setup effort, lower API cost'],boxes=[
  ('Offer data and exercise files',['Offer text and negotiator role (JSON)','Optional prior-offer context','Role materials and fitted reading rules','Scoring table, vocabulary and format']),
  ('Python script A2-1',['Retrieves likely relevant table entries','Builds a request with their options','Includes exercise-specific reading notes']),
  ('Economical LLM',['e.g., OpenAI GPT-5.6 Luna','Selects supported issues and options','Returns supporting words and questions']),
  ('Interpretation (JSON)',['Issues, options and quoted evidence','Clarification questions','Ideas retained without points']),
  ('Python script A2-2',['Applies fitted exercise-specific rules','Checks the result and retrieves scores','Records which custom rules were used']),
  ('Scored offer (JSON)',['Scores by issue and option','Role-specific totals when complete','Clarifications and unpriced ideas'])])}

def esc(s):return html.escape(s)
def text(x,y,lines,size=28,bold=False,anchor='middle'):
 return '<text x="'+str(x)+'" y="'+str(y)+'" text-anchor="'+anchor+'" font-family="Arial, sans-serif" font-size="'+str(size)+'"'+(' font-weight="bold"' if bold else '')+'>'+''.join('<tspan x="'+str(x)+'" dy="'+('0' if i==0 else str(size*1.26))+'">'+esc(v)+'</tspan>' for i,v in enumerate(lines))+'</text>'
def box(x,y,w,h,title,body,core=False):
 parts=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="black" stroke-width="{3 if core else 1.8}"/>',text(x+w/2,y+42,[title],31,True)]
 ypos=y+85
 for line in body:
  wrapped=textwrap.wrap(line,width=int((w-54)/13),break_long_words=False)
  parts.append(text(x+27,ypos,['• '+wrapped[0]]+['  '+s for s in wrapped[1:]],27,anchor='start'));ypos+=34*len(wrapped)+8
 assert ypos<=y+h+5,(title,ypos,y+h)
 return ''.join(parts)
def arrow(x1,y1,x2,y2,label=None):
 s=f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="black" stroke-width="2.3" marker-end="url(#arrow)"/>'
 if label:s+=text(x1+18,(y1+y2)/2,[label],24,anchor='start')
 return s
def svg(width,height,body):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="black"/></marker></defs><rect width="100%" height="100%" fill="white"/>'+body+'</svg>'
def main():
 OUT.mkdir(exist_ok=True)
 heights=[285,215,220,220,230,220];ys=[];y=115
 for height in heights:ys.append(y);y+=height+45
 parts=[]
 for i,(key,col) in enumerate(MAIN.items()):
  x=35+i*750;cx=x+345;parts.append(text(cx,40,col['header'],31,True))
  for j,((title,body),top,height) in enumerate(zip(col['boxes'],ys,heights)):
   parts.append(box(x,top,690,height,title,body,core=j==5))
   if j<5:parts.append(arrow(cx,top+height+3,cx,ys[j+1]-5))
 (OUT/'Figure_2_Current_Architectures.svg').write_text(svg(1510,y-10,''.join(parts)),encoding='utf-8')
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
 (OUT/'Figure_Content.json').write_text(json.dumps(dict(main=MAIN,tutorial_nodes=nodes,script_numbering='Logical processing stages; not necessarily separate physical files.'),ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'README.md').write_text('''# Architecture figures

`Figure_2_Current_Architectures.svg` compares the latest evaluated job A1 and A2 configurations. `Figure_B2_Tutorial_Path.svg` shows the existing tutorial A2 path separately. SVG text and boxes can be edited in a vector editor. PNG copies are ready to inspect or insert into a manuscript.

Suggested caption: **Figure 2. Alternative scorer architectures in NOVA.**

Suggested note: The language model identifies the proposed issues and options; Python scripts apply researcher-defined scores. A1 receives every active issue definition. A2 retrieves possible issues and uses fitted reading rules. Script numbers identify processing stages rather than separate source files. The optional second tutorial reading is shown separately, not as part of the fitted one-call A2 job scorer.

`Figure_Content.json` is the common editable text source. `Architecture_Figure_Editable.docx` provides a native Word text-and-box version of the main comparison. The images contain no embedded figure number or caption.
''',encoding='utf-8')
 print(str(OUT))
if __name__=='__main__':main()
