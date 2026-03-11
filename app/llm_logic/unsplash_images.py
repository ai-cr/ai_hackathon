import requests
import dotenv
import os


dotenv.load_dotenv()

url = "https://api.unsplash.com/search/photos"
headers = {
 "Authorization": f'Client-ID {os.getenv("UNSPLASH_ACCESS_KEY")}'
}

def get_unsplash_image(query):
	params = {
	 "query": query,
	 "per_page": 1
	}
	response = requests.get(url, headers=headers, params=params)
	print(response.json()["results"][0]["urls"]["regular"])
