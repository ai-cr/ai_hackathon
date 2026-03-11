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

def get_unsplash_image(query):
	params = {
	 "query": query,
	 "per_page": 1
	}
	response = requests.get(url, headers=headers, params=params)
	return response.json()["results"][0]["urls"]["regular"]

def get_image_object(image_url: str) -> Image.Image:
	response = requests.get(image_url)
	return BytesIO(response.content)

def download_image(image_url: str, save_path: str = "image.jpg") -> str:
	response = requests.get(image_url)
	with open(save_path, "wb") as f:
		f.write(response.content)
	return save_path
