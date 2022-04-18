import os

class Config:

	def __init__(self, folder_name, filename):

		self.path_chat_room = f"../data/chat_rooms/{folder_name}/{filename}"
		self.path_chat_room_with_prefix = f"../data/chat_rooms/{folder_name}/{filename}"
		self.path_graphs = f"../data/chat_rooms/{folder_name}/{filename}/graphs"
		self.path_query_result = f"../data/chat_rooms/{folder_name}/{filename}/query_result"

	def get_path_chat_room(self) -> str:
		# Create folder
		if not os.path.exists(f"{self.path_chat_room}"):
			os.makedirs(f"{self.path_chat_room}")

		return self.path_chat_room

	def get_path_prefix_filename(self) -> str:
		# Create folder
		if not os.path.exists(f"{self.path_chat_room_with_prefix}"):
			os.makedirs(f"{self.path_chat_room_with_prefix}")

		return self.path_chat_room_with_prefix

	def get_path_graphs(self) -> str:
		# Create folder
		if not os.path.exists(f"{self.path_graphs}"):
			os.makedirs(f"{self.path_graphs}")

		return self.path_graphs

	def get_path_query_result(self) -> str:
		# Create folder
		if not os.path.exists(f"{self.path_query_result}"):
			os.makedirs(f"{self.path_query_result}")

		return self.path_query_result