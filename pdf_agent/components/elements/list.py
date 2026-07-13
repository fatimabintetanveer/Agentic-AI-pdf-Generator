from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph

from pdf_agent.models import ThemeSpec

from .util import format_inline_markdown


def render_list(items, theme: ThemeSpec, ordered: bool = False):
    styles = getSampleStyleSheet()
    bullet_style = ParagraphStyle(
        "BulletText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.0,
        leading=14.0,
        textColor=colors.HexColor(theme.secondary_color),
        leftIndent=14,
        bulletIndent=0,
        spaceAfter=4,
    )
    flowables = []
    if isinstance(items, (list, tuple)):
        for i, item in enumerate(items, start=1):
            bullet = f"{i}." if ordered else "•"
            flowables.append(Paragraph(format_inline_markdown(str(item)), bullet_style, bulletText=bullet))
    else:
        flowables.append(Paragraph(format_inline_markdown(str(items)), bullet_style))
    return flowables
