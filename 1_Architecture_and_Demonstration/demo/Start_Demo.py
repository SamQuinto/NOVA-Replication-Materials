"""Start a local NOVA scoring demonstration. Python 3.11 or newer; no packages needed."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import argparse,json,os,subprocess,sys,urllib.parse,webbrowser
ROOT=Path(__file__).resolve().parents[1]
CODE=ROOT/'code'

def local_environment():
    env=dict(os.environ)
    path=ROOT/'.env'
    if not env.get('OPENAI_API_KEY') and path.is_file():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if line.strip().startswith('OPENAI_API_KEY='):
                env['OPENAI_API_KEY']=line.split('=',1)[1].strip().strip('"\'')
    return env

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass # Never log offers, requests, or API keys.
    def send(self,value,status=200):
        body=json.dumps(value,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.path=='/api/status':return self.send({'key_ready':bool(local_environment().get('OPENAI_API_KEY'))})
        if self.path not in ['/','/index.html']:return self.send({'error':'Not found'},404)
        body=(ROOT/'demo/index.html').read_bytes();self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
    def do_POST(self):
        host=self.headers.get('Host','');origin=self.headers.get('Origin','')
        if host not in [f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'] or (origin and origin not in ['http://'+host]):return self.send({'error':'Only this local page may send requests.'},403)
        if self.path!='/api/score':return self.send({'error':'Not found'},404)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<40000:raise ValueError('Please use an offer shorter than 30,000 characters.')
            data=json.loads(self.rfile.read(length));exercise=data.get('exercise','job');architecture=data.get('architecture','A1');reasoning=data.get('reasoning','low')
            if exercise not in ['job','tutorial'] or architecture not in ['A1','A2'] or reasoning not in ['low','high']:raise ValueError('Invalid setting.')
            env=local_environment();live=bool(data.get('live'))
            if live and not env.get('OPENAI_API_KEY'):raise ValueError('Add your key to the local .env file, then try again.')
            args=[sys.executable,str(CODE/'nova_cli.py'),'--architecture',architecture,'--exercise',exercise,'--reasoning',reasoning]
            if live:
                offer=str(data.get('offer','')).strip();role=data.get('role','Candidate')
                if role not in ['Candidate','Recruiter'] or not offer:raise ValueError('Enter an offer and choose a role.')
                args+=['--offer',offer,'--role',role,'--previous-offer',str(data.get('previous_offer','')),'--live']
            else:args+=['--case-json',str(CODE/'examples'/(exercise+'_offer.json')),'--interpretation-json',str(CODE/'examples'/(exercise+'_interpretation.json'))]
            completed=subprocess.run(args,cwd=CODE,env=env,capture_output=True,text=True,encoding='utf-8',timeout=240)
            if completed.returncode:
                # Show a safe summary, not a traceback containing paths or credentials.
                message=completed.stderr.strip().splitlines()[-1] if completed.stderr.strip() else 'Scoring did not complete.'
                key=env.get('OPENAI_API_KEY','')
                if key:message=message.replace(key,'[key removed]')
                return self.send({'error':message},502)
            result=json.loads(completed.stdout)
            # Receipts are useful, but provider identifiers are not needed by the UI.
            for receipt in result.get('receipts',[]):receipt.pop('response_id',None)
            result['mode']='live' if live else 'saved example'
            if not live:result['example']=json.loads((CODE/'examples'/(exercise+'_offer.json')).read_text(encoding='utf-8'))
            self.send(result)
        except (ValueError,subprocess.TimeoutExpired) as exc:self.send({'error':str(exc) if isinstance(exc,ValueError) else 'The request timed out. It was not automatically repeated.'},400)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--port',type=int,default=8765);parser.add_argument('--no-browser',action='store_true');args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler);url=f'http://127.0.0.1:{server.server_port}/'
    print('NOVA demonstration: '+url,flush=True);print('Your key stays on this computer. Live calls incur API charges.',flush=True)
    if not args.no_browser:webbrowser.open(url)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
if __name__=='__main__':main()
