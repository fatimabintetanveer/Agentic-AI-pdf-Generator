import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from pdf_agent.components import render_key_value_summary
from pdf_agent.models import ThemeSpec


def test_key_value_summary_component_renders_pdf():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "key_value_summary_component.pdf")

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

    summary_1 = [
        ("Founded", "1985"),
        ("Headquarters", "Jeddah, SA"),
        ("Employees", "1,200"),
        ("Revenue (2025)", "$340M"),
    ]

    summary_2 = [
        ("Market", "Saudi Arabia"),
        ("Period", "MAT ending May 2026"),
        ("Brands", "All 6 Basamh brands"),
        ("Retailers", "CARREFOUR, LULU, OTHAIM, PANDA"),
        ("Status", "Live and reporting"),
    ]

    summary_3 = [
        ("Core Brand", "GOODY"),
        ("Position", "Market driver"),
        ("Coverage", "4 retailers"),
        ("Main Category", "Tuna and pantry"),
        ("Insight", "Broadest footprint across the network"),
    ]

    component_1 = render_key_value_summary(
        summary_1,
        theme,
        width,
        title="Company Snapshot",
        subtitle="Clean default profile summary",
    )
    component_2 = render_key_value_summary(
        summary_2,
        theme,
        width,
        title="Document Context",
        subtitle="Useful for report defaults and cover-style metadata",
    )
    component_3 = render_key_value_summary(
        summary_3,
        theme,
        width,
        title="Brand Summary",
        subtitle="A more analytical summary variant",
    )

    assert component_1 is not None
    assert component_2 is not None
    assert component_3 is not None

    story = [
        Paragraph("Key Value Summary Component Test", styles["Heading1"]),
        Spacer(1, 10),
        Paragraph(
            "This test renders the real key-value summary component using the same preview cases.",
            styles["BodyText"],
        ),
        Spacer(1, 16),
        component_1,
        Spacer(1, 18),
        component_2,
        Spacer(1, 18),
        component_3,
    ]

    doc.build(story)
    print(f"Key value summary component PDF saved to: {pdf_path}")


if __name__ == "__main__":
    test_key_value_summary_component_renders_pdf()
