import pandas as pd
import numpy as np
import os
from config.config import Config

# Print quantity median stargazers(Github) for each folder theme.
class SelectChatrooms:

    def __init__(self):
        self.path_folder_general = f"../data/general_information"
        self.file_path = f"../data/chat_rooms"

    def process(self):

        # Create path to folder
        if not os.path.exists(f"{self.path_folder_general}/selected_chatrooms"):
            os.makedirs(f"{self.path_folder_general}/selected_chatrooms")

        for folder_name in os.listdir(self.file_path):
            df_messages = pd.read_csv(f"{self.path_folder_general}/quantity_messages_chatroom/{folder_name}_relation_messages.csv",  encoding='utf-8', sep = '|')
            df_stargazers = pd.read_csv(f"{self.path_folder_general}/quantity_stargazers_chatroom/{folder_name}_relation_stargazers.csv",  encoding='utf-8', sep = '|')

            df_merge = pd.merge(df_messages, df_stargazers, how='inner', on=['chat_room'])
            df_merge.to_csv(f"{self.path_folder_general}/selected_chatrooms/{folder_name}_selected_chatrooms.csv", encoding='utf-8', index=False, sep = '|')