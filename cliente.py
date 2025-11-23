# import aiohttp
# import asyncio
# import os

# class Cliente:
#     def __init__(self, base_url: str):
#         self.base_url = base_url
#         self.session = None

#     async def __aenter__(self):
#         self.session = aiohttp.ClientSession()
#         return self

#     async def __aexit__(self, exc_type, exc, tb):
#         await self.session.close()

#     async def enviar_csv(self, caminho_csv: str):
#         # validação simples
#         if not os.path.exists(caminho_csv):
#             raise FileNotFoundError(f"Arquivo não encontrado: {caminho_csv}")

#         url = f"{self.base_url}/upload"

#         with open(caminho_csv, "rb") as f:
#             form = aiohttp.FormData()
#             form.add_field(
#                 "file",
#                 f,
#                 filename=os.path.basename(caminho_csv),
#                 content_type="text/csv"
#             )

#             async with self.session.post(url, data=form) as resp:
#                 status = resp.status
#                 texto = await resp.text()
#                 return status, texto


# # =============================
# # Exemplo de uso
# # =============================
# async def main():
#     tabela = r"C:\Users\admin\Desktop\Desen_sistemas\python_server\cliente\CSV\H-1.csv"

#     async with Cliente("http://localhost:8000") as client:

#         status, resposta = await client.enviar_csv(tabela)
#         print("Status:", status)
#         print("Resposta:", resposta)

# asyncio.run(main())
