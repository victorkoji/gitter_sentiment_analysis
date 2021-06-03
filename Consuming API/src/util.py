import urllib.request, urllib.response
import requests
from src.config import Config
import datetime, json
import os.path

class Util:

	# Call a GET request on the URL and return JSON data
	def get_json(url: str) -> dict:
		headers = {
			'Authorization':'Bearer ' + Config.get_token(),
			'Accept': 'application/json'
		}
		
		response = requests.get(url, headers=headers)
		return response.json()

	# Write data to a file on disk
	def write_json(data: str, path: str) -> None:

		#Caso o arquivo exista, apenas concatena
		if os.path.isfile(path): 
			with open(path) as json_file: 
				json_exist = json.load(json_file) 

				json_exist = data + json_exist

				json_data: str = json.JSONEncoder().encode(json_exist)

				out_file = open(path, 'w')
				out_file.write(json_data)
				out_file.close()

		#Caso o arquivo não exista
		else: 
			json_data: str = json.JSONEncoder().encode(data)

			out_file = open(path, 'w')
			out_file.write(json_data)
			out_file.close()
