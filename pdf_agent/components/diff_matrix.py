from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Optional

from reportlab.graphics.shapes import Circle, Drawing, Line
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle

from pdf_agent.models import ThemeSpec
from .elements.util import format_inline_markdown


def _styles(theme: ThemeSpec):
    styles = getSampleStyleSheet()
    return {
        "row_label": ParagraphStyle(
            "DiffMatrixRowLabel",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=11.0,
            textColor=colors.HexColor(theme.primary_color),
            spaceAfter=0,
            spaceBefore=0,
        ),
        "col_label": ParagraphStyle(
            "DiffMatrixColLabel",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=10.5,
            alignment=1,
            textColor=colors.HexColor(theme.table_row_odd_bg),
            spaceAfter=0,
            spaceBefore=0,
        ),
        "cell": ParagraphStyle(
            "DiffMatrixCell",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.0,
            leading=10.5,
            alignment=1,
            textColor=colors.HexColor(theme.primary_color),
            spaceAfter=0,
            spaceBefore=0,
        ),
        "legend": ParagraphStyle(
            "DiffMatrixLegend",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=10.0,
            textColor=colors.HexColor(theme.secondary_color),
            spaceAfter=0,
            spaceBefore=0,
        ),
    }


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _symbol_drawing(symbol: str, fill_color=colors.black, stroke_color=colors.black):
    drawing = Drawing(10, 10)
    if symbol == "present":
        drawing.add(Circle(5, 5, 3.2, fillColor=fill_color, strokeColor=stroke_color, strokeWidth=0.6))
    elif symbol == "absent":
        drawing.add(Circle(5, 5, 3.2, fillColor=colors.white, strokeColor=stroke_color, strokeWidth=0.8))
    elif symbol == "stable":
        drawing.add(Circle(5, 5, 3.2, fillColor=fill_color, strokeColor=stroke_color, strokeWidth=0.6))
    elif symbol == "gain":
        drawing.add(Circle(5, 5, 3.2, fillColor=fill_color, strokeColor=stroke_color, strokeWidth=0.6))
        drawing.add(Line(7.2, 5, 9.2, 5, strokeColor=stroke_color, strokeWidth=0.7))
        drawing.add(Line(8.2, 4.2, 9.2, 5, strokeColor=stroke_color, strokeWidth=0.7))
        drawing.add(Line(8.2, 5.8, 9.2, 5, strokeColor=stroke_color, strokeWidth=0.7))
    elif symbol == "loss":
        drawing.add(Circle(5, 5, 3.2, fillColor=colors.white, strokeColor=stroke_color, strokeWidth=0.8))
        drawing.add(Line(0.8, 5, 2.8, 5, strokeColor=stroke_color, strokeWidth=0.7))
        drawing.add(Line(1.8, 4.2, 0.8, 5, strokeColor=stroke_color, strokeWidth=0.7))
        drawing.add(Line(1.8, 5.8, 0.8, 5, strokeColor=stroke_color, strokeWidth=0.7))
    else:
        drawing.add(Circle(5, 5, 3.2, fillColor=fill_color, strokeColor=stroke_color, strokeWidth=0.6))
    return drawing


def _state_from_cell(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("state") or cell.get("mode") or cell.get("type") or "").strip().lower()
    text = _normalize_text(cell).strip().lower()
    mapping = {
        "âœ“": "present",
        "yes": "present",
        "y": "present",
        "true": "present",
        "present": "present",
        "stable": "stable",
        "same": "stable",
        "absent": "absent",
        "-": "absent",
        "none": "absent",
        "added": "gain",
        "gained": "gain",
        "gain": "gain",
        "new": "gain",
        "removed": "loss",
        "lost": "loss",
        "loss": "loss",
    }
    return mapping.get(text, text)


def _display_from_cell(cell: Any, mode: str) -> str:
    if isinstance(cell, dict):
        if cell.get("display") is not None:
            return str(cell.get("display"))
        if cell.get("label") is not None:
            return str(cell.get("label"))
    state = _state_from_cell(cell)
    if mode == 'presence_absence':
        return "present" if state == "present" else "absent"
    if mode == 'status_diff':
        if state in {'gain', 'present'}:
            return '●'
        if state in {'loss', 'absent'}:
            return '○'
        if state == 'stable':
            return '●'
    return _normalize_text(cell)


def _cell_fill_and_text(theme: ThemeSpec, mode: str, cell: Any):
    state = _state_from_cell(cell)
    if mode == "presence_absence":
        if state == "present":
            return colors.HexColor(theme.background_color), colors.white
        return colors.white, colors.HexColor(theme.background_color)
    if mode == "status_diff":
        if state in {"gain", "present"}:
            return colors.HexColor("#ecfdf5"), colors.HexColor("#047857")
        if state in {"loss", "absent"}:
            return colors.HexColor("#fef2f2"), colors.HexColor("#b91c1c")
        return colors.HexColor(theme.highlight.body_bg), colors.HexColor(theme.primary_color)
    return colors.white, colors.HexColor(theme.primary_color)


def _legend_row(legend: Optional[List[Dict[str, str]]], mode: str):
    if legend is not None:
        return legend
    if mode == 'presence_absence':
        return [
            {'symbol': 'present', 'label': 'present'},
            {'symbol': 'absent', 'label': 'absent'},
        ]
    return []


def render_diff_matrix(
    row_labels: List[str],
    column_labels: List[str],
    cells: List[List[Any]],
    theme: ThemeSpec,
    width: float,
    mode: str = "presence_absence",
    legend: Optional[List[Dict[str, str]]] = None,
    cell_renderer: Optional[Callable[[Any], str]] = None,
) -> Table:
    """
    Render a generic diff matrix for presence/absence and change-style data.
    """
    if not row_labels or not column_labels:
        return Table([[""]], colWidths=[width])

    styles = _styles(theme)
    num_cols = len(column_labels) + 1
    row_label_width = max(84.0, min(width * 0.28, 130.0))
    cell_width = max(34.0, (width - row_label_width) / max(1, len(column_labels)))
    col_widths = [row_label_width] + [cell_width] * len(column_labels)

    table_data = [[Paragraph("", styles["col_label"])]]
    for col in column_labels:
        table_data[0].append(Paragraph(format_inline_markdown(_normalize_text(col)), styles["col_label"]))

    if len(cells) != len(row_labels):
        raise ValueError("cells row count must match row_labels length")

    for row_label, row_cells in zip(row_labels, cells):
        if len(row_cells) != len(column_labels):
            raise ValueError("each cells row must match column_labels length")
        row = [Paragraph(format_inline_markdown(_normalize_text(row_label)), styles["row_label"])]
        for cell in row_cells:
            display = cell_renderer(cell) if cell_renderer else _display_from_cell(cell, mode)
            if mode == "presence_absence":
                if display == "present":
                    row.append(_symbol_drawing("present", fill_color=colors.HexColor(theme.primary_color), stroke_color=colors.HexColor(theme.primary_color)))
                else:
                    row.append(_symbol_drawing("absent", fill_color=colors.white, stroke_color=colors.HexColor(theme.primary_color)))
            else:
                row.append(Paragraph(format_inline_markdown(display), styles["cell"]))
        table_data.append(row)

    t_styles = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.accent_color)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(theme.table_row_odd_bg)),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.HexColor(theme.table_grid_color)),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor(theme.table_grid_color)),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor(theme.table_grid_color)),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor(theme.table_row_even_bg)),
        ("TEXTCOLOR", (0, 1), (0, -1), colors.HexColor(theme.table_row_odd_bg)),
    ]

    for row_idx, row_cells in enumerate(cells, start=1):
        for col_idx, cell in enumerate(row_cells, start=1):
            bg_color, text_color = _cell_fill_and_text(theme, mode, cell)
            t_styles.extend(
                [
                    ("BACKGROUND", (col_idx, row_idx), (col_idx, row_idx), bg_color),
                    ("TEXTCOLOR", (col_idx, row_idx), (col_idx, row_idx), text_color),
                ]
            )

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(t_styles))

    legend_items = _legend_row(legend, mode)
    if not legend_items:
        return t

    legend_style = styles["legend"]
    legend_row = []
    legend_widths = []
    for idx, item in enumerate(legend_items):
        symbol = item.get("symbol", "")
        if mode in {"presence_absence"}:
            symbol_flowable = _symbol_drawing(symbol, fill_color=colors.HexColor(theme.primary_color), stroke_color=colors.HexColor(theme.primary_color))
        else:
            symbol_flowable = Paragraph(f"<b>{format_inline_markdown(symbol)}</b>", legend_style)
        legend_row.append(
            Table(
                [[symbol_flowable, Paragraph(format_inline_markdown(item.get("label", "")), legend_style)]],
                colWidths=[12, max(48.0, width / max(1, len(legend_items)) - 12)],
                style=TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ]
                ),
            )
        )
        legend_widths.append(max(70.0, width / max(1, len(legend_items))))
    legend_table = Table([legend_row], colWidths=legend_widths)
    legend_table.setStyle(
        TableStyle(
            [
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    return Table([[t], [legend_table]], colWidths=[width], style=TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
