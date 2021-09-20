from src.Query.analisar_threads_positivo_negativo import AnalisarThreadsPositivoNegativo

import sys

class Main:
    
    def __init__(self):
        self.folder_name = input("Folder name: ")
        self.filename = input("Filename: ")
    
    def processar(self):
        AnalisarThreadsPositivoNegativo(self.folder_name, self.filename).processar()
        
m = Main()
m.processar()