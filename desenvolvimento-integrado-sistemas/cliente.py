import aiohttp
import asyncio
import os
import json
import random
import datetime
import psutil

class Cliente:
    def __init__(self, base_url: str,nome_cliente:str=''):
        self.base_url = base_url
        self.session = None
        self.nome_cliente = nome_cliente

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
        
    async def enviar_json(self):
        url = f"{self.base_url}/upload"
        payload = self.define_json()


        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                status = resp.status
                texto = await resp.text()
                return resp.status, texto, payload
            
    def gera_relatorio(self,dados,tempo):
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # pega uso atual de CPU e memória
        cpu = psutil.cpu_percent(interval=None)            # ex: 23.5
        memoria = psutil.virtual_memory().percent          # ex: 64.2

        conteudo = (
            f"Data/Hora: {agora}\n"
            f"CPU (%): {cpu}\n"
            f"Memória (%): {memoria}\n"
            f"Cliente: {dados['cliente']}\n"
            f"Matriz: {dados['matriz']}\n"
            f"Sinal: {dados['sinal']}\n"
            f"Algoritmo: {dados['algoritmo']}\n"
            f"Tempo de envio (s): {tempo:.2f}\n"
        )

    
    def define_json(self):
        matriz = random.choice(["H-1.csv", "H-2.csv"])
        sinal = random.randint(1,3)
        algoritmo = random.choice(["CGNR", "CGNE"])

        print("o sinal é:", sinal)
        
        if(matriz == "H-2.csv"):
           sinal= sinal+3
        
        sinal = str(sinal)

        sinal = f"{sinal}.csv"

        dados = {
            "cliente": self.nome_cliente,
            "matriz": matriz,
            "sinal": sinal,
            "algoritmo": algoritmo
        }
        print(dados)
        return dados
                
