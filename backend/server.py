from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from json import dumps, loads
from pathlib import Path
import sys
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ai.assistant import generate_reply


TASKS = [
    {
        "title": "Finalize launch checklist",
        "status": "In progress",
        "owner": "Mina",
        "due": "Tue",
        "details": "Confirm copy, assets, and release notes before the demo review.",
    },
    {
        "title": "Review feedback notes",
        "status": "Needs review",
        "owner": "Jordan",
        "due": "Wed",
        "details": "Collect the latest comments from the design review and trim duplicates.",
    },
    {
        "title": "Sync team priorities",
        "status": "Planned",
        "owner": "Avery",
        "due": "Fri",
        "details": "Turn the open discussion into a short list of next actions for the week.",
    },
]


class TeamboardHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_frontend(self):
        index_path = FRONTEND_DIR / "index.html"
        content = index_path.read_text(encoding="utf-8").encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        route = urlparse(self.path).path

        if route == "/api/tasks":
            self._send_json(200, TASKS)
            return

        if route in {"/", "/index.html"}:
            self._serve_frontend()
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        route = urlparse(self.path).path

        if route != "/api/assistant":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8")
        payload = loads(raw_body or "{}")
        message = payload.get("message", "")
        reply = generate_reply(message)
        self._send_json(200, {"reply": reply})

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), TeamboardHandler)
    print("Teamboard demo running at http://127.0.0.1:8000/")
    server.serve_forever()


if __name__ == "__main__":
    main()
