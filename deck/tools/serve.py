#!/usr/bin/env python3
"""Serve the repo for presenting: http://127.0.0.1:8000/deck/ (no caching, so edits show on reload)."""
import functools, http.server
from pathlib import Path

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, *a):
        pass

root = Path(__file__).resolve().parents[2]
http.server.ThreadingHTTPServer(('127.0.0.1', 8000), functools.partial(NoCache, directory=str(root))).serve_forever()
