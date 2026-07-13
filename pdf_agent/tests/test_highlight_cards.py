import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

from pdf_agent.models import ThemeSpec, HighlightStyle
from pdf_agent.components.highlight_cards import render_highlight_cards

def test_highlight_cards():
    doc = SimpleDocTemplate("output/test_highlight_cards.pdf", pagesize=A4)

    theme = ThemeSpec(
        primary_color="#0f766e",
        secondary_color="#475569",
        accent_color="#0d9488",
        background_color="#f0fdfa",
        highlight=HighlightStyle(header_bg="#0f766e", header_text="#ffffff", body_bg="#f0fdfa", border_color="#0d9488")
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'MainTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=16,
        textColor=colors.HexColor(theme.primary_color), spaceAfter=15
    )

    # 2-card test: Major Achievements + Challenges
    sections_2 = {
        "Major Achievements": [
            "Revenue reached an all-time quarterly high",
            "Customer acquisition exceeded targets",
            "AI-powered automation reduced processing time",
            "Cloud migration reached 70% completion",
        ],
        "Challenges": [
            "Increased infrastructure costs",
            "Delays in two enterprise customer projects",
            "Higher employee onboarding costs",
            "Supply chain uncertainty in one region",
        ]
    }

    # 3-card test: SWOT-style
    sections_3 = {
        "Strengths": [
            "Strong brand recognition",
            "Innovative product portfolio",
            "Loyal enterprise client base",
        ],
        "Weaknesses": [
            "High operational costs",
            "Limited regional coverage",
        ],
        "Opportunities": [
            "AI market expansion",
            "New verticals in healthcare",
            "Emerging markets in SEA",
        ]
    }

    width = A4[0] - 4 * cm
    os.makedirs("output", exist_ok=True)

    story = [
        Paragraph("Test: 2-Column Highlight Cards (Achievements + Challenges)", title_style),
        Spacer(1, 10),
        render_highlight_cards(sections_2, theme, width),
        Spacer(1, 35),
        Paragraph("Test: 3-Column Highlight Cards (SWOT-style)", title_style),
        Spacer(1, 10),
        render_highlight_cards(sections_3, theme, width),
    ]

    doc.build(story)
    print("Successfully built output/test_highlight_cards.pdf")

if __name__ == "__main__":
    test_highlight_cards()
