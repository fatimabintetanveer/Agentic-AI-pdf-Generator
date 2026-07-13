import os
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors as _colors
from reportlab.lib.enums import TA_CENTER

from pdf_agent.models import Document, LayoutSpecification, SectionHeaderStyle
from pdf_agent.components.elements import render_heading, render_paragraph, render_list, render_table
from pdf_agent.components.callout import render_callout
from pdf_agent.components.kpi_cards import render_kpi_cards
from pdf_agent.components.structures import render_two_column
from pdf_agent.components.cover import render_cover_page
from pdf_agent.components.timeline import render_timeline
from pdf_agent.components.image import render_image
from pdf_agent.components.highlight_cards import render_highlight_cards
from pdf_agent.components.diff_matrix import render_diff_matrix
from pdf_agent.components.ranked_bar_list import render_ranked_bar_list
from pdf_agent.components.stacked_entity_row import render_stacked_entity_row
from pdf_agent.components.key_value_summary import render_key_value_summary
from pdf_agent.models import LayoutNode, DesignSpecification
from pdf_agent.components.decorations import (
    draw_band,
    draw_circle,
    draw_frame,
    draw_ribbon,
    draw_wave,
    draw_polygon,
    draw_full_width_top_band,
)


def _tint_hex_color(hex_color: str, mix: float = 0.82) -> str:
    """Blend a hex color with white to create a lighter background tint."""
    try:
        rgb = colors.HexColor(hex_color)
        r = 1.0 - ((1.0 - rgb.red) * (1.0 - mix))
        g = 1.0 - ((1.0 - rgb.green) * (1.0 - mix))
        b = 1.0 - ((1.0 - rgb.blue) * (1.0 - mix))
        return colors.Color(r, g, b).hexval()
    except Exception:
        return hex_color


def _resolve_heading_style(design: DesignSpecification, level: int) -> SectionHeaderStyle:
    fallback = getattr(design, "section_header_style", SectionHeaderStyle.STANDARD)
    if isinstance(fallback, str):
        try:
            fallback = SectionHeaderStyle(fallback)
        except ValueError:
            fallback = SectionHeaderStyle.STANDARD

    field_name = f"heading_level_{level}_style"
    style_value = getattr(design, field_name, fallback)
    if isinstance(style_value, str):
        try:
            style_value = SectionHeaderStyle(style_value)
        except ValueError:
            style_value = fallback
    if style_value is None:
        style_value = fallback
    return style_value

class NumberedCanvas(canvas.Canvas):
    """
    Custom canvas that calculates total pages dynamically and draws consistent 
    running headers and footers (with page numbers) on all pages except the cover page.
    """
    footer_text = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            # if self._pageNumber > 1: # Suppress header/footer on cover page
            self.draw_header_footer(page_count)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        
        # Grid layout points based on A4 margins
        left_margin = 2.0 * cm
        right_margin = A4[0] - (2.0 * cm)
        
        # 1. Header decoration
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b")) # Slate gray
        #self.drawString(left_margin, A4[1] - 1.2 * cm, "Quarterly Business Performance Report")
        self.setStrokeColor(colors.HexColor("#cbd5e1")) # Light gray line
        self.setLineWidth(0.5)
        #self.line(left_margin, A4[1] - 1.3 * cm, right_margin, A4[1] - 1.3 * cm)
        
        # 2. Footer decoration
        self.line(left_margin, 1.5 * cm, right_margin, 1.5 * cm)
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(right_margin, 1.1 * cm, page_str)
        if self.footer_text:
            self.drawString(left_margin, 1.1 * cm, self.footer_text)
        
        self.restoreState()


def _draw_design_decoration(c: canvas.Canvas, design: DesignSpecification):
    decoration = getattr(design, "decoration", None)
    deco_type = getattr(decoration, "type", None)

    if deco_type is None:
        return

    deco_name = deco_type.value if hasattr(deco_type, "value") else str(deco_type)
    color = getattr(decoration, "color", "#1e3a8a")
    secondary_color = getattr(decoration, "secondary_color", None)
    opacity = getattr(decoration, "opacity", 1.0)
    size_cm = getattr(decoration, "size_cm", 2.0)
    soft_color = _tint_hex_color(color, 0.88)
    soft_secondary = _tint_hex_color(secondary_color, 0.88) if secondary_color else None

    if deco_name == "top_band":
        draw_full_width_top_band(c, color=soft_color, secondary_color=soft_secondary)
    elif deco_name == "bottom_band":
        draw_band(c, position="bottom", thickness_cm=max(size_cm, 1.2), color=soft_color, opacity=0.75)
    elif deco_name == "left_sidebar":
        draw_band(c, position="left", thickness_cm=max(size_cm, 1.8), color=soft_color, opacity=0.72)
    elif deco_name == "right_sidebar":
        draw_band(c, position="right", thickness_cm=max(size_cm, 1.8), color=soft_color, opacity=0.72)
    elif deco_name == "corner_triangles":
        draw_ribbon(c, corner="top_right", color=soft_color, width_cm=max(size_cm, 5.0), opacity=0.35)
        if soft_secondary:
            draw_ribbon(c, corner="bottom_left", color=soft_secondary, width_cm=max(size_cm, 5.0), opacity=0.30)
    elif deco_name == "circles":
        draw_circle(c, cx_cm=2.0, cy_cm=27.0, radius_cm=max(size_cm * 1.8, 2.5), color=soft_color, opacity=0.18)
    elif deco_name == "geometric_polygons":
        draw_polygon(
            c,
            vertices_cm=[(0, 0), (7, 0), (4.5, 5.5)],
            color=soft_color,
            opacity=0.16,
        )
    elif deco_name == "thin_border":
        draw_frame(c, margin_cm=1.35, thickness_pt=0.9, color=soft_color, accent_corners=True, accent_color=soft_secondary or soft_color)
    elif deco_name == "watermark":
        draw_wave(c, position="bottom", color=soft_color, opacity=max(0.08, min(opacity, 0.16)), height_cm=5.0, amplitude_cm=2.5)

def generate_pdf(document: Document, layout_spec: LayoutSpecification, output_path: str) -> str:
    """
    Compiles a Document and a LayoutSpecification into a polished PDF.
    Recursively renders the layout specifications based on a LayoutNode composition tree.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 1. Convert margin cm configurations to points
    m = layout_spec.margins
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=m.get("left", 2.0) * cm,
        rightMargin=m.get("right", 2.0) * cm,
        topMargin=m.get("top", 2.0) * cm,
        bottomMargin=m.get("bottom", 2.0) * cm
    )
    
    # Width of the usable page canvas
    page_width = A4[0] - (doc.leftMargin + doc.rightMargin)
    story = []
    theme = layout_spec.theme
    design = getattr(layout_spec, "design", None)
    if design is None:
        design = DesignSpecification()
    cover = getattr(document, "cover", {}) or {}
    footer = getattr(document, "footer", None) or {}
    footer_text = ""
    if isinstance(footer, dict):
        footer_text = str(footer.get("text", "") or "").strip()

    def _cover_metadata_to_dict(value):
        if isinstance(value, dict):
            return {k: v for k, v in value.items() if v}
        if isinstance(value, list):
            result = {}
            for item in value:
                if isinstance(item, dict):
                    key = str(item.get("key", "")).strip()
                    val = item.get("value")
                    if key and val:
                        result[key] = val
            return result
        return {}

    cover_meta = _cover_metadata_to_dict(cover.get("metadata", []))
    # 2. Cover Page Placement
    if layout_spec.has_cover_page:
        title = cover.get("title") or document.title or "Business Report"
        subtitle = cover.get("subtitle") or ""
        meta = cover_meta or document.metadata or {}
        story.extend(render_cover_page(title, subtitle, meta, theme, getattr(design, "cover_style", None)))
        story.append(PageBreak())
    elif document.title:

        title_style = ParagraphStyle(
            "DocumentTitle",
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=34,
            alignment = TA_CENTER,
            textColor=_colors.HexColor(theme.primary_color),
            spaceAfter=4,
        )
        subtitle_style = ParagraphStyle(
            "DocumentSubtitle",
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            alignment = TA_CENTER,
            textColor=_colors.HexColor(theme.secondary_color),
            spaceAfter=20,
        )
        story.append(Paragraph(document.title, title_style))
        # Render any top-level metadata (date, author) as a subtitle line
        meta_parts = []
        if document.metadata.get("date"):
            meta_parts.append(document.metadata["date"])
        if document.metadata.get("author"):
            meta_parts.append(f"Prepared by: {document.metadata['author']}")
        if meta_parts:
            story.append(Paragraph("  ·  ".join(meta_parts), subtitle_style))

    # 3. Content Construction Loop
    def compile_node(node: LayoutNode, width: float) -> list:
        flowables = []
        
        # -- 1. Container Nodes --
        if node.type == "section":
            section_title = node.properties.get("section_title")
            # Skip rendering the section title if it duplicates the document title
            # (the document title is already rendered at the top of the page)
            doc_title = (document.title or "").strip()
            if section_title and section_title.strip() != doc_title:
                flowables.append(render_heading(section_title, 1, theme, _resolve_heading_style(design, 1)))
                #flowables.append(Spacer(1, 8))
            for child in node.children:
                flowables.extend(compile_node(child, width))
                
        elif node.type == "two_column":
            col_ratio = node.properties.get("col_ratio", 0.5)
            spacing = node.properties.get("spacing", 12.0)
            left_w = (width - spacing) * col_ratio
            right_w = (width - spacing) * (1.0 - col_ratio)

            # Compile left children at the correct column width
            left_fl = []
            for child in node.children_left:
                left_fl.extend(compile_node(child, left_w))

            # Compile right children at the correct column width
            right_fl = []
            for child in node.children_right:
                right_fl.extend(compile_node(child, right_w))

            flowables.append(render_two_column(left_fl, right_fl, width, spacing=spacing, col_ratio=col_ratio))

        # -- 2. Leaf Component Nodes --
        else:
            comp_type = node.type
            
            # Explicit Data Binding: fetch the exact block from the document
            block = None
            if getattr(node, 'block_index', None) is not None:
                idx = node.block_index
                if 0 <= idx < len(document.blocks):
                    block = document.blocks[idx]

            # If it's highlight_cards, it relies on structured properties instead of document blocks
            if comp_type == "highlight_cards":
                cards_list = node.properties.get("cards") if node.properties else None
                if cards_list:
                    # Convert list of dicts to Dict[str, List[str]]
                    sections_dict = {card.get("title"): card.get("items", []) for card in cards_list if card.get("title")}
                    flowables.append(render_highlight_cards(sections_dict, theme, width, getattr(design, "highlight_style", None)))
                    flowables.append(Spacer(1, 15))
                return flowables

            # If it's timeline, it relies on structured properties instead of document blocks
            if comp_type == "timeline":
                steps = node.properties.get("steps") if node.properties else None
                if steps:
                    flowables.append(render_timeline(steps, theme, width))
                    flowables.append(Spacer(1, 15))
                return flowables

            # If it's ranked_bar_list, it relies on structured properties instead of document blocks
            if comp_type == "ranked_bar_list":
                props = node.properties or {}
                ranked_spec = props.get("ranked_bar_list") if isinstance(props, dict) else None

                if isinstance(ranked_spec, dict):
                    title = ranked_spec.get("title") or props.get("title") or props.get("section_title") or "Ranked Bar List"
                    subtitle = ranked_spec.get("subtitle") or props.get("subtitle")
                    items = ranked_spec.get("items") or []
                    max_value = ranked_spec.get("max_value")
                else:
                    title = props.get("title") or props.get("section_title") or "Ranked Bar List"
                    subtitle = props.get("subtitle")
                    items = props.get("items") or []
                    max_value = props.get("max_value")

                if items:
                    flowables.append(
                        render_ranked_bar_list(
                            items,
                            theme,
                            width,
                            title=str(title),
                            subtitle=str(subtitle) if subtitle else None,
                            max_value=max_value,
                        )
                    )
                    flowables.append(Spacer(1, 15))
                return flowables

            # If it's diff_matrix, it relies on structured properties instead of document blocks
            if comp_type == "diff_matrix":
                props = node.properties or {}
                diff_spec = props.get("diff_matrix") if isinstance(props, dict) else None

                if isinstance(diff_spec, dict):
                    row_labels = diff_spec.get("row_labels") or []
                    column_labels = diff_spec.get("column_labels") or []
                    cells = diff_spec.get("cells") or []
                    mode = diff_spec.get("mode") or "presence_absence"
                else:
                    row_labels = props.get("row_labels") or []
                    column_labels = props.get("column_labels") or []
                    cells = props.get("cells") or []
                    mode = props.get("mode") or "presence_absence"

                if row_labels and column_labels and cells:
                    flowables.append(
                        render_diff_matrix(
                            row_labels=row_labels,
                            column_labels=column_labels,
                            cells=cells,
                            theme=theme,
                            width=width,
                            mode=str(mode),
                        )
                    )
                    flowables.append(Spacer(1, 15))
                return flowables

            # If it's stacked_entity_row, it relies on structured properties instead of document blocks
            if comp_type == "stacked_entity_row":
                props = node.properties or {}
                stacked_spec = props.get("stacked_entity_row") if isinstance(props, dict) else None

                if isinstance(stacked_spec, dict):
                    rows = stacked_spec.get("rows") or []
                    title_key = stacked_spec.get("title_key") or props.get("title_key")
                    value_key = stacked_spec.get("value_key") or props.get("value_key")
                    detail_keys = stacked_spec.get("detail_keys") or props.get("detail_keys") or []
                else:
                    rows = []
                    title_key = props.get("title_key")
                    value_key = props.get("value_key")
                    detail_keys = props.get("detail_keys") or []

                if rows and title_key and value_key:
                    flowables.append(
                        render_stacked_entity_row(
                            rows,
                            theme,
                            width,
                            str(title_key),
                            str(value_key),
                            [str(k) for k in detail_keys],
                        )
                    )
                    flowables.append(Spacer(1, 10))
                return flowables

            # If it's a leaf node but no block was bound (or block is missing), just return empty
            if block is None:
                return []
                
            if comp_type == "heading":
                level = block.metadata.get("level", 2) if block.type == "header" else 2
                if level == 1:
                    return []
                flowables.append(render_heading(str(block.content), level, theme, _resolve_heading_style(design, level)))
                
            elif comp_type == "paragraph":
                flowables.append(render_paragraph(str(block.content), theme))
                
            elif comp_type == "list":
                if block.type == "list":
                    ordered = block.metadata.get("ordered", False)
                    flowables.extend(render_list(block.content, theme, ordered))
                    flowables.append(Spacer(1, 6))
                else:
                    flowables.append(render_paragraph(str(block.content), theme))
                    
            elif comp_type == "table":
                if block.type == "table":
                    flowables.append(render_table(block.content, theme, width, getattr(design, "table_style", None)))
                    flowables.append(Spacer(1, 10))
                else:
                    flowables.append(render_paragraph(str(block.content), theme))

            elif comp_type == "kpi_cards":
                if block.type == "table":
                    kpi_dict = {}
                    for row in block.content[1:]:
                        if len(row) >= 2:
                            kpi_dict[row[0]] = row[1]
                    if kpi_dict:
                        flowables.append(render_kpi_cards(kpi_dict, theme, width, getattr(design, "kpi_style", None)))
                        flowables.append(Spacer(1, 10))
                else:
                    flowables.append(render_paragraph(str(block.content), theme))

            elif comp_type == "key_value_summary":
                props = node.properties or {}
                summary_spec = props.get("key_value_summary") if isinstance(props, dict) else None

                summary_items = []
                section_title = "Summary"
                section_subtitle = None

                if isinstance(summary_spec, dict):
                    section_title = summary_spec.get("title") or props.get("section_title") or props.get("title") or "Summary"
                    section_subtitle = summary_spec.get("subtitle") or props.get("subtitle")
                    items = summary_spec.get("items") or []
                    for item in items:
                        if isinstance(item, dict):
                            summary_items.append((str(item.get("label", "")), str(item.get("value", ""))))
                        elif isinstance(item, (list, tuple)) and len(item) >= 2:
                            summary_items.append((str(item[0]), str(item[1])))

                if summary_items:
                    flowables.append(
                        render_key_value_summary(
                            summary_items,
                            theme,
                            width,
                            title=str(section_title),
                            subtitle=str(section_subtitle) if section_subtitle else None,
                        )
                    )
                    flowables.append(Spacer(1, 10))
                else:
                    flowables.append(render_paragraph(str(block.content), theme))
                    
            elif comp_type == "image":
                img_path = str(block.content).strip()
                caption = block.metadata.get("caption") or block.metadata.get("alt", "")
                
                # Default width is 100% of the available container width. 
                # LLM can adjust this to 0.5 (50%), 0.8 (80%) etc.
                width_ratio = node.properties.get("width_ratio", 1.0) if node.properties else 1.0
                adjusted_width = width * width_ratio
                
                flowables.extend(render_image(img_path, caption, theme, adjusted_width, getattr(design, "image_style", None)))

            elif comp_type == "callout":
                flowables.append(render_callout(str(block.content), theme, width, getattr(design, "callout_style", None)))
                flowables.append(Spacer(1, 8))
                
        return flowables

    # Render each section directly from the Layout Tree
    for section_node in layout_spec.sections:
        if section_node.type == "section":
            story.extend(compile_node(section_node, page_width))
            
    # 4. Generate final document
    def first_page(c, doc_obj):
        _draw_design_decoration(c, design)

    def later_pages(c, doc_obj):
        _draw_design_decoration(c, design)

    def _canvas_maker(*args, **kwargs):
        class _NumberedCanvas(NumberedCanvas):
            pass

        _NumberedCanvas.footer_text = footer_text
        return _NumberedCanvas(*args, **kwargs)

    doc.build(story, canvasmaker=_canvas_maker, onFirstPage=first_page, onLaterPages=later_pages)
    return output_path
