from datetime import date
from typing import Literal

from pydantic import BaseModel


class OptionalMetadata(BaseModel):
    """Optional metadata for presentation generation"""
    author_name: str 
    company_organization: str  # name of company or org
    presentation_date: date


class PresentationPrompt(BaseModel):
    """
    The main model that describes the content of a 
    presentation prompt
    """

    topic: str
    target_audience: str
    slide_tone: Literal["Formal", "Professional", "Conversational", "Casual", "Fun"]
    additional_details: str
    number_of_slides: int

    include_images: bool

    optional_metadata: OptionalMetadata

    generate_speaker_notes: bool

    language : str | Literal["English"]