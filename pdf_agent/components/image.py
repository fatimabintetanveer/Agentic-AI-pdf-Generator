import os
from typing import List, Any
from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from pdf_agent.models import ThemeSpec, ImageStyleVariant
from pdf_agent.components.elements import render_paragraph

def render_image(img_path: str, caption: str, theme: ThemeSpec, width: float, style_variant: ImageStyleVariant | None = None) -> List[Any]:
    """
    Renders an image scaled to the provided width while preserving aspect ratio.
    Optionally renders a styled caption below the image.
    """
    flowables = []
    if os.path.exists(img_path):
        try:
            from reportlab.lib.utils import ImageReader
            # Read original image dimensions to preserve aspect ratio
            img_reader = ImageReader(img_path)
            orig_w, orig_h = img_reader.getSize()
            aspect_ratio = orig_h / float(orig_w)
            calculated_height = width * aspect_ratio
            
            # Scale image to fit within page width while preserving aspect ratio
            img = Image(img_path, width=width, height=calculated_height)
            img.hAlign = "CENTER"
            flowables.append(img)
            
            # Render caption below the image if present
            variant = style_variant or theme.image.variant
            if isinstance(variant, str):
                try:
                    variant = ImageStyleVariant(variant)
                except ValueError:
                    variant = theme.image.variant

            if caption:
                caption_style = ParagraphStyle(
                    'ImageCaption',
                    fontName='Helvetica-Oblique',
                    fontSize=8.5,
                    leading=12,
                    textColor=colors.HexColor(theme.secondary_color),
                    alignment=1,  # Center
                    spaceBefore=4,
                    spaceAfter=10,
                )
                if variant == ImageStyleVariant.CAPTION_OVERLAY:
                    caption_style.textColor = colors.HexColor(theme.primary_color)
                flowables.append(Paragraph(caption, caption_style))
            else:
                flowables.append(Spacer(1, 10))
        except Exception as e:
            flowables.append(render_paragraph(f"[Image: {img_path}]", theme))
    else:
        flowables.append(render_paragraph(f"[Image not found: {img_path}]", theme))
        
    return flowables
