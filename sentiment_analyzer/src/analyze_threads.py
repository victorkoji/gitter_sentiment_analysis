import pandas as pd
import csv
import os

from config.config import Config

class AnalyzeThreads:

    def __init__(self, folder_name, filename):
        config = Config(folder_name, filename)
        self.file_path = config.get_path_prefix_filename()
        self.file_path_query_result = config.get_path_query_result()
        self.folder_name = folder_name
        self.filename = filename

    def process(self):
        # Thread id by message id mapping
        mapping_threads = {}
        df = pd.read_csv(fr"{self.file_path}_threads_classificado.csv",  encoding='utf-8', sep = '|')

        # These 2 objects will be used to save only the threads that start negative.
        mapping_threads_start_negative = {}
        mapping_old_threads = {}

        for index, row in df.iterrows():
            threads_id = row['thread_id']
            
            # Format string into array
            string = threads_id.replace(']','').replace('[','')
            threads_array = string.replace('"','').replace(' ','').split(",")

            # Cycle through thread id to save in dict
            for thread in threads_array:

                ###############################################################
                ###################### Normal Threads #########################
                if thread and mapping_threads.get(thread) != None:
                    mapping_threads[thread]['message_id']+= f",{row['id']}"         
                    mapping_threads[thread][row['classify']] += 1
                elif thread:
                    mapping_threads[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    mapping_threads[thread][row['classify']] += 1
                ###############################################################

                ####################################################################
                ################## Threads com inicio negativo #####################
                #Verificar não está vazia existe && Verificar se ela já foi inserida
                if thread and mapping_threads_start_negative.get(thread) != None :
                    mapping_threads_start_negative[thread]['message_id'] += f",{row['id']}"         
                    mapping_threads_start_negative[thread][row['classify']] += 1

                #Verificar não está vazia && Verificar se ela não apareceu em rows antigas
                elif thread and row['classify'] == "Negative" and mapping_old_threads.get(thread) == None :
                    mapping_threads_start_negative[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    mapping_threads_start_negative[thread][row['classify']] += 1
                else:
                    mapping_old_threads[thread] = {'thread_id': thread}
                ################## Threads com início negativo #####################
                ####################################################################

        # Create folder
        if not os.path.exists(self.file_path_query_result):
            os.makedirs(self.file_path_query_result)


        print(f"{self.file_path_query_result}/{self.filename}_threads_caminhos_iniciam_negativos.csv")

        # Saves the paths of each thread id in a CSV file
        with open(fr"{self.file_path_query_result}/{self.filename}_threads_caminhos.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|")
            w.writeheader()
            for item in mapping_threads.items():
                w.writerow(item[1])
                
        # Saves the paths of each thread id in a CSV file
        with open(fr"{self.file_path_query_result}/{self.filename}_threads_caminhos_iniciam_negativos.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|")
            w.writeheader()
            for item in mapping_threads_start_negative.items():
                w.writerow(item[1])