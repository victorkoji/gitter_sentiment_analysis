import sys, os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from config.config import Config

class GeneralGraph:
    def __init__(self):
        
        self.file_path_general_graph = "../data/general_information/general_graphs"

        # Create folder
        if not os.path.exists(f"{self.file_path_general_graph}"):
            os.makedirs(f"{self.file_path_general_graph}")
            
        plt.rcParams.update({'figure.max_open_warning': 0})
        print("Started Generating General Graphics")

    def generate(self):

        # self.graph_sentiments_by_month()
        self.graph_quantity_by_sentiments_general_threads()
        self.graph_quantity_by_sentiments_popular_threads()

    def graph_quantity_by_sentiments_general_threads(self):

        for folder_name in os.listdir("../data/chat_rooms"):
            count_projects = len(next(os.walk(f"../data/chat_rooms/{folder_name}"))[1]);

            fig, ax = plt.subplots(1, count_projects, figsize=(15, 3))
            fig.set_figheight(4)
            fig.patch.set_facecolor('white')

            num_graph = 0

            for project in os.listdir(f"../data/chat_rooms/{folder_name}"):
                
                config = Config(folder_name, project)
                file_path_prefix = config.get_path_prefix_filename()

                df = pd.read_csv(f"{file_path_prefix}_threads_classificado.csv", usecols = ['id', 'classify'], encoding='utf-8', sep = '|')
                classify = df['classify'].value_counts().to_dict()

                # Number of classified values: positive, neutral and negative.
                positive = classify['Positive']
                neutral = classify['Neutral']
                negative = classify['Negative']

                # Defines the amount of column and its values
                quantidade_sentimentos = [positive, neutral, negative]

                colors = ['#65fb6a', 'lightgrey', 'lightcoral']
                explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                ax[num_graph].set_title(project, y=1.0, pad=-30)
                ax[num_graph].pie(quantidade_sentimentos, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 8})
                ax[num_graph].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                num_graph = num_graph + 1

            labels = ['Positiva', 'Neutra', 'Negativa']
            ax[0].legend(labels=labels, loc='best', bbox_to_anchor=(0, 0.5))

            fig.suptitle('Distribuição dos Sentimentos em Threads Genéricas', fontsize=16)

            # Create folder
            if not os.path.exists(f"{self.file_path_general_graph}/{folder_name}"):
                os.makedirs(f"{self.file_path_general_graph}/{folder_name}")

            # Save image
            plt.savefig(f"{self.file_path_general_graph}/{folder_name}/dataset_quantidade_sentimentos_threads_gerais.png", transparent=False)
            plt.close(fig)

    def graph_quantity_by_sentiments_popular_threads(self):

        for folder_name in os.listdir("../data/chat_rooms"):
            count_projects = len(next(os.walk(f"../data/chat_rooms/{folder_name}"))[1]);

            fig, ax = plt.subplots(1, count_projects, figsize=(15, 3))
            fig.set_figheight(4)
            fig.patch.set_facecolor('white')

            num_graph = 0

            for project in os.listdir(f"../data/chat_rooms/{folder_name}"):
                
                config = Config(folder_name, project)
                file_path_prefix = config.get_path_query_result()

                classify = pd.read_csv(f"{file_path_prefix}/{project}_threads_caminhos_populares.csv", usecols = ['thread_id', 'message_id', 'Positive', 'Neutral', "Negative"], encoding='utf-8', sep = '|')
                # classify = df['classify'].value_counts().to_dict()

                # Number of classified values: positive, neutral and negative.
                positive = classify['Positive'].sum()
                neutral = classify['Neutral'].sum()
                negative = classify['Negative'].sum()

                # Defines the amount of column and its values
                quantidade_sentimentos = [positive, neutral, negative]

                colors = ['#65fb6a', 'lightgrey', 'lightcoral']
                explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                ax[num_graph].set_title(project, y=1.0, pad=-30)
                ax[num_graph].pie(quantidade_sentimentos, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 8})
                ax[num_graph].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                num_graph = num_graph + 1

            labels = ['Positiva', 'Neutra', 'Negativa']
            ax[0].legend(labels=labels, loc='best', bbox_to_anchor=(0, 0.5))

            fig.suptitle('Distribuição dos Sentimentos em Threads Populares', fontsize=16)

            # Create folder
            if not os.path.exists(f"{self.file_path_general_graph}/{folder_name}"):
                os.makedirs(f"{self.file_path_general_graph}/{folder_name}")

            # Save image
            plt.savefig(f"{self.file_path_general_graph}/{folder_name}/dataset_quantidade_sentimentos_threads_populares.png", transparent=False)
            plt.close(fig)

    # Alterar manualmente as datas a serem plotadas.
    #
    # def graph_sentiments_by_month(self):

    #     for folder_name in os.listdir("../data/chat_rooms"):
    #         count_projects = len(next(os.walk(f"../data/chat_rooms/{folder_name}"))[1]);

    #         fig, ax = plt.subplots(count_projects, 1, figsize=(20,8))
    #         fig.set_figheight(4)
    #         fig.patch.set_facecolor('white')

    #         num_graph = 0

    #         mes_ano_projeto = set()

    #         for project in os.listdir(f"../data/chat_rooms/{folder_name}"):

    #             config = Config(folder_name, project)
    #             file_path_prefix = config.get_path_prefix_filename()
    #             df = pd.read_csv(f"{file_path_prefix}_threads_classificado.csv", encoding='utf-8', sep = '|')

    #             information = self.info_dataset(df)
    #             graph_datetime_thread = information['graph_datetime_thread']

    #             mes_ano = graph_datetime_thread.index.tolist()

    #             for x in mes_ano:
    #                 mes_ano_projeto.add(x)

    #             positive = np.cumsum(graph_datetime_thread['Positive'])
    #             neutral = np.cumsum(graph_datetime_thread['Neutral'])
    #             negative = np.cumsum(graph_datetime_thread['Negative'])

    #             ax[num_graph].plot(mes_ano, positive)
    #             ax[num_graph].plot(mes_ano, neutral)
    #             ax[num_graph].plot(mes_ano, negative)
    #             # ax[num_graph].legend()

    #             num_graph = num_graph + 1

    #         fig.suptitle('Número de mensagens X Quantidades de Sentimentos', fontsize=16)

    #         # Create folder
    #         if not os.path.exists(f"{self.file_path_general_graph}/{folder_name}"):
    #             os.makedirs(f"{self.file_path_general_graph}/{folder_name}")

    #         # Save image
    #         plt.savefig(f"{self.file_path_general_graph}/{folder_name}/progressao_sentimentos_mensal.png", transparent=False)
    #         plt.xticks(rotation=-60)
    #         plt.grid(True)
    #         plt.close(fig)

    def info_dataset(self, df):
        graph_datetime_thread = {}
        anos_utilizados = ["2018"]

        for index, row in df.iterrows():

            date_time_str = row["datetime"]
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_year_month = date_time_obj.strftime("%m/%Y")
            date_year = date_time_obj.strftime("%Y")

            if date_year in anos_utilizados:

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

        graph_datetime_thread = pd.DataFrame(graph_datetime_thread).T

        return {
            'graph_datetime_thread' : graph_datetime_thread
        }


m = GeneralGraph()
m.generate()