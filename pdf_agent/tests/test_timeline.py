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
from reportlab.lib.units import cm
from reportlab.lib import colors

from pdf_agent.models import ThemeSpec, TimelineStyle
from pdf_agent.components.timeline import render_timeline

def test_timeline_generation():
    doc = SimpleDocTemplate("output/test_timeline_output.pdf", pagesize=A4)
    
    theme = ThemeSpec(
        primary_color="#0f766e",     # Teal
        secondary_color="#475569",   # Slate Gray
        accent_color="#3b82f6",      # Blue accent
        background_color="#f0fdfa",  # Mint tint
        timeline=TimelineStyle(circle_color="#3b82f6", line_color="#cbd5e1")
    )
    
    steps = [
        {
            "title": "Phase 1",
            "description": "• AI Document Assistant<br/>• Customer Analytics Dashboard<br/>• Workflow Automation"
        },
        {
            "title": "Phase 2",
            "description": "• Multi-language Support<br/>• Enterprise Security Enhancements<br/>• Predictive Analytics"
        },
        {
            "title": "Phase 3",
            "description": "• Autonomous Reporting<br/>• AI Knowledge Search<br/>• Agent Marketplace"
        }
    ]
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor(theme.primary_color),
        spaceAfter=15
    )
    
    width = A4[0] - 4*cm
    
    story = [
        Paragraph("Vertical Implementation Roadmap", title_style),
        Spacer(1, 15),
        render_timeline(steps, theme, width, orientation="vertical"),
        Spacer(1, 40),
        Paragraph("Horizontal Implementation Roadmap", title_style),
        Spacer(1, 15),
        render_timeline(steps, theme, width, orientation="horizontal"),
    ]
    
    os.makedirs("output", exist_ok=True)
    doc.build(story)
    print("Successfully built output/test_timeline_output.pdf")

if __name__ == "__main__":
    test_timeline_generation()
