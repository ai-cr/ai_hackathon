from app.frontend.presentation_model import PresentationPrompt, OptionalMetadata

from typing import List, Optional
from datetime import date
import os
import json
import dotenv
dotenv.load_dotenv()

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_presentation_text(presentation: PresentationPrompt, model="gemini-3-pro-preview"):
	prompt = build_prompt(presentation)
	response = CLIENT.models.generate_content(
		model=model,
		contents=[prompt],
		config=types.GenerateContentConfig(
			response_mime_type="application/json",
			response_schema=PresentationOutput,
			temperature=1,
			top_p=0.95,
			top_k=40,
			max_output_tokens=32000
		)
	)
	if response.text:
		return PresentationOutput(**json.loads(response.text))
	elif response.parsed:
		return response.parsed
	else:
		return {"error": "No response text generated"}


class Slide(BaseModel):
	slide_number: int = Field(description="The slide number, starting at 1")
	slide_title: str = Field(description="Title of the slide")
	bullet_points: List[str] = Field(description="List of bullet points or content for this slide")
	speaker_notes: Optional[str] = Field(default=None, description="Speaker notes for this slide, if requested")
	image_query: Optional[str] = Field(default=None, description="Short image search query for this slide, if images are requested")

class SlideTheme(BaseModel):
	background_color_hex: str = Field(description="Background color for all slides as a hex string without '#', e.g. '1A1A2E'")
	accent_color_hex: str = Field(description="Accent color for slide titles and highlights as a hex string without '#', e.g. '4FC3F7'")
	text_color_hex: str = Field(description="Main text color for bullet points as a hex string without '#', e.g. 'FFFFFF'")
	theme_name: str = Field(description="A short descriptive name for the theme, e.g. 'Dark Ocean' or 'Warm Sunset'")


class PresentationOutput(BaseModel):
	title: str = Field(description="The main title of the presentation")
	slides: List[Slide] = Field(description="All slides of the presentation, ordered by slide number")
	theme: SlideTheme = Field(description="The visual color theme for the entire presentation")



def build_prompt(presentation: PresentationPrompt) -> str:
	prompt = f"""
You are an expert presentation designer. Generate a complete presentation based on the following specifications:

- Topic: {presentation.topic}
- Target Audience: {presentation.target_audience}
- Tone: {presentation.slide_tone}
- Number of Slides: {presentation.number_of_slides}
- Language: {presentation.language}
- Additional Details: {presentation.additional_details}
- Include Images: {presentation.include_images}
- Generate Speaker Notes: {presentation.generate_speaker_notes}

Instructions:
- Create exactly {presentation.number_of_slides} slides.
- Each slide must have a title and bullet points.
{"- Add speaker notes for every slide." if presentation.generate_speaker_notes else "- Do not include speaker notes."}
{"- For each slide, provide a short image search query (in English) in the 'image_query' field." if presentation.include_images else "- Leave 'image_query' empty."}
- Respond in {presentation.language}.
- Choose a visually appealing color theme that fits the topic and tone. Provide hex color values (without '#') for background, accent (titles), and text colors.
- Return structured JSON output matching the required schema.
""".strip()
	return prompt



if __name__ == "__main__":

	entry = PresentationPrompt(
	    topic="Einführung in Künstliche Intelligenz",
	    target_audience="Studierende im ersten Semester",
	    slide_tone="Professional",
	    additional_details="Bitte Beispiele aus dem Alltag einbeziehen und technische Begriffe erklären.",
	    number_of_slides=10,
	    include_images=True,
	    optional_metadata=OptionalMetadata(
		    author_name="Max Mustermann",
		    company_organization="Technische Universität Berlin",
		    presentation_date=date(2026, 3, 11),
	    ),
	    generate_speaker_notes=True,
	    language="German",
    )

	pres = get_presentation_text(entry)
