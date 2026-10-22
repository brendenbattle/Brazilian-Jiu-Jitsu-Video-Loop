"""Tiny local server: serves player/ at / and playlist.json. Stdlib only."""
import http.server, os, functools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split('?')[0]
        if p == '/playlist.json': return os.path.join(ROOT, 'playlist.json')
        return os.path.join(ROOT, 'player', p.lstrip('/') or 'index.html')
    def log_message(self, *a): pass
def run(port=8765):
    http.server.ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
if __name__ == '__main__': run()
