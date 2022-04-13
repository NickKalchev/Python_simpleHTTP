from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime
import json


def do_get_op(self):
    time_now = datetime.now()
    parsed_url = urlparse(self.path)
    get_arr = parse_qs(parsed_url.query)
    result = ""

    if 'a' not in get_arr:
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        js_arr = {"status": "error", "reason": "a not found in query string"}
        self.wfile.write(bytes(json.dumps(js_arr), "utf-8"))
    elif 'b' not in get_arr:
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        js_arr = {"status": "error", "reason": "b not found in query string"}
        self.wfile.write(bytes(json.dumps(js_arr), "utf-8"))
    elif 'op' not in get_arr:
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        js_arr = {"status": "error", "reason": "op not found in query string"}
        self.wfile.write(bytes(json.dumps(js_arr), "utf-8"))

    if get_arr['op'][0] == "*":
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        result = float(get_arr['a'][0]) * float(get_arr['b'][0])
    elif get_arr['op'][0] == "/":
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        result = float(get_arr['a'][0]) / float(get_arr['b'][0])
    elif get_arr['op'][0] == "-":
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        result = float(get_arr['a'][0]) - float(get_arr['b'][0])
    elif get_arr['op'][0] == "+":
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        result = float(get_arr['a'][0]) + float(get_arr['b'][0])

    js_arr = {"status": "ok", "date": time_now.strftime('%Y-%m-%d %H:%M'), "result": result}
    message = (json.dumps(js_arr)).encode('utf-8')
    self.wfile.write(bytes(message))
    print(get_arr)


class MiniHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        do_get_op(self)


if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8000), MiniHTTP)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped")

