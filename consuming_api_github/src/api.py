from src.util import Util
import os

class API:

	def __init__(self):
		self.url_base_api = "https://api.github.com"

	def start(self) -> None:

		android_repository = {
			"androidannotations": "https://github.com/androidannotations/androidannotations",
			"android-components" : "https://github.com/mozilla-mobile/android-components",
			"AndroidImageSlider": "https://github.com/daimajia/AndroidImageSlider",
			"android-open-project": "https://github.com/Trinea/android-open-project",
			"frisbee": "https://github.com/gdg-x/frisbee",
			"magnum": "https://github.com/mosra/magnum",
			"MPAndroidChart": "https://github.com/PhilJay/MPAndroidChart",
			"open-event-attendee-android": "https://github.com/fossasia/open-event-attendee-android",
			"ruboto": "https://github.com/ruboto/ruboto",
			"sbt-android": "https://github.com/scala-android/sbt-android",
			"Signal-Android": "https://github.com/signalapp/Signal-Android",
			"Android-Password-Store": "https://github.com/android-password-store/Android-Password-Store",
			"AndroidTraining": "https://github.com/mixi-inc/AndroidTraining",
			"ffmpeg-android-java": "https://github.com/WritingMinds/ffmpeg-android-java",
			"litho": "https://github.com/facebook/litho",
			"macroid": "https://github.com/47degrees/macroid",
			"material-calendarview": "https://github.com/prolificinteractive/material-calendarview",
			"python-gcm": "https://github.com/geeknam/python-gcm",
			"open-source-android-apps": "https://github.com/pcqpcq/open-source-android-apps",
			"simpletask-android": "https://gitter.im/mpcjanssen/simpletask-android"
		}

		ios_repository = {
			"appium": "https://github.com/appium/appium",
			"BEMSimpleLineGraph": "https://github.com/Boris-Em/BEMSimpleLineGraph",
			"Kitura": "https://github.com/Kitura/Kitura",
			"PerfectlySoft": "https://github.com/PerfectlySoft/Perfect",
			"PureSwiftCacao": "https://github.com/PureSwift/Cacao",
			"Alcatraz": "https://github.com/alcatraz/Alcatraz",
			"BEMAnalogClock": "https://github.com/Boris-Em/BEMAnalogClock",
			"CocoaPods": "https://github.com/CocoaPods/CocoaPods",
			"CodeHub": "https://github.com/CodeHubApp/CodeHub",
			"Dollar": "https://github.com/ankurp/Dollar",
			"iOS-Goodies": "https://github.com/iOS-Goodies/iOS-Goodies",
			"iOSTraining": "https://github.com/mixi-inc/iOSTraining",
			"TheUnoPlatform": "https://github.com/unoplatform/uno",
			"nzero-push": "https://github.com/linitix/nzero-push",
			"PromiseKit": "https://github.com/mxcl/PromiseKit",
			"PureLayout": "https://github.com/PureLayout/PureLayout",
			"sea-c24-iOS-F2": "https://github.com/codefellows/sea-c24-iOS-F2",
			"tvheadend-iphone-client": "https://github.com/zipleen/tvheadend-iphone-client",
			"Typhoon": "https://github.com/appsquickly/Typhoon",
			"wordpress-hybrid-client": "https://github.com/wordpress-clients/hybrid"
		}

		type_repository = {
			"ANDROID": android_repository,
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
				if not os.path.exists(f"../data/chat_rooms/{type}/{name_project}/Github-data"):
					os.makedirs(f"../data/chat_rooms/{type}/{name_project}/Github-data")

				if data:
					# Escreve os dados para o caminho informado
					Util.write_json(data, f"../data/chat_rooms/{type}/{name_project}/Github-data/{tipo_busca}.json")
					Util.transformJsonToCsv(f"../data/chat_rooms/{type}/{name_project}/Github-data/{tipo_busca}.json")
