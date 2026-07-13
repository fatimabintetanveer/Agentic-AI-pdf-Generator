from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
import re


def format_inline_markdown(text: str) -> str:
    if not isinstance(text, str):
        return str(text) if text is not None else ""
    bold_spans = []

    def capture_bold(m):
        bold_spans.append(m.group(1))
        return f"\x00BOLD{len(bold_spans)-1}\x00"

    text = re.sub(r"\*\*(.*?)\*\*", capture_bold, text)
    italic_spans = []

    def capture_italic(m):
        italic_spans.append(m.group(1))
        return f"\x00ITALIC{len(italic_spans)-1}\x00"

    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', capture_italic, text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for i, span in enumerate(bold_spans):
        safe_span = span.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        text = text.replace(f"\x00BOLD{i}\x00", f"<b>{safe_span}</b>")
    for i, span in enumerate(italic_spans):
        safe_span = span.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        text = text.replace(f"\x00ITALIC{i}\x00", f"<i>{safe_span}</i>")
    return text


def create_text_style(name: str, font_name: str, size: float, leading: float, text_color: str, space_after: float = 8) -> ParagraphStyle:
    styles = getSampleStyleSheet()
    return ParagraphStyle(
        name,
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=size,
        leading=leading,
        textColor=colors.HexColor(text_color),
        spaceAfter=space_after,
    )


def _tint_hex(hex_color: str, mix: float = 0.88) -> str:
    rgb = colors.HexColor(hex_color)
    r = 1.0 - ((1.0 - rgb.red) * (1.0 - mix))
    g = 1.0 - ((1.0 - rgb.green) * (1.0 - mix))
    b = 1.0 - ((1.0 - rgb.blue) * (1.0 - mix))
    return colors.Color(r, g, b).hexval()

