from reportlab.platypus import Flowable, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from typing import List, Dict, Any
from pdf_agent.models import ThemeSpec

class CircleBadge(Flowable):
    """A custom flowable that draws a clean circular badge with a step number centered inside."""
    def __init__(self, number: str, bg_color: str, text_color: str = "#ffffff", size: float = 22):
        super().__init__()
        self.number = number
        self.bg_color = colors.HexColor(bg_color)
        self.text_color = colors.HexColor(text_color)
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.bg_color)
        self.canv.setStrokeColor(self.bg_color)
        radius = self.size / 2.0
        # Draw circular background
        self.canv.circle(radius, radius, radius, fill=1, stroke=1)
        
        # Draw centered text
        self.canv.setFillColor(self.text_color)
        self.canv.setFont("Helvetica-Bold", self.size * 0.5)
        # Offset the text slightly to align vertically in the center
        self.canv.drawCentredString(radius, radius - (self.size * 0.16), str(self.number))
        self.canv.restoreState()

class HorizontalTimelineNode(Flowable):
    """Custom flowable that draws a horizontal connector line and a centered circle badge."""
    def __init__(self, number: str, bg_color: str, line_color: str, is_first: bool, is_last: bool, size: float = 20, col_width: float = 100):
        super().__init__()
        self.number = number
        self.bg_color = colors.HexColor(bg_color)
        self.line_color = colors.HexColor(line_color)
        self.is_first = is_first
        self.is_last = is_last
        self.size = size
        self.width = col_width
        self.height = size

    def draw(self):
        self.canv.saveState()
        y_center = self.size / 2.0
        x_center = self.width / 2.0
        
        # Draw horizontal connector line
        self.canv.setStrokeColor(self.line_color)
        self.canv.setLineWidth(1.5)
        x_start = x_center if self.is_first else 0.0
        x_end = x_center if self.is_last else self.width
        
        if not (self.is_first and self.is_last):
            self.canv.line(x_start, y_center, x_end, y_center)
            
        # Draw circular badge centered
        self.canv.setFillColor(self.bg_color)
        self.canv.setStrokeColor(self.bg_color)
        self.canv.circle(x_center, y_center, y_center, fill=1, stroke=1)
        
        # Draw centered number text
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Helvetica-Bold", self.size * 0.5)
        self.canv.drawCentredString(x_center, y_center - (self.size * 0.16), str(self.number))
        self.canv.restoreState()

def render_timeline(steps: List[Dict[str, Any]], theme: ThemeSpec, width: float, orientation: str = "vertical") -> Table:
    """
    Renders a vertical or horizontal timeline flowable.
    orientation: 'vertical' or 'horizontal'
    steps: List of dicts, each with keys:
      - 'title': Title of the step
      - 'date': (Optional) Date or subtitle
      - 'description': Brief text details — can be a plain string or a list of bullet strings
    """
    def _render_description(description: Any, style: ParagraphStyle) -> List[Paragraph]:
        """Handles both plain text and list descriptions."""
        if not description:
            return []
        if isinstance(description, list):
            return [Paragraph(f"• {item}", style) for item in description if item]
        # String case: split on newlines and render each non-empty line
        lines = str(description).split("\n")
        paragraphs = []
        for line in lines:
            line = line.strip()
            if line:
                paragraphs.append(Paragraph(line, style))
        return paragraphs
    styles = getSampleStyleSheet()
    
    if orientation == "horizontal":
        title_style = ParagraphStyle(
            'TimelineHTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10.0,
            leading=13.0,
            textColor=colors.HexColor(theme.primary_color),
            alignment=1  # Centered
        )
        
        date_style = ParagraphStyle(
            'TimelineHDate',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8.5,
            leading=11.0,
            textColor=colors.HexColor(theme.secondary_color),
            spaceBefore=1,
            alignment=1  # Centered
        )
        
        desc_style = ParagraphStyle(
            'TimelineHDesc',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.0,
            leading=12.0,
            textColor=colors.HexColor("#475569"),
            spaceBefore=3,
            alignment=1  # Centered
        )
        
        n = len(steps)
        if n == 0:
            return Table([[]])
            
        col_width = width / n
        col_widths = [col_width] * n
        
        row_nodes = []
        row_texts = []
        
        for i, step in enumerate(steps):
            # Badge & Line Node
            node = HorizontalTimelineNode(
                str(i + 1),
                theme.timeline.circle_color,
                theme.timeline.line_color,
                is_first=(i == 0),
                is_last=(i == n - 1),
                size=20,
                col_width=col_width
            )
            row_nodes.append(node)
            
            # Step Text Content
            cell_elements = []
            cell_elements.append(Paragraph(step.get('title', ''), title_style))
            if step.get('date'):
                cell_elements.append(Paragraph(step.get('date'), date_style))
            cell_elements.extend(_render_description(step.get('description'), desc_style))
                
            row_texts.append(cell_elements)
            
        timeline_table = Table([row_nodes, row_texts], colWidths=col_widths)
        timeline_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 1), (-1, 1), 6),  # Padding above content block
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        return timeline_table
        
    else:  # vertical orientation
        title_style = ParagraphStyle(
            'TimelineTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11.0,
            leading=14.0,
            textColor=colors.HexColor(theme.primary_color)
        )
        
        date_style = ParagraphStyle(
            'TimelineDate',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9.0,
            leading=12.0,
            textColor=colors.HexColor(theme.secondary_color),
            spaceBefore=2
        )
        
        desc_style = ParagraphStyle(
            'TimelineDesc',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.0,
            textColor=colors.HexColor("#334155")
        )
        
        # Grid column widths: Left half-col (14), Right half-col (14), Content col (width - 28)
        badge_col_half = 14.0
        content_width = width - (badge_col_half * 2)
        col_widths = [badge_col_half, badge_col_half, content_width]
        
        table_data = []
        t_styles = [
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]
        
        for i, step in enumerate(steps):
            badge = CircleBadge(str(i + 1), theme.timeline.circle_color, "#ffffff", size=20)
            
            title_content = []
            title_content.append(Paragraph(step.get('title', ''), title_style))
            if step.get('date'):
                title_content.append(Paragraph(step.get('date'), date_style))
                
            table_data.append([badge, "", title_content])
            badge_row_idx = 2 * i
            t_styles.append(('SPAN', (0, badge_row_idx), (1, badge_row_idx)))
            t_styles.append(('ALIGN', (0, badge_row_idx), (1, badge_row_idx), 'CENTER'))
            t_styles.append(('BOTTOMPADDING', (2, badge_row_idx), (2, badge_row_idx), 4))
            
            desc_paragraphs = _render_description(step.get('description'), desc_style)
            desc_container = desc_paragraphs + [Spacer(1, 15)]
            
            table_data.append(["", "", desc_container])
            content_row_idx = 2 * i + 1
            t_styles.append(('LEFTPADDING', (2, content_row_idx), (2, content_row_idx), 0))
            t_styles.append(('BOTTOMPADDING', (2, content_row_idx), (2, content_row_idx), 8))
            
            if i < len(steps) - 1:
                t_styles.extend([
                    ('LINEAFTER', (0, badge_row_idx), (0, content_row_idx), 1.5, colors.HexColor(theme.timeline.line_color)),
                    ('TOPPADDING', (0, badge_row_idx), (1, badge_row_idx), 1),
                ])
                
        timeline_table = Table(table_data, colWidths=col_widths)
        timeline_table.setStyle(TableStyle(t_styles))
        return timeline_table

