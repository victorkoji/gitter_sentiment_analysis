import pandas as pd
import csv, os
from config.config import Config

class ThreadsPositiveNegative:

    def __init__(self, folder_name, filename):
        config = Config(folder_name, filename)
        self.file_path_prefix = config.get_path_prefix_filename()
        self.file_query_result = config.get_path_query_result()
        self.folder_name = folder_name
        self.filename = filename

    def processar(self):
        # Thread id by message id mapping
        threads_classificacao = {}
        threads_nao_utilizar = {}

        # View data
        dataset_classificado = pd.read_csv(fr"{self.file_path_prefix}_threads_classificado.csv",  encoding='utf-8', sep = '|')

        for index, row in dataset_classificado.iterrows():
            message_id = row['thread_id'].replace("[", "").replace("]", "").replace(" ", "").split(",")

            # Search only messages that have threads
            if(message_id[0]):
                for discussion_id in message_id:

                    # threads that should be disregarded
                    if discussion_id not in threads_nao_utilizar:

                        # Check if this thread does not already exist in the mapping
                        if discussion_id not in threads_classificacao:

                            if row['classify'] == "Negative":
                                threads_classificacao[discussion_id] = {
                                    'thread_id': discussion_id,
                                    'message_id': row['id'],
                                    'Positive': 0, 'Neutral': 0, 'Negative': 0,
                                    'first_message' : row['classify']
                                }
                            else:
                                threads_nao_utilizar[discussion_id] = True

                        # Check if this thread does not already exist in the mapping
                        else:
                            threads_classificacao[discussion_id]['last_message'] = row['classify']

                        # Keeps the message's rating and id
                        if discussion_id not in threads_nao_utilizar:
                            # Count thread classification
                            threads_classificacao[discussion_id][row['classify']] += 1
                            threads_classificacao[discussion_id]['message_id'] += f",{row['id']}"      

        # Cycles through the records leaving only threads that start negative and finish positive
        for index, item in threads_classificacao.copy().items():
            if item['last_message'] != "Positive":
                threads_classificacao.pop(index)

        # Create path to folder
        if not os.path.exists(f"{self.file_query_result}/threads_positive_negative"):
            os.makedirs(f"{self.file_query_result}/threads_positive_negative")

        # Saves the paths of each thread id to a CSV file
        with open(fr"{self.file_query_result}/threads_positive_negative/threads_caminhos_positivo_negativo.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative', 'first_message', 'last_message'], delimiter="|")
            w.writeheader()
            for item in threads_classificacao.items():
                w.writerow(item[1])