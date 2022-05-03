import pandas as pd
import csv, os
from config.config import Config

class ThreadByUser:

    def __init__(self, folder_name, filename, user):
        config = Config(folder_name, filename)
        self.file_path_prefix = config.get_path_prefix_filename()
        self.file_query_result = config.get_path_query_result()
        self.folder_name = folder_name
        self.filename = filename
        self.user = user

    def processar(self):
        # Thread id by message id mapping
        threads_caminhos = {}

        # These 2 dicts I will use to save only the threads that start negative.
        threads_caminhos_iniciam_negativas = {}
        threads_caminhos_antigos = {}

        # View data
        df = pd.read_csv(fr"{self.file_path_prefix}/{self.filename}_threads_classificado.csv",  encoding='utf-8', sep = '|')

        userMessages = df[df['username'] == self.user]

        for index, row in userMessages.iterrows():
            threads_id = row['thread_id']
            
            # Format string to array
            string = threads_id.replace(']','').replace('[','')
            threads_array = string.replace('"','').replace(' ','').split(",")

            # Cycle through thread id to save in dictionary
            for thread in threads_array:

                #####################################################################
                ################## Threads with negative start ######################
                # Check is not empty exists && Check if it has already been entered
                if thread and threads_caminhos_iniciam_negativas.get(thread) != None :
                    threads_caminhos_iniciam_negativas[thread]['message_id'] += f",{row['id']}"         
                    threads_caminhos_iniciam_negativas[thread][row['classify']] += 1

                # Check is not empty && Check if it did not appear in old rows
                elif thread and row['classify'] == "Negative" and threads_caminhos_antigos.get(thread) == None :
                    threads_caminhos_iniciam_negativas[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    threads_caminhos_iniciam_negativas[thread][row['classify']] += 1
                else:
                    threads_caminhos_antigos[thread] = {'thread_id': thread}
                ################## Threads with negative start ######################
                #####################################################################

                ##############################################################
                ################### Normal Thread Paths ######################
                if thread and threads_caminhos.get(thread) != None:
                    threads_caminhos[thread]['message_id']+= f",{row['id']}"         
                    threads_caminhos[thread][row['classify']] += 1
                elif thread:
                    threads_caminhos[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    threads_caminhos[thread][row['classify']] += 1
                ##############################################################


        # Create path to folder
        if not os.path.exists(f"{self.file_query_result}/Threads_by_users"):
            os.makedirs(f"{self.file_query_result}/Threads_by_users")

        # Saves the paths of each thread id in a CSV file
        with open(fr"{self.file_query_result}/Threads_by_users/threads_{self.user}.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|")
            w.writeheader()
            for item in threads_caminhos.items():
                w.writerow(item[1])
                
        # Saves the paths of each thread id in a CSV file
        with open(fr"{self.file_query_result}/Threads_by_users/threads_{self.user}_iniciam_negativos.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|")
            w.writeheader()
            for item in threads_caminhos_iniciam_negativas.items():
                w.writerow(item[1])
                
