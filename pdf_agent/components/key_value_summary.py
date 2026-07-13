from typing import Iterable, Optional, Tuple

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle

from pdf_agent.models import ThemeSpec
from .elements.util import format_inline_markdown, _tint_hex


def _normalize_items(items: Iterable[Tuple[str, str]]) -> list[tuple[str, str]]:
    normalized: list[tuple[str, str]] = []
    for item in items:
        if isinstance(item, dict):
            label = str(item.get("label") or item.get("key") or "")
            value = str(item.get("value") or "")
        else:
            label = str(item[0]) if len(item) > 0 else ""
            value = str(item[1]) if len(item) > 1 else ""
        if label or value:
            normalized.append((label, value))
    return normalized


def render_key_value_summary(
    items: Iterable[Tuple[str, str]],
    theme: ThemeSpec,
    width: float,
    title: str,
    subtitle: Optional[str] = None,
) -> Table:
    styles = getSampleStyleSheet()
    rows = _normalize_items(items)

    title_style = ParagraphStyle(
        "KeyValueSummaryTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13.0,
        leading=16.0,
        textColor=colors.HexColor(theme.primary_color),
        spaceAfter=0,
        spaceBefore=0,
    )
    subtitle_style = ParagraphStyle(
        "KeyValueSummarySubtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.0,
        leading=11.5,
        textColor=colors.HexColor(theme.secondary_color),
        spaceAfter=0,
        spaceBefore=0,
    )
    label_style = ParagraphStyle(
        "KeyValueSummaryLabel",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9.3,
        leading=11.8,
        textColor=colors.HexColor(theme.primary_color),
        spaceAfter=0,
        spaceBefore=0,
    )
    value_style = ParagraphStyle(
        "KeyValueSummaryValue",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=11.8,
        textColor=colors.HexColor(theme.secondary_color),
        spaceAfter=0,
        spaceBefore=0,
    )

    header_text = format_inline_markdown(title)
    if subtitle:
        header_text = f"{header_text}<br/><font size='9' color='{theme.secondary_color}'>{format_inline_markdown(subtitle)}</font>"

    table_rows = [[Paragraph(header_text, title_style), ""]]
    if not rows:
        table_rows.append([Paragraph("", label_style), Paragraph("", value_style)])
    else:
        for label, value in rows:
            table_rows.append(
                [
                    Paragraph(format_inline_markdown(label), label_style),
                    Paragraph(format_inline_markdown(value), value_style),
                ]
            )

    table = Table(table_rows, colWidths=[width * 0.38, width * 0.62], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("SPAN", (0, 0), (-1, 0)),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.HexColor(theme.table_grid_color)),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (0, -1), colors.HexColor(_tint_hex(theme.primary_color, mix=0.93))),
                ("BACKGROUND", (1, 1), (1, -1), colors.white),
                ("GRID", (0, 1), (-1, -1), 0.45, colors.HexColor(theme.table_grid_color)),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(theme.table_row_even_bg)]),
            ]
        )
    )
    return table
