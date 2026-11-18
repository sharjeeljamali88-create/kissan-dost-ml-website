"""Run the website locally without installing any packages: python server.py"""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import webbrowser
if __name__=='__main__':
 root=Path(__file__).resolve().parent/'dist'
 print('Kisan Dost: http://127.0.0.1:8000 (Ctrl+C to stop)',flush=True)
 webbrowser.open('http://127.0.0.1:8000')
 ThreadingHTTPServer(('127.0.0.1',8000),partial(SimpleHTTPRequestHandler,directory=str(root))).serve_forever()
