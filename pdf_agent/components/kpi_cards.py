from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from typing import Dict
from pdf_agent.models import ThemeSpec, KpiStyleVariant

def render_kpi_cards(kpis: Dict[str, str], theme: ThemeSpec, width: float, style_variant: KpiStyleVariant | None = None) -> Table:
    """
    Renders metric key-value pairs as a horizontal grid of rounded/bordered card blocks.
    Each block features a large styled statistic and a small label below it.
    All cards will have equal height and width, and will wrap symmetrically.
    """
    styles = getSampleStyleSheet()
    
    value_style = ParagraphStyle(
        'KPIValue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16.0,  # Slightly reduced for better wrapping in long content
        leading=19.0,
        textColor=colors.HexColor(theme.primary_color),
        alignment=1  # Centered
    )
    
    label_style = ParagraphStyle(
        'KPILabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.0,
        textColor=colors.HexColor(theme.kpi.label_color),
        alignment=1  # Centered
    )
    
    n = len(kpis)
    if n == 0:
        return Table([[]])
        
    gap = 12.0
    total_gaps = (n - 1) * gap if n > 1 else 0
    card_width = (width - total_gaps) / n
    
    row_content = []
    col_widths = []
    t_styles = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]
    variant = style_variant or theme.kpi.variant
    if isinstance(variant, str):
        try:
            variant = KpiStyleVariant(variant)
        except ValueError:
            variant = theme.kpi.variant
    
    col_index = 0
    for i, (label, val) in enumerate(kpis.items()):
        # Each cell gets a list of paragraphs/flowables
        cell_flowables = [
            Paragraph(f"<b>{val}</b>", value_style),
            Spacer(1, 4),
            Paragraph(label, label_style)
        ]
        
        # Add card cell
        row_content.append(cell_flowables)
        col_widths.append(card_width)
        
        # Apply style to this card column
        card_styles = [
            ('BACKGROUND', (col_index, 0), (col_index, 0), colors.HexColor(theme.kpi.bg_color)),
            ('BOX', (col_index, 0), (col_index, 0), 0.5, colors.HexColor(theme.kpi.border_color)),
            ('TOPPADDING', (col_index, 0), (col_index, 0), 10),
            ('BOTTOMPADDING', (col_index, 0), (col_index, 0), 10),
            ('LEFTPADDING', (col_index, 0), (col_index, 0), 8),
            ('RIGHTPADDING', (col_index, 0), (col_index, 0), 8),
        ]
        if variant == KpiStyleVariant.OUTLINED:
            card_styles.append(('BACKGROUND', (col_index, 0), (col_index, 0), colors.white))
        elif variant == KpiStyleVariant.FILLED:
            card_styles.append(('BACKGROUND', (col_index, 0), (col_index, 0), colors.HexColor(theme.kpi.bg_color)))
        elif variant == KpiStyleVariant.TOP_ACCENT:
            card_styles.append(('LINEABOVE', (col_index, 0), (col_index, 0), 2.0, colors.HexColor(theme.kpi.value_color)))
        elif variant == KpiStyleVariant.BOTTOM_ACCENT:
            card_styles.append(('LINEBELOW', (col_index, 0), (col_index, 0), 2.0, colors.HexColor(theme.kpi.value_color)))
        t_styles.extend(card_styles)
        col_index += 1
        
        # Add spacer cell if not the last card
        if i < n - 1:
            row_content.append("")
            col_widths.append(gap)
            col_index += 1
            
    outer_table = Table([row_content], colWidths=col_widths)
    outer_table.setStyle(TableStyle(t_styles))
    return outer_table
