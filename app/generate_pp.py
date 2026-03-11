from io import BytesIO

from app.llm_logic.llm import PresentationOutput
from app.llm_logic.unsplash_images import get_unsplash_image, get_image_object

from pptx import Presentation
from pptx.util import Inches, Pt
import datetime as dt


def generate_ppt(prompt: PresentationOutput) -> str:
    filename = f"pp_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
    prs = Presentation()

    slide_width = prs.slide_width
    slide_height = prs.slide_height

    title_slide_layout = prs.slide_layouts[0]
    title_slide = prs.slides.add_slide(title_slide_layout)
    title_slide.shapes.title.text = prompt.title

    for slide_data in prompt.slides:
        layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(layout)

        slide.shapes.title.text = slide_data.slide_title

        content_placeholder = slide.placeholders[1]
        tf = content_placeholder.text_frame
        tf.clear()
        for i, bullet in enumerate(slide_data.bullet_points):
            if i == 0:
                tf.paragraphs[0].text = bullet
            else:
                p = tf.add_paragraph()
                p.text = bullet
                p.level = 0

        if slide_data.speaker_notes:
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = slide_data.speaker_notes

        if slide_data.image_query:
            image_url = get_unsplash_image(slide_data.image_query)
            if image_url:
                image_stream: BytesIO = get_image_object(image_url)
                img_width = Inches(3.5)
                img_height = Inches(3.0)
                left = slide_width - img_width - Inches(0.3)
                top = (slide_height - img_height) // 2
                slide.shapes.add_picture(image_stream, left, top, img_width, img_height)

    prs.save(filename)
    return filename