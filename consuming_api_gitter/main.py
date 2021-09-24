from src.api import API as API
from src.config import Config

class ConsumeAPI: 

	def static_init() -> None:
		return API.static_init()

	def get_messages_chatroom() -> str:
		Config.static_init()
		return API.get_json_messages_chatroom()


ConsumeAPI.static_init()
ConsumeAPI.get_messages_chatroom()