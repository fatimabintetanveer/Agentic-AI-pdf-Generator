import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from reportlab.lib.pagesizes import A4
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from pdf_agent.components.elements.paragraph import render_paragraph
from pdf_agent.components.elements.headings import render_heading
from pdf_agent.models import SectionHeaderStyle, ThemeSpec


def test_section_headers():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "test_section_headers.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    theme = ThemeSpec()
    story = []

    story.append(Paragraph("Section Header Variants Test", render_heading("Section Header Variants Test", 1, theme).style))
    story.append(Spacer(1, 16))

    for idx, variant in enumerate(SectionHeaderStyle):
        story.append(Paragraph(f"Variant: {variant.value}", render_heading(f"Variant: {variant.value}", 2, theme).style))
        story.append(render_paragraph("This paragraph appears immediately before the section header so we can inspect the natural top gap.", theme))
        story.append(render_heading("Quarterly Performance Overview", 1, theme, variant))
        story.append(render_paragraph("This paragraph appears immediately after the section header so we can inspect the natural bottom gap.", theme))
        story.append(render_heading("Revenue and category trends for the period", 2, theme, variant))

        if idx < len(SectionHeaderStyle) - 1:
            story.append(PageBreak())

    doc.build(story)
    print(f"Section header test PDF saved to: {pdf_path}")


if __name__ == "__main__":
    test_section_headers()
