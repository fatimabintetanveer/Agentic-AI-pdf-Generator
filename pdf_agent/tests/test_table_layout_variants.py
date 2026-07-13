import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from pdf_agent.components.elements.util import format_inline_markdown, create_text_style, _tint_hex
from pdf_agent.models import ThemeSpec


def _key_value_table(rows, theme: ThemeSpec, width: float) -> Table:
    styles = getSampleStyleSheet()
    label_style = ParagraphStyle(
        "KeyValueLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.0,
        leading=11.0,
        textColor=colors.HexColor(theme.primary_color),
    )
    value_style = create_text_style(
        "KeyValueValue",
        "Helvetica",
        9.2,
        12.0,
        theme.secondary_color,
        space_after=0,
    )

    data = [["", ""]]
    for label, value in rows:
        data.append(
            [
                Paragraph(format_inline_markdown(str(label)), label_style),
                Paragraph(format_inline_markdown(str(value)), value_style),
            ]
        )

    table = Table(data, colWidths=[width * 0.28, width * 0.72], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.primary_color)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(theme.table_header_text)),
                ("SPAN", (0, 0), (-1, 0)),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 1), (-1, -1), 0.5, colors.HexColor(theme.table_grid_color)),
                ("BACKGROUND", (0, 1), (0, -1), colors.HexColor(_tint_hex(theme.primary_color, mix=0.92))),
            ]
        )
    )
    return table


def _grouped_table(groups, theme: ThemeSpec, width: float) -> Table:
    styles = getSampleStyleSheet()
    group_style = ParagraphStyle(
        "GroupedTableTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13.0,
        textColor=colors.HexColor(theme.background_color),
    )
    header_style = ParagraphStyle(
        "GroupedTableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.8,
        leading=11.0,
        textColor=colors.HexColor(theme.primary_color),
    )
    body_style = create_text_style(
        "GroupedTableBody",
        "Helvetica",
        8.8,
        11.2,
        theme.secondary_color,
        space_after=0,
    )

    rows = [["", "", ""]]
    styles_data = [
        ("SPAN", (0, 0), (-1, 0)),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.primary_color)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(theme.background_color)),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]

    for group_name, items in groups:
        rows.append(
            [
                Paragraph(format_inline_markdown(group_name), group_style),
                "",
                "",
            ]
        )
        styles_data.extend(
            [
                ("SPAN", (0, len(rows) - 1), (-1, len(rows) - 1)),
                ("BACKGROUND", (0, len(rows) - 1), (-1, len(rows) - 1), colors.HexColor(theme.accent_color)),
                ("TOPPADDING", (0, len(rows) - 1), (-1, len(rows) - 1), 7),
                ("BOTTOMPADDING", (0, len(rows) - 1), (-1, len(rows) - 1), 7),
            ]
        )
        rows.append(
            [
                Paragraph("Item", header_style),
                Paragraph("Detail", header_style),
                Paragraph("Value", header_style),
            ]
        )
        styles_data.extend(
            [
                ("BACKGROUND", (0, len(rows) - 1), (-1, len(rows) - 1), colors.HexColor(theme.table_header_bg)),
                ("TEXTCOLOR", (0, len(rows) - 1), (-1, len(rows) - 1), colors.HexColor(theme.table_header_text)),
            ]
        )
        for idx, item in enumerate(items, start=1):
            rows.append(
                [
                    Paragraph(format_inline_markdown(str(item["item"])), body_style),
                    Paragraph(format_inline_markdown(str(item["detail"])), body_style),
                    Paragraph(format_inline_markdown(str(item["value"])), body_style),
                ]
            )
            if idx % 2 == 0:
                styles_data.append(("BACKGROUND", (0, len(rows) - 1), (-1, len(rows) - 1), colors.HexColor(theme.table_row_even_bg)))

    table = Table(rows, colWidths=[width * 0.28, width * 0.47, width * 0.25], repeatRows=2)
    table.setStyle(
        TableStyle(
            styles_data
            + [
                ("GRID", (0, 1), (-1, -1), 0.45, colors.HexColor(theme.table_grid_color)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def _ranked_list(rows, theme: ThemeSpec, width: float) -> Table:
    styles = getSampleStyleSheet()
    rank_style = ParagraphStyle(
        "RankedListRank",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.0,
        leading=11.5,
        textColor=colors.HexColor(theme.background_color),
        alignment=1,
    )
    name_style = ParagraphStyle(
        "RankedListName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=11.5,
        textColor=colors.HexColor(theme.primary_color),
    )
    value_style = ParagraphStyle(
        "RankedListValue",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.0,
        leading=12.0,
        textColor=colors.HexColor(theme.accent_color),
        alignment=2,
    )
    note_style = create_text_style(
        "RankedListNote",
        "Helvetica",
        8.7,
        10.8,
        theme.secondary_color,
        space_after=0,
    )

    data = [[
        Paragraph("Rank", name_style),
        Paragraph("Entity", name_style),
        Paragraph("Value", name_style),
        Paragraph("Note", name_style),
    ]]
    for rank, row in enumerate(rows, start=1):
        data.append(
            [
                Paragraph(str(rank), rank_style),
                Paragraph(format_inline_markdown(str(row["name"])), name_style),
                Paragraph(format_inline_markdown(str(row["value"])), value_style),
                Paragraph(format_inline_markdown(str(row["note"])), note_style),
            ]
        )

    table = Table(data, colWidths=[width * 0.10, width * 0.34, width * 0.20, width * 0.36], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(theme.primary_color)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor(theme.table_header_text)),
                ("ALIGN", (0, 0), (-1, 0), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("GRID", (0, 1), (-1, -1), 0.45, colors.HexColor(theme.table_grid_color)),
                ("BACKGROUND", (0, 1), (0, -1), colors.HexColor(theme.accent_color)),
                ("TEXTCOLOR", (0, 1), (0, -1), colors.HexColor(theme.background_color)),
            ]
        )
    )
    return table


def test_table_layout_variants():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "table_layout_variants_preview.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    theme = ThemeSpec(
        primary_color="#0f766e",
        secondary_color="#475569",
        accent_color="#3b82f6",
        background_color="#ffffff",
        table_header_bg="#e2e8f0",
        table_header_text="#0f172a",
        table_row_even_bg="#f8fafc",
        table_row_odd_bg="#ffffff",
        table_grid_color="#dbe4ee",
    )
    width = A4[0] - 80
    styles = getSampleStyleSheet()

    story = [
        Paragraph("Table Layout Variants Preview", styles["Heading1"]),
        Spacer(1, 10),
        Paragraph(
            "This preview keeps the variants local to the test so you can judge the presentation before turning any of them into reusable components.",
            styles["BodyText"],
        ),
        Spacer(1, 16),
        Paragraph("1. Key Value Table", styles["Heading2"]),
        Spacer(1, 6),
        _key_value_table(
            [
                ("Market", "Saudi Arabia"),
                ("Period", "MAT ending May 2026"),
                ("Brands", "All 6 Basamh brands"),
                ("Retailers", "CARREFOUR, LULU, OTHAIM, PANDA"),
            ],
            theme,
            width,
        ),
        Spacer(1, 18),
        Paragraph("2. Grouped Table", styles["Heading2"]),
        Spacer(1, 6),
        _grouped_table(
            [
                (
                    "Retailer Coverage",
                    [
                        {"item": "CARREFOUR", "detail": "Large footprint, mixed category spread", "value": "Stable"},
                        {"item": "LULU", "detail": "Broader brand coverage", "value": "Strong"},
                        {"item": "OTHAIM", "detail": "High-value cluster", "value": "High"},
                    ],
                ),
                (
                    "Brand Footprint",
                    [
                        {"item": "GOODY", "detail": "Core driver across the market", "value": "Dominant"},
                        {"item": "TREVA", "detail": "Focused but narrower reach", "value": "Selective"},
                        {"item": "LIBBY'S", "detail": "Single-category presence", "value": "Niche"},
                    ],
                ),
            ],
            theme,
            width,
        ),
        Spacer(1, 18),
        Paragraph("3. Ranked List", styles["Heading2"]),
        Spacer(1, 6),
        _ranked_list(
            [
                {"name": "OTHAIM", "value": "12,115,392", "note": "Highest value sales in the set"},
                {"name": "PANDA", "value": "9,896,884", "note": "Strong broad-based performance"},
                {"name": "LULU", "value": "2,336,393", "note": "Mid-tier but stable"},
                {"name": "CARREFOUR", "value": "1,782,475", "note": "Smaller but still relevant"},
            ],
            theme,
            width,
        ),
    ]

    doc.build(story)
    print(f"Table layout variants preview saved to: {pdf_path}")


if __name__ == "__main__":
    test_table_layout_variants()
