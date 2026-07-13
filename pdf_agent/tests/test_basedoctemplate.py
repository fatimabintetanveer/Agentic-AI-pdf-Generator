import os
import sys
from pathlib import Path



# Auto-resolve and append the project root directory to Python's import search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(project_root)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pdf_agent.tools.markdown_parser import parse_markdown_file


SAMPLE_FILE = ROOT / "pdf_agent" / "sample_inputs" / "business_report.md"
OUTPUT_FILE = ROOT / "output" / "base_doc_template_demo.pdf"

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.fontSize = 24
title_style.leading = 30
title_style.textColor = colors.HexColor("#1e3a8a")

heading_style = styles["Heading2"]
heading_style.textColor = colors.HexColor("#2563eb")
heading_style.spaceAfter = 6

body_style = styles["BodyText"]
body_style.leading = 14
body_style.alignment = TA_LEFT
body_style.spaceAfter = 6


def draw_background(canvas, doc):
    """Draw a simple branded background behind the content."""
    w, h = doc.pagesize
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#f8fafc"))
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#1e3a8a"))
    canvas.rect(0, h - 2.0 * cm, w, 2.0 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#dbeafe"))
    canvas.circle(w - 2.2 * cm, h - 2.2 * cm, 1.4 * cm, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.setLineWidth(0.6)
    canvas.line(1.6 * cm, 1.2 * cm, w - 1.6 * cm, 1.2 * cm)
    canvas.restoreState()


def build_story(document):
    story = []
    story.append(Paragraph(document.title or "Report", title_style))
    story.append(Spacer(1, 0.4 * cm))

    if document.metadata:
        meta_text = ", ".join(f"{k}: {v}" for k, v in document.metadata.items())
        story.append(Paragraph(meta_text, styles["Italic"]))
        story.append(Spacer(1, 0.4 * cm))

    for block in document.blocks[:10]:
        if block.type == "header":
            level = block.metadata.get("level", 1)
            if level == 1:
                story.append(Paragraph(str(block.content), title_style))
            elif level == 2:
                story.append(Paragraph(str(block.content), heading_style))
            else:
                story.append(Paragraph(str(block.content), styles["Heading3"]))
            story.append(Spacer(1, 0.2 * cm))
        elif block.type == "paragraph":
            story.append(Paragraph(str(block.content), body_style))
        elif block.type == "quote":
            story.append(Paragraph(f"“{block.content}”", styles["Italic"]))
        elif block.type == "list":
            items = [f"• {item}" for item in block.content]
            story.append(Paragraph("<br/>".join(items), body_style))
        elif block.type == "table":
            table_data = block.content
            if table_data:
                table = Table(table_data, repeatRows=1, hAlign="LEFT")
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#94a3b8")),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                        ]
                    )
                )
                story.append(table)
                story.append(Spacer(1, 0.3 * cm))

    return story


def main():
    document = parse_markdown_file(str(SAMPLE_FILE))
    output_dir = OUTPUT_FILE.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUTPUT_FILE),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    page_width, page_height = doc.pagesize

    title_frame = Frame(1.6 * cm, page_height - 5.4 * cm, page_width - 3.2 * cm, 3.4 * cm, showBoundary=0)
    left_frame = Frame(1.6 * cm, 2.0 * cm, page_width / 2 - 2.0 * cm, page_height - 8.2 * cm, showBoundary=0)
    right_frame = Frame(page_width / 2 + 0.2 * cm, 2.0 * cm, page_width / 2 - 2.0 * cm, page_height - 8.2 * cm, showBoundary=0)

    template = PageTemplate(id="demo", frames=[title_frame, left_frame, right_frame], onPage=draw_background)
    doc.addPageTemplates(template)

    story = build_story(document)
    doc.build(story)
    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()