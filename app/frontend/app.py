"""PowerPoint Slide Generator - Streamlit Frontend"""

from io import BytesIO
import datetime as dt

import streamlit as st
from pydantic import ValidationError
from app.frontend.form_state import FormState, init_form_state
from app.frontend.generate_ppt import generate_presentation
from app.llm_logic.llm import PresentationOutput
from app.llm_logic.unsplash_images import get_unsplash_image
from app.generate_pp import generate_ppt

import datetime as dt

st.session_state.show_down_btn = False
st.session_state.generated_presentation = None
st.session_state.generated = False
st.session_state.show_btn = False
st.session_state.validated_model = None
st.session_state.ppt_buffer = None

def render_sidebar(form_state: FormState) -> None:
    """Render the sidebar with settings and options"""
    with st.sidebar:
        st.header("⚙️ Settings")

        # Language
        form_state.language = st.selectbox(
            "Language",
            ["English", "Spanish", "French", "German", "Chinese", "Japanese"],
            index=["English", "Spanish", "French", "German", "Chinese", "Japanese"].index(form_state.language)
        )

        # Theme selection
        form_state.theme = st.selectbox(
            "Presentation Theme",
            ["Professional", "Modern", "Minimal", "Creative", "Corporate"],
            index=["Professional", "Modern", "Minimal", "Creative", "Corporate"].index(form_state.theme),
            help="Choose the visual style for your presentation"
        )
        
        # Number of slides
        form_state.number_of_slides = st.slider(
            "Number of Slides",
            min_value=3,
            max_value=20,
            value=form_state.number_of_slides,
            help="Approximate number of slides to generate"
        )
        
        # Additional options
        st.subheader("Options")
        form_state.include_images = st.checkbox(
            "Include images", 
            value=form_state.include_images
        )
        # form_state.include_charts = st.checkbox(
        #     "Include charts/graphs", 
        #     value=form_state.include_charts
        # )
        form_state.generate_speaker_notes = st.checkbox(
            "Generate speaker notes", 
            value=form_state.generate_speaker_notes
        )

        render_optional_metadata_settings(form_state)

        st.divider()
        st.markdown("### 💡 Tips")
        st.info("Be specific about your topic and target audience for best results!")


def render_main_form(form_state: FormState) -> None:
    """Render the main form section with presentation details"""
    st.header("📝 Presentation Details")
    
    # Topic input
    form_state.topic = st.text_input(
        "Presentation Topic*",
        value=form_state.topic,
        placeholder="e.g., Introduction to Machine Learning",
        help="Main topic of your presentation"
    )
    
    # Target audience
    form_state.target_audience = st.text_input(
        "Target Audience",
        value=form_state.target_audience,
        placeholder="e.g., Business executives, Students, Technical team",
        help="Who will be viewing this presentation?"
    )
    
    # Detailed description
    form_state.additional_details = st.text_area(
        "Additional Details",
        value=form_state.additional_details,
        placeholder="Provide any specific points, data, or structure you want to include...",
        height=150,
        help="Optional: Add specific requirements, key points, or structure"
    )
    
    # Tone selection
    form_state.slide_tone = st.select_slider(
        "Tone",
        options=["Formal", "Professional", "Conversational", "Casual", "Fun"],
        value=form_state.slide_tone
    )


def render_optional_metadata_settings(form_state: FormState) -> None:
    """Render the preview settings section"""
    
    # Additional metadata
    with st.expander("📌 Optional Metadata"):
        form_state.author_name = st.text_input(
            "Author Name",
            value=form_state.author_name
        )
        form_state.company_organization = st.text_input(
            "Company/Organization",
            value=form_state.company_organization
        )
        form_state.presentation_date = st.date_input(
            "Presentation Date",
            value=form_state.presentation_date
        )


def handle_generation(form_state: FormState) -> None:
    """Handle the generation button click and validation"""
    col_gen1, col_gen2, _ = st.columns([1, 1, 2])
    
    with col_gen1:
        generate_btn = st.button("🚀 Generate Slides", type="primary", use_container_width=True)
    
    with col_gen2:
        print("show button down") 
        presentation_output = st.session_state.get("generated_presentation", None)
        generated = st.session_state.get('generated', False)
        ppt_buffer = st.session_state.get("ppt_buffer", None)
        show_btn = st.session_state.get('show_down_btn', False)
        validated_model = st.session_state.get('validated_model', None)

        if validated_model:
            filename = f"{validated_model.topic[:30].replace(' ', '_')}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        else:
            filename = "test"

        if ppt_buffer is not None:
            st.download_button(
                label="📥 Download PPTX",
                data=st.session_state['ppt_buffer'],
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                type="secondary",
                use_container_width=True
            )
        else:
            print("not showing down button")

      
    # Handle generation
    if generate_btn:
        try:
            # Convert form state to validated Pydantic model
            validated_model = form_state.to_pydantic_model()
            
            # Store validated model in session state
            st.session_state['validated_model'] = validated_model
            
            with st.spinner("✨ Generating your presentation..."):
                # Clear any previously cached PPT
                if 'ppt_buffer' in st.session_state:
                    del st.session_state['ppt_buffer']
                
                print("Generating Presentation")
                models = [
                    "gemini-3.1-pro-preview",
                    # "gemini-3.1-flash-lite-preview",
                    # "gemini-2.5-pro",
                    "gemini-2.5-flash-lite", # budget
                    "gemini-2.5-flash",
                    "Gemini-2-flash"
                ]
                for model in models:
                    print("using model: ", model)
                    try:
                        presentation = generate_presentation(form_state.to_pydantic_model(), model)
                        break
                    except Exception as e:
                        print("Error on gen: ", e)
                print("Pres generation done")

                st.session_state["generated_presentation"] = presentation
                st.session_state['generated'] = True

                prs = generate_ppt(presentation, validated_model, save_localy=False)
                print("ppt file created")
                
                # Save the Presentation object to a BytesIO buffer
                ppt_buffer = BytesIO()
                prs.save(ppt_buffer)
                ppt_buffer.seek(0)
                st.session_state["ppt_buffer"] = ppt_buffer
                print("ppt saved to buffer")

                st.session_state.show_down_btn = True

                print("set all states")
                
            st.success(f"✅ Generated {validated_model.number_of_slides} slides for '{validated_model.topic}'!")
            st.rerun()


            # Display the validated form data
            # with st.expander("📋 View Form Data"):
            #     st.json(validated_model.model_dump(mode='json'))
                
        except ValidationError as e:
            st.error("⚠️ Please fix the following errors:")
            for error in e.errors():
                field = " → ".join(str(x) for x in error['loc'])
                st.error(f"**{field}**: {error['msg']}")


def render_slides_preview(form_state: FormState) -> None:
    """Render the generated slides preview section"""

    presentation: PresentationOutput = st.session_state.get('generated_presentation')

    if not st.session_state.get('generated', False) or presentation is None:
        return


    st.divider()
    st.header("📄 Generated Slides Preview")
    
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Slides", "📝 Outline", "🎤 Speaker Notes"])
    
    with tab1:
        st.info("Slide previews will appear here")

        for i, slide in enumerate(presentation.slides): 
            with st.container():
                st.subheader(f"Slide {i + 1}")
                st.markdown(f"**Title:**  {slide.slide_title}")
                for bp in slide.bullet_points: 
                    st.markdown(f"- {bp}")
                
                # Display image if available
                if slide.image_query:
                    image_url = get_unsplash_image(slide.image_query)
                    if image_url:
                        st.image(image_url)
                    else:
                        st.caption(f"📷 Image not found for: {slide.image_query}")
    
    with tab2:
        st.markdown("""
        ### Presentation Outline
        1. **Introduction**
           - Opening slide
           - Agenda
        
        2. **Main Content**
           - Key points
           - Supporting data
        
        3. **Conclusion**
           - Summary
           - Call to action
        """)
    
    with tab3:
        if form_state.generate_speaker_notes:
            st.markdown("### Speaker Notes")
            st.markdown("Detailed speaker notes for each slide will appear here...")
            for i, slide in enumerate(presentation.slides):
                st.markdown(f'Slide: {i + 1}')
                st.markdown(slide.speaker_notes)


        else:
            st.info("Speaker notes generation is disabled. Enable in settings.")

def render_footer() -> None:
    """Render the page footer"""
    st.divider()


def app():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title="AI PowerPoint Generator",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize form state (no validation yet)
    form_state = init_form_state()
    
    # Header
    st.title("📊 AI PowerPoint Slide Generator")
    st.markdown("Generate professional presentations powered by AI")
    st.divider()
    
    # Render sidebar settings
    render_sidebar(form_state)
    
    # Main content area
    # col1, col2 = st.columns([2, 1])
    
    # with col1:
    render_main_form(form_state)
    
    
    st.divider()
    
    # Handle generation and validation
    handle_generation(form_state)
    
    # Display generated slides preview
    render_slides_preview(form_state)
    
    # Footer
    render_footer()