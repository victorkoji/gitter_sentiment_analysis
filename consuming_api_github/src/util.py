import requests, json, os.path, csv
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

		# If exist file, remove then
		if os.path.exists(path):
			os.remove(path)

		json_data: str = json.JSONEncoder().encode(data)

		out_file = open(path, 'w')
		out_file.write(json_data)
		out_file.close()
	
	def transformJsonToCsvObject(path: str):
		print(path)
		path_csv = path.replace(".json", ".csv")

		try:
			df = pd.read_json(path)
			df.to_csv (path_csv, sep="|")
		except:
			# If an error occurred, remove the file csv 
			if os.path.exists(path_csv):
				os.remove(path_csv)

			print("Não foi possível converter para csv.")

	def transformJsonToCsv(path: str):
		print(path)
		path_csv = path.replace(".json", ".csv")

		try:
			df = pd.read_json(path, typ='series')
			with open(path_csv, "w") as f:
				wr = csv.DictWriter(f, delimiter="|", fieldnames=list(df[0].keys()), extrasaction='ignore')
				wr.writeheader()
				wr.writerows(df)
		except:
			# If an error occurred, remove the file csv 
			if os.path.exists(path_csv):
				os.remove(path_csv)

			print("Não foi possível converter para csv.")


		# df.to_csv(path_csv, encoding='utf-8', index=False, sep="|", header=True)