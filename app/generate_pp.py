from io import BytesIO
from lxml import etree

from app.llm_logic.llm import PresentationOutput
from app.llm_logic.unsplash_images import get_unsplash_image, get_image_object

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import datetime as dt


# 16:9 dimensions
SLIDE_WIDTH  = Inches(13.33)
SLIDE_HEIGHT = Inches(7.5)

IMG_WIDTH  = Inches(5.5)
IMG_HEIGHT = Inches(5.5)
MARGIN     = Inches(0.3)
FONT_SIZE  = Pt(14)


def hex_to_rgb(hex_str: str) -> RGBColor:
    """Convert a hex color string (without '#') to RGBColor."""
    hex_str = hex_str.strip().lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return RGBColor(r, g, b)


def apply_background_color(slide, color: RGBColor):
    """Apply a solid background fill color to a slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def generate_ppt(prompt: PresentationOutput) -> str:
    filename = f"pp_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
    prs = Presentation()

    # Set 16:9 aspect ratio
    prs.slide_width  = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    # Parse theme colors
    theme = prompt.theme
    bg_color     = hex_to_rgb(theme.background_color_hex)
    accent_color = hex_to_rgb(theme.accent_color_hex)
    text_color   = hex_to_rgb(theme.text_color_hex)

    # --- Title Slide ---
    title_slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    apply_background_color(title_slide, bg_color)

    title_box = title_slide.shapes.add_textbox(
        Inches(1.5), Inches(2.5), Inches(10.0), Inches(2.5)
    )
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = prompt.title
    run = p.runs[0]
    run.font.size = Pt(40)
    run.font.bold = True
    run.font.color.rgb = accent_color

    # --- Content Slides ---
    for slide_data in prompt.slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
        apply_background_color(slide, bg_color)

        has_image = bool(slide_data.image_query)

        if has_image:
            img_left   = MARGIN
            img_top    = (SLIDE_HEIGHT - IMG_HEIGHT) / 2
            text_left  = IMG_WIDTH + MARGIN * 2
            text_width = SLIDE_WIDTH - text_left - MARGIN
        else:
            text_left  = MARGIN
            text_width = SLIDE_WIDTH - MARGIN * 2

        text_top    = Inches(0.5)
        text_height = SLIDE_HEIGHT - Inches(1.0)

        # Slide title
        title_box = slide.shapes.add_textbox(text_left, text_top, text_width, Inches(0.9))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = slide_data.slide_title
        run_title = p_title.runs[0]
        run_title.font.size = Pt(24)
        run_title.font.bold = True
        run_title.font.color.rgb = accent_color

        # Bullet points
        bullet_top = text_top + Inches(1.0)
        bullet_box = slide.shapes.add_textbox(text_left, bullet_top, text_width, text_height - Inches(1.0))
        tf_bullets = bullet_box.text_frame
        tf_bullets.word_wrap = True
        for i, bullet in enumerate(slide_data.bullet_points):
            p = tf_bullets.paragraphs[0] if i == 0 else tf_bullets.add_paragraph()
            p.text = f"• {bullet}"
            run = p.runs[0]
            run.font.size = FONT_SIZE
            run.font.color.rgb = text_color

        # Speaker notes
        if slide_data.speaker_notes:
            slide.notes_slide.notes_text_frame.text = slide_data.speaker_notes

        # Image (left side)
        if has_image:
            image_url = get_unsplash_image(slide_data.image_query)
            if image_url:
                image_stream: BytesIO = get_image_object(image_url)
                slide.shapes.add_picture(image_stream, img_left, img_top, IMG_WIDTH, IMG_HEIGHT)

    prs.save(filename)
    return filename