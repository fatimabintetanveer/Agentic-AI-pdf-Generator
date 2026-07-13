import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from pdf_agent.components.elements import render_table
from pdf_agent.models import TableStyleVariant, ThemeSpec


def _style_theme() -> ThemeSpec:
    return ThemeSpec()


def test_table_style_variants_preview():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "table_style_variants_preview.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    theme = _style_theme()
    width = A4[0] - 80

    table_data = [
        ["Retailer", "Active Brands", "Monthly Value Sales"],
        ["OTHAIM", "GOODY, TREVA, COFIQUE, LIBBY'S", "12,115,392"],
        ["PANDA", "GOODY, TREVA, COFIQUE, LIBBY'S, TIM HORTONS", "9,896,884"],
        ["LULU", "GOODY, TREVA, COFIQUE, LIBBY'S, TIM HORTONS", "2,336,393"],
        ["CARREFOUR", "GOODY, TREVA, COFIQUE, LIBBY'S, TIM HORTONS", "1,782,475"],
    ]

    variant_titles = [
        ("Zebra", TableStyleVariant.ZEBRA),
        ("Filled Header", TableStyleVariant.FILLED_HEADER),
        ("Corporate", TableStyleVariant.CORPORATE),
    ]

    story = [
        Paragraph("Table Style Variants Preview", styles["Heading1"]),
        Spacer(1, 10),
        Paragraph(
            "This preview isolates the table renderer so you can compare zebra, filled header, and corporate styles side by side.",
            styles["BodyText"],
        ),
        Spacer(1, 16),
    ]

    for title, variant in variant_titles:
        story.extend(
            [
                Paragraph(title, styles["Heading2"]),
                Spacer(1, 6),
                render_table(table_data, theme, width, variant),
                Spacer(1, 18),
            ]
        )

    doc.build(story)
    print(f"Table style variants preview saved to: {pdf_path}")


if __name__ == "__main__":
    test_table_style_variants_preview()
