from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

# ==========================================
# Palette System
# ==========================================

class PaletteFamily(str, Enum):
    NAVY = "navy"
    TEAL = "teal"
    AMBER = "amber"
    SLATE = "slate"
    BLUE = "blue"
    GREEN = "green"
    BURGUNDY = "burgundy"
    CHARCOAL = "charcoal"


class PaletteTone(str, Enum):
    COOL = "cool"
    WARM = "warm"
    NEUTRAL = "neutral"
    PREMIUM = "premium"
    EDITORIAL = "editorial"
    TECHNICAL = "technical"


class ContrastLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class PaletteSpec:
    """High-level palette direction chosen by the planner."""
    family: PaletteFamily = PaletteFamily.NAVY
    tone: PaletteTone = PaletteTone.NEUTRAL
    contrast_level: ContrastLevel = ContrastLevel.MEDIUM
    seed_color: Optional[str] = None
    accent_hint: Optional[str] = None


# ==========================================
# Component Style Variants (Enums)
# ==========================================

class CoverStyle(str, Enum):
    CENTERED = "centered"
    LEFT_ALIGNED = "left_aligned"
    RIGHT_ALIGNED = "right_aligned"
    FULL_COLOR_BAND = "full_color_band"
    DIAGONAL_RIBBON = "diagonal_ribbon"
    SPLIT_LAYOUT = "split_layout"
    HERO_IMAGE = "hero_image"
    LARGE_WATERMARK = "large_watermark"
    MINIMAL = "minimal"

class SectionHeaderStyle(str, Enum):
    STANDARD = "standard"
    UNDERLINE = "underline"
    RIBBON = "ribbon"
    BANNER = "banner"
    VERTICAL_ACCENT_BAR = "vertical_accent_bar"
    FILLED_RECTANGLE = "filled_rectangle"

class TableStyleVariant(str, Enum):
    ZEBRA = "zebra"
    FILLED_HEADER = "filled_header"
    ROUNDED = "rounded"
    CORPORATE = "corporate"
    STACKED_ENTITY_ROW = "stacked_entity_row"

class CalloutStyleVariant(str, Enum):
    LEFT_BORDER = "left_border"
    FILLED_BOX = "filled_box"
    QUOTE = "quote"
    FLOATING_CARD = "floating_card"

class DividerStyleVariant(str, Enum):
    THIN_LINE = "thin_line"
    DOUBLE_LINE = "double_line"
    DOTTED = "dotted"
    DASHED = "dashed"
    WAVE = "wave"
    ACCENT_BAR = "accent_bar"
    DECORATIVE_ICON = "decorative_icon"
    
class ImageStyleVariant(str, Enum):
    FULL_WIDTH = "full_width"
    LEFT_WRAP = "left_wrap"
    RIGHT_WRAP = "right_wrap"
    CARD = "card"
    CAPTION_OVERLAY = "caption_overlay"

class KpiStyleVariant(str, Enum):
    FLAT = "flat"
    FILLED = "filled"
    OUTLINED = "outlined"
    SHADOW = "shadow"
    GRADIENT = "gradient"
    GLASS = "glass"
    TOP_ACCENT = "top_accent"
    BOTTOM_ACCENT = "bottom_accent"

class CardStyleVariant(str, Enum):
    FLAT = "flat"
    SHADOW = "shadow"
    ROUNDED = "rounded"
    OUTLINE = "outline"
    GLASS = "glass"
    FILLED = "filled"
    GRADIENT = "gradient"

class DecorationType(str, Enum):
    NONE = "none"
    TOP_BAND = "top_band"
    BOTTOM_BAND = "bottom_band"
    LEFT_SIDEBAR = "left_sidebar"
    RIGHT_SIDEBAR = "right_sidebar"
    CORNER_TRIANGLES = "corner_triangles"
    CIRCLES = "circles"
    GEOMETRIC_POLYGONS = "geometric_polygons"
    THIN_BORDER = "thin_border"
    WATERMARK = "watermark"

@dataclass
class DecorationSpec:
    """Specifies a parameterized background decoration layer."""
    type: DecorationType = DecorationType.NONE
    color: str = "#1e3a8a"
    secondary_color: Optional[str] = None
    opacity: float = 1.0
    size_cm: float = 2.0  # Context-dependent size (e.g. band thickness, circle radius)
    
# ==========================================
# Domain Data Models
# ==========================================

@dataclass
class TypographyStyle:
    section_header: SectionHeaderStyle = SectionHeaderStyle.STANDARD
    heading_font: str = "Helvetica-Bold"
    body_font: str = "Helvetica"
    heading_size: float = 16.0
    subheading_size: float = 12.0
    body_size: float = 10.5
    caption_size: float = 8.5
    line_height: float = 1.25

@dataclass
class SpacingStyle:
    section_spacing: float = 12.0
    paragraph_spacing: float = 6.0
    card_padding: float = 10.0
    element_spacing: float = 8.0

@dataclass
class TableStyle:
    variant: TableStyleVariant = TableStyleVariant.CORPORATE

@dataclass
class CalloutStyle:
    variant: CalloutStyleVariant = CalloutStyleVariant.LEFT_BORDER
    bg_color: str = "#eff6ff"
    border_color: str = "#2563eb"
    border_width: float = 4.0
    text_color: str = "#111827"
    padding: float = 12.0

@dataclass
class KpiStyle:
    variant: KpiStyleVariant = KpiStyleVariant.FLAT
    bg_color: str = "#ffffff"
    value_color: str = "#1e3a8a"
    label_color: str = "#4b5563"
    border_color: str = "#e2e8f0"
    border_radius: float = 6.0
    padding: float = 10.0

@dataclass
class TimelineStyle:
    circle_color: str = "#2563eb"
    line_color: str = "#cbd5e1"
    title_color: str = "#111827"
    text_color: str = "#4b5563"
    badge_text_color: str = "#ffffff"

@dataclass
class HighlightStyle:
    variant: CardStyleVariant = CardStyleVariant.FLAT
    header_bg: str = "#1e3a8a"
    header_text: str = "#ffffff"
    body_bg: str = "#ffffff"
    body_text: str = "#1e293b"
    border_color: str = "#cbd5e1"
    padding: float = 10.0
    border_radius: float = 6.0

@dataclass
class ImageStyle:
    variant: ImageStyleVariant = ImageStyleVariant.FULL_WIDTH
    caption_color: str = "#6b7280"
    caption_font: str = "Helvetica-Oblique"
    border_color: str = "#e2e8f0"
    border_width: float = 0.5
    corner_radius: float = 4.0

@dataclass
class DividerStyle:
    variant: DividerStyleVariant = DividerStyleVariant.THIN_LINE
    color: str = "#e2e8f0"
    thickness: float = 0.5
    spacing_before: float = 15.0
    spacing_after: float = 15.0

@dataclass
class ThemeSpec:
    """
    Defines the visual branding guidelines of the document.
    The theme is now split into high-level color fields plus component-specific
    style groups, making it easier to expand and reuse across renderers.
    """
    name: str = "corporate_navy"
    primary_color: str = "#1e3a8a"  # Slate 900
    secondary_color: str = "#4b5563"  # Slate 600
    accent_color: str = "#2563eb"  # Blue 500
    background_color: str = "#eff6ff"  # Slate 50
    font_style: str = "sans_serif"  # Abstract style: 'sans_serif' or 'serif'
    cover_style: CoverStyle = CoverStyle.CENTERED
    table_header_bg: str = "#1f2937"
    table_header_text: str = "#ffffff"
    table_row_even_bg: str = "#f3f4f6"
    table_row_odd_bg: str = "#ffffff"
    table_grid_color: str = "#e2e8f0"
    table_border_width: float = 0.5
    table_padding: float = 6.0

    # Nested styles
    typography: TypographyStyle = field(default_factory=TypographyStyle)
    spacing: SpacingStyle = field(default_factory=SpacingStyle)
    table: TableStyle = field(default_factory=TableStyle)
    callout: CalloutStyle = field(default_factory=CalloutStyle)
    kpi: KpiStyle = field(default_factory=KpiStyle)
    timeline: TimelineStyle = field(default_factory=TimelineStyle)
    highlight: HighlightStyle = field(default_factory=HighlightStyle)
    image: ImageStyle = field(default_factory=ImageStyle)
    # divider: DividerStyle = field(default_factory=DividerStyle)
