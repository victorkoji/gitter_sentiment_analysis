from src.api import API as API
from src.config import Config

class ConsumeAPI: 

	def __init__(self):
		self.api_github = API()

	def start(self) -> str:
		Config.static_init()
		return self.api_github.start()

consume_api = ConsumeAPI()
consume_api.start()