from http.server import BaseHTTPRequestHandler as requestH
from http.server import  HTTPServer as ServerH
import os

class Handler(requestH):##class de tratamento de request
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)

         # Caminho onde você quer salvar
        destino = r"C:\Users\admin\Desktop\Desen_sistemas\python_server\csv_recebido"

        # cria a pasta se não existir
        os.makedirs(destino, exist_ok=True)

        # caminho final do arquivo
        caminho_arquivo = os.path.join(destino, "recebido.csv")

        with open(caminho_arquivo, "wb") as f:
            f.write(body)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Arquivo recebido com sucesso")

server = ServerH(("localhost", 8000), Handler)
print("Servidor rodando em http://localhost:8000")
server.serve_forever()
