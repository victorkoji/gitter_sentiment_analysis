import pandas as pd
import csv

class AnalisarThreadsPositivoNegativo:

    def __init__(self, pasta_tema, nome_arquivo):
        self.pasta_tema = pasta_tema
        self.nome_arquivo = nome_arquivo

    def processar(self):
        #Mapeamento de id da thread por id da mensagem 
        threads_classificacao = {}
        threads_nao_utilizar = {}

        #Visualizando os dados:
        dataset_classificado = pd.read_csv(fr"./ChatRooms/{self.pasta_tema}/{self.nome_arquivo}/{self.nome_arquivo}_threads_classificado.csv",  encoding='utf-8', sep = '|')

        #Percorre todas as linhas do CSV
        for index, row in dataset_classificado.iterrows():
            message_id = row['DiscussionId'].replace("[", "").replace("]", "").replace(" ", "").split(",")

            #Busca somente mensagens que possuem threads
            if(message_id[0]):
                for discussion_id in message_id:

                    #threads que devem ser desconsideradas
                    if discussion_id not in threads_nao_utilizar:

                        # Verificar se essa thread já não existe no mapeamento
                        if discussion_id not in threads_classificacao:

                            if row['Classificação'] == "Negative":
                                threads_classificacao[discussion_id] = {
                                    'thread_id': discussion_id,
                                    'message_id': row['ID'],
                                    'Positive': 0, 'Neutral': 0, 'Negative': 0,
                                    'primeira_mensagem' : row['Classificação']
                                }
                            else:
                                threads_nao_utilizar[discussion_id] = True

                        # Verificar se essa thread já não existe no mapeamento
                        else:
                        # elif 'ultima_mensagem' not in threads_classificacao[discussion_id] :
                            threads_classificacao[discussion_id]['ultima_mensagem'] = row['Classificação']

                        #Guarda a classificação e o id da mensagem
                        if discussion_id not in threads_nao_utilizar:
                            #Contabilizar a classificação das threads
                            threads_classificacao[discussion_id][row['Classificação']] += 1
                            threads_classificacao[discussion_id]['message_id'] += f",{row['ID']}"      

        #Percorre os registros deixando somente as threads que começam negativas e terminam positivas
        for index, item in threads_classificacao.copy().items():
            if item['ultima_mensagem'] != "Positive":
                threads_classificacao.pop(index)

        #Salva em um arquivo CSV os caminhos de cada id da thread
        with open(fr"./ChatRooms/{self.pasta_tema}/{self.nome_arquivo}/Consulta/{self.nome_arquivo}_threads_caminhos_positivo_negativo.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative', 'primeira_mensagem', 'ultima_mensagem'], delimiter="|")
            w.writeheader()
            for item in threads_classificacao.items():
                w.writerow(item[1])