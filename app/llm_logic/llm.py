import requests
import dotenv

dotenv.load_dotenv()

import requests
def call_gemini_api(prompt, api_key):
	headers = {"Authorization": f"Bearer {api_key}"}
	payload = {"text": prompt}
	response = requests.post("https://api.gemini.ai/generate", json=payload, headers=headers)
	return response.json()


