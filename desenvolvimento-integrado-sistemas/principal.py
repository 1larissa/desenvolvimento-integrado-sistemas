import server
import threading
import cliente
import asyncio
import random
import time 
import sys

class Principal:
    def __init__(self):
        self.servidor = server.Server()
        self.clienteA = cliente.Cliente("http://localhost:8000",'A')
        self.clienteB = cliente.Cliente("http://localhost:8000",'B')
        self.clienteC = cliente.Cliente("http://localhost:8000",'C')
        
        # lista de clientes
        self.clientes = [self.clienteA, self.clienteB, self.clienteC]

    def iniciar_gerenciamento(self):
        thread_g = threading.Thread(target=self.servidor._gerenciar_fila, daemon=False)
        thread_g.start()

    def iniciar_percorredor_json(self):
        thread_json = threading.Thread(target=self.servidor.percorre_fila_json)
        thread_json.daemon = False
        thread_json.start()

    def inicia_servidor_thread(self):
        thread_servidor = threading.Thread(target=self.servidor.iniciarServidor)
        thread_servidor.daemon = True
        thread_servidor.start()
    
    async def enviar_json(self,cliente):
        async with cliente as c:
            status, resposta, payload = await c.enviar_json()
            return status, resposta
        
    async def loop_envio(self, cliente):
        for _ in range(10):
            inicio = time.time()
            delay = random.uniform(3, 4)
            await asyncio.sleep(delay)
            status, resposta = await self.enviar_json(cliente)
            fim = time.time()
            print(
                f"Status: {status}, Resposta: {resposta}, "
                f"Tempo de envio: {fim - inicio:.2f} segundos"
            )
            cliente.gera_relatorio(cliente.define_json(), fim - inicio)
        
    async def executar(self):
        self.inicia_servidor_thread()

        tarefaA = asyncio.create_task(self.loop_envio(self.clienteA))
        tarefaB = asyncio.create_task(self.loop_envio(self.clienteB))
        tarefaC = asyncio.create_task(self.loop_envio(self.clienteC))

        self.iniciar_percorredor_json()

        self.iniciar_gerenciamento()

        await asyncio.gather(tarefaA, tarefaB, tarefaC)
