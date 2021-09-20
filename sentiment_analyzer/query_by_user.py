from src.query.analisar_threads_por_usuario import AnalisarThreadsPorUsuario

class Main:
    
    def __init__(self):
        self.folder_name = input("Folder name: ")
        self.filename = input("Filename: ")
        self.user = input("Username: ")
    
    def process(self):
        AnalisarThreadsPorUsuario(self.folder_name, self.filename, self.user).processar()

m = Main()
m.process()