from reportlab.platypus import Paragraph

from pdf_agent.models import ThemeSpec

from .util import format_inline_markdown, create_text_style


def render_paragraph(text: str, theme: ThemeSpec) -> Paragraph:
    style = create_text_style(
        "BodyText",
        "Helvetica",
        10.5,
        14.0,
        theme.secondary_color,
        space_after=6,
    )

    html_text = format_inline_markdown(text)
    print("PARAGRAPH HTML:", html_text)
    return Paragraph(html_text, style)
    #return Paragraph(format_inline_markdown(text), style)
