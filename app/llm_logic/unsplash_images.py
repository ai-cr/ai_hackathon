import requests
import os

import dotenv
dotenv.load_dotenv()

from PIL import Image
from io import BytesIO


dotenv.load_dotenv()

url = "https://api.unsplash.com/search/photos"
headers = {
 "Authorization": f'Client-ID {os.getenv("UNSPLASH_ACCESS_KEY")}'
}

def get_unsplash_image(query, retries=10):
	params = {
	 "query": query,
	 "per_page": 1
	}
	print(query)
	for _ in range(retries):
		try:
			response = requests.get(url, headers=headers, params=params)
			return response.json()["results"][0]["urls"]["regular"]
		except Exception as e:
			print(f"Error fetching image: {e}")
			continue

def get_image_object(image_url: str) -> BytesIO:
	response = requests.get(image_url)
	return BytesIO(response.content)

def download_image(image_url: str, save_path: str = "image.jpg") -> str:
	response = requests.get(image_url)
	with open(save_path, "wb") as f:
		f.write(response.content)
	return save_path
