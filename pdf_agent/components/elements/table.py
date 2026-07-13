from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle

from pdf_agent.models import ThemeSpec, TableStyleVariant
from .util import format_inline_markdown, create_text_style


def render_table(grid_data, theme: ThemeSpec, width: float, table_style: TableStyleVariant | None = None) -> Table:
    if grid_data and isinstance(grid_data[0], dict):
        grid_data = [list(row.values()) for row in grid_data]

    cell_style = create_text_style("TableCell", "Helvetica", 9.0, 12.0, "#1e293b", space_after=0)
    first_col_style = create_text_style("TableFirstCell", "Helvetica-Bold", 9.0, 12.0, "#1e293b", space_after=0)
    header_text_color = theme.table_header_text
    header_style = create_text_style("TableHeaderCell", "Helvetica-Bold", 9.0, 12.0, header_text_color, space_after=0)

    formatted_data = []
    for row_idx, row in enumerate(grid_data):
        formatted_row = []
        for col_idx, cell in enumerate(row):
            style = header_style if row_idx == 0 else first_col_style if col_idx == 0 else cell_style
            formatted_row.append(Paragraph(format_inline_markdown(str(cell)), style))
        formatted_data.append(formatted_row)

    num_cols = len(grid_data[0])
    col_max_lengths = [0] * num_cols
    for row in grid_data:
        for col_idx, cell in enumerate(row):
            if col_idx < num_cols:
                col_max_lengths[col_idx] = max(col_max_lengths[col_idx], len(str(cell)))

    total_chars = sum(col_max_lengths)
    if total_chars > 0:
        min_col_width = width * 0.10
        distributable_width = width - (min_col_width * num_cols)
        col_widths = [min_col_width + (distributable_width * (char_len / total_chars)) for char_len in col_max_lengths]
    else:
        col_widths = [width / num_cols] * num_cols

    table = Table(formatted_data, colWidths=col_widths)
    t_style = [
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), theme.table_padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), theme.table_padding),
        ("LEFTPADDING", (0, 0), (-1, -1), theme.table_padding + 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), theme.table_padding + 2),
    ]

    variant = table_style or theme.table.variant
    if isinstance(variant, str):
        try:
            variant = TableStyleVariant(variant)
        except ValueError:
            variant = theme.table.variant

    if variant == TableStyleVariant.FILLED_HEADER:
        t_style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.table_header_bg)),
            ("LINEBELOW", (0, 1), (-1, -1), theme.table_border_width, colors.HexColor(theme.table_grid_color)),
        ])
    elif variant == TableStyleVariant.CORPORATE:
        t_style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.table_header_bg)),
            ("BACKGROUND", (0, 1), (0, -1), colors.HexColor(theme.table_row_even_bg)),
            ("GRID", (0, 0), (-1, -1), theme.table_border_width, colors.HexColor(theme.table_grid_color)),
            ("BOX", (0, 0), (-1, -1), max(theme.table_border_width * 2, 1.0), colors.HexColor(theme.primary_color)),
        ])
    elif variant == TableStyleVariant.ROUNDED:
        t_style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.table_header_bg)),
            ("LINEBELOW", (0, 0), (-1, -1), theme.table_border_width, colors.HexColor(theme.table_grid_color)),
            ("BOX", (0, 0), (-1, -1), theme.table_border_width, colors.HexColor(theme.table_grid_color)),
            ("LINELEFT", (0, 0), (0, -1), 3.0, colors.HexColor(theme.primary_color)),
        ])
    elif variant == TableStyleVariant.ZEBRA:
        t_style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.table_header_bg)),
            ("LINEBELOW", (0, 0), (-1, 0), 1.5, colors.HexColor(theme.primary_color)),
            ("LINEBELOW", (0, 1), (-1, -1), theme.table_border_width, colors.HexColor(theme.table_grid_color)),
        ])
        for row_idx in range(1, len(grid_data)):
            if row_idx % 2 == 0:
                t_style.append(("BACKGROUND", (0, row_idx), (-1, row_idx), colors.HexColor(theme.table_row_even_bg)))
    else:
        t_style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.table_header_bg)),
            ("LINEBELOW", (0, 0), (-1, 0), 1.5, colors.HexColor(theme.primary_color)),
            ("LINEBELOW", (0, 1), (-1, -1), theme.table_border_width, colors.HexColor(theme.table_grid_color)),
        ])
        for row_idx in range(1, len(grid_data)):
            if row_idx % 2 == 0:
                t_style.append(("BACKGROUND", (0, row_idx), (-1, row_idx), colors.HexColor(theme.table_row_even_bg)))

    table.setStyle(TableStyle(t_style))
    return table
