from src.query.get_thread_by_user import ThreadByUser

class Main:
    
    def __init__(self):
        self.folder_name = input("Folder name: ")
        self.filename = input("Filename: ")
        self.user = input("Username: ")
    
    def process(self):
        ThreadByUser(self.folder_name, self.filename, self.user).processar()

m = Main()
m.process()