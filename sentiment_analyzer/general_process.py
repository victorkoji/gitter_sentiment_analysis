import os, math
import pandas as pd
import numpy as np
from config.config import Config

class GeneralProcess:

    def __init__(self):
        self.path_general_data = f"../data/general_information/general_data"

        if not os.path.exists(f"{self.path_general_data}"):
            os.makedirs(f"{self.path_general_data}")

    def process(self):
        self.generate_table_after_pre_processing()
        self.generate_table_quantity_sentiments_and_threads()
        self.generate_table_median_by_chatroom()
        self.generate_table_only_popular_threads()
        self.create_data_separate_sentiments()

    # Create a table with pre-processed and post-processed messages
    def generate_table_after_pre_processing(self):

        chat_rooms = []
        communities = []
        messages_before_processing = []
        messages_after_processing = []

        for community_name in os.listdir("../data/chat_rooms"):
            for project_name in os.listdir(f"../data/chat_rooms/{community_name}"):

                config = Config(community_name, project_name)
                file_path_prefix = config.get_path_prefix_filename()

                df_before_process = pd.read_csv(f"{file_path_prefix}/{project_name}.csv", usecols = ['id'], encoding='utf-8', sep = '|')
                df_after_process = pd.read_csv(f"{file_path_prefix}/{project_name}_threads_pre_processado.csv", usecols = ['id'], encoding='utf-8', sep = '|')
                
                chat_rooms.append(project_name)
                communities.append(community_name)
                messages_before_processing.append(len(df_before_process))
                messages_after_processing.append(len(df_after_process))

        dict = {
            'chat_room': chat_rooms, 
            'community': communities, 
            'quantity_messages_before_processing': messages_before_processing,
            'quantity_messages_after_processing': messages_after_processing
        } 
            
        df = pd.DataFrame(dict)
        df.sort_values(by=['community', 'quantity_messages_before_processing'])

        # Save csv again with formatted data
        df.to_csv(f"{self.path_general_data}/chat_room_messages_before_after_pre_processing.csv", encoding='utf-8', index=False, sep = '|')

    # Create a table with the amount of sentiments and threads
    def generate_table_quantity_sentiments_and_threads(self):

        chat_rooms = []
        communities = []
        quantity_messages = []
        quantity_sentiment_positive = []
        quantity_sentiment_neutral = []
        quantity_sentiment_negative = []
        quantity_threads = []

        for community_name in os.listdir("../data/chat_rooms"):
            for project_name in os.listdir(f"../data/chat_rooms/{community_name}"):

                config = Config(community_name, project_name)
                file_path_prefix = config.get_path_prefix_filename()
                file_path_query_result = config.get_path_query_result()

                df_classify = pd.read_csv(f"{file_path_prefix}/{project_name}_threads_classificado.csv", usecols = ['id', 'classify'], encoding='utf-8', sep = '|')
                df_threads = pd.read_csv(f"{file_path_query_result}/{project_name}_threads_caminhos_gerais.csv", usecols = ['thread_id', 'message_id', 'Positive', 'Neutral', "Negative"], encoding='utf-8', sep = '|')
                classify = df_classify['classify'].value_counts().to_dict()

                num_messages = len(df_classify)
                num_threads = len(df_threads)
                positive = classify['Positive']
                neutral = classify['Neutral']
                negative = classify['Negative']

                
                chat_rooms.append(project_name)
                communities.append(community_name)
                quantity_messages.append(num_messages)
                quantity_sentiment_positive.append(positive)
                quantity_sentiment_neutral.append(neutral)
                quantity_sentiment_negative.append(negative)
                quantity_threads.append(num_threads)

        dict = {
            'chat_room': chat_rooms, 
            'community': communities, 
            'messages': quantity_messages,
            'quantity_sentiment_positive': quantity_sentiment_positive,
            'quantity_sentiment_neutral': quantity_sentiment_neutral,
            'quantity_sentiment_negative': quantity_sentiment_negative,
            'quantity_threads': quantity_threads
        } 

        df = pd.DataFrame(dict)

        # Save csv again with formatted data
        df.to_csv(f"{self.path_general_data}/chat_room_quantity_sentiments_and_threads.csv", encoding='utf-8', index=False, sep = '|')

    # Create a table with the median of chat rooms and messages
    def generate_table_median_by_chatroom(self):

        chat_rooms = []
        communities = []
        quantity_median_users = []
        quantity_median_messages = []

        for community_name in os.listdir("../data/chat_rooms"):
            for project_name in os.listdir(f"../data/chat_rooms/{community_name}"):

                config = Config(community_name, project_name)
                file_path_prefix = config.get_path_chat_room()
                
                # Thread id by message id mapping
                mapping_threads = {}
                df = pd.read_csv(f"{file_path_prefix}/{project_name}_threads_classificado.csv",  encoding='utf-8', sep = '|')

                for index, row in df.iterrows():
                    threads_id = row['thread_id']
                    
                    # Format string into array
                    string = threads_id.replace(']','').replace('[','')
                    threads_array = string.replace('"','').replace(' ','').split(",")

                    # Cycle through thread id to save in dict
                    for thread in threads_array:
                        if thread and mapping_threads.get(thread) != None:
                            mapping_threads[thread]['message_id']+= f",{row['id']}"         
                            mapping_threads[thread][row['classify']] += 1
                            mapping_threads[thread]['users'].add(row['username'])
                        elif thread:
                            mapping_threads[thread] = {'thread_id': thread, 'message_id': row['id'], 'Positive': 0, 'Neutral': 0, 'Negative': 0}
                            mapping_threads[thread][row['classify']] += 1
                            mapping_threads[thread]['users'] = {row['username']}
                
                # Calculate the median of users and messages
                users_median = self.calculateMedianUsersByThreads(mapping_threads)
                messages_median = self.calculateMedianMessagesByThreads(mapping_threads)

                chat_rooms.append(project_name)
                communities.append(community_name)
                quantity_median_users.append(int(self.round_half_down(users_median)))
                quantity_median_messages.append(int(self.round_half_down(messages_median)))
        
        dict = {
            'chat_room': chat_rooms, 
            'community': communities, 
            'quantity_median_users': quantity_median_users,
            'quantity_median_messages': quantity_median_messages,
        } 

        df = pd.DataFrame(dict)

        # Save csv again with formatted data
        df.to_csv(f"{self.path_general_data}/chat_room_median_users_and_messages.csv", encoding='utf-8', index=False, sep = '|')

    # Create a table with only data from popular threads
    def generate_table_only_popular_threads(self):

        for community_name in os.listdir("../data/chat_rooms"):
            chat_rooms = []
            communities = []
            thread_id = []
            total_messages = []
            total_users = []
            quantity_sentiment_positive = []
            quantity_sentiment_neutral = []
            quantity_sentiment_negative = []

            for project_name in os.listdir(f"../data/chat_rooms/{community_name}"):

                config = Config(community_name, project_name)
                file_path_query_result = config.get_path_query_result()
                
                df_popular_threads = pd.read_csv(f"{file_path_query_result}/{project_name}_threads_caminhos_populares.csv", encoding='utf-8', sep = '|')
                bigger_number_user = df_popular_threads.sort_values(by='total_users', ascending=False).nlargest(3, 'total_users')

                chat_room_temp = []
                communities_temp = []
                for item in range(len(bigger_number_user)):
                    chat_room_temp.append(project_name)
                    communities_temp.append(community_name)

                chat_rooms.extend(chat_room_temp)
                communities.extend(communities_temp)
                thread_id.extend(bigger_number_user['thread_id'])
                total_messages.extend(bigger_number_user['total_messages'])
                total_users.extend(bigger_number_user['total_users'])
                quantity_sentiment_positive.extend(bigger_number_user['Positive'])
                quantity_sentiment_neutral.extend(bigger_number_user['Neutral'])
                quantity_sentiment_negative.extend(bigger_number_user['Negative'])

            dict = {
                'chat_room': chat_rooms, 
                'community': communities, 
                'thread_id': thread_id,
                'total_messages': total_messages,
                'total_users': total_users,
                'positive': quantity_sentiment_positive,
                'neutral': quantity_sentiment_neutral,
                'negative': quantity_sentiment_negative
            } 

            df_popular_threads_chat_rooms = pd.DataFrame(dict)
            df_popular_threads_chat_rooms = df_popular_threads_chat_rooms[df_popular_threads_chat_rooms['community'] == community_name]
            df_popular_threads_chat_rooms = df_popular_threads_chat_rooms.sort_values(by='total_users', ascending=False).nlargest(1, 'total_users')

            # Save csv again with formatted data
            df_popular_threads_chat_rooms.to_csv(f"{self.path_general_data}/popular_threads_chat_rooms_{community_name}.csv", encoding='utf-8', index=False, sep = '|')

    # Create multiple tables for messages and sentiments
    def create_data_separate_sentiments(self):
        path_messages_concated = f"{self.path_general_data}/messagens_concatenadas"

        df_positive_all = pd.DataFrame()
        df_neutral_all = pd.DataFrame()
        df_negative_all = pd.DataFrame()

        for community_name in os.listdir("../data/chat_rooms"):
            df_positive_community = pd.DataFrame()
            df_neutral_community = pd.DataFrame()
            df_negative_community = pd.DataFrame()

            for project_name in os.listdir(f"../data/chat_rooms/{community_name}"):
                config = Config(community_name, project_name)
                file_path_prefix = config.get_path_prefix_filename()

                df = pd.read_csv(f"{file_path_prefix}/{project_name}_threads_classificado.csv", usecols = ['clean_message', 'classify'], encoding='utf-8', sep = '|')
                df_positive_chatroom = df[df['classify'] == 'Positive']
                df_neutral_chatroom = df[df['classify'] == 'Neutral']
                df_negative_chatroom = df[df['classify'] == 'Negative']

                if not os.path.exists(f"{path_messages_concated}/{community_name}/{project_name}"):
                    os.makedirs(f"{path_messages_concated}/{community_name}/{project_name}")
    
                # Generate data by chat room
                df_positive_chatroom.to_csv(f"{path_messages_concated}/{community_name}/{project_name}/mensagens_positivas.csv", encoding='utf-8', index=False, sep = '|')
                df_neutral_chatroom.to_csv(f"{path_messages_concated}/{community_name}/{project_name}/mensagens_neutras.csv", encoding='utf-8', index=False, sep = '|')
                df_negative_chatroom.to_csv(f"{path_messages_concated}/{community_name}/{project_name}/mensagens_negativas.csv", encoding='utf-8', index=False, sep = '|')

                df_positive_community = df_positive_community.append(df_positive_chatroom, ignore_index=True)
                df_neutral_community = df_neutral_community.append(df_neutral_chatroom, ignore_index=True)
                df_negative_community = df_negative_community.append(df_negative_chatroom, ignore_index=True)

            df_positive_all = df_positive_all.append(df_positive_community, ignore_index=True)
            df_neutral_all = df_neutral_all.append(df_neutral_community, ignore_index=True)
            df_negative_all = df_negative_all.append(df_negative_community, ignore_index=True)

            if not os.path.exists(f"{path_messages_concated}/{community_name}"):
                os.makedirs(f"{path_messages_concated}/{community_name}")

            # Generate data by community
            df_positive_community.to_csv(f"{path_messages_concated}/{community_name}/mensagens_positivas.csv", encoding='utf-8', index=False, sep = '|')
            df_neutral_community.to_csv(f"{path_messages_concated}/{community_name}/mensagens_neutras.csv", encoding='utf-8', index=False, sep = '|')
            df_negative_community.to_csv(f"{path_messages_concated}/{community_name}/mensagens_negativas.csv", encoding='utf-8', index=False, sep = '|')

        # Generate data with all messages sentiments
        df_positive_all.to_csv(f"{path_messages_concated}/mensagens_positivas.csv", encoding='utf-8', index=False, sep = '|')
        df_neutral_all.to_csv(f"{path_messages_concated}/mensagens_neutras.csv", encoding='utf-8', index=False, sep = '|')
        df_negative_all.to_csv(f"{path_messages_concated}/mensagens_negativas.csv", encoding='utf-8', index=False, sep = '|')

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

    def round_half_down(self, n, decimals=0):
        n = round(n, 2)
        multiplier = 10 ** decimals
        return math.ceil(n*multiplier - 0.5) / multiplier