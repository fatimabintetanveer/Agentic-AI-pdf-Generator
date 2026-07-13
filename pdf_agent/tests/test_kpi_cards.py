import os
import sys

# Auto-resolve and append the project root directory to Python's import search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

from pdf_agent.models import ThemeSpec, KpiStyle
from pdf_agent.components.kpi_cards import render_kpi_cards

def test_kpi_cards_compilation():
    print("Testing kpi_cards.py components with edge cases...")
    
    # 1. Setup doc template
    output_pdf = "output/test_kpis.pdf"
    os.makedirs("output", exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    width = A4[0] - 4*cm # Usable page width
    story = []
    
    # 2. Setup styles and dummy theme
    styles = getSampleStyleSheet()
    theme = ThemeSpec(
        primary_color="#0f766e",     # Teal
        secondary_color="#475569",   # Slate Gray
        background_color="#f0fdfa",  # Mint tint
        kpi=KpiStyle(bg_color="#f0fdfa", value_color="#0f766e", label_color="#475569", border_color="#cbd5e1")
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor(theme.primary_color),
        spaceBefore=15,
        spaceAfter=8
    )

    
    # --- Case 1: Standard 3 KPIs ---
    story.append(Paragraph("Case 1: Standard 3 KPIs", section_title_style))
    kpis_normal = {
        "Revenue": "$13.4M",
        "Growth": "+18% QoQ",
        "Customer Satisfaction": "93%"
    }
    story.append(render_kpi_cards(kpis_normal, theme, width))
    story.append(Spacer(1, 15))
    
    # --- Case 2: Single KPI Card ---
    story.append(Paragraph("Case 2: Single KPI Card", section_title_style))
    kpis_single = {
        "Single Metric Focus": "99.95% Availability"
    }
    story.append(render_kpi_cards(kpis_single, theme, width))
    story.append(Spacer(1, 15))
    
    # --- Case 3: Many KPI Cards (5 metrics) ---
    story.append(Paragraph("Case 3: Many KPI Cards (5 metrics)", section_title_style))
    kpis_many = {
        "North America": "$5.8M",
        "Europe": "$3.2M",
        "Asia Pacific": "$2.9M",
        "Middle East": "$1.5M",
        "Latin America": "$0.8M"
    }
    story.append(render_kpi_cards(kpis_many, theme, width))
    story.append(Spacer(1, 15))
    
    # --- Case 4: Long Content / Wrapping ---
    story.append(Paragraph("Case 4: Long Text Content & Wrapping", section_title_style))
    kpis_long = {
        "Cloud Migration Project Success Completion Rate": "70.0% Complete (Phase 2)",
        "Mean Resolution Time For Critical Cloud Infrastructure Incidents": "42 Minutes Average"
    }
    story.append(render_kpi_cards(kpis_long, theme, width))
    
    # 5. Render
    doc.build(story)
    print(f"Successfully generated: {output_pdf}")

if __name__ == "__main__":
    test_kpi_cards_compilation()
