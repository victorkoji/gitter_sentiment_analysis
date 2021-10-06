import pandas as pd
import numpy as np
import os
from config.config import Config

# Print quantity median stargazers(Github) for each folder theme.
class QuantityStargazers:

    def __init__(self):
        self.path_folder_general = f"../data/general_information"
        self.file_path = f"../data/chat_rooms"

    def process(self):
        
        project_chatroom_stargazers_median = {}
        project_quantity_stargazers = {}

        # Create path to folder
        if not os.path.exists(f"{self.path_folder_general}/quantity_stargazers_chatroom"):
            os.makedirs(f"{self.path_folder_general}/quantity_stargazers_chatroom")

        for folder_name in os.listdir(self.file_path):

            project_quantity_stargazers[folder_name] = {}

            # Iterate the projects to get the total amount of stargazers
            for filename in os.listdir(f"{self.file_path}/{folder_name}"):
                try:
                    df = pd.read_csv(fr"{self.file_path}/{folder_name}/{filename}/Github-data/general_info.csv",  encoding='utf-8', sep = '|')
                    project_quantity_stargazers[folder_name][filename] = df["stargazers_count"].iloc[0]
                except:
                    print("Arquivo general_info não encontrado!")
                    project_quantity_stargazers[folder_name][filename] = 0

        for folder_theme, theme in project_quantity_stargazers.items():
            median = np.median(list(theme.values()))

            pd_median = pd.DataFrame(theme.items(), columns=['chat_room', 'quantity_stargazers'])
            pd_median = pd_median.sort_values(by=['quantity_stargazers'], ascending=False)
            
            project_selected = pd_median[pd_median['quantity_stargazers'] >= median]

            # Save the paths of each thread id in a CSV file
            project_selected.to_csv(f"{self.path_folder_general}/quantity_stargazers_chatroom/{folder_theme}_relation_stargazers.csv", encoding='utf-8', index=False, sep = '|')
            
            # Save theme and median
            project_chatroom_stargazers_median[folder_theme] = median

        
        df_chatroom_median = pd.DataFrame(project_chatroom_stargazers_median.items(), columns=['chat_room', 'stargazers_median'])
        df_chatroom_median.to_csv(f"{self.path_folder_general}/quantity_stargazers_chatroom/chatroom_stargazers_median.csv", encoding='utf-8', index=False, sep = '|')