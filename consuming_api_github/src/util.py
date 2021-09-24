import requests, json, os.path
import pandas as pd
from src.config import Config
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

		# If exist file,remove then
		if os.path.exists(path):
			os.remove(path)

		json_data: str = json.JSONEncoder().encode(data)

		out_file = open(path, 'w')
		out_file.write(json_data)
		out_file.close()
	
	def transformJsonToCsv(path: str):
		print(path)
		df = pd.read_json(path, typ='series')
		path_csv = path.replace(".json", ".csv")
		df.to_csv(path_csv, encoding='utf-8', index=False, sep="|")