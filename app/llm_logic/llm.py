import os

import requests
import dotenv
dotenv.load_dotenv()
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY_HERE")


# def call_gemini_api(prompt, api_key):
# 	headers = {"Authorization": f"Bearer {api_key}"}
# 	payload = {"text": prompt}
# 	response = requests.post("https://api.gemini.ai/generate", json=payload, headers=headers)
# 	return response.json()

def get_llm_response(prompt, model="gemini-3.1"):
	model = genai.GenerativeModel(model)
	response = model.generate_content(prompt)
	print(response.text)
	return response["candidates"][0]["content"]["parts"][0]["text"]
