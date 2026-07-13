import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from pdf_agent.components import render_ranked_bar_list
from pdf_agent.models import ThemeSpec


def test_ranked_bar_list():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "ranked_bar_list_preview.pdf")

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
        secondary_color="#64748b",
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

    sales_rows = [
        {"label": "OTHAIM", "value": 12115392, "value_fmt": "12.1M"},
        {"label": "PANDA", "value": 9896884, "value_fmt": "9.9M"},
        {"label": "LULU", "value": 2336393, "value_fmt": "2.3M"},
        {"label": "CARREFOUR", "value": 1782475, "value_fmt": "1.8M"},
    ]

    score_rows = [
        {"label": "GOODY", "value": 94, "value_fmt": "94"},
        {"label": "TREVA", "value": 77, "value_fmt": "77"},
        {"label": "LIBBY'S", "value": 52, "value_fmt": "52"},
        {"label": "COFIQUE", "value": 38, "value_fmt": "38"},
        {"label": "TIM HORTONS", "value": 24, "value_fmt": "24"},
    ]

    close_values_rows = [
        {"label": "North Region", "value": 84, "value_fmt": "84"},
        {"label": "South Region", "value": 82, "value_fmt": "82"},
        {"label": "East Region", "value": 80, "value_fmt": "80"},
        {"label": "West Region", "value": 78, "value_fmt": "78"},
    ]

    story = [
        Paragraph("Ranked Bar List Preview", styles["Heading1"]),
        Spacer(1, 10),
        Paragraph(
            "This preview shows the reusable ranked bar list component so you can judge whether the layout feels polished enough for report use.",
            styles["BodyText"],
        ),
        Spacer(1, 16),
        Paragraph("1. Monthly Value Sales", styles["Heading2"]),
        Spacer(1, 6),
        render_ranked_bar_list(
            sales_rows,
            theme,
            width,
            title="MONTHLY VALUE SALES - Sep 2024",
            subtitle="Magnitude comparison by retailer",
            max_value=12115392,
        ),
        Spacer(1, 18),
        Paragraph("2. Brand Score", styles["Heading2"]),
        Spacer(1, 6),
        render_ranked_bar_list(
            score_rows,
            theme,
            width,
            title="BRAND SCORE RANKING",
            subtitle="Clear gaps and strong relative spread",
        ),
        Spacer(1, 18),
        Paragraph("3. Close Values Example", styles["Heading2"]),
        Spacer(1, 6),
        render_ranked_bar_list(
            close_values_rows,
            theme,
            width,
            title="REGIONAL PERFORMANCE",
            subtitle="Use this to see how the bars behave when values are close together",
        ),
    ]

    doc.build(story)
    print(f"Ranked bar list preview saved to: {pdf_path}")


if __name__ == "__main__":
    test_ranked_bar_list()
