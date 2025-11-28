import cliente 
import server
import principal
import asyncio

# Inicializa servidor e manda tabelas
async def main():
    p = principal.Principal()
    await p.executar()

asyncio.run(main())