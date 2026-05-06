#!/usr/bin/env python3
"""
serve.py  –  Serves the Expense Tracker web UI on http://localhost:8000

Run this alongside api.py:
    Terminal 1:  python api.py
    Terminal 2:  python serve.py
Then open http://localhost:8000 in your browser.

NOTE: Rename the HTML file to  expense_tracker.html  (remove the space and
      parentheses) so the URL http://localhost:8000/ works cleanly.
      If you keep the original filename, the redirect below still works.
"""

import http.server
import socketserver
import os
import glob

PORT      = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Auto-detect the HTML file (works with any name variation)
def find_html():
    candidates = [
        "expense_tracker.html",                 # preferred renamed file
        "expense_tracker_gui.html",
        "expense_tracker_gui (1).html",         # original name
    ]
    for name in candidates:
        if os.path.exists(os.path.join(DIRECTORY, name)):
            return name
    # Fallback: first .html file found
    hits = glob.glob(os.path.join(DIRECTORY, "*.html"))
    return os.path.basename(hits[0]) if hits else None


HTML_FILE = find_html()


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Redirect bare / to the HTML file
        if self.path in ("/", ""):
            self.path = "/" + HTML_FILE if HTML_FILE else "/index.html"
        return super().do_GET()

    def end_headers(self):
        # Allow the browser to send credentials (cookies) cross-origin to Flask
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Suppress per-request noise; show only errors
        if args[1] not in ("200", "304"):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    if not HTML_FILE:
        print("❌  No HTML file found in", DIRECTORY)
        raise SystemExit(1)

    os.chdir(DIRECTORY)
    print(f"✅  Web UI  →  http://localhost:{PORT}")
    print(f"📄  Serving: {HTML_FILE}")
    print(f"🔗  Make sure api.py is running at http://localhost:5000")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
