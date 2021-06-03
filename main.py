from src.pre_processamento import PreProcessamento
from src.identificar import Identificar
from src.classificar import Classificar
from src.analisar_threads import AnalisarThreads

import sys

class Main:
    
    def __init__(self):
        self.pasta_tema = input("Nome da pasta: ")
        self.nome_arquivo = input("Nome do arquivo: ")
    
    def processar(self):
        #Responsável por processar as mensagens e retirar texto irrelevantes para identificação de threads
        #Além disso, irá concatenar as mensagens adjacentes do mesmo usuário
        # PreProcessamento(self.pasta_tema, self.nome_arquivo).processar()

        #Identisfica as threads a partir das mensagens pré processadas
        # Identificar(self.pasta_tema, self.nome_arquivo).processar()

        #Classifica as mensagens como: Positive, Negative e Neutral
        Classificar(self.pasta_tema, self.nome_arquivo).processar()

        #Com o dados prontos, iremos analisar os dados que obtivemos procurando padrões e novas descobertas.
        # AnalisarThreads(self.pasta_tema, self.nome_arquivo).processar()
        
m = Main()
m.processar()