from src.analisar_threads_por_usuario import AnalisarThreadsPorUsuario

import sys

class Main:
    
    def __init__(self):
        self.pasta_tema = input("Nome da pasta: ")
        self.nome_arquivo = input("Nome do arquivo: ")
        self.usuario = input("Nome do usuário: ")
    
    def processar(self):
        AnalisarThreadsPorUsuario(self.pasta_tema, self.nome_arquivo, self.usuario).processar()
        
m = Main()
m.processar()