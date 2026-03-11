from app.llm_logic.llm import PresentationPrompt, get_presentation_text, OptionalMetadata
from app.generate_pp import generate_ppt
from app.frontend.app import app

from datetime import date

if __name__ == "__main__":
    # app()

    print("generating presentation...")
    entry = PresentationPrompt(
	    topic="Einführung in Künstliche Intelligenz",
	    target_audience="Studierende im ersten Semester",
	    slide_tone="Professional",
	    additional_details="Bitte Beispiele aus dem Alltag einbeziehen und technische Begriffe erklären.",
	    number_of_slides=4,
	    include_images=True,
	    optional_metadata=OptionalMetadata(
		    author_name="Max Mustermann",
		    company_organization="Technische Universität Berlin",
		    presentation_date=date(2026, 3, 11),
	    ),
	    generate_speaker_notes=True,
	    language="German",
    )
    prompt = get_presentation_text(entry, model="gemini-2.5-flash")
    print(generate_ppt(prompt, entry, True))
