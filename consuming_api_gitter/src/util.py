import urllib.response
import requests
from src.config import Config
import json
import os.path

class Util:

	def get_json(url: str) -> dict:
		headers = {
			'Authorization':'Bearer ' + Config.get_token(),
			'Accept': 'application/json'
		}
		
		response = requests.get(url, headers=headers)
		return response.json()

	def write_json(data: str, path: str) -> None:

		# If the file exist, just add
		if os.path.isfile(path): 
			with open(path) as json_file: 
				json_exist = json.load(json_file) 

				json_exist = data + json_exist

				json_data: str = json.JSONEncoder().encode(json_exist)

				out_file = open(path, 'w')
				out_file.write(json_data)
				out_file.close()

		# If the file doesn't exist, create the file.
		else: 
			json_data: str = json.JSONEncoder().encode(data)

			out_file = open(path, 'w')
			out_file.write(json_data)
			out_file.close()