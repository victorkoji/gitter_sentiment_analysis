import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import math

from config.config import Config
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

class Graph:

    def __init__(self, df, folder_name, filename):
        config = Config(folder_name, filename)
        self.file_path = config.get_path_graphs()
        self.df = df
        
        plt.rcParams.update({'figure.max_open_warning': 0})
        print("Started Generating Graphics")

    # Method to generate the graph with the amount of positive, neutral and positive messages.
    def generate_graph(self, classify):

        # Create folder
        if not os.path.exists(f"{self.file_path}"):
            os.makedirs(f"{self.file_path}")

        information = self.info_dataset()
        self.graph_quantity_by_sentiments(classify)
        self.graph_threads_by_messages(information['graph_thread_id'], information['graph_quantity_thread'])
        self.graph_threads_by_messages_by_sentiments(information['graph_classification_by_thread'])
        self.grafico_threads_por_mensagens_por_sentimentos_divido(information['graph_classification_by_thread'])
        self.graph_sentiments_by_month(information['graph_datetime_thread'])
        self.graph_signals_mapping_threads(information['graph_classification_by_thread'], information['route_threads_by_sentiments'])

    def info_dataset(self):
        graph_thread_id = []
        graph_quantity_thread = {}
        graph_datetime_thread = {}

        graph_classify_messages = []
        classification_mapping = {"Positive" : 1, "Neutral" : 0, "Negative" : -1}
        graph_classification_by_thread = {}

        # This variable will keep track of feelings within each threads.
        # Negative = -1 | Neutral = 0 | Positive = 1
        # Ex: Thread 1 = [0, 1, 0, 1, -1, -1]
        route_threads_by_sentiments = {}

        for index, row in self.df.iterrows():
            thread_array = row["thread_id"].replace("[", "").replace("]", "").replace(" ", "").split(",")

            date_time_str = row["datetime"]
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_year_month = date_time_obj.strftime("%m/%Y")

            if date_year_month in graph_datetime_thread: 
                graph_datetime_thread[date_year_month][row["classify"]] += 1
            else: 
                graph_datetime_thread[date_year_month] = {
                    'Ano': date_time_obj.strftime("%Y"), 
                    'Mes': date_time_obj.strftime("%m"), 
                    'Positive': 0, 
                    'Neutral': 0, 
                    'Negative': 0
                }
                graph_datetime_thread[date_year_month][row["classify"]] += 1

            if thread_array[0] == "":
                continue

            for thread_id in thread_array:
                graph_classify_messages.append(classification_mapping[row["classify"]])
                graph_thread_id.append(int(thread_id))

                if thread_id in graph_quantity_thread: 
                    graph_quantity_thread[thread_id] += 1

                    if row["classify"] in graph_classification_by_thread[thread_id]:
                        graph_classification_by_thread[thread_id][row["classify"]] += 1

                else: 
                    graph_quantity_thread[thread_id] = 1
                    graph_classification_by_thread[thread_id] = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    graph_classification_by_thread[thread_id][row["classify"]] += 1
                    
                    # Create thread position with empty array
                    route_threads_by_sentiments[thread_id] = []

                # Save the value of feelings for each thread
                route_threads_by_sentiments[thread_id].append(classification_mapping[row["classify"]])

        graph_classification_by_thread = pd.DataFrame(graph_classification_by_thread).T
        graph_datetime_thread = pd.DataFrame(graph_datetime_thread).T

        return {
            'graph_thread_id' : graph_thread_id, 
            'graph_quantity_thread' : graph_quantity_thread,
            'graph_datetime_thread' : graph_datetime_thread,
            'graph_classify_messages' : graph_classify_messages,
            'classification_mapping' : classification_mapping,
            'graph_classification_by_thread': graph_classification_by_thread,
            'route_threads_by_sentiments' : route_threads_by_sentiments
        }

    def graph_quantity_by_sentiments(self, classify):

        # Number of classified values: positive, neutral and negative.
        positive = classify.count('Positive')
        neutral = classify.count('Neutral')
        negative = classify.count('Negative')

        # Defines the amount of column and its values
        quantity_columns = np.arange(3)
        values = [positive, neutral, negative]

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('white')

        colors = ['green', 'grey', 'red']

        label_positive = mpatches.Patch(color='green', label='Positive')
        label_neutral = mpatches.Patch(color='grey', label='Neutral')
        label_negative = mpatches.Patch(color='red', label='Negative')
        
        plt.figure(figsize=(10, 10))
        plt.bar(quantity_columns, values, color=colors)
        plt.xticks(quantity_columns, ('Positive', 'Neutral', 'Negative'))
        plt.xlabel('Sentimentos', labelpad=25, fontsize=16)
        plt.ylabel('Números Mensagens', labelpad=25, fontsize=16)
        plt.legend(handles=[label_positive, label_neutral, label_negative], loc=1)

        # Save image
        plt.savefig(f"{self.file_path}/dataset_quantidade_sentimentos.png", transparent=False)
        plt.close(fig)


    ###################################
    #### Threads x Number messages ####
    def graph_threads_by_messages(self, graph_discussion_id, graph_discussion_contador_grafico):

        fig, ax = plt.subplots()
        x = np.arange(len(graph_discussion_id))
        
        plt.title('Threads X Números Mensagens')
        plt.xlabel('Threads')
        plt.ylabel('Números Mensagens')
        plt.figure(figsize=(10, 10))
        plt.xticks(x)

        ax.scatter(list(dict.fromkeys(graph_discussion_id)), list(graph_discussion_contador_grafico.values()))

        fig.savefig(f"{self.file_path}/threads_por_mensagens.png", transparent=False)
        plt.close(fig)

    ######################################
    #### Quantity Sentiments by Month ####
    def graph_sentiments_by_month(self, graph_datetime_thread):

        color_sentiments = {
            'Positive' : "green",
            'Neutral' : "grey",
            'Negative' : "red",
        }

        # Search every year
        years = graph_datetime_thread['Ano'].unique()

        for year in years:
            sentiments_by_year = graph_datetime_thread[graph_datetime_thread['Ano'] == year]

            # Number of classified values: positive, neutral and negative.
            sentiments = {
                "Positive" : sentiments_by_year['Positive'],
                "Neutral" : sentiments_by_year['Neutral'],
                "Negative" : sentiments_by_year['Negative'],
            }

            for key, quantity_sentiments in sentiments.items():

                fig, ax = plt.subplots()
                plt.subplots_adjust(left=0.12, bottom=0.2, right=0.95, top=0.9)
                plt.figure(figsize=(30, 40))

                x = np.arange(len(sentiments_by_year))

                ax.set_title(key, fontsize=14)
                ax.set_yticks(x)
                ax.set_yticklabels(sentiments_by_year.index, fontsize=8)

                ax.barh(x, quantity_sentiments, color=color_sentiments[key])

                ax.set_ylabel('Meses')
                ax.set_xlabel('Quantidade Sentimentos')

                # Create folder
                if not os.path.exists(f"{self.file_path}/sentimentos_anual"):
                    os.makedirs(f"{self.file_path}/sentimentos_anual")

                fig.savefig(f"{self.file_path}/sentimentos_anual/sentimentos_{key}_{year}_por_mes.png", transparent=False)
                plt.close(fig)

    #########################################
    #### Threads x Messages x Sentiments ####
    def graph_threads_by_messages_by_sentiments(self, graph_classification_by_thread):

        # Normalizar as Threads
        # graph_classification_by_thread = self.normalize_number_threads(graph_classification_by_thread)

        number_threads_by_graph = 50
        number_array = 0

        for num_threads in range(1, math.ceil(len(graph_classification_by_thread) / number_threads_by_graph) + 1):

            fig, ax = plt.subplots()
            plt.title('Threads x Números Mensagens x Classificacão')
            plt.xlabel('Threads')
            plt.ylabel('Números Mensagens')
            plt.figure(figsize=(20, 10))

            total_threads = num_threads * number_threads_by_graph

            if total_threads > len(graph_classification_by_thread):
                total_threads = len(graph_classification_by_thread)

            classification = graph_classification_by_thread[number_array : total_threads]

            # N = len(classification)
            positive = classification['Positive']
            negative = classification['Negative']
            neutral = classification['Neutral']
            ind = np.arange(number_array, total_threads)  
            width = 0.8

            ax.bar(ind, positive, width=width, label='Positive', align='center', color='green')
            ax.bar(ind, neutral, width=width, label='Neutral', align='center', color='grey')
            ax.bar(ind, negative, width=width, label='Negative', align='center', color='red')
            ax.legend()
            ax.set_xticks(np.arange(number_array, total_threads, 10))

            number_array = total_threads

            fig.savefig(f"{self.file_path}/threads_mensagens_sentimentos_{number_array}.png", format='png', transparent=False)
            plt.close(fig)

    ##############################################
    #### Signal Chart - Messages x Sentiments ####
    def graph_signals_mapping_threads(self, graph_classification_by_thread, route_threads_by_sentiments):

        # Calculate the median and identify the threads that are above the median
        median = graph_classification_by_thread['total'].median()
        # Filters only threads above the median
        highest_median_threads = graph_classification_by_thread[graph_classification_by_thread['total'] >= median]
        # Gets the thread ID list.
        threads_id = highest_median_threads.index

        for thread_id in threads_id:
            length = len(route_threads_by_sentiments[thread_id])

            # Get only messages from the specific thread
            x_axis_number_message = np.arange(0, len(route_threads_by_sentiments[thread_id]))
            # Get only sentiments from the specific thread
            y_axis_classification_sentiment = route_threads_by_sentiments[thread_id]
            scale_x = 5

            # Change scale according to size
            if length > 100:
                scale_x = 10

            fig, ax = plt.subplots()
            ax.plot(x_axis_number_message, y_axis_classification_sentiment)
            ax.set_xlabel('Percurso')
            ax.set_ylabel('Threads')
            plt.yticks([1, 0, -1])
            plt.xticks(range(0, length, scale_x))
            ax.grid(True)

            # Create path to folder
            if not os.path.exists(f"{self.file_path}/percurso_threads_sentimentos"):
                os.makedirs(f"{self.file_path}/percurso_threads_sentimentos")

            fig.savefig(f"{self.file_path}/percurso_threads_sentimentos/thread_{thread_id}.png", format='png', transparent=False)
            plt.close(fig)

    # Essa função irá separar por threads com mais de 50 mensagens e menos.
    def grafico_threads_por_mensagens_por_sentimentos_divido(self, graph_classification_by_thread):

        total = graph_classification_by_thread["Positive"] + graph_classification_by_thread["Neutral"] + graph_classification_by_thread["Negative"]
        graph_classification_by_thread["total"] = total
        threads_entre_50_100 = graph_classification_by_thread[(graph_classification_by_thread['total'] > 50) & (graph_classification_by_thread['total'] <= 100)]
        threads_maior_100 = graph_classification_by_thread[graph_classification_by_thread['total'] > 100]

        fig, ax = plt.subplots()
        plt.title('Threads x Números Mensagens x Classificacão')
        plt.xlabel('Threads')
        plt.ylabel('Números Mensagens')
        plt.figure(figsize=(20, 10))

        N = len(threads_entre_50_100)
        positive = threads_entre_50_100['Positive']
        negative = threads_entre_50_100['Negative']
        neutral = threads_entre_50_100['Neutral']
        ind = np.arange(0, N)  
        width = 0.8

        ax.bar(ind, positive, width=width, label='Positive', align='center', color='green')
        ax.bar(ind, neutral, width=width, label='Neutral', align='center', color='grey')
        ax.bar(ind, negative, width=width, label='Negative', align='center', color='red')
        ax.legend()
        ax.set_xticks(np.arange(0, N, 5))

        fig.savefig(f"{self.file_path}/threads_mensagens_sentimentos_entre_50_100.png", format='png', transparent=False)
        plt.close(fig)

        fig1, ax1 = plt.subplots()
        plt.title('Threads x Números Mensagens x Classificacão')
        plt.xlabel('Threads')
        plt.ylabel('Números Mensagens')
        plt.figure(figsize=(20, 10))

        N = len(threads_maior_100)
        positive = threads_maior_100['Positive']
        negative = threads_maior_100['Negative']
        neutral = threads_maior_100['Neutral']
        ind = np.arange(0, N)  
        width = 0.8

        ax1.bar(ind, positive, width=width, label='Positive', align='center', color='green')
        ax1.bar(ind, neutral, width=width, label='Neutral', align='center', color='grey')
        ax1.bar(ind, negative, width=width, label='Negative', align='center', color='red')
        ax1.legend()
        ax1.set_xticks(np.arange(0, N, 5))

        fig1.savefig(f"{self.file_path}/threads_mensagens_sentimentos_maior_100.png", format='png', transparent=False)
        plt.close(fig1)


    # Function to normalize the amount of feelings per thread
    def normalize_number_threads(self, graph_classification_by_thread):
        scaler = MinMaxScaler()
        
        x = graph_classification_by_thread.values
        x_scaled = scaler.fit_transform(x)
        graph_classification_by_thread = pd.DataFrame(x_scaled)
        graph_classification_by_thread.columns = ["Positive", "Neutral", "Negative"]

        return graph_classification_by_thread