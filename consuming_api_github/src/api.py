from src.util import Util
import os

class API:

	def __init__(self):
		self.url_base_api = "https://api.github.com"

	def start(self) -> None:

		android_repository = {
			#ANDROID
			# "android-open-project": "https://github.com/Trinea/android-open-project",
			# "magnum": "https://github.com/mosra/magnum",
			# "sbt-android": "https://github.com/scala-android/sbt-android",
			# "open-event-attendee-android": "https://github.com/fossasia/open-event-attendee-android",
			# "frisbee": "https://github.com/gdg-x/frisbee",
			# "androidannotations": "https://github.com/androidannotations/androidannotations",
			# "MPAndroidChart": "https://github.com/PhilJay/MPAndroidChart",
			# "Fossasia": "https://github.com/fossasia/open-event-attendee-android",
			# "Frisbee": "https://github.com/gdg-x/frisbee",
			# "Ruboto": "https://github.com/ruboto/ruboto",
			# "Signal-Android": "https://github.com/signalapp/Signal-Android",
			# "AndroidImageSlider": "https://github.com/daimajia/AndroidImageSlider",
		}

		ios_repository = {
			#iOS
			"appium": "https://github.com/appium/appium",
			# "Bem-Simple-Line-Graph": "https://github.com/Boris-Em/BEMSimpleLineGraph",
			# "Kitura": "https://github.com/Kitura/Kitura",
			# "Perfectly-Soft": "https://github.com/PerfectlySoft/Perfect",
			# "Pure-Swift-Cacao": "https://github.com/PureSwift/Cacao"
		}

		type_repository = {
			# "ANDROID": android_repository,
			"IOS": ios_repository
		}

		self.getSearch(type_repository, "releases")
		self.getSearch(type_repository, "issues")
		self.getSearch(type_repository, "pulls")
		self.getSearch(type_repository, "stargazers")


	# Tipo de busca utilizados:
	# 1 - issues
	# 2 - releases
	# 3 - pull requests
	# 4 - stargazers
	def getSearch(self, type_repository, tipo_busca):
		for type, repository in type_repository.items():
			for name_project, url in repository.items():

				name_repository = url.replace("https://github.com/", "")

				# Build URL
				url_releases = f"{self.url_base_api}/repos/{name_repository}/{tipo_busca}"

				#Busca os dados na url informada
				data = Util.get_json(url_releases)

				#Criar a pasta de consutas
				if not os.path.exists(f"../chat_rooms/{type}/{name_project}/Github-data"):
					os.makedirs(f"../chat_rooms/{type}/{name_project}/Github-data")

				if data:
					# Escreve os dados para o caminho informado
					Util.write_json(data, f"../chat_rooms/{type}/{name_project}/Github-data/{tipo_busca}.json")
					Util.transformJsonToCsv(f"../chat_rooms/{type}/{name_project}/Github-data/{tipo_busca}.json")
