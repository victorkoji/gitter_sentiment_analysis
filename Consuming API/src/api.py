from src.util import Util
from src.config import Config
import json, io

class API:

	# Static initialization
	def static_init() -> None:

		return Config.static_init()

	# Get the astronomy image of the day
	def get_json_messages_chatroom() -> None:

		chatRooms = {
			# "54494e55db8155e6700cdebc": "appium",
			# "54f1e68c15522ed4b3dc9d22": "deep_learning",
			# "5357a9915e986b0712f04385": "pydata_pandas",
			# "541a528c163965c9bc2053e1": "scikit-learn",
			# "56cb505ce610378809c2d56b": "IBM_swift_kitura",
			# "530650f15e986b0712ef95ab": "bem_simple_line_graph",
			# "564a088316b6c7089cbaea01": "perfectly_soft",
			# "574f743bc43b8c6019763b74": "pure_swift_cacao",
			# "555731d315522ed4b3e07eec": "Fossasia",
			# "54f21a7e15522ed4b3dc9eca": "MPAndroidChart",
			# "54919b17db8155e6700e0339": "Trinea-android-open-project",
			# "5487e8b5db8155e6700dd965": "WhisperSystems-Signal-Android",
			# "5540f16515522ed4b3dfb066": "Scala-Android-Sbt-Android",
			# "54885c33db8155e6700ddb9a": "Daimajia-AndroidImageSlider",
			# "54db6a8d15522ed4b3dbe41e": "Gdg-x-Frisbee",
			# "53c6133c107e137846ba6c63": "Ruboto"
		}

		nome_pasta = "BOT"

		for id, nome_chatroom in chatRooms.items():
			chatRoomId = id

			# Build URL
			url_base: str = f"https://api.gitter.im/v1/rooms/{chatRoomId}/chatMessages?limit=100"

			id = ""
			url = url_base
			contador = 0

			#Enquanto houver mensagens, irá continuar com as requisições
			while True and id != -1:
				if id:
					url = f"{url_base}&beforeId={id}"
					
				#Busca os dados na url informada
				data = Util.get_json(url)

				if len(data) == 100 and data:
					id = data[0]['id']
				else:
					id = -1
				contador += len(data)

				if data:
					# Escreve os dados para o caminho informado
					Util.write_json(data, f"../ChatRooms/{nome_pasta}/{nome_chatroom}.json")