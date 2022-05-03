import os, math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

from datetime import datetime
from config.config import Config

class GeneralGraph:
    def __init__(self):
        self.file_path_general_graph = "../data/general_information/general_graphs"
        self.path_general_data = f"../data/general_information/general_data"

        # Create folder
        if not os.path.exists(f"{self.file_path_general_graph}"):
            os.makedirs(f"{self.file_path_general_graph}")
            
        plt.rcParams.update({'figure.max_open_warning': 0})
        print("Started Generating General Graphics")

    def generate(self):

        self.graph_quantity_sentiments_by_community()
        self.graph_sentiments_by_month()
        self.graph_quantity_sentiments_popular_threads_by_community()
        self.graph_distribution_sentiment_most_popular_threads_community()
        self.graph_quantity_by_sentiments_chat_rooms()
        self.graph_quantity_by_sentiments_general_threads_by_chat_rooms()
        self.graph_quantity_by_sentiments_popular_threads()

    # Graphs of the quantity of sentiment by community
    def graph_quantity_sentiments_by_community(self):

        community = []
        total_quantity_positive = []
        total_quantity_neutral = []
        total_quantity_negative = []

        for folder_name in os.listdir("../data/chat_rooms"):
            community.append(folder_name)

            quantity_positive = 0
            quantity_neutral = 0
            quantity_negative = 0

            for project in os.listdir(f"../data/chat_rooms/{folder_name}"):
                
                config = Config(folder_name, project)
                file_path_prefix = config.get_path_prefix_filename()

                df = pd.read_csv(f"{file_path_prefix}/{project}_threads_classificado.csv", usecols = ['id', 'classify'], encoding='utf-8', sep = '|')
                classify = df['classify'].value_counts().to_dict()

                positive = classify['Positive']
                neutral = classify['Neutral']
                negative = classify['Negative']

                quantity_positive += positive
                quantity_neutral += neutral
                quantity_negative += negative
            
            total_sentiments = quantity_positive + quantity_neutral + quantity_negative

            porcentage_positive = self.round_half_down((quantity_positive / total_sentiments) * 100, 1)
            porcentage_neutral = self.round_half_down((quantity_neutral / total_sentiments) * 100, 1)
            porcentage_negative = self.round_half_down((quantity_negative / total_sentiments) * 100, 1)

            total_quantity_positive.append(porcentage_positive)
            total_quantity_neutral.append(porcentage_neutral)
            total_quantity_negative.append(porcentage_negative)
        
        fig, ax = plt.subplots(figsize=(10,7))
        ind = np.arange(len(community)) 
        width = 0.25

        bar1 = plt.bar(ind, total_quantity_positive, width, color = '#65fb6a')
        bar2 = plt.bar(ind+width, total_quantity_neutral, width, color='lightgrey')
        bar3 = plt.bar(ind+width*2, total_quantity_negative, width, color = 'lightcoral')

        for i in range(len(community)):
            plt.text(i, total_quantity_positive[i] + 0.3, str(total_quantity_positive[i]) + "%", ha = 'center')
            plt.text(i + width, total_quantity_neutral[i] + 0.3, str(total_quantity_neutral[i]) + "%", ha = 'center')
            plt.text(i + width*2, total_quantity_negative[i] + 0.3, str(total_quantity_negative[i]) + "%", ha = 'center')

        fmt = '%.0f%%'
        xticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(xticks)

        plt.title("Sentimentos por Comunidade")
        plt.xticks(ind+width, community, fontsize=14)
        plt.legend( (bar1, bar2, bar3), ('Positivo', 'Neutro', 'Negativo') )
        plt.savefig(f"{self.file_path_general_graph}/dataset_quantidade_sentimentos_por_comunidade.png", transparent=False)
        plt.close(fig)
    
    # Graph of the quantity sentiments for chat rooms
    def graph_quantity_by_sentiments_chat_rooms(self):

        for folder_name in os.listdir("../data/chat_rooms"):
            count_projects = len(next(os.walk(f"../data/chat_rooms/{folder_name}"))[1]);

            fig, ax = plt.subplots(1, count_projects, figsize=(15, 3))
            fig.set_figheight(4)
            fig.patch.set_facecolor('white')

            num_graph = 0

            for project in os.listdir(f"../data/chat_rooms/{folder_name}"):
                
                config = Config(folder_name, project)
                file_path_prefix = config.get_path_prefix_filename()

                df = pd.read_csv(f"{file_path_prefix}/{project}_threads_classificado.csv", usecols = ['id', 'classify'], encoding='utf-8', sep = '|')
                classify = df['classify'].value_counts().to_dict()

                num_threads = len(df)
                # Number of classified values: positive, neutral and negative.
                positive = classify['Positive']
                neutral = classify['Neutral']
                negative = classify['Negative']

                # Defines the amount of column and its values
                quantidade_sentimentos = [positive, neutral, negative]

                colors = ['#65fb6a', 'lightgrey', 'lightcoral']
                explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                ax[num_graph].set_title(project.capitalize(), y=1.0, pad=-30)
                # ax[num_graph].set_xlabel(f"Nº Threads: {num_threads}", labelpad=-20)
                ax[num_graph].pie(quantidade_sentimentos, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 8})
                ax[num_graph].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                num_graph = num_graph + 1

            labels = ['Positiva', 'Neutra', 'Negativa']
            ax[0].legend(labels=labels, loc='best', bbox_to_anchor=(0, 0.5))

            fig.suptitle('Distribuição dos Sentimentos nos Chat rooms', fontsize=16)

            # Save image
            plt.savefig(f"{self.file_path_general_graph}/{folder_name}/dataset_quantidade_sentimentos_por_projeto.png", transparent=False)
            plt.close(fig)

    # Graphs of the quantity sentiments of popular threads by community
    def graph_quantity_sentiments_popular_threads_by_community(self):

        community = []
        total_quantity_positive = []
        total_quantity_neutral = []
        total_quantity_negative = []

        for folder_name in os.listdir("../data/chat_rooms"):
            community.append(folder_name)

            quantity_positive = 0
            quantity_neutral = 0
            quantity_negative = 0

            for project in os.listdir(f"../data/chat_rooms/{folder_name}"):
                
                config = Config(folder_name, project)
                file_path_prefix = config.get_path_query_result()

                classify = pd.read_csv(f"{file_path_prefix}/{project}_threads_caminhos_populares.csv", usecols = ['thread_id', 'message_id', 'Positive', 'Neutral', "Negative"], encoding='utf-8', sep = '|')

                # Number of classified values: positive, neutral and negative.
                positive = classify['Positive'].sum()
                neutral = classify['Neutral'].sum()
                negative = classify['Negative'].sum()

                quantity_positive += positive
                quantity_neutral += neutral
                quantity_negative += negative
            
            total_sentiments = quantity_positive + quantity_neutral + quantity_negative

            porcentage_positive = self.round_half_down((quantity_positive / total_sentiments) * 100, 1)
            porcentage_neutral = self.round_half_down((quantity_neutral / total_sentiments) * 100, 1)
            porcentage_negative = self.round_half_down((quantity_negative / total_sentiments) * 100, 1)

            total_quantity_positive.append(porcentage_positive)
            total_quantity_neutral.append(porcentage_neutral)
            total_quantity_negative.append(porcentage_negative)
        
        fig, ax = plt.subplots(figsize=(10,7))
        ind = np.arange(len(community)) 
        width = 0.25

        bar1 = plt.bar(ind, total_quantity_positive, width, color = '#65fb6a')
        bar2 = plt.bar(ind+width, total_quantity_neutral, width, color='lightgrey')
        bar3 = plt.bar(ind+width*2, total_quantity_negative, width, color = 'lightcoral')

        for i in range(len(community)):
            plt.text(i, total_quantity_positive[i] + 0.3, str(total_quantity_positive[i]) + "%", ha = 'center')
            plt.text(i + width, total_quantity_neutral[i] + 0.3, str(total_quantity_neutral[i]) + "%", ha = 'center')
            plt.text(i + width*2, total_quantity_negative[i] + 0.3, str(total_quantity_negative[i]) + "%", ha = 'center')

        fmt = '%.0f%%'
        xticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(xticks)

        plt.title("Sentimentos por Comunidade")
        plt.xticks(ind+width, community, fontsize=14)
        plt.legend( (bar1, bar2, bar3), ('Positivo', 'Neutro', 'Negativo') )
        plt.savefig(f"{self.file_path_general_graph}/dataset_quantidade_sentimentos_threads_popular_por_comunidade.png", transparent=False)
        plt.close(fig)

    # Graph of the quantity sentiments of general threads by chat rooms
    def graph_quantity_by_sentiments_general_threads_by_chat_rooms(self):

        for folder_name in os.listdir("../data/chat_rooms"):
            count_projects = len(next(os.walk(f"../data/chat_rooms/{folder_name}"))[1]);

            fig, ax = plt.subplots(1, count_projects, figsize=(15, 3))
            fig.set_figheight(4)
            fig.patch.set_facecolor('white')

            num_graph = 0

            for project in os.listdir(f"../data/chat_rooms/{folder_name}"):
                
                config = Config(folder_name, project)
                file_path_prefix = config.get_path_query_result()

                classify = pd.read_csv(f"{file_path_prefix}/{project}_threads_caminhos_gerais.csv", usecols = ['thread_id', 'message_id', 'Positive', 'Neutral', "Negative"], encoding='utf-8', sep = '|')

                num_threads = len(classify)
                # Number of classified values: positive, neutral and negative.
                positive = classify['Positive'].sum()
                neutral = classify['Neutral'].sum()
                negative = classify['Negative'].sum()

                # Defines the amount of column and its values
                quantidade_sentimentos = [positive, neutral, negative]

                colors = ['#65fb6a', 'lightgrey', 'lightcoral']
                explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                ax[num_graph].set_title(project.capitalize(), y=1.0, pad=-30)
                ax[num_graph].set_xlabel(f"Nº Threads: {num_threads}", labelpad=-20)
                ax[num_graph].pie(quantidade_sentimentos, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 8})
                ax[num_graph].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                num_graph = num_graph + 1

            labels = ['Positiva', 'Neutra', 'Negativa']
            ax[0].legend(labels=labels, loc='best', bbox_to_anchor=(0, 0.5))

            fig.suptitle('Distribuição dos Sentimentos em Threads Genéricas', fontsize=16)

            # Save image
            plt.savefig(f"{self.file_path_general_graph}/{folder_name}/dataset_quantidade_sentimentos_threads_gerais.png", transparent=False)
            plt.close(fig)

    # Graph of sentiment distribution of most popular threads by community
    def graph_distribution_sentiment_most_popular_threads_community(self):

        for community_name in os.listdir("../data/chat_rooms"):
            fig, ax = plt.subplots(1, figsize=(7, 3))
            fig.patch.set_facecolor('white')

            df = pd.read_csv(f"{self.path_general_data}/popular_threads_chat_rooms_{community_name}.csv", encoding='utf-8', sep = '|')

            chat_room = df['chat_room'][0]

            # Number of classified values: positive, neutral and negative.
            positive = df['positive'][0]
            neutral = df['neutral'][0]
            negative = df['negative'][0]

            # Defines the amount of column and its values
            quantidade_sentimentos = [positive, neutral, negative]

            colors = ['#65fb6a', 'lightgrey', 'lightcoral']
            explode = (0.1, 0, 0)

            ax.pie(quantidade_sentimentos, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 8})
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            labels = ['Positivo', 'Neutro', 'Negativo']
            ax.legend(labels=labels, loc='lower left')

            fig.suptitle(chat_room.capitalize(), fontsize=16)

            # Save image
            plt.savefig(f"{self.file_path_general_graph}/top_popular_threads_by_community_{chat_room}.png", transparent=False)
            plt.close(fig)

    # Graph of quantity sentiments of popular threads by community
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

                num_threads = len(classify)
                # Number of classified values: positive, neutral and negative.
                positive = classify['Positive'].sum()
                neutral = classify['Neutral'].sum()
                negative = classify['Negative'].sum()

                # Defines the amount of column and its values
                quantidade_sentimentos = [positive, neutral, negative]

                colors = ['#65fb6a', 'lightgrey', 'lightcoral']
                explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                ax[num_graph].set_title(project.capitalize(), y=1.0, pad=-30)
                ax[num_graph].set_xlabel(f"Nº Threads: {num_threads}", labelpad=-20)
                ax[num_graph].pie(quantidade_sentimentos, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 8})
                ax[num_graph].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                num_graph = num_graph + 1

            labels = ['Positiva', 'Neutra', 'Negativa']
            ax[0].legend(labels=labels, loc='best', bbox_to_anchor=(0, 0.5))

            fig.suptitle('Distribuição dos Sentimentos em Threads Populares', fontsize=16)

            # Save image
            plt.savefig(f"{self.file_path_general_graph}/{folder_name}/dataset_quantidade_sentimentos_threads_populares.png", transparent=False)
            plt.close(fig)

    # Partial graph of the flow of feelings by chat room
    def graph_sentiments_by_month(self):
        
        # Search for the chat room with the shortest chat lifetime
        smallest_quantity_month_project = float('inf')
        for folder_name in os.listdir("../data/chat_rooms"):
            for project in os.listdir(f"../data/chat_rooms/{folder_name}"):
                config = Config(folder_name, project)
                file_path_prefix = config.get_path_prefix_filename()
                df = pd.read_csv(f"{file_path_prefix}/{project}_threads_classificado.csv", encoding='utf-8', sep = '|')

                information = self.info_dataset(df, float('inf'))
                graph_datetime_thread = information['graph_datetime_thread']

                mes_ano = graph_datetime_thread.index.tolist()

                if len(mes_ano) <= smallest_quantity_month_project:
                    smallest_quantity_month_project = len(mes_ano)

        # Get the amount in a period of 12 months(1 year)
        smallest_quantity_month_project -= smallest_quantity_month_project % 12

        for folder_name in os.listdir("../data/chat_rooms"):

            for project in os.listdir(f"../data/chat_rooms/{folder_name}"):

                fig, ax = plt.subplots(figsize=(16,7))

                config = Config(folder_name, project)
                file_path_prefix = config.get_path_prefix_filename()
                file_path_graphs = config.get_path_graphs()
                df = pd.read_csv(f"{file_path_prefix}/{project}_threads_classificado.csv", encoding='utf-8', sep = '|')

                information = self.info_dataset(df, smallest_quantity_month_project)
                graph_datetime_thread = information['graph_datetime_thread']

                # mes_ano = graph_datetime_thread.index.tolist()
                mes_ano = graph_datetime_thread.index

                positive = np.cumsum(graph_datetime_thread['Positive'])
                neutral = np.cumsum(graph_datetime_thread['Neutral'])
                negative = np.cumsum(graph_datetime_thread['Negative'])

                ax.plot(mes_ano, positive, label="Positive", color='#65fb6a')
                ax.plot(mes_ano, neutral, label="Neutral", color='dimgray')
                ax.plot(mes_ano, negative, label="Negative", color='lightcoral')
                ax.legend(fontsize=16)

                ax.set_title(project.capitalize(), fontsize=28)
                ax.set_ylabel('Quantidade Mensagens', fontsize=20)
                ax.set_xlabel('Meses/Ano', fontsize=20)

                plt.xticks(rotation=-60, fontsize=12)
                plt.yticks(fontsize=12)
                plt.grid(True)
                plt.savefig(f"{file_path_graphs}/progressao_sentimentos_mensal_parcial.png",  transparent=False, bbox_inches='tight')
                plt.close(fig)

    def info_dataset(self, df, quantidade_maxima_meses):
        graph_datetime_thread = {}
        anos_utilizados = set()

        for index, row in df.iterrows():

            date_time_str = row["datetime"]
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_year_month = date_time_obj.strftime("%m/%Y")

            if len(anos_utilizados) < quantidade_maxima_meses:
                anos_utilizados.add(date_year_month)

        for index, row in df.iterrows():

            date_time_str = row["datetime"]
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_year_month = date_time_obj.strftime("%m/%Y")
            # date_year = date_time_obj.strftime("%Y")

            if date_year_month in anos_utilizados:
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

        return { 'graph_datetime_thread' : graph_datetime_thread }

    def round_half_down(self, n, decimals=0):
        n = round(n, 2)
        multiplier = 10 ** decimals
        return math.ceil(n*multiplier - 0.5) / multiplier