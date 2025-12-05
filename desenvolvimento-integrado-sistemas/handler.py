import os
from http.server import BaseHTTPRequestHandler
import json
import queue

class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, server_obj=None, **kwargs):
        self.meu_server = server_obj 
        super().__init__(*args, **kwargs)


    def do_POST(self):
        content_type = self.headers.get("Content-Type", "")
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        body_str = body.decode("utf-8")
        
        try:
            dados = json.loads(body_str)

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            print("json invalido")
            return
        
        self.meu_server.include_fila_json(dados)

        # resposta HTTP
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Json recebido")