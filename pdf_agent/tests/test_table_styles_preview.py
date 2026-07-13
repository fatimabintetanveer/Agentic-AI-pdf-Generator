import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from pdf_agent.components import render_stacked_entity_row
from pdf_agent.models import ThemeSpec


def _styles(theme: ThemeSpec):
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "PreviewTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=14,
            textColor=colors.HexColor(theme.primary_color),
        ),
        "metric": ParagraphStyle(
            "PreviewMetric",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=15,
            textColor=colors.HexColor(theme.accent_color),
        ),
        "body": ParagraphStyle(
            "PreviewBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12.5,
            textColor=colors.HexColor(theme.secondary_color),
        ),
    }


def render_headered_card(rows, theme: ThemeSpec, width: float) -> Table:
    s = _styles(theme)
    cards = []
    label_style = ParagraphStyle(
        "FieldLabel",
        parent=s["body"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10,
        textColor=colors.HexColor(theme.secondary_color),
    )

    for row in rows:
        title = str(row["Retailer"])
        metric = str(row["Monthly Value Sales"])
        brands = str(row["Active Basamh Brands"])
        card = Table(
            [
                [Paragraph(title, s["title"])],
                [Table(
                    [
                        [Paragraph("Active Basamh Brands", label_style), Paragraph(brands, s["body"])],
                        [Paragraph("Monthly Value Sales", label_style), Paragraph(metric, s["metric"])],
                    ],
                    colWidths=[width * 0.22, width * 0.78],
                )],
            ],
            colWidths=[width],
        )
        card.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor(theme.table_grid_color)),
                    ("LINEBEFORE", (0, 0), (0, -1), 5, colors.HexColor(theme.accent_color)),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )
        cards.append(card)

    wrapper = Table([[card] for card in cards], colWidths=[width])
    wrapper.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return wrapper


def render_label_value_stack(rows, theme: ThemeSpec, width: float) -> Table:
    s = _styles(theme)
    cards = []
    label_style = ParagraphStyle(
        "StackLabel",
        parent=s["body"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10,
        textColor=colors.HexColor(theme.primary_color),
    )

    for row in rows:
        title = str(row["Retailer"])
        metric = str(row["Monthly Value Sales"])
        brands = str(row["Active Basamh Brands"])
        card = Table(
            [
                [Paragraph(title, s["title"])],
                [Table(
                    [
                        [Paragraph("Retailer: ", label_style), Paragraph(title, s["body"])],
                        [Paragraph("Brands: ", label_style), Paragraph(brands, s["body"])],
                        [Paragraph("Monthly Value Sales: ", label_style), Paragraph(metric, s["metric"])],
                    ],
                    colWidths=[width * 0.18, width * 0.82],
                )],
            ],
            colWidths=[width],
        )
        card.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor(theme.table_grid_color)),
                    ("LINEBEFORE", (0, 0), (0, -1), 5, colors.HexColor(theme.primary_color)),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )
        cards.append(card)

    wrapper = Table([[card] for card in cards], colWidths=[width])
    wrapper.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return wrapper


def test_table_styles_preview():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "table_styles_preview.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    theme = ThemeSpec()
    width = A4[0] - 80

    headers = ["Retailer", "Active Basamh Brands", "Monthly Value Sales"]
    rows = [
        {
            "Retailer": "OTHAIM",
            "Active Basamh Brands": "GOODY, TREVA, COFIQUE, LIBBY'S",
            "Monthly Value Sales": "12,115,392",
        },
        {
            "Retailer": "PANDA",
            "Active Basamh Brands": "GOODY, TREVA, COFIQUE, LIBBY'S, TIM HORTONS",
            "Monthly Value Sales": "9,896,884",
        },
        {
            "Retailer": "LULU",
            "Active Basamh Brands": "GOODY, TREVA, COFIQUE, LIBBY'S, TIM HORTONS",
            "Monthly Value Sales": "2,336,393",
        },
        {
            "Retailer": "CARREFOUR",
            "Active Basamh Brands": "GOODY, TREVA, COFIQUE, LIBBY'S, TIM HORTONS",
            "Monthly Value Sales": "1,782,475",
        },
    ]

    story = [
        Paragraph("Stacked Entity Row Preview", getSampleStyleSheet()["Heading1"]),
        Spacer(1, 12),
        Paragraph(
            "This preview shows only the stacked entity row variant so you can evaluate the layout by itself.",
            getSampleStyleSheet()["BodyText"],
        ),
        Spacer(1, 16),
        Paragraph("Mode A: Headered Card", getSampleStyleSheet()["Heading2"]),
        Spacer(1, 6),
        render_headered_card(rows, theme, width),
        Spacer(1, 18),
        Paragraph("Mode B: Label Value Stack", getSampleStyleSheet()["Heading2"]),
        Spacer(1, 6),
        render_label_value_stack(rows, theme, width),
        Spacer(1, 18),
        Paragraph("Parameterized Stacked Entity Row", getSampleStyleSheet()["Heading2"]),
        Spacer(1, 6),
        render_stacked_entity_row(rows, theme, width, title_key="Retailer", value_key="Monthly Value Sales", detail_keys=["Active Basamh Brands"]),
    ]

    doc.build(story)
    print(f"Stacked entity row preview saved to: {pdf_path}")


if __name__ == "__main__":
    test_table_styles_preview()
