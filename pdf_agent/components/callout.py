from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from pdf_agent.models import ThemeSpec, CalloutStyleVariant
from pdf_agent.components.elements.util import format_inline_markdown

def render_callout(text: str, theme: ThemeSpec, width: float, style_variant: CalloutStyleVariant | None = None) -> Table:
    """
    Renders text inside a modern callout panel with a solid accent bar on the left 
    and a matching light background color.
    """
    styles = getSampleStyleSheet()
    quote_text_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10.0,
        leading=14.0,
        textColor=colors.HexColor(theme.primary_color)
    )
    
    p = Paragraph(format_inline_markdown(text), quote_text_style)
    # Renders the callout container as a 1x1 table
    callout_table = Table([[p]], colWidths=[width])
    
    # Base padding
    t_style = [
        ('TOPPADDING', (0, 0), (-1, -1), theme.callout.padding),
        ('BOTTOMPADDING', (0, 0), (-1, -1), theme.callout.padding),
        ('LEFTPADDING', (0, 0), (-1, -1), theme.callout.padding),
        ('RIGHTPADDING', (0, 0), (-1, -1), theme.callout.padding),
    ]

    variant = style_variant or theme.callout.variant
    if isinstance(variant, str):
        try:
            variant = CalloutStyleVariant(variant)
        except ValueError:
            variant = theme.callout.variant

    if variant == CalloutStyleVariant.FILLED_BOX:
        t_style.extend([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(theme.callout.bg_color)),
            ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor(theme.callout.border_color)),
        ])
    elif variant == CalloutStyleVariant.QUOTE:
        # Quote style: no background, thick top/bottom borders
        t_style.extend([
            ('LINEABOVE', (0, 0), (-1, 0), 2.0, colors.HexColor(theme.callout.border_color)),
            ('LINEBELOW', (0, 0), (-1, -1), 2.0, colors.HexColor(theme.callout.border_color)),
        ])
    elif variant == CalloutStyleVariant.FLOATING_CARD:
        # Simulate a card: white background, light gray box border
        t_style.extend([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ffffff")),
            ('BOX', (0, 0), (-1, -1), theme.table_border_width, colors.HexColor(theme.table_grid_color)),
        ])
    else:
        # LEFT_BORDER (default)
        t_style.extend([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(theme.callout.bg_color)),
            ('LEFTPADDING', (0, 0), (-1, -1), theme.callout.padding + 4),
            ('LINELEFT', (0, 0), (0, -1), theme.callout.border_width, colors.HexColor(theme.callout.border_color)),
        ])

    callout_table.setStyle(TableStyle(t_style))
    return callout_table
