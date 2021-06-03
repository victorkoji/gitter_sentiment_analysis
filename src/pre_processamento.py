# Importando as bibliotecas que iremos utilizar:
import pandas as pd
import os, string, re, json, pkg_resources
import pytz, dateutil.parser
import nltk

from symspellpy import SymSpell, Verbosity
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# nltk.download('stopwords')
# nltk.download('rslp')
# nltk.download('wordnet')

class PreProcessamento:

    def __init__(self, pasta_tema, nome_arquivo):
        self.pasta_tema = pasta_tema
        self.nome_arquivo = nome_arquivo
        #Caminho do arquivo
        self.path_arquivo = f"./ChatRooms/{pasta_tema}/{nome_arquivo}"

        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        # term_index is the column of the term and count_index is the
        # column of the term frequency
        self.sym_spell.load_dictionary("./SymSpell/frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)
        self.sym_spell.load_bigram_dictionary("./SymSpell/frequency_bigramdictionary_en_243_342.txt", term_index=0, count_index=2)


    def processar(self):
        #Criar um arquivo csv a partir do JSON de dados
        with open(f"{self.path_arquivo}.json", encoding='utf-8-sig') as f_input:
            df = pd.read_json(f_input)

        df.to_csv(f"{self.path_arquivo}.csv", encoding='utf-8', index=False, sep = '|')

        # Visualizando os dados:
        df = pd.read_csv(f"{self.path_arquivo}.csv", usecols = ['id','text', 'sent', 'fromUser'], encoding='utf-8', sep = '|')
        
        #Renomeia o nome da coluna fromUser para username
        df = df.rename(columns=({'fromUser':'username'}))

        # Busca apenas os nomes dos usuários
        df['username'] = [self.getUserObject(i) for i in df['username']]

        # Busca as mensagens adjacentes do mesmo usuário e concatena 
        df = self.concatMessageSameUser(df)

        #Irá remover as rows com valores vazios ou 'nan'
        df.replace({'text' : { '' : float("NaN"), 'nan' : float("NaN")}}, inplace=True)
        df = df.dropna(subset=['text'])

        # Aplica a função em todos os dados:
        messages = [self.Preprocessing(i) for i in df['text']]

        #Insere a coluna clean com as mensagens pré processadas
        df.insert(2, "clean", messages)

        #Salva o csv novamente com os dados formatados
        df.to_csv(f"{self.path_arquivo}_threads_pre_processado.csv", encoding='utf-8', index=False, sep = '|')

        #Criar o caminho da pasta
        if not os.path.exists(f"{self.path_arquivo}"):
            os.makedirs(f"{self.path_arquivo}")
            
        #Mover os arquivos para uma pasta específica
        os.replace(f"{self.path_arquivo}.csv", f"{self.path_arquivo}/{self.nome_arquivo}.csv")
        os.replace(f"{self.path_arquivo}_threads_pre_processado.csv", f"{self.path_arquivo}/{self.nome_arquivo}_threads_pre_processado.csv")

    #Função principal
    def Preprocessing(self, instancia):
        instancia = self.Limpeza_dados(instancia)
        instancia = self.corretor_ortografico(instancia)
        palavras = self.RemoveStopWords(instancia)
        #palavras = Stemming(palavras)
        palavras = self.Lemmatization(palavras)
        #palavras = RemovePunctuation(palavras)
        
        return palavras

    #Remove pontuação
    def RemovePunctuation(self, instancia):
        palavras = []
        table = str.maketrans("", "", string.punctuation)
        for w in instancia.split():
            palavras.append(w.translate(table))
        return (" ".join(palavras))

    # Função para remover Stopwords da nossa base:
    def RemoveStopWords(self, instancia):
        stopwords = set(nltk.corpus.stopwords.words('english'))
        palavras = [i for i in instancia.split() if not i in stopwords]
        return (" ".join(palavras))

    #Stemming é a técnica de remover sufixos e prefixos de uma palavra, chamada stem.
    #Por exemplo, o stem da palavra cooking é cook. Um bom algoritmo sabe que “ing” é um sufixo e pode ser removido
    def Stemming(self, instancia):
        stemmer = nltk.stem.RSLPStemmer()
        palavras = []
        for w in instancia.split():
            palavras.append(stemmer.stem(w))
        return (" ".join(palavras))

    #Vamos remover as pontuações e os links, pois eles não adiciona nenhuma informação extra.
    #Iremos ignorar mensagens que começam com código hexadecimal
    def Limpeza_dados(self, instancia):
        hexadecimal = instancia[:2]
        if hexadecimal != "0x":
            #Transforma tudo em string
            instancia = re.sub("[^a-zA-Z]", " ", str(instancia))

            #Remove os números 
            instancia = re.sub(r"\d+", "", instancia)
            
            #Remove links, pontos, virgulas,ponto e virgulas dos tweets
            #instancia = re.sub(r"http\S+", "", instancia).lower().replace('.','').replace(';','').replace('-','').replace(':','').replace(')','')
        return (instancia)
    
    def Lemmatization(self, instancia):
        #Reduz as palavras flexionadas adequadamente, garantindo que a palavra raiz pertença ao idioma.
        wordnet_lemmatizer = WordNetLemmatizer()

        palavras = []
        for w in instancia.split():
            palavras.append(wordnet_lemmatizer.lemmatize(w))
        return (" ".join(palavras))

    #Pega o json do usuário e retorna somente o username.
    def getUserObject(self, user_string):
        user_array = user_string.split(",")
        user_string = "{" + user_array[1] + "}"
        
        #Se o texto interno possuir aspas dupla, iremos colocar o \"
        #user_string = user_string.replace('"', '\\"')
        
        #Iremos substituir todas as ocorrências de aspas simples por aspas dupla
        user_string = user_string.replace('\'', '"')
        
        if user_string != "":
            #Transforma a string em json
            user = json.loads(user_string)
            username = user['username']
            
        return username
    
    #Função para remover as mensagens adjacentes do mesmo usuário
    def concatMessageSameUser(self, df):
        index_remove = []

        #Cria a coluna da diferença de datas
        df.insert(3, "diff_date_user", "")

        #datetime auxiliar
        first_user = {"num_row": "", "username": "", "datetime": ""}

        #Percorre todas as mensagens
        for i in range(len(df) - 1):

            #Transforma a data para o nosso padrão
            utctime = dateutil.parser.parse(df['sent'][i])
            datetime_message = utctime.astimezone(pytz.timezone("America/Campo_Grande"))
            df['sent'][i] = datetime_message.strftime("%Y-%m-%d %H:%M:%S")

            #Verifica se o próximo usuário é diferente do primeiro usuário encontrado
            if first_user["username"] != df['username'][i]:
                first_user["num_row"] = i
                first_user["username"] = df['username'][i]
                first_user["datetime"] = datetime_message

            #Verifica se é o mesmo usuário da mensagem posterior
            if df['username'][i] == df['username'][i + 1]:

                #Concatena os id
                df['id'][first_user["num_row"]] = str(df['id'][first_user["num_row"]]) + ',' + str(df['id'][i + 1])

                #Concatena a mensagem
                df['text'][first_user["num_row"]] = str(df['text'][first_user["num_row"]]) + " \n " + str(df['text'][i + 1])
                
                #Transforma a data para o nosso padrão
                utctime_pos = dateutil.parser.parse(df['sent'][i + 1])
                datetime_message_pos = utctime_pos.astimezone(pytz.timezone("America/Campo_Grande"))
                
                #Guarda a diferenca entre as mensagens
                df['diff_date_user'][first_user["num_row"]] =  "Diferença:    " + str(datetime_message_pos - first_user["datetime"]) + "\n\n"
                df['diff_date_user'][first_user["num_row"]] += "Data Inicial: " + first_user["datetime"].strftime("%Y-%m-%d %H:%M:%S") + "\n"
                df['diff_date_user'][first_user["num_row"]] += "Data Final:   " + datetime_message_pos.strftime("%Y-%m-%d %H:%M:%S") 

                #Guarda o número da linha para remover
                index_remove.append(i + 1)

        #Apaga as linhas
        df.drop(df.index[index_remove], inplace=True)
                
        return df

    #Função para corrigir as mensagens do Gitter. Ela utiliza uma biblioteca externa.
    def corretor_ortografico(self, message):
    
        suggestions = self.sym_spell.lookup_compound(message, max_edit_distance=2, transfer_casing=True)
        for suggestion in suggestions:
            return suggestion.term
