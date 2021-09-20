import pandas as pd
import numpy as np
import os

# Print quantity median messages for each folder theme.
class QuantityMessages:

    def process(self):
        
        # project_median = {}
        project_quantity_message = {}

        for folder_name in os.listdir("../chat_rooms"):

            project_quantity_message[folder_name] = {}

            for filename in os.listdir(f"../chat_rooms/{folder_name}"):
                df = pd.read_csv(fr"../chat_rooms/{folder_name}/{filename}/{filename}.csv",  encoding='utf-8', sep = '|')

                project_quantity_message[folder_name][filename] = len(df)

        for folder_theme, theme in project_quantity_message.items():
            median = np.median(list(theme.values()))
            pd_median = pd.DataFrame(theme.items(), columns=['chat_room', 'quantity_messages'])
            pd_median = pd_median.sort_values(by=['quantity_messages'], ascending=False)
            project_selected = pd_median[pd_median['quantity_messages'] >= median]
            
            print(f"{folder_theme} quantity messages median: ", np.median(list(theme.values())))
            print(project_selected)