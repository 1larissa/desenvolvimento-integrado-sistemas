from typing import List
from datetime import datetime
import numpy as np

class Solicitacao:
    # struct global da solicitacao de reconstrucao de imagem
    def __init__(self, id_solicitacao: int=0, linhas: int=0, colunas: int=0,
                  algoritmo: str='',cliente: str='', sinal_n: str='', csv: str=''):
        self.id = id_solicitacao
        self.linhas = linhas
        self.colunas = colunas
        self.algoritmo = algoritmo
        self.cedido = 0 # Quantas vezes cedeu a vez
        self.tempo_inicio: datetime = datetime.now()
        self.tempo_fim: datetime = None
        self.total_interacoes: int = 0
        self.tempo_total_reconstrucao: float = 0.0 # em ms
        self.imagem_reconstruida: np.ndarray = None
        self.cliente = cliente
        self.sinal_n=sinal_n
        self.csv=csv

    # def __lt__(self, other):
    #     """Define prioridade para uso em PriorityQueue (para a lógica de cedência)"""

    #     # A prioridade será dada ao item que cedeu mais vezes (menor 'cedido' vem primeiro)
    #     # Se os dois cederam o mesmo número de vezes, prioriza o mais antigo (menor timestamp)
    #     return (self.cedido, self.tempo_inicio) < (other.cedido, other.tempo_inicio)

