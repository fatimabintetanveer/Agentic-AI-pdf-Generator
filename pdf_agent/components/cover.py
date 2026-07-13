from reportlab.platypus import Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from typing import List, Any
from pdf_agent.models import ThemeSpec, CoverStyle

def render_cover_page(title: str, subtitle: str, metadata: dict, theme: ThemeSpec, cover_style: CoverStyle = CoverStyle.CENTERED) -> List[Any]:
    """
    Renders flowable blocks for a professional cover page.
    Utilizes spacing to center contents beautifully on the page.
    """
    styles = getSampleStyleSheet()
    
    if cover_style in (CoverStyle.CENTERED, CoverStyle.MINIMAL):
        title_alignment = 1
        title_size = 30.0 if cover_style == CoverStyle.CENTERED else 28.0
        subtitle_size = 14.0 if cover_style == CoverStyle.CENTERED else 13.0
    else:
        title_alignment = 0
        title_size = 30.0
        subtitle_size = 14.0

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=title_size,
        leading=title_size + 6.0,
        textColor=colors.HexColor(theme.primary_color),
        spaceAfter=15,
        alignment=title_alignment
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=subtitle_size,
        leading=subtitle_size + 4.0,
        textColor=colors.HexColor(theme.secondary_color),
        spaceAfter=40,
        alignment=title_alignment
    )
    
    meta_label_style = ParagraphStyle(
        'CoverMetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.0,
        leading=14.0,
        textColor=colors.HexColor(theme.accent_color),
        spaceAfter=2
    )
    
    meta_val_style = ParagraphStyle(
        'CoverMetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.0,
        leading=14.0,
        textColor=colors.HexColor(theme.primary_color),
        spaceAfter=10
    )
    
    story = []

    if cover_style == CoverStyle.MINIMAL:
        story.append(Spacer(1, 140))
    elif cover_style == CoverStyle.CENTERED:
        story.append(Spacer(1, 130))
    elif cover_style == CoverStyle.SPLIT_LAYOUT:
        story.append(Spacer(1, 90))
    else:
        story.append(Spacer(1, 110))
    
    # Title & Subtitle block
    story.append(Paragraph(title, title_style))
    if subtitle:
        story.append(Paragraph(subtitle, subtitle_style))
        
    story.append(Spacer(1, 100))
    
    # Metadata fields (e.g. Prepared for, Prepared by)
    meta_blocks = []
    for k, v in metadata.items():
        if v:
            meta_blocks.append(Paragraph(f"{k.upper()}:", meta_label_style))
            meta_blocks.append(Paragraph(str(v), meta_val_style))
            
    if meta_blocks:
        story.append(KeepTogether(meta_blocks))
    
    return story
