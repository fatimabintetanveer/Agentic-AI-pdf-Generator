from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from typing import Tuple, List, Optional
import math

# ==========================================
# Parameterized Drawing Primitives
# ==========================================

def hex_to_color(hex_str: str, alpha: float = 1.0) -> colors.Color:
    """Converts a hex string to a ReportLab Color object with optional alpha transparency."""
    if not hex_str:
        return colors.transparent
    c = colors.HexColor(hex_str)
    c.alpha = alpha
    return c

def draw_band(c: canvas.Canvas, position: str = "top", thickness_cm: float = 2.0, color: str = "#1e3a8a", opacity: float = 1.0, offset_cm: float = 0.0):
    """Draws a horizontal or vertical solid band."""
    c.saveState()
    width, height = A4
    c.setFillColor(hex_to_color(color, opacity))
    
    thick = thickness_cm * cm
    offset = offset_cm * cm
    
    if position == "top":
        c.rect(0, height - thick - offset, width, thick, stroke=0, fill=1)
    elif position == "bottom":
        c.rect(0, offset, width, thick, stroke=0, fill=1)
    elif position == "left":
        c.rect(offset, 0, thick, height, stroke=0, fill=1)
    elif position == "right":
        c.rect(width - thick - offset, 0, thick, height, stroke=0, fill=1)
        
    c.restoreState()

def draw_circle(c: canvas.Canvas, cx_cm: float, cy_cm: float, radius_cm: float, color: str = "#1e3a8a", opacity: float = 1.0):
    """Draws a solid circle. cx/cy are measured from bottom-left."""
    c.saveState()
    c.setFillColor(hex_to_color(color, opacity))
    c.circle(cx_cm * cm, cy_cm * cm, radius_cm * cm, stroke=0, fill=1)
    c.restoreState()

def draw_frame(c: canvas.Canvas, margin_cm: float = 1.5, thickness_pt: float = 0.5, color: str = "#94a3b8", accent_corners: bool = False, accent_color: str = "#0f172a"):
    """Draws a thin border around the page with optional corner accents."""
    c.saveState()
    width, height = A4
    margin = margin_cm * cm
    
    c.setStrokeColor(hex_to_color(color))
    c.setLineWidth(max(thickness_pt, 0.85))
    c.rect(margin, margin, width - 2*margin, height - 2*margin, stroke=1, fill=0)
    
    if accent_corners:
        c.setFillColor(hex_to_color(accent_color))
        box_size = 0.55 * cm
        c.rect(margin - box_size/2, height - margin - box_size/2, box_size, box_size, stroke=0, fill=1) # TL
        c.rect(width - margin - box_size/2, height - margin - box_size/2, box_size, box_size, stroke=0, fill=1) # TR
        c.rect(margin - box_size/2, margin - box_size/2, box_size, box_size, stroke=0, fill=1) # BL
        c.rect(width - margin - box_size/2, margin - box_size/2, box_size, box_size, stroke=0, fill=1) # BR
        
    c.restoreState()

def draw_ribbon(c: canvas.Canvas, corner: str = "top_left", color: str = "#1e3a8a", width_cm: float = 4.0, opacity: float = 1.0):
    """Draws a diagonal ribbon across a corner."""
    c.saveState()
    page_width, page_height = A4
    c.setFillColor(hex_to_color(color, opacity))
    
    w = width_cm * cm
    p = c.beginPath()
    
    if corner == "top_left":
        p.moveTo(0, page_height - w)
        p.lineTo(w, page_height)
        p.lineTo(0, page_height)
    elif corner == "top_right":
        p.moveTo(page_width - w, page_height)
        p.lineTo(page_width, page_height - w)
        p.lineTo(page_width, page_height)
    elif corner == "bottom_left":
        p.moveTo(0, w)
        p.lineTo(w, 0)
        p.lineTo(0, 0)
    elif corner == "bottom_right":
        p.moveTo(page_width - w, 0)
        p.lineTo(page_width, w)
        p.lineTo(page_width, 0)
        
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def draw_wave(c: canvas.Canvas, position: str = "bottom", color: str = "#2563eb", opacity: float = 1.0, height_cm: float = 4.0, amplitude_cm: float = 2.0):
    """Draws a fluid wave across the bottom or top of the page."""
    c.saveState()
    width, page_height = A4
    c.setFillColor(hex_to_color(color, opacity))
    
    h = height_cm * cm
    amp = amplitude_cm * cm
    p = c.beginPath()
    
    if position == "bottom":
        p.moveTo(0, 0)
        p.lineTo(0, h)
        p.curveTo(width * 0.3, h + amp, width * 0.7, h - amp, width, h)
        p.lineTo(width, 0)
    else: # top
        p.moveTo(0, page_height)
        p.lineTo(0, page_height - h)
        p.curveTo(width * 0.3, page_height - h - amp, width * 0.7, page_height - h + amp, width, page_height - h)
        p.lineTo(width, page_height)
        
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def draw_polygon(c: canvas.Canvas, vertices_cm: List[Tuple[float, float]], color: str = "#1e3a8a", opacity: float = 1.0):
    """Draws an arbitrary polygon given a list of (x, y) coordinates in cm."""
    if not vertices_cm or len(vertices_cm) < 3:
        return
        
    c.saveState()
    c.setFillColor(hex_to_color(color, opacity))
    
    p = c.beginPath()
    p.moveTo(vertices_cm[0][0] * cm, vertices_cm[0][1] * cm)
    for x, y in vertices_cm[1:]:
        p.lineTo(x * cm, y * cm)
        
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def draw_full_width_top_band(c: canvas.Canvas, color: str = "#1e3a8a", secondary_color: Optional[str] = None):
    """Draws a stronger cover-like top band that is easy to see behind content."""
    draw_band(c, position="top", thickness_cm=1.5, color=color, opacity=0.95)
    if secondary_color:
        draw_band(c, position="top", thickness_cm=0.18, color=secondary_color, opacity=1.0, offset_cm=1.48)
