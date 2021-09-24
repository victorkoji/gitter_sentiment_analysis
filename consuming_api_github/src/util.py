from os import sep
import urllib.response
import requests
import json
import os.path
import pandas as pd

class Util:

	# Call a GET request on the URL and return JSON data
	def get_json(url: str) -> dict:
		response = requests.get(url)
		return response.json()

	# Write data to a file on disk
	def write_json(data: str, path: str) -> None:

		#Caso o arquivo exista, apenas concatena
		if os.path.isfile(path): 
			with open(path) as json_file: 
				json_exist = json.load(json_file) 

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
	
	def transformJsonToCsv(path: str):
		print(path)
		df = pd.read_json(path, typ='series')
		path_csv = path.replace(".json", ".csv")
		df.to_csv(path_csv, encoding='utf-8', index=False, sep="|")