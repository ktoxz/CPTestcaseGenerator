"""Optional private Windows→WSL proxy for loopback-only Ollama."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.client_address[0] != self.server.allowed_client or self.path != "/api/chat":
            self.send_error(403)
            return
        size = int(self.headers.get("Content-Length", "0"))
        if size <= 0 or size > 2_000_000:
            self.send_error(413)
            return
        request = Request(self.server.upstream.rstrip("/") + "/api/chat", data=self.rfile.read(size),
                          headers={"Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=660) as upstream:
                body, status = upstream.read(), upstream.status
        except HTTPError as error:
            body, status = error.read(), error.code
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    root = Path(__file__).resolve().parents[1]
    settings = json.loads((root / "config" / "pipeline.json").read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", required=True, help="Windows vEthernet IP shown as WSL default gateway")
    parser.add_argument("--allow", required=True, help="Exact WSL eth0 IP")
    parser.add_argument("--port", type=int, default=11435)
    parser.add_argument("--upstream", default=settings["ollama_url"])
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.bind, args.port), Handler)
    server.allowed_client = args.allow
    server.upstream = args.upstream
    server.serve_forever()


if __name__ == "__main__":
    main()
