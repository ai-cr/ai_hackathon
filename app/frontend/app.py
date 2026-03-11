"""PowerPoint Slide Generator - Streamlit Frontend"""

import streamlit as st
from typing import Optional


def app():
    # Page configuration
    st.set_page_config(
        page_title="AI PowerPoint Generator",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("📊 AI PowerPoint Slide Generator")
    st.markdown("Generate professional presentations powered by AI")
    st.divider()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Theme selection
        theme = st.selectbox(
            "Presentation Theme",
            ["Professional", "Modern", "Minimal", "Creative", "Corporate"],
            help="Choose the visual style for your presentation"
        )
        
        # Number of slides
        num_slides = st.slider(
            "Number of Slides",
            min_value=3,
            max_value=20,
            value=5,
            help="Approximate number of slides to generate"
        )
        
        # Additional options
        st.subheader("Options")
        include_images = st.checkbox("Include images", value=True)
        include_charts = st.checkbox("Include charts/graphs", value=False)
        speaker_notes = st.checkbox("Generate speaker notes", value=True)
        
        st.divider()
        st.markdown("### 💡 Tips")
        st.info("Be specific about your topic and target audience for best results!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Presentation Details")
        
        # Topic input
        topic = st.text_input(
            "Presentation Topic*",
            placeholder="e.g., Introduction to Machine Learning",
            help="Main topic of your presentation"
        )
        
        # Target audience
        audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Business executives, Students, Technical team",
            help="Who will be viewing this presentation?"
        )
        
        # Detailed description
        description = st.text_area(
            "Additional Details",
            placeholder="Provide any specific points, data, or structure you want to include...",
            height=150,
            help="Optional: Add specific requirements, key points, or structure"
        )
        
        # Tone selection
        tone = st.select_slider(
            "Tone",
            options=["Formal", "Professional", "Conversational", "Casual", "Fun"],
            value="Professional"
        )
    
    with col2:
        st.header("📋 Preview Settings")
        
        # Language
        language = st.selectbox(
            "Language",
            ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
        )
        
        # Aspect ratio
        aspect_ratio = st.radio(
            "Slide Aspect Ratio",
            ["16:9 (Widescreen)", "4:3 (Standard)"],
            index=0
        )
        
        # Additional metadata
        with st.expander("📌 Optional Metadata"):
            author = st.text_input("Author Name")
            company = st.text_input("Company/Organization")
            date = st.date_input("Presentation Date")
    
    st.divider()
    
    # Generation section
    col_gen1, col_gen2, col_gen3 = st.columns([1, 1, 2])
    
    with col_gen1:
        generate_btn = st.button("🚀 Generate Slides", type="primary", use_container_width=True)
    
    with col_gen2:
        if st.session_state.get('generated', False):
            st.button("📥 Download PPTX", type="secondary", use_container_width=True)
    
    # Handle generation
    if generate_btn:
        if not topic:
            st.error("⚠️ Please enter a presentation topic!")
        else:
            with st.spinner("✨ Generating your presentation..."):
                # Placeholder for actual generation logic
                import time
                time.sleep(2)  # Simulate processing
                
                # Store generation state
                st.session_state['generated'] = True
                st.session_state['topic'] = topic
                st.session_state['slides'] = num_slides
                
            st.success(f"✅ Generated {num_slides} slides for '{topic}'!")
    
    # Display generated slides preview
    if st.session_state.get('generated', False):
        st.divider()
        st.header("📄 Generated Slides Preview")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Slides", "📝 Outline", "🎤 Speaker Notes"])
        
        with tab1:
            st.info("Slide previews will appear here")
            # Placeholder for slide previews
            for i in range(1, min(4, st.session_state.get('slides', 3) + 1)):
                with st.container():
                    st.subheader(f"Slide {i}")
                    st.markdown(f"**Title:** Sample Slide Title {i}")
                    st.markdown("Content preview will appear here...")
                    st.markdown("---")
        
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
            if speaker_notes:
                st.markdown("### Speaker Notes")
                st.markdown("Detailed speaker notes for each slide will appear here...")
            else:
                st.info("Speaker notes generation is disabled. Enable in settings.")
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding: 20px;'>
        Made with ❤️ using AI | Need help? Check the documentation
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    app()