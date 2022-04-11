import pandas as pd
import csv
import os
import numpy as np

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
        # users_by_thread = {}

        for index, row in df.iterrows():
            threads_id = row['thread_id']
            # users_by_thread.add(row['username'])
            
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
                    mapping_threads[thread]['users'].add(row['username'])
                elif thread:
                    mapping_threads[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    mapping_threads[thread][row['classify']] += 1
                    mapping_threads[thread]['users'] = {row['username']}
                ###############################################################

                ####################################################################
                ################## Threads with start negative #####################
                # Check is not empty exists && Check if it has already been entered
                if thread and mapping_threads_start_negative.get(thread) != None :
                    mapping_threads_start_negative[thread]['message_id'] += f",{row['id']}"         
                    mapping_threads_start_negative[thread][row['classify']] += 1

                # Check is not empty && Check if it did not appear in old rows

                elif thread and row['classify'] == "Negative" and mapping_old_threads.get(thread) == None :
                    mapping_threads_start_negative[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    mapping_threads_start_negative[thread][row['classify']] += 1
                else:
                    mapping_old_threads[thread] = {'thread_id': thread}
                ################## Threads with start negative #####################
                ####################################################################

        self.generateCsvWithAboveMedian(mapping_threads)
        self.generateCsvThreadsPath(mapping_threads)
        self.generateCsvThreadsStartNegative(mapping_threads_start_negative)

    # Saves the paths of each thread id in a CSV file
    def generateCsvThreadsPath(self, mapping_threads):
        with open(fr"{self.file_path_query_result}/{self.filename}_threads_caminhos_gerais.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|", extrasaction='ignore')
            w.writeheader()
            for item in mapping_threads.items():
                w.writerow(item[1])

        
    # Saves the paths of each thread id in a CSV file
    def generateCsvThreadsStartNegative(self, mapping_threads_start_negative):
        with open(fr"{self.file_path_query_result}/{self.filename}_threads_caminhos_iniciam_negativos.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|", extrasaction='ignore')
            w.writeheader()
            for item in mapping_threads_start_negative.items():
                w.writerow(item[1])

    def generateCsvWithAboveMedian(self, mapping_threads):
        threads_to_save = []

        users_median = self.calculateMedianUsersByThreads(mapping_threads)
        messages_median = self.calculateMedianMessagesByThreads(mapping_threads)

        # Save only threads above the median 
        for key, item in mapping_threads.items():
            messages_array = item['message_id'].split(",")

            if len(item['users']) >= users_median and len(messages_array) >= messages_median:
                threads_to_save.append(item['thread_id'])

        with open(fr"{self.file_path_query_result}/{self.filename}_threads_caminhos_populares.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|", extrasaction='ignore')
            w.writeheader()

            for key, item in mapping_threads.items():
                if item['thread_id'] in threads_to_save:
                    w.writerow(item)


    def calculateMedianUsersByThreads(self, mapping_threads):
        total_users_by_threads = {}

        for key, item in mapping_threads.items():
            total_users_by_threads[item['thread_id']] = len(item['users'])

        median_users_by_threads = np.median(list(total_users_by_threads.values()))
        return median_users_by_threads

    def calculateMedianMessagesByThreads(self, mapping_threads):
        total_messages_by_threads = {}

        for key, item in mapping_threads.items():
            messages_array = item['message_id'].split(",")
            total_messages_by_threads[item['message_id']] = len(messages_array)

        median_messages_by_threads = np.median(list(total_messages_by_threads.values()))
        return median_messages_by_threads