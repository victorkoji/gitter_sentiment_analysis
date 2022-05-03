import pandas as pd

from config.config import Config
from src.graph import Graph
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Classify:

    def __init__(self, folder_name, filename):
        config = Config(folder_name, filename)
        self.file_path = config.get_path_prefix_filename()
        self.folder_name = folder_name
        self.filename = filename
        print("Started Message Classification")

    def process(self):

        analyzer = SentimentIntensityAnalyzer()
        text = []
        classify = []

        df = pd.read_csv(f"{self.file_path}/{self.filename}_threads_identificadas.csv", usecols = ['id', 'text', 'sent', 'clean', 'username', "diff_date_user", 'discussionId'], encoding='utf-8', sep = '|')
        df_messages = df['text']

        for message in df_messages:
            vs = analyzer.polarity_scores(str(message))
            text.append(message)
            
            # Decide sentiment as positive, negative and neutral 
            if vs['compound'] >= 0.05 : 
                classify.append("Positive")

            elif vs['compound'] <= -0.05 : 
                classify.append("Negative")

            else : 
                classify.append("Neutral")

        # Map the object with its values
        file_csv = {
            "id": df['id'],
            "message": text,
            'clean_message': df['clean'],
            "classify": classify,
            "datetime": df['sent'],
            "diff_datetime_messages": df['diff_date_user'],
            "username": df['username'],
            "thread_id": df['discussionId']
        }

        # Create pandas data frame
        df = pd.DataFrame(file_csv, columns= ['id', 'message', 'clean_message', 'classify', 'datetime', "diff_datetime_messages", 'username', 'thread_id'])

        # Create csv
        df.to_csv(fr"{self.file_path}/{self.filename}_threads_classificado.csv", index = False, header=True, sep = '|')    

        # Generate graph
        graph = Graph(self.folder_name, self.filename)
        graph.generate_graph_classify(classify)