class Config:

	def __init__(self, folder_name, filename):

		self.path_chat_room = f"../chat_rooms/{folder_name}/{filename}/{filename}"
		self.path_chat_room_with_prefix = f"../chat_rooms/{folder_name}/{filename}/{filename}"
		self.path_graphs = f"../chat_rooms/{folder_name}/{filename}/graphs"
		self.path_query_result = f"../chat_rooms/{folder_name}/{filename}/query_result"

	def get_path_chat_room(self) -> str:
		return self.path_chat_room

	def get_path_prefix_filename(self) -> str:
		return self.path_chat_room_with_prefix

	def get_path_graphs(self) -> str:
		return self.path_graphs

	def get_path_query_result(self) -> str:
		return self.path_query_result