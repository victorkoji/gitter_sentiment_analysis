import pandas as pd
import os
from config.config import Config

class ThreadById:

    def __init__(self, folder_name, filename, threads_id):
        config = Config(folder_name, filename)
        self.file_path_prefix = config.get_path_prefix_filename()
        self.file_query_result = config.get_path_query_result()
        self.folder_name = folder_name
        self.filename = filename
        self.threads_id = threads_id.split(",")

    def process(self):
        # Thread id by message id mapping
        found_threads = []

        df = pd.read_csv(fr"{self.file_path_prefix}_threads_classificado.csv",  encoding='utf-8', sep = '|')

        # Remove messages without thread id
        messages_with_thread = df[df['thread_id'] != '['']' ]

        for thread_id in self.threads_id:
            # Iterate rows csv
            for index, row in messages_with_thread.iterrows():
                threads_id = row['thread_id']

                removeString = { 
                    '[': '', 
                    ']': '', 
                    '"' : '', 
                    ' ' : ''
                }
                
                # Remove the brackets
                string = self.replace_all(threads_id, removeString)
                
                # Transform string to array
                threads_array = string.split(",")

                if(thread_id in threads_array):
                    found_threads.append(row)

            new_dataframe = pd.DataFrame(data=found_threads)

            # Create path to folder
            if not os.path.exists(f"{self.file_query_result}/Threads_by_id"):
                os.makedirs(f"{self.file_query_result}/Threads_by_id")

            # Save the CSV with the new data
            new_dataframe.to_csv(f"{self.file_query_result}/Threads_by_id/thread_{thread_id}.csv", encoding='utf-8', index=False, sep = '|')

    def replace_all(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text