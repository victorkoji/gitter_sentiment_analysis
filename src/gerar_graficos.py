import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import math

class Grafico:

    def __init__(self, df, path_arquivo):
        self.path_arquivo = path_arquivo
        self.df = df

    #Método para gerar o gráfico com a quantidade de mensagens positivas, neutras e positivas.
    def gerar_grafico(self, classificacao):

        #Criar o caminho da pasta
        if not os.path.exists(f"{self.path_arquivo}"):
            os.makedirs(f"{self.path_arquivo}")

        informacao = self.info_dataset()
        self.grafico_quantidade_sentimentos(classificacao)
        self.grafico_threads_por_mensagens(informacao['discussion_id_grafico'], informacao['discussion_contador_grafico'])
        self.grafico_threads_por_mensagens_por_sentimentos(informacao['classificacao_por_thread_grafico'])

    def info_dataset(self):
        # discussion_contador = {}
        # mensagem_grafico = []
        discussion_id_grafico = []
        discussion_contador_grafico = {}

        classificacao_mensagens_grafico = []
        classificacao_mapeamento = {"Positive" : 1, "Neutral" : 0, "Negative" : -1}
        classificacao_por_thread_grafico = {}

        #Percorrer a coluna de discussão
        for index, row in self.df.iterrows():
            discussion_array = row["DiscussionId"].replace("[", "").replace("]", "").replace(" ", "").split(",")

            if discussion_array[0] == "":
                continue

            #Percorrer as threads dessa mensagem
            for discussion_id in discussion_array:
                classificacao_mensagens_grafico.append(classificacao_mapeamento[row["Classificação"]])
                discussion_id_grafico.append(int(discussion_id))

                if discussion_id in discussion_contador_grafico: 
                    discussion_contador_grafico[discussion_id] += 1

                    if row["Classificação"] in classificacao_por_thread_grafico[discussion_id]:
                        classificacao_por_thread_grafico[discussion_id][row["Classificação"]] += 1

                else: 
                    discussion_contador_grafico[discussion_id] = 1
                    classificacao_por_thread_grafico[discussion_id] = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    classificacao_por_thread_grafico[discussion_id][row["Classificação"]] += 1

        classificacao_por_thread_grafico = pd.DataFrame(classificacao_por_thread_grafico).T

        return {
            'discussion_id_grafico' : discussion_id_grafico, 
            'discussion_contador_grafico' : discussion_contador_grafico,
            'classificacao_mensagens_grafico' : classificacao_mensagens_grafico,
            'classificacao_mapeamento' : classificacao_mapeamento,
            'classificacao_por_thread_grafico': classificacao_por_thread_grafico
        }

    def grafico_quantidade_sentimentos(self, classificacao):

        #Quantidade de valores classificados: positivos, neutros e negativos.
        positive = classificacao.count('Positive')
        neutral = classificacao.count('Neutral')
        negative = classificacao.count('Negative')

        #Define a quantidade de coluna e os seus valores
        x = np.arange(3)
        values = [positive, neutral, negative]

        #Monta o gráfico
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('white')

        colors = ['green', 'grey', 'red']

        label_positive = mpatches.Patch(color='green', label='Positive')
        label_neutral = mpatches.Patch(color='grey', label='Neutral')
        label_negative = mpatches.Patch(color='red', label='Negative')
        
        plt.figure(figsize=(10, 10))
        plt.bar(x, values, color=colors)
        plt.xticks(x, ('Positive', 'Neutral', 'Negative'))
        plt.legend(handles=[label_positive, label_neutral, label_negative], loc=1)

        #Salva a imagem
        plt.savefig(f"{self.path_arquivo}/quantidade_sentimentos.png", transparent=False)


    ########################################
    #### Threads x números de mensagens ####
    def grafico_threads_por_mensagens(self, discussion_id_grafico, discussion_contador_grafico):

        fig, ax = plt.subplots()
        x = np.arange(len(discussion_id_grafico))
        
        plt.title('Threads X Números Mensagens')
        plt.xlabel('Threads')
        plt.ylabel('Números Mensagens')
        plt.figure(figsize=(10, 10))
        plt.xticks(x)

        ax.scatter(list(dict.fromkeys(discussion_id_grafico)), list(discussion_contador_grafico.values()))

        fig.savefig(f"{self.path_arquivo}/threads_por_mensagens.png", transparent=False)


    ###########################################
    #### Threads x Mensagens x Sentimentos ####
    def grafico_threads_por_mensagens_por_sentimentos(self, classificacao_por_thread_grafico):
        num_threads_por_grafico = 50
        num_array = 0

        for num_threads in range(1, math.ceil(len(classificacao_por_thread_grafico) / num_threads_por_grafico) + 1):

            fig, ax = plt.subplots()
            plt.title('Threads x Números Mensagens x Classificacão')
            plt.xlabel('Threads')
            plt.ylabel('Números Mensagens')
            plt.figure(figsize=(20, 10))

            total_thread = num_threads * num_threads_por_grafico

            if total_thread > len(classificacao_por_thread_grafico):
                total_thread = len(classificacao_por_thread_grafico)

            classificacao = classificacao_por_thread_grafico[num_array : total_thread]


            N = len(classificacao)
            positive = classificacao['Positive']
            negative = classificacao['Negative']
            neutral = classificacao['Neutral']
            ind = np.arange(num_array, total_thread)  
            width = 0.8

            p1 = ax.bar(ind, positive, width=width, label='Positive', align='center', color='green')
            p2 = ax.bar(ind, neutral, width=width, label='Neutral', align='center', color='grey')
            p3 = ax.bar(ind, negative, width=width, label='Negative', align='center', color='red')
            ax.legend()
            ax.set_xticks(np.arange(num_array, total_thread, 10))

            # Label with label_type 'center' instead of the default 'edge'
            # ax.bar_label(p1, label_type='center')
            # ax.bar_label(p2, label_type='center')
            # ax.bar_label(p3, label_type='center')
            # ax.bar_label(p1)

            num_array = total_thread

            fig.savefig(f"{self.path_arquivo}/threads_mensagens_sentimentos_{num_array}.png", format='png', transparent=False)
            plt.close(fig)