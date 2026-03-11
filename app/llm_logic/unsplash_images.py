import requests
import dotenv

dotenv.load_dotenv()

url = "https://api.unsplash.com/search/photos"
headers = {
 "Authorization": "Client-ID YOUR_ACCESS_KEY"
}
params = {
 "query": "technology",
 "per_page": 1
}
response = requests.get(url, headers=headers,
params=params)
print(response.json()["results"][0]["urls"]["regular"])

