from pdf_agent.tools import markdown_parser
from typing import List, Dict, Any, Optional, Literal
from openai import OpenAI
from pydantic import BaseModel, Field
from pdf_agent.models import Document, LayoutSpecification, ThemeSpec, LayoutNode, DesignSpecification, DecorationSpec, DecorationType
from pdf_agent.themes import get_predefined_theme
from dataclasses import asdict
import json
import os

from pdf_agent.schemas.layout_schema import LayoutSpecSchema, LayoutNodeSchema


# def _palette_from_schema(palette_schema) -> PaletteSpec:
#     family_value = getattr(palette_schema, "family", PaletteFamily.NAVY.value)
#     tone_value = getattr(palette_schema, "tone", PaletteTone.NEUTRAL.value)
#     contrast_value = getattr(palette_schema, "contrast_level", ContrastLevel.MEDIUM.value)
#
#     try:
#         family = PaletteFamily(family_value)
#     except ValueError:
#         family = PaletteFamily.NAVY
#
#     try:
#         tone = PaletteTone(tone_value)
#     except ValueError:
#         tone = PaletteTone.NEUTRAL
#
#     try:
#         contrast_level = ContrastLevel(contrast_value)
#     except ValueError:
#         contrast_level = ContrastLevel.MEDIUM
#
#     return PaletteSpec(
#         family=family,
#         tone=tone,
#         contrast_level=contrast_level,
#         seed_color=getattr(palette_schema, "seed_color", None),
#         accent_hint=getattr(palette_schema, "accent_hint", None),
#     )


def _decoration_from_schema(decoration_value) -> DecorationSpec:
    if decoration_value is None:
        return DecorationSpec()

    if hasattr(decoration_value, "type"):
        decoration_type = getattr(decoration_value, "type", DecorationType.NONE)
        color = getattr(decoration_value, "color", "#1e3a8a")
        secondary_color = getattr(decoration_value, "secondary_color", None)
        opacity = getattr(decoration_value, "opacity", 1.0)
        size_cm = getattr(decoration_value, "size_cm", 2.0)
    else:
        decoration_type = decoration_value
        color = "#1e3a8a"
        secondary_color = None
        opacity = 1.0
        size_cm = 2.0

    try:
        deco_type = DecorationType(decoration_type)
    except ValueError:
        deco_type = DecorationType.NONE

    return DecorationSpec(
        type=deco_type,
        color=color,
        secondary_color=secondary_color,
        opacity=opacity,
        size_cm=size_cm,
    )


# Layout Planner Implementation

def _table_sample_rows(table_content, max_rows: int = 3):
    if not table_content or not isinstance(table_content, list) or len(table_content) < 2:
        return []

    headers = [str(cell) for cell in table_content[0]]
    samples = []
    for row in table_content[1 : 1 + max_rows]:
        if not isinstance(row, list):
            continue
        sample = {}
        for idx, header in enumerate(headers):
            if idx < len(row):
                sample[header] = row[idx]
        if sample:
            samples.append(sample)
    return samples


def plan_layout(document: Document, preferred_theme: str = "cool_teal", palette_hint: Optional[str] = None) -> LayoutSpecification:
    """
    Uses GPT-4o to generate a LayoutSpecification for a parsed document.
    """

    client = OpenAI()

    # -------------------------------------------------------
    # 1. Serialize the parsed document
    # -------------------------------------------------------
    structured_blocks = []
    for idx, block in enumerate(document.blocks):
        entry = {
            "index": idx,
            "type": block.type,
        }

        if block.type == "header":
            entry["level"] = block.metadata.get("level", 1)
            entry["text"] = str(block.content)

        elif block.type == "paragraph":
            entry["text"] = str(block.content)

        elif block.type == "quote":
            entry["text"] = str(block.content)

        elif block.type == "list":
            entry["ordered"] = block.metadata.get("ordered", False)
            entry["items"] = block.content

        elif block.type == "table":
            entry["headers"] = block.content[0] if block.content else []
            entry["row_count"] = len(block.content) - 1 if block.content else 0
            entry["rows"] = block.content[1:] if block.content else []
            #entry["sample_rows"] = _table_sample_rows(block.content)

        elif block.type == "image":
            entry["path"] = str(block.content)
            entry["caption"] = block.metadata.get("caption", "")

        structured_blocks.append(entry)

    document_json = json.dumps(
        {
            "title": document.title,
            "metadata": document.metadata,
            "blocks": structured_blocks,
        },
        indent=2,
    )

    # -------------------------------------------------------
    # 2. Load the system prompt
    # -------------------------------------------------------
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "prompt",
        "layout_planner_new.md",
    )

    with open(os.path.normpath(prompt_path), "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # -------------------------------------------------------
    # 3. Build the user prompt
    # -------------------------------------------------------
    # palette_hint_text = f"\nUser palette preference: {palette_hint}" if palette_hint else ""
    user_prompt = f"""Design a LayoutSpecification for the following parsed document.
Parsed Document: {document_json}
"""

    # -------------------------------------------------------
    # 4. Call GPT with Structured Outputs
    # -------------------------------------------------------
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        response_format=LayoutSpecSchema,
    )

    # -------------------------------------------------------
    # 5. Parse the structured response
    # -------------------------------------------------------
    spec_data: LayoutSpecSchema = response.choices[0].message.parsed
    theme_spec = get_predefined_theme(spec_data.theme.name, font_style=spec_data.theme.font_style)
    # if getattr(spec_data, "design", None) and getattr(spec_data.design, "palette", None):
    #     theme_spec = derive_theme_from_palette(_palette_from_schema(spec_data.design.palette), font_style=spec_data.theme.font_style)

    def map_node(node_schema: LayoutNodeSchema) -> LayoutNode:
        children = [map_node(c) for c in node_schema.children] if node_schema.children else []
        children_left = [map_node(c) for c in node_schema.children_left] if node_schema.children_left else []
        children_right = [map_node(c) for c in node_schema.children_right] if node_schema.children_right else []
        properties = node_schema.properties.model_dump(exclude_none=True) if node_schema.properties else {}

        return LayoutNode(
            type=node_schema.type,
            children=children,
            children_left=children_left,
            children_right=children_right,
            properties=properties,
            block_index=node_schema.block_index,
        )

    sections = [map_node(s) for s in spec_data.sections]

    design = DesignSpecification(
        # palette=_palette_from_schema(spec_data.design.palette),
        cover_style=spec_data.design.cover_style,
        heading_level_1_style=spec_data.design.heading_level_1_style,
        heading_level_2_style=spec_data.design.heading_level_2_style,
        heading_level_3_style=spec_data.design.heading_level_3_style,
        table_style=spec_data.design.table_style,
        callout_style=spec_data.design.callout_style,
        kpi_style=spec_data.design.kpi_style,
        highlight_style=spec_data.design.highlight_style,
        decoration=_decoration_from_schema(spec_data.design.decoration),
    )

    margins_dict = {
        "top": spec_data.margins.top,
        "bottom": spec_data.margins.bottom,
        "left": spec_data.margins.left,
        "right": spec_data.margins.right,
    }

    return LayoutSpecification(
        theme=theme_spec,
        design=design,
        has_cover_page=spec_data.has_cover_page,
        page_numbers=spec_data.page_numbers,
        margins=margins_dict,
        sections=sections,
    )
