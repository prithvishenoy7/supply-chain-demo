from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"supply-chain-demo: healthy\n")

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    HTTPServer(("", 8080), Handler).serve_forever()
