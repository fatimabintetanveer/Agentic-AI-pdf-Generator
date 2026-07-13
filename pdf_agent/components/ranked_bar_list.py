from __future__ import annotations

from typing import Any, Dict, List, Optional

from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle

from pdf_agent.models import ThemeSpec
from .elements.util import format_inline_markdown


def _numeric_value(item: Dict[str, Any]) -> float:
    value = item.get("value", 0)
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "").replace("%", "")
    try:
        return float(text)
    except ValueError:
        return 0.0


def _format_value(item: Dict[str, Any]) -> str:
    if item.get("value_fmt"):
        return str(item["value_fmt"])
    value = item.get("value", "")
    if isinstance(value, (int, float)):
        return f"{value:,.0f}"
    return str(value)


def _render_bar(value: float, max_value: float, width: float, height: float, fill: str, track: str) -> Drawing:
    drawing = Drawing(width, height)
    drawing.add(
        Rect(
            0,
            height * 0.25,
            width,
            height * 0.5,
            rx=height * 0.22,
            ry=height * 0.22,
            fillColor=colors.HexColor(track),
            strokeColor=None,
        )
    )

    if max_value <= 0:
        bar_width = 0
    else:
        bar_width = max(0, min(width, width * (value / max_value)))

    if bar_width > 0:
        drawing.add(
            Rect(
                0,
                height * 0.25,
                bar_width,
                height * 0.5,
                rx=height * 0.22,
                ry=height * 0.22,
                fillColor=colors.HexColor(fill),
                strokeColor=None,
            )
        )
    return drawing


def render_ranked_bar_list(
    items: List[Dict[str, Any]],
    theme: ThemeSpec,
    width: float,
    title: str,
    subtitle: Optional[str] = None,
    max_value: Optional[float] = None,
) -> Table:
    if not items:
        return Table([[""]], colWidths=[width])

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "RankedBarTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13.0,
        leading=16.0,
        textColor=colors.HexColor(theme.primary_color),
        spaceAfter=0,
        spaceBefore=0,
    )
    rank_style = ParagraphStyle(
        "RankedBarRank",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=11.0,
        textColor=colors.HexColor(theme.secondary_color),
        alignment=1,
        spaceAfter=0,
        spaceBefore=0,
    )
    label_style = ParagraphStyle(
        "RankedBarLabel",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9.4,
        leading=11.0,
        textColor=colors.HexColor(theme.primary_color),
        spaceAfter=0,
        spaceBefore=0,
    )
    value_style = ParagraphStyle(
        "RankedBarValue",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=11.0,
        textColor=colors.HexColor(theme.accent_color),
        alignment=2,
        spaceAfter=0,
        spaceBefore=0,
    )

    items_sorted = sorted(items, key=_numeric_value, reverse=True)
    max_numeric = max_value if max_value is not None else max((_numeric_value(item) for item in items_sorted), default=0.0)

    header_text = format_inline_markdown(title)
    if subtitle:
        header_text = f"{header_text}<br/><font size='9' color='{theme.secondary_color}'>{format_inline_markdown(subtitle)}</font>"

    row_data: List[List[Any]] = [[Paragraph(header_text, title_style), "", "", ""]]
    row_styles = [
        ("SPAN", (0, 0), (-1, 0)),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.75, colors.HexColor(theme.table_grid_color)),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]

    bar_area_width = width * 0.52
    label_area_width = width * 0.28
    value_area_width = width * 0.12
    rank_area_width = width * 0.08

    for idx, item in enumerate(items_sorted, start=1):
        label = str(item.get("label", ""))
        value = _format_value(item)
        numeric_value = _numeric_value(item)
        bar = _render_bar(
            numeric_value,
            max_numeric,
            width=bar_area_width,
            height=12,
            fill=theme.accent_color,
            track=theme.table_row_even_bg,
        )
        row_data.append(
            [
                Paragraph(str(idx), rank_style),
                Paragraph(format_inline_markdown(label), label_style),
                bar,
                Paragraph(format_inline_markdown(value), value_style),
            ]
        )

    table = Table(
        row_data,
        colWidths=[rank_area_width, label_area_width, bar_area_width, value_area_width],
        repeatRows=1,
    )
    table.setStyle(
        TableStyle(
            row_styles
            + [
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor(theme.table_grid_color)),
                ("LINEBELOW", (0, 1), (-1, -1), 0.4, colors.HexColor(theme.table_grid_color)),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(theme.table_row_even_bg)]),
            ]
        )
    )
    return table
