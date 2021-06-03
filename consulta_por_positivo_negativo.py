from src.analisar_threads_positivo_negativo import AnalisarThreadsPositivoNegativo

import sys

class Main:
    
    def __init__(self):
        self.pasta_tema = input("Nome da pasta: ")
        self.nome_arquivo = input("Nome do arquivo: ")
    
    def processar(self):
        AnalisarThreadsPositivoNegativo(self.pasta_tema, self.nome_arquivo).processar()
        
m = Main()
m.processar()