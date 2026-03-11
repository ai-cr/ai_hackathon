from app.frontend.presentation_model import PresentationPrompt

import os
import json
import dotenv
dotenv.load_dotenv()

from google import genai
from google.genai import types

CLIENT = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))


def get_llm_response(prompt, model="gemini-3-pro-preview"):
	response = CLIENT.models.generate_content(
		model=model,
		contents=[
			prompt
		],
		config=types.GenerateContentConfig(
			response_mime_type="application/json",
			response_schema=PresetationPrompt,
			temperature=1,
			top_p=0.95,
			top_k=40,
			max_output_tokens=32000
		)
	)
	if response.text:
		return json.loads(response.text)
	elif response.parsed:
		return response.parsed
	else:
		return {"error": "No response text generated"}


# def get_response_schema():
# 	return {
#         "type": "OBJECT",
#         "properties": {field: {"type": "STRING"} for field in REQUIRED_FIELDS},
#         "required": REQUIRED_FIELDS
#     }