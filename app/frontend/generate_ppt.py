from app.llm_logic.llm import get_presentation_text
from app.frontend.presentation_model import PresentationPrompt


def generate_presentation(p: PresentationPrompt, model: str):
    return get_presentation_text(p, model)