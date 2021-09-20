from src.query.get_threads_positive_negative import ThreadsPositiveNegative

import sys

class Main:
    
    def __init__(self):
        self.folder_name = input("Folder name: ")
        self.filename = input("Filename: ")
    
    def processar(self):
        ThreadsPositiveNegative(self.folder_name, self.filename).processar()
        
m = Main()
m.processar()