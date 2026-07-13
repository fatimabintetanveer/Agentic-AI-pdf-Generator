from reportlab.platypus import Table, TableStyle, HRFlowable, Spacer, Paragraph
from reportlab.lib import colors
from typing import List, Any, Optional
from pdf_agent.models import ThemeSpec, DividerStyleVariant

def render_divider(theme: ThemeSpec, width: float, style_variant: DividerStyleVariant | None = None) -> HRFlowable:
    """Renders a elegant, thin horizontal divider colored in secondary theme tone."""
    variant = style_variant or theme.divider.variant
    if isinstance(variant, str):
        try:
            variant = DividerStyleVariant(variant)
        except ValueError:
            variant = theme.divider.variant

    thickness = theme.divider.thickness
    color = colors.HexColor(theme.divider.color)
    if variant == DividerStyleVariant.DOUBLE_LINE:
        thickness = max(thickness, 0.8)
    elif variant == DividerStyleVariant.ACCENT_BAR:
        thickness = max(thickness, 1.2)
        color = colors.HexColor(theme.primary_color)
    elif variant == DividerStyleVariant.DOTTED:
        thickness = max(thickness, 0.35)
    elif variant == DividerStyleVariant.DASHED:
        thickness = max(thickness, 0.35)
    elif variant == DividerStyleVariant.WAVE:
        thickness = max(thickness, 1.0)
    return HRFlowable(
        width=width,
        thickness=thickness,
        color=color,
        spaceBefore=0,
        spaceAfter=15
    )

def render_two_column(left_flowables: List[Any], right_flowables: List[Any], width: float, spacing: float = 12, col_ratio: float = 0.5) -> Table:
    """
    Renders elements side by side using a 2-column Layout Table.
    col_ratio controls how much of the total width the LEFT column takes:
    - 0.5 = equal 50/50 split (default)
    - 0.6 = left takes 60%, right takes 40%
    - 0.4 = left takes 40%, right takes 60%
    """
    usable_width = width - spacing
    left_w = usable_width * col_ratio
    right_w = usable_width * (1.0 - col_ratio)
    outer_table = Table([[left_flowables, right_flowables]], colWidths=[left_w, right_w])
    outer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        # Outer left and right: no padding
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('RIGHTPADDING', (-1, 0), (-1, -1), 0),
        # Inner gutter: half the spacing on each inner edge
        ('RIGHTPADDING', (0, 0), (0, -1), spacing / 2),
        ('LEFTPADDING', (1, 0), (1, -1), spacing / 2),
    ]))
    return outer_table
