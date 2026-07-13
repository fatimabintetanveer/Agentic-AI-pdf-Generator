from reportlab.platypus import Paragraph, Flowable
from reportlab.lib import colors

from pdf_agent.models import ThemeSpec, SectionHeaderStyle
from .util import format_inline_markdown, create_text_style


class RibbonHeading(Flowable):
    def __init__(self, text: str, level: int, theme: ThemeSpec):
        super().__init__()
        self.text = format_inline_markdown(text)
        self.level = level
        self.theme = theme
        self.base_size = max(22.0 - (level * 2.0), 11.0)
        self.inner_width = 0
        self.inner_height = 0
        self.bar_thickness = 4
        self.gap = 6
        self.pad_x = 6
        self.pad_y = 4
        self.spaceBefore = 6
        self.spaceAfter = 10
        self.paragraph = Paragraph(
            self.text,
            create_text_style(
                name=f"RibbonHeading_{level}",
                font_name="Helvetica-Bold",
                size=self.base_size,
                leading=self.base_size + 4,
                text_color=theme.primary_color,
                space_after=0,
            ),
        )
        self.paragraph.style.alignment = 1

    def wrap(self, availWidth, availHeight):
        self.inner_width = max(1, availWidth - (2 * self.pad_x))
        _, self.inner_height = self.paragraph.wrap(self.inner_width, availHeight)
        self.width = availWidth
        self.height = (2 * self.bar_thickness) + (2 * self.pad_y) + self.gap + self.inner_height
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(colors.HexColor(self.theme.primary_color))
        c.rect(0, self.height - self.bar_thickness, self.width, self.bar_thickness, stroke=0, fill=1)
        c.rect(0, 0, self.width, self.bar_thickness, stroke=0, fill=1)
        inner_y = self.bar_thickness + self.pad_y
        self.paragraph.wrapOn(c, self.inner_width, self.inner_height)
        self.paragraph.drawOn(c, self.pad_x, inner_y)
        c.restoreState()


class BannerHeading(Flowable):
    def __init__(self, text: str, level: int, theme: ThemeSpec):
        super().__init__()
        self.text = format_inline_markdown(text)
        self.level = level
        self.theme = theme
        self.base_size = max(22.0 - (level * 2.0), 11.0)
        self.pad_x = 12
        self.pad_y = 14
        self.band_height = self.base_size + 34
        self.arrow_w = max(34, int(self.base_size * 1.8))
        self.spaceBefore = 8
        self.spaceAfter = 12
        self.inner_width = 0
        self.inner_height = 0
        self.paragraph = Paragraph(
            self.text,
            create_text_style(
                name=f"BannerHeading_{level}",
                font_name="Helvetica-Bold",
                size=self.base_size + 1,
                leading=self.base_size + 6,
                text_color=theme.background_color,
                space_after=0,
            ),
        )
        self.paragraph.style.alignment = 0

    def wrap(self, availWidth, availHeight):
        self.inner_width = max(1, availWidth - self.arrow_w - (2 * self.pad_x))
        _, self.inner_height = self.paragraph.wrap(self.inner_width, availHeight)
        self.width = availWidth
        self.height = max(self.band_height, self.inner_height + (2 * self.pad_y))
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        band_color = colors.HexColor(self.theme.primary_color)
        accent = colors.HexColor(self.theme.accent_color)
        text_color = colors.HexColor(self.theme.background_color)

        c.setFillColor(band_color)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)

        c.setFillColor(accent)
        arrow = c.beginPath()
        arrow.moveTo(0, 0)
        arrow.lineTo(self.arrow_w, self.height / 2.0)
        arrow.lineTo(0, self.height)
        arrow.close()
        c.drawPath(arrow, stroke=0, fill=1)

        inner_x = self.arrow_w + self.pad_x
        inner_y = max(self.pad_y, (self.height - self.inner_height) / 2.0 + 1)
        self.paragraph.style.textColor = text_color
        self.paragraph.wrapOn(c, self.inner_width, self.inner_height)
        self.paragraph.drawOn(c, inner_x, inner_y)
        c.restoreState()


class VerticalAccentHeading(Flowable):
    def __init__(self, text: str, level: int, theme: ThemeSpec):
        super().__init__()
        self.text = format_inline_markdown(text)
        self.level = level
        self.theme = theme
        self.base_size = max(22.0 - (level * 2.0), 11.0)
        self.bar_width = 12
        self.bar_gap = 10
        self.pad_y = 2
        self.spaceBefore = 18
        self.spaceAfter = 18
        self.inner_width = 0
        self.inner_height = 0
        self.paragraph = Paragraph(
            self.text,
            create_text_style(
                name=f"VerticalAccentHeading_{level}",
                font_name="Helvetica-Bold",
                size=self.base_size,
                leading=self.base_size + 4,
                text_color=theme.primary_color,
                space_after=0,
            ),
        )

    def wrap(self, availWidth, availHeight):
        self.inner_width = max(1, availWidth - self.bar_width - self.bar_gap)
        _, self.inner_height = self.paragraph.wrap(self.inner_width, availHeight)
        self.width = availWidth
        self.height = self.inner_height + (2 * self.pad_y)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(colors.HexColor(self.theme.accent_color))
        c.rect(0, 0, self.bar_width, self.height, stroke=0, fill=1)
        self.paragraph.wrapOn(c, self.inner_width, self.inner_height)
        self.paragraph.drawOn(c, self.bar_width + self.bar_gap, self.pad_y)
        c.restoreState()


def render_heading(text: str, level: int, theme: ThemeSpec, style_variant: SectionHeaderStyle = SectionHeaderStyle.STANDARD) -> Paragraph:
    base_size = max(22.0 - (level * 2.0), 11.0)
    space_after = 12
    space_before = 0
    text_color = theme.primary_color
    font_name = "Helvetica-Bold"
    leading = base_size + 4
    heading_text = format_inline_markdown(text)
    back_color = None
    border_color = theme.accent_color
    align = "left"

    if style_variant == SectionHeaderStyle.UNDERLINE:
        space_after = 10
        heading_text = f"<u>{heading_text}</u>"
    elif style_variant == SectionHeaderStyle.RIBBON:
        return RibbonHeading(text, level, theme)
    elif style_variant == SectionHeaderStyle.BANNER:
        return BannerHeading(text, level, theme)
    elif style_variant == SectionHeaderStyle.VERTICAL_ACCENT_BAR:
        return VerticalAccentHeading(text, level, theme)
    elif style_variant == SectionHeaderStyle.FILLED_RECTANGLE:
        space_before = 18
        space_after = 18
        text_color = theme.background_color
        back_color = theme.primary_color

    style = create_text_style(
        name=f"HeadingLevel_{level}",
        font_name=font_name,
        size=base_size,
        leading=leading,
        text_color=text_color,
        space_after=space_after,
    )
    style.spaceBefore = space_before
    style.alignment = 1 if align == "center" else 0
    if back_color:
        style.backColor = colors.HexColor(back_color)
    if style_variant in (
        SectionHeaderStyle.FILLED_RECTANGLE,
        SectionHeaderStyle.RIBBON,
        SectionHeaderStyle.BANNER,
    ):
        style.borderPadding = 6
        style.borderWidth = 0
        if style_variant == SectionHeaderStyle.RIBBON:
            style.borderTopWidth = 2
            style.borderBottomWidth = 2
            style.borderLeftWidth = 0
            style.borderRightWidth = 0
            style.borderTopColor = colors.HexColor(border_color)
            style.borderBottomColor = colors.HexColor(border_color)
            style.backColor = colors.white
            style.leading = leading + 2
            style.spaceBefore = 18
            style.spaceAfter = 18
        elif style_variant == SectionHeaderStyle.BANNER:
            style.borderLeftWidth = 0
            style.borderTopWidth = 0
            style.borderBottomWidth = 0
            style.backColor = colors.HexColor(theme.primary_color)
            style.textColor = colors.HexColor(theme.background_color)
            style.spaceBefore = 18
            style.spaceAfter = 18
        else:
            style.borderLeftWidth = 3
            style.borderLeftColor = colors.HexColor(border_color)
        style.leftIndent = 0
        style.firstLineIndent = 0
    if style_variant == SectionHeaderStyle.FILLED_RECTANGLE:
        style.borderPadding = 8
        style.borderLeftWidth = 0
        style.textColor = colors.HexColor(theme.background_color)
        style.spaceBefore = 18
        style.spaceAfter = 18
    return Paragraph(heading_text, style)
