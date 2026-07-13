from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from typing import Dict, List
from pdf_agent.models import ThemeSpec, CardStyleVariant


def render_highlight_cards(sections: Dict[str, List[str]], theme: ThemeSpec, width: float, style_variant: CardStyleVariant | None = None) -> Table:
    """
    Renders a horizontal row of styled panel cards. Each card has:
     - A bold section title header in a tinted accent background
     - A bullet list of items on a light background
     - A clean border with spacing between cards
    
    Args:
        sections: Ordered dict of { "Section Title": ["item 1", "item 2", ...] }
        theme: ThemeSpec with color definitions
        width: Total available page width in points
    """
    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        'HCHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.0,
        textColor=colors.HexColor(theme.highlight.header_text),
        spaceAfter=0,
        spaceBefore=0,
    )

    item_style = ParagraphStyle(
        'HCItem',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.0,
        textColor=colors.HexColor(theme.highlight.body_text),
        spaceAfter=0,
        spaceBefore=2,
    )

    n = len(sections)
    if n == 0:
        return Table([[""]])

    variant = style_variant or theme.highlight.variant
    if isinstance(variant, str):
        try:
            variant = CardStyleVariant(variant)
        except ValueError:
            variant = theme.highlight.variant

    gap = 10.0
    total_gaps = (n - 1) * gap
    card_width = (width - total_gaps) / n

    # Build one header row and one body row per card, interleaved with gap columns
    header_row = []
    body_row = []
    col_widths = []

    for i, (title, items) in enumerate(sections.items()):
        # Header cell
        header_cell = Paragraph(title, heading_style)
        header_row.append(header_cell)

        # Body cell - list of bullet item paragraphs
        body_items = [Paragraph(f"• {item}", item_style) for item in items]
        body_row.append(body_items)

        col_widths.append(card_width)

        # Insert gap column between cards
        if i < n - 1:
            header_row.append("")
            body_row.append("")
            col_widths.append(gap)

    table_data = [header_row, body_row]

    t_styles = [
        # Global alignment
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]

    # Apply per-card column styles
    col_idx = 0
    for i in range(n):
        # Header row (row 0): accent background, white text
        t_styles.extend([
            ('BACKGROUND', (col_idx, 0), (col_idx, 0), colors.HexColor(theme.highlight.header_bg)),
            ('TOPPADDING', (col_idx, 0), (col_idx, 0), 8),
            ('BOTTOMPADDING', (col_idx, 0), (col_idx, 0), 8),
            ('LEFTPADDING', (col_idx, 0), (col_idx, 0), 10),
            ('RIGHTPADDING', (col_idx, 0), (col_idx, 0), 10),
        ])
        # Body row (row 1): light background
        t_styles.extend([
            ('BACKGROUND', (col_idx, 1), (col_idx, 1), colors.HexColor(theme.highlight.body_bg)),
            ('BOX', (col_idx, 0), (col_idx, 1), 0.5, colors.HexColor(theme.highlight.border_color)),
            ('TOPPADDING', (col_idx, 1), (col_idx, 1), 8),
            ('BOTTOMPADDING', (col_idx, 1), (col_idx, 1), 10),
            ('LEFTPADDING', (col_idx, 1), (col_idx, 1), 10),
            ('RIGHTPADDING', (col_idx, 1), (col_idx, 1), 10),
        ])
        if variant == CardStyleVariant.SHADOW:
            t_styles.append(('BOX', (col_idx, 0), (col_idx, 1), 1.0, colors.HexColor(theme.highlight.border_color)))
        elif variant == CardStyleVariant.ROUNDED:
            t_styles.append(('BOX', (col_idx, 0), (col_idx, 1), 0.7, colors.HexColor(theme.highlight.border_color)))
        elif variant == CardStyleVariant.OUTLINE:
            t_styles.append(('LINEBELOW', (col_idx, 1), (col_idx, 1), 0.75, colors.HexColor(theme.highlight.border_color)))
        col_idx += 1
        # Skip gap column
        if i < n - 1:
            col_idx += 1

    outer_table = Table(table_data, colWidths=col_widths)
    outer_table.setStyle(TableStyle(t_styles))
    return outer_table
