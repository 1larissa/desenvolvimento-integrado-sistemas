import server
import threading
import cliente
import asyncio
import random
import time 

class Principal:
    def __init__(self):
        self.servidor = server.Server()
        self.clienteA = cliente.Cliente("http://localhost:8000",'A')
        self.clienteB = cliente.Cliente("http://localhost:8000",'B')
        self.clienteC = cliente.Cliente("http://localhost:8000",'C')
        self.rodando = True
        
        # lista de clientes
        self.clientes = [self.clienteA, self.clienteB, self.clienteC]

    #para parar loop de envios
    def monitorar_tecla(self):
        while self.rodando:
            tecla = input()
            if tecla.strip().upper() == "D":
                print("parando loop...")
                self.rodando = False
                break
    
    #monitora tecla por thread
    def inicia_monitoramento(self):
        thread = threading.Thread(target=self.monitorar_tecla, daemon=True)
        thread.start()


    def inicia_servidor_thread(self):
        thread_servidor = threading.Thread(target=self.servidor.iniciarServidor)
        thread_servidor.daemon = True
        thread_servidor.start()
    
    async def enviar_json(self,cliente):
        async with cliente as c:
            status, resposta = await c.enviar_json()
            return status, resposta
    
    async def executar(self):
        self.inicia_servidor_thread()

        self.inicia_monitoramento() 

        while self.rodando:

            tempo=time.time()
            
            #fica travado esperando entre 3 a 5 segundos
            #await asyncio.sleep(random.randint(3, 5))
            #escolhe um cliente aleatoriamente
            cliente = random.choice(self.clientes)

            status, resposta = await self.enviar_json(cliente)
            tempo=time.time()-tempo
            print(f"Status: {status}, Resposta: {resposta}, Tempo de envio: {tempo:.2f} segundos")
        