import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from pdf_agent.models import ThemeSpec, TableStyleVariant, CalloutStyleVariant
from pdf_agent.components.elements import render_table
from pdf_agent.components.callout import render_callout

def test_variants():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "test_variants.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    h1 = styles['Heading1']
    h2 = styles['Heading2']
    
    story = []
    story.append(Paragraph("Component Variants Test", h1))
    story.append(Spacer(1, 20))
    
    base_theme = ThemeSpec() # corporate_navy
    page_width = A4[0] - 80
    
    # ---------------------------------------------------------
    # TEST CALLOUT VARIANTS
    # ---------------------------------------------------------
    story.append(Paragraph("Callout Variants", h2))
    story.append(Spacer(1, 10))
    
    callout_text = "**Pro Tip:** This is a callout component demonstrating the new style variants. Notice how the padding and borders adapt perfectly to the chosen variant."
    
    for variant in CalloutStyleVariant:
        story.append(Paragraph(f"Variant: {variant.value}", styles['Normal']))
        story.append(Spacer(1, 5))
        base_theme.callout.variant = variant
        story.append(render_callout(callout_text, base_theme, page_width))
        story.append(Spacer(1, 15))
        
    # ---------------------------------------------------------
    # TEST TABLE VARIANTS
    # ---------------------------------------------------------
    story.append(Paragraph("Table Variants", h2))
    story.append(Spacer(1, 10))
    
    table_data = [
        ["Metric", "Current Year", "Previous Year", "Growth"],
        ["Revenue", "$1.2M", "$900K", "+33%"],
        ["Users", "45,000", "32,000", "+40%"],
        ["Churn", "2.1%", "2.8%", "-25%"]
    ]
    
    for variant in TableStyleVariant:
        story.append(Paragraph(f"Variant: {variant.value}", styles['Normal']))
        story.append(Spacer(1, 5))
        base_theme.table.variant = variant
        story.append(render_table(table_data, base_theme, page_width))
        story.append(Spacer(1, 20))
        
    doc.build(story)
    print(f"Variants test PDF saved to: {pdf_path}")

if __name__ == "__main__":
    test_variants()
