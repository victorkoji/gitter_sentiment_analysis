from src.preprocessing import Preprocessing
from src.identify_threads import IdentifyThreads
from src.classify import Classify
from src.analyze_threads import AnalyzeThreads
from config.config import Config

import os

class Main:
    
    def __init__(self):
        self.folder_name = ""
        self.filename = ""
    
    def processMenu(self): 

        print("1 - Projeto individual")
        print("2 - Todos os projetos dentro da pasta \"chat_rooms\" ")
        type_menu = input("Selecione o processamento a ser feito:")

    
        if type_menu == "1":
            self.folder_name = input("Folder name: ")
            self.filename = input("Filename: ")
            self.process()
            
        elif type_menu == "2":
            self.processAllFolder()


    def process(self):
        # Responsible for processing messages and removing irrelevant text for thread identification
        # Also, it will concatenate adjacent messages from the same user.
        # Preprocessing(self.folder_name, self.filename).process()

        # # Identify threads from preprocessed messages
        # IdentifyThreads(self.folder_name, self.filename).process()

        # Classify messages as: Positive, Negative and Neutral
        Classify(self.folder_name, self.filename).process()

        # Analyze the data we've obtained looking for patterns and new discoveries.
        # AnalyzeThreads(self.folder_name, self.filename).process()

    def processAllFolder(self):
        for folder_name in os.listdir("../chat_rooms"):
            for project in os.listdir(f"../chat_rooms/{folder_name}"):
                self.folder_name = folder_name
                self.filename = project

                # Responsible for processing messages and removing irrelevant text for thread identification
                # Also, it will concatenate adjacent messages from the same user.
                Preprocessing(self.folder_name, self.filename).process()

                # # Identify threads from preprocessed messages
                IdentifyThreads(self.folder_name, self.filename).process()

                # # Classify messages as: Positive, Negative and Neutral
                Classify(self.folder_name, self.filename).process()

                # Analyze the data we've obtained looking for patterns and new discoveries.
                AnalyzeThreads(self.folder_name, self.filename).process()
        
m = Main()
m.processMenu()