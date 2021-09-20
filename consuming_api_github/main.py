from src.api import API as API

class ConsumeAPI: 

	def __init__(self):
		self.api_github = API()

	def start(self) -> str:
		return self.api_github.start()

consume_api = ConsumeAPI()
consume_api.start()