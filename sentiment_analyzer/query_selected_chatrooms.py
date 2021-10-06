from src.query.get_quantity_stars import QuantityStargazers
from src.query.get_quantity_messages import QuantityMessages
from src.query.get_selected_chatrooms import SelectChatrooms

class Main:
    
    def process(self):
        # Calcula a mediana da quantidade de estrelas.
        # Depois filtra somente os projetos que estão acima dessa mediana
        QuantityStargazers().process()

        # Calcula a mediana da quantidade de mensagens
        # Depois filtra somente os projetos que estão acima dessa mediana
        QuantityMessages().process()

        # Seleciona os projetos que estão acima da mediana nos 2 casos acima 
        SelectChatrooms().process()

m = Main()
m.process()