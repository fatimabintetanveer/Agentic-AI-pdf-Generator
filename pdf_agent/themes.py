from copy import deepcopy
from typing import Dict

from pdf_agent.models import (
    CalloutStyle,
    DividerStyle,
    HighlightStyle,
    ImageStyle,
    KpiStyle,
    PaletteFamily,
    PaletteTone,
    ContrastLevel,
    PaletteSpec,
    SpacingStyle,
    TableStyle,
    ThemeSpec,
    TimelineStyle,
    TypographyStyle,
)

PREDEFINED_THEMES: Dict[str, ThemeSpec] = {
    "corporate_navy": ThemeSpec(
        name="corporate_navy",
        primary_color="#1e3a8a",
        secondary_color="#4b5563",
        accent_color="#2563eb",
        background_color="#eff6ff",
        table_header_bg="#1f2937",
        table_header_text="#ffffff",
        table_row_even_bg="#f3f4f6",
        table_row_odd_bg="#ffffff",
        table_grid_color="#e2e8f0",
        table_border_width=0.5,
        table_padding=6.0,
        typography=TypographyStyle(
            heading_font="Helvetica-Bold",
            body_font="Helvetica",
            heading_size=16.0,
            subheading_size=12.0,
            body_size=10.5,
            caption_size=8.5,
            line_height=1.25,
        ),
        spacing=SpacingStyle(
            section_spacing=12.0,
            paragraph_spacing=6.0,
            card_padding=10.0,
            element_spacing=8.0,
        ),
        table=TableStyle(
            variant="corporate",
        ),
        callout=CalloutStyle(
            bg_color="#eff6ff",
            border_color="#2563eb",
            border_width=4.0,
            text_color="#111827",
            padding=12.0,
        ),
        kpi=KpiStyle(
            bg_color="#ffffff",
            value_color="#1e3a8a",
            label_color="#4b5563",
            border_color="#e2e8f0",
            border_radius=6.0,
            padding=10.0,
        ),
        timeline=TimelineStyle(
            circle_color="#1f2937",
            line_color="#cbd5e1",
            title_color="#111827",
            text_color="#4b5563",
            badge_text_color="#ffffff",
        ),
        highlight=HighlightStyle(
            header_bg="#1f2937",
            header_text="#ffffff",
            body_bg="#ffffff",
            body_text="#1e293b",
            border_color="#cbd5e1",
            padding=10.0,
            border_radius=6.0,
        ),
        image=ImageStyle(
            caption_color="#6b7280",
            caption_font="Helvetica-Oblique",
            border_color="#e2e8f0",
            border_width=0.5,
            corner_radius=4.0,
        ),
        # divider=DividerStyle(
        #     color="#e5e7eb",
        #     thickness=0.5,
        #     spacing_before=15.0,
        #     spacing_after=15.0,
        # ),
    ),
    "cool_teal": ThemeSpec(
        name="cool_teal",
        primary_color="#0f766e",
        secondary_color="#475569",
        accent_color="#0d9488",
        background_color="#f0fdfa",
        table_header_bg="#0f766e",
        table_header_text="#ffffff",
        table_row_even_bg="#f1f5f9",
        table_row_odd_bg="#ffffff",
        table_grid_color="#ccfbf1",
        table_border_width=0.5,
        table_padding=6.0,
        typography=TypographyStyle(
            heading_font="Helvetica-Bold",
            body_font="Helvetica",
            heading_size=16.0,
            subheading_size=12.0,
            body_size=10.5,
            caption_size=8.5,
            line_height=1.25,
        ),
        spacing=SpacingStyle(
            section_spacing=12.0,
            paragraph_spacing=6.0,
            card_padding=10.0,
            element_spacing=8.0,
        ),
        table=TableStyle(
            variant="corporate",
        ),
        callout=CalloutStyle(
            bg_color="#f0fdfa",
            border_color="#0d9488",
            border_width=4.0,
            text_color="#111827",
            padding=12.0,
        ),
        kpi=KpiStyle(
            bg_color="#ffffff",
            value_color="#0f766e",
            label_color="#475569",
            border_color="#ccfbf1",
            border_radius=6.0,
            padding=10.0,
        ),
        timeline=TimelineStyle(
            circle_color="#0d9488",
            line_color="#ccfbf1",
            title_color="#111827",
            text_color="#475569",
            badge_text_color="#ffffff",
        ),
        highlight=HighlightStyle(
            header_bg="#0f766e",
            header_text="#ffffff",
            body_bg="#ffffff",
            body_text="#1e293b",
            border_color="#ccfbf1",
            padding=10.0,
            border_radius=6.0,
        ),
        image=ImageStyle(
            caption_color="#64748b",
            caption_font="Helvetica-Oblique",
            border_color="#ccfbf1",
            border_width=0.5,
            corner_radius=4.0,
        ),
        # divider=DividerStyle(
        #     color="#e5e7eb",
        #     thickness=0.25,
        #     spacing_before=15.0,
        #     spacing_after=15.0,
        # ),
    ),
    "warm_amber": ThemeSpec(
        name="warm_amber",
        primary_color="#b45309",
        secondary_color="#4b5563",
        accent_color="#d97706",
        background_color="#fef3c7",
        table_header_bg="#374151",
        table_header_text="#ffffff",
        table_row_even_bg="#f9fafb",
        table_row_odd_bg="#ffffff",
        table_grid_color="#fde68a",
        table_border_width=0.5,
        table_padding=6.0,
        typography=TypographyStyle(
            heading_font="Helvetica-Bold",
            body_font="Helvetica",
            heading_size=16.0,
            subheading_size=12.0,
            body_size=10.5,
            caption_size=8.5,
            line_height=1.25,
        ),
        spacing=SpacingStyle(
            section_spacing=12.0,
            paragraph_spacing=6.0,
            card_padding=10.0,
            element_spacing=8.0,
        ),
        table=TableStyle(
            variant="corporate",
        ),
        callout=CalloutStyle(
            bg_color="#fef3c7",
            border_color="#d97706",
            border_width=4.0,
            text_color="#111827",
            padding=12.0,
        ),
        kpi=KpiStyle(
            bg_color="#ffffff",
            value_color="#b45309",
            label_color="#4b5563",
            border_color="#fde68a",
            border_radius=6.0,
            padding=10.0,
        ),
        timeline=TimelineStyle(
            circle_color="#d97706",
            line_color="#fde68a",
            title_color="#111827",
            text_color="#4b5563",
            badge_text_color="#ffffff",
        ),
        highlight=HighlightStyle(
            header_bg="#b45309",
            header_text="#ffffff",
            body_bg="#ffffff",
            body_text="#1e293b",
            border_color="#fde68a",
            padding=10.0,
            border_radius=6.0,
        ),
        image=ImageStyle(
            caption_color="#78716c",
            caption_font="Helvetica-Oblique",
            border_color="#fde68a",
            border_width=0.5,
            corner_radius=4.0,
        ),
        # divider=DividerStyle(
        #     color="#fde68a",
        #     thickness=0.25,
        #     spacing_before=15.0,
        #     spacing_after=15.0,
        # ),
    ),
}


def get_predefined_theme(name: str, font_style: str = "sans_serif") -> ThemeSpec:
    theme = PREDEFINED_THEMES.get(name, PREDEFINED_THEMES["corporate_navy"])
    theme_copy = deepcopy(theme)
    theme_copy.font_style = font_style
    return theme_copy








""""
def derive_theme_from_palette(
    palette: PaletteSpec,
    font_style: str = "sans_serif",
) -> ThemeSpec:

    def _enum_value(value, enum_cls, default):
        if isinstance(value, enum_cls):
            return value
        if isinstance(value, str):
            try:
                return enum_cls(value)
            except ValueError:
                try:
                    return enum_cls[value.upper()]
                except KeyError:
                    return default
        return default

    family = _enum_value(palette.family, PaletteFamily, PaletteFamily.NAVY)
    tone = _enum_value(palette.tone, PaletteTone, PaletteTone.NEUTRAL)
    contrast = _enum_value(palette.contrast_level, ContrastLevel, ContrastLevel.MEDIUM)

    family_map = {
        PaletteFamily.NAVY: ("#1e3a8a", "#4b5563", "#2563eb", "#eff6ff", "#1f2937", "#f3f4f6"),
        PaletteFamily.TEAL: ("#0f766e", "#475569", "#0d9488", "#f0fdfa", "#0f766e", "#f1f5f9"),
        PaletteFamily.AMBER: ("#b45309", "#4b5563", "#d97706", "#fef3c7", "#374151", "#f9fafb"),
        PaletteFamily.SLATE: ("#334155", "#64748b", "#0f172a", "#f8fafc", "#334155", "#f8fafc"),
        PaletteFamily.BLUE: ("#1d4ed8", "#475569", "#3b82f6", "#eff6ff", "#1e40af", "#f8fafc"),
        PaletteFamily.GREEN: ("#166534", "#4b5563", "#22c55e", "#f0fdf4", "#14532d", "#f8fafc"),
        PaletteFamily.BURGUNDY: ("#7f1d1d", "#57534e", "#b91c1c", "#fef2f2", "#7f1d1d", "#fdf2f8"),
        PaletteFamily.CHARCOAL: ("#111827", "#4b5563", "#374151", "#f3f4f6", "#111827", "#f9fafb"),
    }

    tone_accent = {
        PaletteTone.COOL: "#2563eb",
        PaletteTone.WARM: "#d97706",
        PaletteTone.NEUTRAL: None,
        PaletteTone.PREMIUM: "#6d28d9",
        PaletteTone.EDITORIAL: "#9f1239",
        PaletteTone.TECHNICAL: "#0284c7",
    }

    primary, secondary, accent, background, table_header, table_row_even = family_map.get(
        family,
        family_map[PaletteFamily.NAVY],
    )

    if tone in tone_accent and tone_accent[tone]:
        accent = tone_accent[tone]

    if contrast == ContrastLevel.LOW:
        background = "#fafafa"
    elif contrast == ContrastLevel.HIGH:
        secondary = "#1f2937"

    theme = get_predefined_theme(
        "corporate_navy" if family == PaletteFamily.NAVY else "cool_teal",
        font_style=font_style,
    )
    theme.name = family.value
    theme.primary_color = palette.seed_color or primary
    theme.secondary_color = secondary
    theme.accent_color = palette.accent_hint or accent
    theme.background_color = background
    theme.table_header_bg = table_header
    theme.table_header_text = "#ffffff"
    theme.table_row_even_bg = table_row_even
    theme.table_row_odd_bg = "#ffffff"
    theme.table_grid_color = "#e2e8f0"
    theme.table_border_width = 0.5
    theme.table_padding = 6.0
    return theme
"""
