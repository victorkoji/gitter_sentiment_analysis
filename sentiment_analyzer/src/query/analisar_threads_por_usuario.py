import pandas as pd
import csv

class AnalisarThreadsPorUsuario:

    def __init__(self, pasta_tema, nome_arquivo, usuario):
        self.pasta_tema = pasta_tema
        self.nome_arquivo = nome_arquivo
        self.usuario = usuario

    def processar(self):
        #Mapeamento de id da thread por id da mensagem 
        threads_caminhos = {}

        #Essas 2 objetos irei utilizar para salvar somente as threads que iniciam negativas.
        threads_caminhos_iniciam_negativas = {}
        threads_caminhos_antigos = {}

        #Visualizando os dados:
        df = pd.read_csv(fr"./ChatRooms/{self.pasta_tema}/{self.nome_arquivo}/{self.nome_arquivo}_threads_classificado.csv",  encoding='utf-8', sep = '|')

        usuarioMessages = df[df['Username'] == self.usuario]

        #Percorre todas as linhas do CSV
        for index, row in usuarioMessages.iterrows():
            threads_id = row['DiscussionId']
            
            #Formata a string em array
            string = threads_id.replace(']','').replace('[','')
            threads_array = string.replace('"','').replace(' ','').split(",")

            #Percorre os id das threads para salvar no dicionário
            for thread in threads_array:

                ####################################################################
                ################## Threads com início negativo ######################
                #Verificar não está vazia existe && Verificar se ela já foi inserida
                if thread and threads_caminhos_iniciam_negativas.get(thread) != None :
                    threads_caminhos_iniciam_negativas[thread]['message_id'] += f",{row['ID']}"         
                    threads_caminhos_iniciam_negativas[thread][row['Classificação']] += 1

                #Verificar não está vazia && Verificar se ela não apareceu em rows antigas
                elif thread and row['Classificação'] == "Negative" and threads_caminhos_antigos.get(thread) == None :
                    threads_caminhos_iniciam_negativas[thread] = {'thread_id': thread, 'message_id': row['ID'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    threads_caminhos_iniciam_negativas[thread][row['Classificação']] += 1
                else:
                    threads_caminhos_antigos[thread] = {'thread_id': thread}
                ################## Threads com início negativo ######################
                ####################################################################

                #######################################################################
                ################### Caminhos das Threads normais ######################
                if thread and threads_caminhos.get(thread) != None:
                    threads_caminhos[thread]['message_id']+= f",{row['ID']}"         
                    threads_caminhos[thread][row['Classificação']] += 1
                elif thread:
                    threads_caminhos[thread] = {'thread_id': thread, 'message_id': row['ID'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                    threads_caminhos[thread][row['Classificação']] += 1
                ######################################################################

        #Salva em um arquivo CSV os caminhos de cada id da thread
        with open(fr"./ChatRooms/{self.pasta_tema}/{self.nome_arquivo}/Consulta/{self.nome_arquivo}_threads_{self.usuario}.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|")
            w.writeheader()
            for item in threads_caminhos.items():
                w.writerow(item[1])
                
        #Salva em um arquivo CSV os caminhos de cada id da thread
        with open(fr"./ChatRooms/{self.pasta_tema}/{self.nome_arquivo}/Consulta/{self.nome_arquivo}_threads_{self.usuario}_iniciam_negativos.csv", 'w') as f:  
            w = csv.DictWriter(f, fieldnames=['thread_id', 'message_id', 'Positive', 'Neutral', 'Negative'], delimiter="|")
            w.writeheader()
            for item in threads_caminhos_iniciam_negativas.items():
                w.writerow(item[1])
                
