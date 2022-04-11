# Importando as bibliotecas que iremos utilizar:
import pandas as pd
import os, string, re, json, pkg_resources
import pytz, dateutil.parser
import nltk

from symspellpy import SymSpell
from nltk.stem import WordNetLemmatizer
from config.config import Config

################# Run the first time #################
# nltk.download('stopwords')
# nltk.download('rslp')
# nltk.download('wordnet')
################# Run the first time #################

class Preprocessing:

    def __init__(self, folder_name, filename):
        config = Config(folder_name, filename)
        self.file_path = config.get_path_chat_room()
        self.folder_name = folder_name
        self.filename = filename

        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        # term_index is the column of the term and count_index is the
        # column of the term frequency
        self.sym_spell.load_dictionary("./src/SymSpell/frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)
        self.sym_spell.load_bigram_dictionary("./src/SymSpell/frequency_bigramdictionary_en_243_342.txt", term_index=0, count_index=2)

        print("Start Preprocessing")


    def process(self):
        
        # Create a csv file from data JSON
        with open(f"{self.file_path}.json", encoding='utf-8-sig') as f_input:
            df = pd.read_json(f_input)
            df.to_csv(f"{self.file_path}.csv", encoding='utf-8', index=False, sep = '|')

        # Read csv
        df = pd.read_csv(f"{self.file_path}.csv", usecols = ['id','text', 'sent', 'fromUser'], encoding='utf-8', sep = '|')
        
        # Renames the column name fromUser to username
        df = df.rename(columns=({'fromUser':'username'}))

        # Search only usernames
        df['username'] = [self.getUserObject(i) for i in df['username']]

        df = self.concatMessageSameUser(df)
        df = self.remove_empty_messages(df)

        # Applies the function to all data:
        messages = [self.Preprocessing(i) for i in df['text']]

        # Inserts the clean column with pre-processed messages
        df.insert(2, "clean", messages)

        # Save csv again with formatted data
        df.to_csv(f"{self.file_path}_threads_pre_processado.csv", encoding='utf-8', index=False, sep = '|')

    # Main function
    def Preprocessing(self, instancia):
        instancia = self.data_cleaning(instancia)
        instancia = self.spell_checker(instancia)
        palavras = self.RemoveStopWords(instancia)
        palavras = self.Lemmatization(palavras)
        
        return palavras

    # Function to remove stopwords from our data:
    def RemoveStopWords(self, instancia):
        stopwords = set(nltk.corpus.stopwords.words('english'))
        palavras = [i for i in instancia.split() if not i in stopwords]
        return (" ".join(palavras))

    # Remove links as they don't add any extra information.
    def data_cleaning(self, instancia):
       
        # Transform to string
        instancia = re.sub("[^a-zA-Z]", " ", str(instancia))

        # Remove numbers
        instancia = re.sub(r"\d+", "", instancia)
        
        return (instancia)

    # Reduz as palavras flexionadas de maneira adequada, garantindo que a palavra raiz pertença ao idioma.
    def Lemmatization(self, instancia):
        wordnet_lemmatizer = WordNetLemmatizer()

        palavras = []
        for w in instancia.split():
            palavras.append(wordnet_lemmatizer.lemmatize(w))
        return (" ".join(palavras))

    # Functions to takes the user's json and returns only the username.
    def getUserObject(self, user_string):
        user_array = user_string.split(",")
        user_string = "{" + user_array[1] + "}"
        
        # We will replace all occurrences of single quotes with double quotes.
        user_string = user_string.replace('\'', '"')
        
        if user_string != "":
            # Transform string to json
            user = json.loads(user_string)
            username = user['username']
            
        return username
    
    # Function to remove adjacent messages from the same user
    def concatMessageSameUser(self, df_messages):
        index_remove = []

        # Creates the date difference column
        df_messages.insert(3, "diff_date_user", "")

        # Auxiliary datetime
        first_user = {"num_row": "", "username": "", "datetime": ""}

        for index in range(len(df_messages)):

            # Transform date to America/Campo_Grande timezone
            utctime = dateutil.parser.parse(df_messages['sent'][index])
            datetime_message = utctime.astimezone(pytz.timezone("America/Campo_Grande"))
            df_messages['sent'][index] = datetime_message.strftime("%Y-%m-%d %H:%M:%S")

            # Check if the next user is different from the first user found
            if first_user["username"] != df_messages['username'][index]:
                first_user["num_row"] = index
                first_user["username"] = df_messages['username'][index]
                first_user["datetime"] = datetime_message

            # Verify that it is the same user as the post message
            if (index + 1) in df_messages['username'] and df_messages['username'][index] == df_messages['username'][index + 1]:

                # Concatenate the id
                df_messages['id'][first_user["num_row"]] = str(df_messages['id'][first_user["num_row"]]) + ',' + str(df_messages['id'][index + 1])

                # Concatenate the message
                df_messages['text'][first_user["num_row"]] = str(df_messages['text'][first_user["num_row"]]) + " \n " + str(df_messages['text'][index + 1])
                
                # Transform date to America/Campo_Grande timezone
                utctime_pos = dateutil.parser.parse(df_messages['sent'][index + 1])
                datetime_message_pos = utctime_pos.astimezone(pytz.timezone("America/Campo_Grande"))
                
                # Keep the difference in dates between messages
                df_messages['diff_date_user'][first_user["num_row"]] =  "Diference:    " + str(datetime_message_pos - first_user["datetime"]) + "\n\n"
                df_messages['diff_date_user'][first_user["num_row"]] += "Initial date: " + first_user["datetime"].strftime("%Y-%m-%d %H:%M:%S") + "\n"
                df_messages['diff_date_user'][first_user["num_row"]] += "Final date:   " + datetime_message_pos.strftime("%Y-%m-%d %H:%M:%S") 

                # Save line number to remove
                index_remove.append(index + 1)

        # Remove lines from the same user
        df_messages.drop(df_messages.index[index_remove], inplace=True)
                
        return df_messages

    # Function to remove empty messages
    def remove_empty_messages(self, df_messages):
        # Remove rows with empty or 'nan' values
        df_messages.replace({'text' : { '' : float("NaN"), 'nan' : float("NaN")}}, inplace=True)
        df_messages = df_messages.dropna(subset=['text'])

        return df_messages

    # Function to fix Gitter messages. It uses an external library.
    def spell_checker(self, message):
        try:
            suggestions = self.sym_spell.lookup_compound(message, max_edit_distance=2, transfer_casing=True)
            for suggestion in suggestions:
                return suggestion.term
        except:
            return message