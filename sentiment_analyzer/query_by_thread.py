from src.query.get_thread_by_id import ThreadById

class Main:
    
    def __init__(self):
        self.folder_name = input("Folder name: ")
        self.filename = input("Filename: ")
        self.thread_id = input("Threads ID: ")
    
    def process(self):
        ThreadById(self.folder_name, self.filename, self.thread_id).process()

m = Main()
m.process()