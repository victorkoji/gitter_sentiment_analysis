import pandas as pd
import csv, os
from config.config import Config

class ThreadByUser:

    def __init__(self, folder_name, filename, user):
        config = Config(folder_name, filename)
        self.file_path = config.get_path_prefix_filename()
        self.file_query_result = config.get_path_query_result()
        self.folder_name = folder_name
        self.filename = filename
        self.user = user

    def processar(self):
        #Mapeamento de id da thread por id da mensagem 
        threads_caminhos = {}

        #Essas 2 objetos irei utilizar para salvar somente as threads que iniciam negativas.
        threads_caminhos_iniciam_negativas = {}
        threads_caminhos_antigos = {}

        #Visualizando os dados:
        df = pd.read_csv(fr"{self.file_path}_threads_classificado.csv",  encoding='utf-8', sep = '|')

        userMessages = df[df['username'] == self.user]

        #Percorre todas as linhas do CSV
        for index, row in userMessages.iterrows():
            threads_id = row['thread_id']
            
            #Formata a string em array
            string = threads_id.replace(']','').replace('[','')
            threads_array = string.replace('"','').replace(' ','').split(",")

            #Percorre os id das threads para salvar no dicionário
            for thread in threads_array:

                ####################################################################
                ################## Threads com início negativo ######################
                #Verificar não está vazia existe && Verificar se ela já foi inserida
                if thread and threads_caminhos_iniciam_negativas.get(thread) != None :
                    threads_caminhos_iniciam_negativas[thread]['message_id'] += f",{row['id']}"         
                    threads_caminhos_iniciam_negativas[thread][row['classify']] += 1

                #Verificar não está vazia && Verificar se ela não apareceu em rows antigas
                elif thread and row['classify'] == "Negative" and threads_caminhos_antigos.get(thread) == None :
                    threads_caminhos_iniciam_negativas[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    threads_caminhos_iniciam_negativas[thread][row['classify']] += 1
                else:
                    threads_caminhos_antigos[thread] = {'thread_id': thread}
                ################## Threads com início negativo ######################
                ####################################################################

                #######################################################################
                ################### Caminhos das Threads normais ######################
                if thread and threads_caminhos.get(thread) != None:
                    threads_caminhos[thread]['message_id']+= f",{row['id']}"         
                    threads_caminhos[thread][row['classify']] += 1
                elif thread:
                    threads_caminhos[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    threads_caminhos[thread][row['classify']] += 1
                ######################################################################


        # Create path to folder
        if not os.path.exists(f"{self.file_query_result}/ThreadsByUsers"):
            os.makedirs(f"{self.file_query_result}/ThreadsByUsers")

        #Salva em um arquivo CSV os caminhos de cada id da thread
        with open(fr"{self.file_query_result}/ThreadsByUsers/threads_{self.user}.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|")
            w.writeheader()
            for item in threads_caminhos.items():
                w.writerow(item[1])
                
        #Salva em um arquivo CSV os caminhos de cada id da thread
        with open(fr"{self.file_query_result}/ThreadsByUsers/threads_{self.user}_iniciam_negativos.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|")
            w.writeheader()
            for item in threads_caminhos_iniciam_negativas.items():
                w.writerow(item[1])
                
