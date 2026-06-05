"""
logbook/serve.py
================
Simple local HTTP server for the BIT4133 NLP Logbook download page.

Usage:
    python logbook/serve.py

Then open:  http://localhost:8080
Click the green button to download Smart_Farm_Logbook.docx
"""

import http.server
import socketserver
import os
import webbrowser
import threading

PORT = 8080
LOGBOOK_DIR = os.path.dirname(os.path.abspath(__file__))


class SilentHandler(http.server.SimpleHTTPRequestHandler):
    """Serve files from the logbook/ directory with minimal log noise."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=LOGBOOK_DIR, **kwargs)

    def log_message(self, format, *args):
        # Only log actual requests (suppress routine noise)
        if args and "200" in str(args[1]):
            print(f"  [served] {args[0]}")


def open_browser():
    """Open the download page in the default browser after a short delay."""
    import time
    time.sleep(0.8)
    url = f"http://localhost:{PORT}"
    print(f"\n  Opening browser at {url} ...")
    webbrowser.open(url)


if __name__ == "__main__":
    print()
    print("=" * 56)
    print("  BIT4133 NLP Logbook — Local Download Server")
    print("=" * 56)
    print(f"\n  Serving files from:  {LOGBOOK_DIR}")
    print(f"  Download page URL :  http://localhost:{PORT}")
    print()
    print("  Press Ctrl+C to stop the server.")
    print()

    # Open browser automatically
    threading.Thread(target=open_browser, daemon=True).start()

    with socketserver.TCPServer(("", PORT), SilentHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n  Server stopped. Goodbye!")
