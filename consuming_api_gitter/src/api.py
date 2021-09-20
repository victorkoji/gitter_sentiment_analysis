from src.util import Util
from src.config import Config
import os
import ndjson

class API:

	def static_init() -> None:

		return Config.static_init()

	def get_json_messages_chatroom() -> None:
		
		nome_pasta = "ANDROID"
		chatRooms = {}

		with open('./json/gitter-user-rooms-2021-9-5.ndjson') as f:
			dataChatRooms = ndjson.load(f)

		for chat_room in dataChatRooms:
			chatRooms[chat_room['id']] = chat_room['name']

		# chatRooms = {
		# 	"54494e55db8155e6700cdebc": "appium",
		# 	"54f1e68c15522ed4b3dc9d22": "deep_learning",
		# 	"5357a9915e986b0712f04385": "pydata_pandas",
		# 	"541a528c163965c9bc2053e1": "scikit-learn",
		# 	"56cb505ce610378809c2d56b": "IBM_swift_kitura",
		# 	"530650f15e986b0712ef95ab": "bem_simple_line_graph",
		# 	"564a088316b6c7089cbaea01": "perfectly_soft",
		# 	"574f743bc43b8c6019763b74": "pure_swift_cacao",
		# 	"555731d315522ed4b3e07eec": "Fossasia",
		# 	"54f21a7e15522ed4b3dc9eca": "MPAndroidChart",
		# 	"54919b17db8155e6700e0339": "Trinea-android-open-project",
		# 	"5487e8b5db8155e6700dd965": "WhisperSystems-Signal-Android",
		# 	"5540f16515522ed4b3dfb066": "Scala-Android-Sbt-Android",
		# 	"54885c33db8155e6700ddb9a": "Daimajia-AndroidImageSlider",
		# 	"54db6a8d15522ed4b3dbe41e": "Gdg-x-Frisbee",
		# 	"53c6133c107e137846ba6c63": "Ruboto",
		# 	"54885c33db8155e6700ddb9a": "Android-Image-Slider"
		# }

		for id, nome_chatroom in chatRooms.items():
			# Get only name repository
			nome_chatroom = nome_chatroom.split(sep="/")[1]
			chatRoomId = id

			url_base: str = f"https://api.gitter.im/v1/rooms/{chatRoomId}/chatMessages?limit=100"

			id = ""
			url = url_base
			contador = 0

			# Are there any requested messages?
			while True and id != -1:
				if id:
					url = f"{url_base}&beforeId={id}"
					
				# Search for data in the url informed
				data = Util.get_json(url)

				if len(data) == 100 and data:
					id = data[0]['id']
				else:
					id = -1
				contador += len(data)

				if data:
					
					# Create folder
					# if not os.path.exists(f"../chat_room/{nome_pasta}"):
					# 	os.makedirs(f"../chat_room/{nome_pasta}")

					# Create folder
					if not os.path.exists(f"../chat_rooms/{nome_pasta}/{nome_chatroom}"):
						os.makedirs(f"../chat_rooms/{nome_pasta}/{nome_chatroom}")

					# Create file with data to path informed
					Util.write_json(data, f"../chat_rooms/{nome_pasta}/{nome_chatroom}/{nome_chatroom}.json")