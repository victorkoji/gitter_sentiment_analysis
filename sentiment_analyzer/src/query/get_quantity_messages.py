import pandas as pd
import numpy as np
import os
from config.config import Config

# Print quantity median messages for each folder theme.
class QuantityMessages:

    def __init__(self):
        self.path_folder_general = f"../data/general_information"
        self.file_path = f"../data/chat_rooms"

    def process(self):
        
        project_chatroom_messages_median = {}
        project_quantity_message = {}

        # Create path to folder
        if not os.path.exists(f"{self.path_folder_general}/quantity_messages_chatroom"):
            os.makedirs(f"{self.path_folder_general}/quantity_messages_chatroom")

        for folder_name in os.listdir(self.file_path):

            project_quantity_message[folder_name] = {}

            # Iterate the projects to get the total amount of messages
            for filename in os.listdir(f"{self.file_path}/{folder_name}"):
                df = pd.read_csv(fr"{self.file_path}/{folder_name}/{filename}/{filename}.csv",  encoding='utf-8', sep = '|')

                project_quantity_message[folder_name][filename] = len(df)

        for folder_theme, theme in project_quantity_message.items():
            median = np.median(list(theme.values()))

            pd_median = pd.DataFrame(theme.items(), columns=['chat_room', 'quantity_messages'])
            pd_median = pd_median.sort_values(by=['quantity_messages'], ascending=False)
            
            project_selected = pd_median[pd_median['quantity_messages'] >= median]

            # Save the paths of each thread id in a CSV file
            project_selected.to_csv(f"{self.path_folder_general}/quantity_messages_chatroom/{folder_theme}_relation_messages.csv", encoding='utf-8', index=False, sep = '|')
            
            # Save theme and median
            project_chatroom_messages_median[folder_theme] = median

        
        df_chatroom_median = pd.DataFrame(project_chatroom_messages_median.items(), columns=['chat_room', 'messages_median'])
        df_chatroom_median.to_csv(f"{self.path_folder_general}/quantity_messages_chatroom/chatroom_messages_median.csv", encoding='utf-8', index=False, sep = '|')