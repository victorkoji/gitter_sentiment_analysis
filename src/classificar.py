import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.gerar_graficos import Grafico
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Classificar:

    def __init__(self, pasta_tema, nome_arquivo):
        self.pasta_tema = pasta_tema
        self.nome_arquivo = nome_arquivo
        #Caminho do arquivo
        self.path_arquivo = f"./ChatRooms/{pasta_tema}/{nome_arquivo}/{nome_arquivo}"

    def processar(self):
        #Visualizando os dados:
        df = pd.read_csv(f"{self.path_arquivo}_threads_identificadas.csv", usecols = ['id', 'text', 'sent', 'username', "diff_date_user", 'discussionId'], encoding='utf-8', sep = '|')

        #Separando messages e suas classes:
        messages = df['text']

        #Analizando as mensagens 
        analyzer = SentimentIntensityAnalyzer()

        texto = []
        classificacao = []

        #Percorre todas as mensagens classificando cada uma
        for sentence in messages:
            vs = analyzer.polarity_scores(str(sentence))
            texto.append(sentence)
            
            # decide sentiment as positive, negative and neutral 
            if vs['compound'] >= 0.05 : 
                classificacao.append("Positive")

            elif vs['compound'] <= -0.05 : 
                classificacao.append("Negative")

            else : 
                classificacao.append("Neutral")

        #Mapear o objeto com seus valores
        file_csv = {
            "ID": df['id'],
            "Mensagem": texto,
            "Classificação": classificacao,
            "Dt_hora": df['sent'],
            "Diferenca_dt_hora_mensagens": df['diff_date_user'],
            "Username": df['username'],
            "DiscussionId": df['discussionId']
        }

        #Criar data frame do pandas
        df = pd.DataFrame(file_csv, columns= ['ID', 'Mensagem', 'Classificação', 'Dt_hora', "Diferenca_dt_hora_mensagens", 'Username', 'DiscussionId'])

        #Criar o csv
        df.to_csv(fr"{self.path_arquivo}_threads_classificado.csv", index = False, header=True, sep = '|')    

        #Gerar Gráfico
        grafico = Grafico(df, fr"./ChatRooms/{self.pasta_tema}/{self.nome_arquivo}/Graficos")
        grafico.gerar_grafico(classificacao)