from solicitacao import Solicitacao 
import queue
import threading
import keyboard # pip install keyboard
from typing import Optional
import time
import matplotlib
matplotlib.use('Agg')  # faz matplotlib não depender do Tkinter
import matplotlib.pyplot as plt
import psutil #instala com pip install psutil
import numpy as np
from datetime import datetime
from typing import Optional
import numpy as np
import pandas as pd # pip install pandas
import time
from datetime import datetime
import os
from algoritmos import cgnr 
from algoritmos import cgne
from http.server import  HTTPServer as ServerH
from handler import Handler
from pathlib import Path

ARQUIVO_MATRIZ_H = 'H.csv' 
ARQUIVO_VETOR_G = 'g.csv' 
SEP_CHAR = ','

class Server:
    def __init__(self):
        # atributos para controlar a comunicacao
        self.fila_solicitacoes: queue.Queue = queue.Queue()
        self.fila_solicitacoes_prontas: queue.Queue = queue.Queue()
        self.fila_json = queue.Queue()
        # os numeros magicos
        self.LIMITE_MEMORIA_PERCENT = 85.0
        self.LIMITE_CPU_PERCENT = 85.0
        self.threads_ativas = 0
        self.MAX_THREADS = 4
        self.rodando=True

        self.id_solicitacao=0

    #inicia localhost
    def iniciarServidor(self):
        server = ServerH(
            ("localhost", 8000),
            lambda *args, **kwargs: Handler(*args, server_obj=self, **kwargs)
        )
        print("Servidor rodando em http://localhost:8000")
        server.serve_forever()
    
    def include_fila_json(self, dados):
        self.fila_json.put(dados)
    
    def percorre_fila_json(self):
        while self.rodando:
            try:
                dados = self.fila_json.get_nowait()
            except queue.Empty:
                time.sleep(0.01)  # evita usar 100% da CPU
                continue

            self.tratar_envio(dados)

    #trata json recebido pelo servidor
    def tratar_envio(self, dados):
        matriz = dados.get("matriz")
        sinal = dados.get("sinal")
        algoritmo_envio = dados.get("algoritmo")
        cliente = dados.get("cliente")

        # pega a pasta raiz do projeto, pra dar certo em qualquer pc
        PASTA_RAIZ = Path(__file__).resolve().parent
        
        #pasta das matrizes CSV
        PASTA_MATRIZ = PASTA_RAIZ / "CSV" / matriz

        #pasta dos sinais CSV
        PASTA_SINAL = PASTA_RAIZ / "sinais" / sinal

        #abre em pandas
        df_H = pd.read_csv(PASTA_MATRIZ, sep=SEP_CHAR, header=None)
        df_g = pd.read_csv(PASTA_SINAL, sep=SEP_CHAR, header=None)

        #converte pra numpy   
        H_teste = df_H.values
        g_teste = df_g.iloc[:, 0].values

        solicitacao_aux = Solicitacao(
            id_solicitacao=self.id_solicitacao, 
            linhas=H_teste.shape[0], 
            colunas=H_teste.shape[1], 
            algoritmo= algoritmo_envio,
            cliente= cliente
            )
        
        solicitacao_aux.matriz_H = H_teste
        solicitacao_aux.vetor_sinal_g = g_teste
        self.id_solicitacao += 1
        self.adicionarSolicitacao(solicitacao_aux)



    # Metodos de manipulacao de fila
    def adicionarSolicitacao(self, nova_solicitacao: Solicitacao):
        # Adiciona uma solicitação no final da fila
        self.fila_solicitacoes.put(nova_solicitacao)

    def obterProximaSolicitacao(self) -> Optional[Solicitacao]:
        # retorna e remove a solicitacao da fila
        try:
            solicitacao = self.fila_solicitacoes.get_nowait()
            return solicitacao
        except queue.Empty:
            return None # Fila vazia

    def _gerenciar_fila(self):
        while self.rodando:
            # Verifica o consumo atual
            cpu_total = psutil.cpu_percent(interval=None)
            memoria_percent = 100 - psutil.virtual_memory().percent
            
            if not self.fila_solicitacoes.empty():
                try:
                    proxima_solicitacao: Solicitacao = self.fila_solicitacoes.get_nowait()
                except queue.Empty:
                    continue # Fila estava vazia, continua o loop

                if self.threads_ativas >= self.MAX_THREADS:
                    # Devolve para a fila (mantém a ordem) e espera
                    self.fila_solicitacoes.put(proxima_solicitacao) 
                    print(f"Thread Pool Cheio ({self.threads_ativas}/{self.MAX_THREADS}). Aguardando...")
                    
                elif cpu_total >= self.LIMITE_CPU_PERCENT or memoria_percent >= self.LIMITE_MEMORIA_PERCENT:
                    # Retorna para a fila e espera
                    self.fila_solicitacoes.put(proxima_solicitacao) 
                    print(f"CPU em {cpu_total:.1f}%. Acima do limite. Aguardando...")

                else:
                    # Tem threads e cpu disponíveis
                    self.threads_ativas += 1
                    # Inicia a thread de processamento
                    threading.Thread(target=self._processar_imagem, args=(proxima_solicitacao,),daemon=True).start()
                    print(f"Iniciando processamento da {proxima_solicitacao.id}.")
            
            # Pausa pra não virar um loop "infinito"
            time.sleep(0.5)

    def _processar_imagem(self, solicitacao: Solicitacao):
        # executa o CGNR ou CGNE
        try:
            solicitacao.tempo_inicio = datetime.now()
            tempo_inicio_algoritmo = time.time()
            print("oie")
            print(solicitacao.algoritmo)
            # Chama a função CGNR/CGNE
            if solicitacao.algoritmo.upper() == 'CGNR':
                func = cgnr
            else:
                func = cgne

            f_result, num_iters, final_error = func(
                H=solicitacao.matriz_H, 
                g=solicitacao.vetor_sinal_g, 
                max_iterations=10,
                tol=1e-2, 
                min_iterations=1 
            )
            print("CGNR ok")
            tempo_fim_algoritmo = time.time()
            
            # Salva tudo
            solicitacao.tempo_fim = datetime.now()
            solicitacao.total_interacoes = num_iters
            solicitacao.tempo_reconstrucao_ms = (tempo_fim_algoritmo - tempo_inicio_algoritmo) * 1000
            solicitacao.imagem_reconstruida = f_result
            
            # Chama a função de salvamento e relatório
            self._salvar_imagem_e_relatorio(solicitacao)

            # Coloca a imagem processada na fila de resultados
            self.fila_solicitacoes_prontas.put(solicitacao)
            
        except Exception as e:
            print(f"Erro durante o processamento da solicitação {solicitacao.id}: {e}")
        
        finally:
            # Libera a thread sozinha quando finaliza a função, 
            # dai só diminui pra rodar outra
            self.threads_ativas -= 1
       
    def _salvar_imagem_e_relatorio(self, solicitacao: Solicitacao, filename_prefix="img"):
        f_vector = solicitacao.imagem_reconstruida
        tempo_ms = solicitacao.tempo_reconstrucao_ms
        iteracoes = solicitacao.total_interacoes
        
        n_pixels = len(f_vector)
        dimensao = int(np.sqrt(n_pixels))
        
        if dimensao * dimensao != n_pixels:
            print("Erro ao gerar as imagens")
            return

        # Normalização e Formatação
        f_min, f_max = f_vector.min(), f_vector.max()
        if f_max == f_min:
             print("Erro: imagem zerada.")
             return
            
        f_norm = (f_vector - f_min) / (f_max - f_min) * 255
        imagem_2d = f_norm.reshape((dimensao, dimensao))
        
        # cria a pasta de outputs
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        # salva a imagem
        filename = os.path.join(output_dir, f"{filename_prefix}_{solicitacao.id}.png")
        plt.figure(figsize=(6, 6))
        plt.imshow(imagem_2d, cmap='gray')
        plt.title(f"Reconstrução {solicitacao.algoritmo} ({dimensao}x{dimensao})")
        plt.xlabel(f"Tempo: {tempo_ms:.2f} ms | Itera: {iteracoes}")
        plt.savefig(filename)
        plt.close()
        print(f"{filename} salva.")

        # Relatório txt
        nome_relat = "relatorio_imagens.txt"
        try:
            with open(nome_relat, "a", encoding="utf-8") as f:
                f.write("---------------------------------------------------\n")
                f.write(f"ID da Solicitação: {solicitacao.id}\n")
                f.write(f"Algoritmo Utilizado: {solicitacao.algoritmo}\n")
                f.write(f"Tamanho em Pixels: {dimensao}x{dimensao}\n")
                f.write(f"Data/Hora Início: {solicitacao.tempo_inicio.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Data/Hora Término: {solicitacao.tempo_fim.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Iterações Executadas: {solicitacao.total_interacoes}\n")
                f.write(f"Tempo de Reconstrução: {solicitacao.tempo_reconstrucao_ms:.3f} ms\n")
                f.write(f"Sinal:")
                f.write("---------------------------------------------------\n")
        except Exception as e:
            print(f"Erro ao escrever no relatório")

    def run_in_Python(self):
        try:
            print("Carregando arquivos...")
            df_H = pd.read_csv(r"CSV\H-2.csv", sep=SEP_CHAR, header=None)
            df_g = pd.read_csv(r"sinais\4.csv", sep=SEP_CHAR, header=None)
            
            H_teste = df_H.values
            g_teste = df_g.iloc[:, 0].values

            solicitacao_teste = Solicitacao(
                id_solicitacao=999, 
                linhas=H_teste.shape[0], 
                colunas=H_teste.shape[1], 
                algoritmo='CGNR' #alterar conforme a solicitacao
            )
            solicitacao_teste.matriz_H = H_teste
            solicitacao_teste.vetor_sinal_g = g_teste

            # Executa o algoritmo na thread principal para teste,
            # no caso dps altera pra fazer com outras threads
            self._processar_imagem(solicitacao_teste)

        except FileNotFoundError as e:
            print(f"\nERRO: Arquivo {e.filename} não encontrado.")
        except Exception as e:
            print(f"\nERRO FATAL no processamento: {e}")
            
        return 0
