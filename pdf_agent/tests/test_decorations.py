import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def get_dummy_content():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=12
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#333333")
    )
    
    flowables = []
    flowables.append(Paragraph("Quarterly Business Review", title_style))
    flowables.append(Spacer(1, 10))
    flowables.append(Paragraph("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", body_style))
    flowables.append(Spacer(1, 15))
    flowables.append(Paragraph("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", body_style))
    return flowables

# ==========================================
# Background Decoration Functions
# These functions act as canvas callbacks
# ==========================================

def draw_top_band(c: canvas.Canvas, doc):
    c.saveState()
    width, height = A4
    c.setFillColor(colors.HexColor("#1e3a8a"))
    # Draw a 2cm band across the top
    c.rect(0, height - 2*cm, width, 2*cm, stroke=0, fill=1)
    
    # Draw a thin secondary accent line below it
    c.setFillColor(colors.HexColor("#2563eb"))
    c.rect(0, height - 2.2*cm, width, 0.2*cm, stroke=0, fill=1)
    c.restoreState()

def draw_left_sidebar(c: canvas.Canvas, doc):
    c.saveState()
    width, height = A4
    c.setFillColor(colors.HexColor("#f8fafc"))
    # Draw a light background sidebar
    c.rect(0, 0, 4*cm, height, stroke=0, fill=1)
    
    # Draw a bold vertical accent line
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c.rect(4*cm, 0, 0.15*cm, height, stroke=0, fill=1)
    c.restoreState()

def draw_corner_triangles(c: canvas.Canvas, doc):
    c.saveState()
    width, height = A4
    
    # Top Right Triangle
    c.setFillColor(colors.HexColor("#2563eb"))
    p = c.beginPath()
    p.moveTo(width - 5*cm, height)
    p.lineTo(width, height)
    p.lineTo(width, height - 5*cm)
    c.drawPath(p, stroke=0, fill=1)
    
    # Bottom Left Triangle (Secondary color)
    c.setFillColor(colors.HexColor("#475569"))
    p = c.beginPath()
    p.moveTo(0, 5*cm)
    p.lineTo(0, 0)
    p.lineTo(5*cm, 0)
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def draw_geometric_polygons(c: canvas.Canvas, doc):
    c.saveState()
    width, height = A4
    
    # Semi-transparent large circle top left
    c.setFillColor(colors.HexColor("#eff6ff"))
    c.circle(0, height, 8*cm, stroke=0, fill=1)
    
    # Small accent circle
    c.setFillColor(colors.HexColor("#bfdbfe"))
    c.circle(4*cm, height - 5*cm, 1.5*cm, stroke=0, fill=1)
    
    # Slanted rectangle bottom right
    c.setFillColor(colors.HexColor("#dbeafe"))
    c.translate(width, 0)
    c.rotate(45)
    c.rect(-5*cm, -2*cm, 10*cm, 4*cm, stroke=0, fill=1)
    
    c.restoreState()

def draw_diagonal_split(c: canvas.Canvas, doc):
    c.saveState()
    width, height = A4
    
    # Large primary triangle on the top right
    c.setFillColor(colors.HexColor("#f0fdf4")) # Very light green/teal background
    c.rect(0, 0, width, height, stroke=0, fill=1)
    
    # Sharp diagonal cut using primary color
    c.setFillColor(colors.HexColor("#0f766e")) # Teal 700
    p = c.beginPath()
    p.moveTo(0, height)
    p.lineTo(width, height)
    p.lineTo(width, height * 0.4)
    c.drawPath(p, stroke=0, fill=1)
    
    # Accent ribbon parallel to the cut
    c.setFillColor(colors.HexColor("#14b8a6")) # Teal 500
    p = c.beginPath()
    p.moveTo(0, height - 0.5*cm)
    p.lineTo(width - 0.5*cm, height * 0.4 - 0.5*cm)
    p.lineTo(width, height * 0.4 - 0.5*cm)
    p.lineTo(0, height)
    c.drawPath(p, stroke=0, fill=1)
    
    c.restoreState()

def draw_bottom_wave(c: canvas.Canvas, doc):
    c.saveState()
    width, height = A4
    
    # Background wave (lighter)
    c.setFillColor(colors.HexColor("#dbeafe")) # Blue 100
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, 4*cm)
    # bezier curve (x1,y1, x2,y2, x3,y3)
    p.curveTo(width*0.3, 5*cm, width*0.7, 2*cm, width, 4.5*cm)
    p.lineTo(width, 0)
    c.drawPath(p, stroke=0, fill=1)
    
    # Foreground wave (darker)
    c.setFillColor(colors.HexColor("#2563eb")) # Blue 600
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, 2.5*cm)
    p.curveTo(width*0.4, 1.5*cm, width*0.6, 4*cm, width, 2*cm)
    p.lineTo(width, 0)
    c.drawPath(p, stroke=0, fill=1)
    
    c.restoreState()

def draw_tech_grid(c: canvas.Canvas, doc):
    c.saveState()
    width, height = A4
    
    # Subtle background
    c.setFillColor(colors.HexColor("#fafafa"))
    c.rect(0, 0, width, height, stroke=0, fill=1)
    
    # Draw faint grid
    c.setStrokeColor(colors.HexColor("#e5e7eb"))
    c.setLineWidth(0.5)
    
    grid_size = 2*cm
    # Vertical lines
    for x in range(0, int(width), int(grid_size)):
        c.line(x, 0, x, height)
    # Horizontal lines
    for y in range(0, int(height), int(grid_size)):
        c.line(0, y, width, y)
        
    # Highlight some intersections (crosshairs)
    c.setStrokeColor(colors.HexColor("#3b82f6")) # Blue 500
    c.setLineWidth(1.5)
    highlights = [(2, 2), (2, 10), (8, 4), (6, 12)]
    for hx, hy in highlights:
        cx = hx * grid_size
        cy = height - (hy * grid_size)
        c.line(cx - 0.3*cm, cy, cx + 0.3*cm, cy)
        c.line(cx, cy - 0.3*cm, cx, cy + 0.3*cm)
        
    c.restoreState()

def draw_elegant_frame(c: canvas.Canvas, doc):
    c.saveState()
    width, height = A4
    margin = 1.5 * cm
    
    # Thin outer border
    c.setStrokeColor(colors.HexColor("#94a3b8")) # Slate 400
    c.setLineWidth(0.5)
    c.rect(margin, margin, width - 2*margin, height - 2*margin, stroke=1, fill=0)
    
    # Corner accent boxes
    c.setFillColor(colors.HexColor("#0f172a")) # Slate 900
    box_size = 0.4 * cm
    # Top Left
    c.rect(margin - box_size/2, height - margin - box_size/2, box_size, box_size, stroke=0, fill=1)
    # Top Right
    c.rect(width - margin - box_size/2, height - margin - box_size/2, box_size, box_size, stroke=0, fill=1)
    # Bottom Left
    c.rect(margin - box_size/2, margin - box_size/2, box_size, box_size, stroke=0, fill=1)
    # Bottom Right
    c.rect(width - margin - box_size/2, margin - box_size/2, box_size, box_size, stroke=0, fill=1)
    
    c.restoreState()

def main():
    output_dir = "output/decorations_test"
    os.makedirs(output_dir, exist_ok=True)
    
    decorations = {
        "top_band": draw_top_band,
        "left_sidebar": draw_left_sidebar,
        "corner_triangles": draw_corner_triangles,
        "geometric": draw_geometric_polygons,
        "diagonal_split": draw_diagonal_split,
        "bottom_wave": draw_bottom_wave,
        "tech_grid": draw_tech_grid,
        "elegant_frame": draw_elegant_frame
    }
    
    for name, draw_func in decorations.items():
        pdf_path = os.path.join(output_dir, f"{name}.pdf")
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            leftMargin=5*cm if name == "left_sidebar" else 2.5*cm,
            rightMargin=2.5*cm,
            topMargin=7*cm if name == "diagonal_split" else (3*cm if name == "top_band" else 2.5*cm),
            bottomMargin=2.5*cm
        )
        
        # Build the document with the specific onPage callback
        doc.build(get_dummy_content(), onFirstPage=draw_func, onLaterPages=draw_func)
        print(f"Generated {pdf_path}")

if __name__ == "__main__":
    main()
