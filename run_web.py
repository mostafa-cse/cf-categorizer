"""Web Server Launcher for Codeforces Categorizer."""

import os
import sys
import socket
import webbrowser
import uvicorn

# Ensure UTF-8 console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from src import db
from src.server import app


def find_available_port(default_port: int = 8000) -> int:
    for port in [default_port, 8080, 5000, 3000, 8888, 8001]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return default_port


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run Codeforces Categorizer Web Application")
    parser.add_argument('--port', type=int, default=8000, help="Port to bind (default: 8000)")
    parser.add_argument('--host', type=str, default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument('--no-browser', action='store_true', help="Do not automatically launch web browser")
    args = parser.parse_args()

    # Ensure DB tables exist
    db.init_db()

    port = find_available_port(args.port)
    url = f"http://{args.host}:{port}"

    print("=" * 65)
    print("        🚀 CODEFORCES CATEGORIZER WEB APPLICATION 🚀       ")
    print("=" * 65)
    print(f"[*] Server starting on: {url}")
    print("[*] 576-Technique CP Taxonomy Explorer & Interactive Problem Viewer")
    print("[*] Press Ctrl+C anytime to stop the server.")
    print("=" * 65)

    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    uvicorn.run(app, host=args.host, port=port, log_level="info")


if __name__ == '__main__':
    main()
