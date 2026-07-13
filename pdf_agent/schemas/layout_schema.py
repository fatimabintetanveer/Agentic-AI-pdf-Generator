from typing import List, Optional, Literal
from pydantic import BaseModel, Field

"""
class PaletteSchema(BaseModel):
    family: Literal["navy", "teal", "amber", "slate", "blue", "green", "burgundy", "charcoal"] = Field(
        default="navy",
        description="Base palette family chosen from user preference and report tone."
    )
    tone: Literal["cool", "warm", "neutral", "premium", "editorial", "technical"] = Field(
        default="neutral",
        description="High-level emotional tone for the palette."
    )
    contrast_level: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="How strong the contrast should be."
    )
    seed_color: Optional[str] = Field(
        default=None,
        description="Optional user-provided or inferred seed hex color."
    )
    accent_hint: Optional[str] = Field(
        default=None,
        description="Optional accent color hint used to derive the rest of the palette."
    )
"""

class DesignSchema(BaseModel):
    #palette: PaletteSchema = Field(default_factory=PaletteSchema)
    cover_style: Literal["centered", "split_layout", "minimal"] = Field(default="centered")
    heading_level_1_style: Literal["standard", "underline", "ribbon", "vertical_accent_bar", "filled_rectangle", "banner"] = Field(default="standard")
    heading_level_2_style: Literal["standard", "underline", "ribbon", "vertical_accent_bar"] = Field(default="standard")
    heading_level_3_style: Literal["standard", "underline", "ribbon", "vertical_accent_bar"] = Field(default="standard")
    table_style: Literal["zebra", "filled_header", "rounded", "corporate"] = Field(default="corporate")
    callout_style: Literal["left_border", "filled_box", "quote", "floating_card"] = Field(default="left_border")
    kpi_style: Literal["flat", "filled", "outlined", "shadow", "gradient", "glass", "top_accent", "bottom_accent"] = Field(default="flat")
    decoration: Literal["none","bottom_band", "corner_triangles", "circles", "geometric_polygons", "thin_border"] = Field(default="none")


class ThemeSchema(BaseModel):
    name: Literal["cool_teal", "warm_amber", "corporate_navy"] = Field(description="Name of the chosen theme.")
    font_style: Literal["sans_serif", "serif"] = Field(default="sans_serif", description="Abstract font style descriptor.")

class CardItemSchema(BaseModel):
    title: str = Field(description="The heading title for this card panel (e.g. 'Strengths').")
    items: List[str] = Field(description="The bullet points to display inside this card.")

class TimelineStepSchema(BaseModel):
    title: str = Field(description="The main title of the milestone or phase.")
    date: Optional[str] = Field(default=None, description="Optional date, timeframe, or subtitle.")
    description: str = Field(description="Brief details or bullet points summarizing the step.")

class KeyValueSummaryItemSchema(BaseModel):
    label: str = Field(description="The summary label or key.")
    value: str = Field(description="The corresponding value.")

class KeyValueSummarySchema(BaseModel):
    title: Optional[str] = Field(
        default=None,
        description="Optional title for the summary card or section."
    )
    subtitle: Optional[str] = Field(
        default=None,
        description="Optional subtitle or descriptor for the summary card."
    )
    items: List[KeyValueSummaryItemSchema] = Field(
        description="The ordered label/value pairs that make up the summary."
    )

class RankedBarListItemSchema(BaseModel):
    label: str = Field(description="The display label for the ranked item.")
    value: float | int | str = Field(description="The numeric or numeric-like value used for ranking and bar length.")
    value_fmt: Optional[str] = Field(
        default=None,
        description="Optional formatted value string, for example '1.8M'.",
    )

class RankedBarListSchema(BaseModel):
    title: str = Field(description="The title shown above the ranked bar list.")
    items: List[RankedBarListItemSchema] = Field(
        description="Ordered ranked items in the format {label, value, value_fmt}."
    )
    subtitle: Optional[str] = Field(
        default=None,
        description="Optional subtitle shown under the title.",
    )
    max_value: Optional[float] = Field(
        default=None,
        description="Optional explicit maximum used to scale the bar lengths.",
    )

class StackedEntityRowSchema(BaseModel):
    rows: List[List[str]] = Field(
        description="Table-style rows where the first row is the header row and the remaining rows are data rows."
    )
    title_key: str = Field(
        description="Header name used for the entity title column."
    )
    value_key: str = Field(
        description="Header name used for the primary value or metric column."
    )
    detail_keys: List[str] = Field(
        description="Header names used for supporting detail columns."
    )


class DiffMatrixSchema(BaseModel):
    mode: Literal[
        "presence_absence",
        "status_diff",
        "custom",
    ] = Field(
        default="presence_absence",
        description="The rendering mode used to interpret and display the diff matrix.",
    )
    row_labels: List[str] = Field(description="The row labels shown on the left side of the matrix.")
    column_labels: List[str] = Field(description="The column labels shown across the top of the matrix.")
    cells: List[List[str]] = Field(
        description="Matrix cells aligned to row_labels and column_labels. Each row must contain one entry per column."
    )


class NodePropertiesSchema(BaseModel):
    section_title: Optional[str] = Field(default=None, description="Title of the section. Only use this for 'section' nodes.")
    col_ratio: Optional[float] = Field(default=0.5, description="Width ratio of the left column (e.g. 0.5). Only use this for 'two_column' nodes.")
    spacing: Optional[float] = Field(default=12.0, description="Horizontal spacing between the two columns in points. Only use this for 'two_column' nodes.")
    cards: Optional[List[CardItemSchema]] = Field(default=None, description="List of highlight cards data. Only use this for 'highlight_cards' nodes.")
    steps: Optional[List[TimelineStepSchema]] = Field(default=None, description="Chronological milestone steps. Only use this for 'timeline' nodes.")
    key_value_summary: Optional[KeyValueSummarySchema] = Field(default=None, description="Structured data for a compact key-value summary component.")
    ranked_bar_list: Optional[RankedBarListSchema] = Field(default=None, description="Structured data for a ranked bar list component.")
    stacked_entity_row: Optional[StackedEntityRowSchema] = Field(default=None, description="Structured data for a stacked entity row component.")
    label_key: Optional[str] = Field(default=None, description="The column key to use as the label field for 'ranked_bar_list' nodes.")
    rank_order: Optional[Literal["ascending", "descending"]] = Field(default=None, description="Sort order for ranked bar style content.")
    width_ratio: Optional[float] = Field(default=1.0, description="Multiplier for image width (e.g. 1.0 = full width, 0.5 = half width). Only use this for 'image' nodes.")

class LayoutNodeSchema(BaseModel):
    type: Literal[
        "section", 
        "two_column", 
        "heading", 
        "paragraph", 
        "list", 
        "table", 
        "stacked_entity_row",
        "key_value_summary",
        "timeline", 
        "kpi_cards", 
        "ranked_bar_list",
        "highlight_cards", 
        "callout", 
        "image",
    ] = Field(description="The component or container type.")
    children: Optional[List["LayoutNodeSchema"]] = Field(default=None, description="Children nodes for container types (like 'section').")
    children_left: Optional[List["LayoutNodeSchema"]] = Field(default=None, description="Children nodes to render inside the LEFT column. Only use when type is 'two_column'.")
    children_right: Optional[List["LayoutNodeSchema"]] = Field(default=None, description="Children nodes to render inside the RIGHT column. Only use when type is 'two_column'.")
    properties: Optional[NodePropertiesSchema] = Field(default=None, description="Attributes specific to the node type.")
    alignment: Optional[Literal["left", "center", "right"]] = Field(default=None, description="Optional alignment hint.")
    block_index: Optional[int] = Field(default=None, description="For leaf nodes only: the integer index of the document block this node should render.")
 

# Rebuild model to register recursive definitions
LayoutNodeSchema.model_rebuild()

class MarginsSchema(BaseModel):
    top: float = Field(default=2.0)
    bottom: float = Field(default=2.0)
    left: float = Field(default=2.0)
    right: float = Field(default=2.0)

class LayoutSpecSchema(BaseModel):
    theme: ThemeSchema
    design: DesignSchema = Field(default_factory=DesignSchema)
    has_cover_page: bool = Field(description="True if document needs a cover page based on metadata.")
    page_numbers: bool = Field(default=True)
    margins: MarginsSchema = Field(description="Page margins in cm.")
    sections: List[LayoutNodeSchema] = Field(description="Root section nodes (each must be of type 'section').")
