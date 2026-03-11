"""Form state management for Streamlit - no validation until submission"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
from app.frontend.presentation_model import PresentationPrompt, OptionalMetadata


@dataclass
class FormState:
    """Holds raw form state without validation - can be incomplete"""
    # Required fields
    topic: str = ""
    
    # Content
    target_audience: str = ""
    additional_details: str = ""
    
    # Style & theme
    theme: str = "Professional"
    slide_tone: str = "Professional"
    
    # Settings
    number_of_slides: int = 5
    language: str = "English"
    
    # Options
    include_images: bool = True
    # include_charts: bool = False ignore for now - to complicated
    generate_speaker_notes: bool = True
    
    # Optional metadata
    author_name: str = ""
    company_organization: str = ""
    presentation_date: Optional[date] = None
    
    def to_pydantic_model(self) -> PresentationPrompt:
        """
        Convert form state to validated Pydantic model.
        This is where validation happens - will raise ValidationError if invalid.
        """
        # Build optional metadata - always create it with values (can be None)
        optional_metadata = OptionalMetadata(
            author_name=self.author_name if self.author_name else None,
            company_organization=self.company_organization if self.company_organization else None,
            presentation_date=self.presentation_date
        )
        
        # Create and validate the Pydantic model
        return PresentationPrompt(
            topic=self.topic,
            target_audience=self.target_audience,
            slide_tone=self.slide_tone,  # type: ignore
            additional_details=self.additional_details,
            number_of_slides=self.number_of_slides,
            include_images=self.include_images,
            optional_metadata=optional_metadata,
            generate_speaker_notes=self.generate_speaker_notes,
            language=self.language  # type: ignore
        )


def init_form_state():
    """Initialize form state in session_state if not exists"""
    import streamlit as st
    if 'form_state' not in st.session_state:
        st.session_state.form_state = FormState()
    return st.session_state.form_state


def get_form_state() -> FormState:
    """Get current form state from session"""
    import streamlit as st
    return st.session_state.get('form_state', FormState())


def update_form_field(field_name: str, value):
    """Update a single field in form state"""
    import streamlit as st
    form_state = get_form_state()
    setattr(form_state, field_name, value)
    st.session_state.form_state = form_state
