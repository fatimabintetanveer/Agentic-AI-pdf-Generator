import os

import os
import sys

# Auto-resolve and append the project root directory to Python's import search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from pdf_agent.models import ThemeSpec, TableStyle
from pdf_agent.components.elements import render_table
def test_table_generation():
    doc = SimpleDocTemplate("output/test_table_output.pdf", pagesize=A4)
    theme = ThemeSpec(
        primary_color="#0f766e",     # Teal
        secondary_color="#475569",   # Slate Gray
        background_color="#f0fdfa",  # Mint tint
        table=TableStyle(header_bg="#1e293b", row_even_bg="#f1f5f9", grid_color="#e2e8f0")
    )
    
    data = [
        ["Region", "Revenue", "Growth", "Customer Satisfaction", "Enterprise Clients"],
        ["North America", "$5.8M", "21%", "91%", "134"],
        ["Europe", "$3.2M", "16%", "88%", "92"],
        ["Asia Pacific", "$2.9M", "24%", "93%", "118"],
        ["Middle East", "$1.5M", "11%", "86%", "41"]
    ]
    
    width = A4[0] - 4*cm
    table = render_table(data, theme, width)
    
    os.makedirs("output", exist_ok=True)
    doc.build([table])
    print("Successfully built output/test_table_output.pdf")
if __name__ == "__main__":
    test_table_generation()
