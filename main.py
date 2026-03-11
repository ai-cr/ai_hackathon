from app.frontend.app import app


from app.frontend.presentation_model import PresentationPrompt, OptionalMetadata
from app.generate_pp import generate_ppt
from app.llm_logic.llm import get_presentation_text

from datetime import date


if __name__ == "__main__":
    app()


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
    prompt = get_presentation_text(entry)
    generate_ppt(prompt)
