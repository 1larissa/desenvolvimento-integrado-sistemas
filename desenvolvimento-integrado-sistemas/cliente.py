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
                return resp.status, texto
            
    
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
                
