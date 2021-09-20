import pandas as pd
import os

class ThreadById:

    def __init__(self, folder_subject, filename, thread_id):
        self.folder_subject = folder_subject
        self.filename = filename
        self.thread_id = thread_id

    def process(self):
        # Mapeamento de id da thread por id da mensagem 
        found_threads = []

        df = pd.read_csv(fr"./ChatRooms/{self.folder_subject}/{self.filename}/{self.filename}_threads_classificado.csv",  encoding='utf-8', sep = '|')

        # Remove messages without thread id
        messages_with_thread = df[df['DiscussionId'] != '['']' ]

        # Iterate rows csv
        for index, row in messages_with_thread.iterrows():
            threads_id = row['DiscussionId']

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

            if(self.thread_id in threads_array):
                found_threads.append(row)

        new_dataframe = pd.DataFrame(data=found_threads)

        # Create path to folder
        if not os.path.exists(f"./ChatRooms/{self.folder_subject}/{self.filename}/Consulta/ThreadsById"):
            os.makedirs(f"./ChatRooms/{self.folder_subject}/{self.filename}/Consulta/ThreadsById")

        # Save the CSV with the new data
        new_dataframe.to_csv(f"./ChatRooms/{self.folder_subject}/{self.filename}/Consulta/ThreadsById/thread_{self.thread_id}.csv", encoding='utf-8', index=False, sep = '|')

    def replace_all(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text