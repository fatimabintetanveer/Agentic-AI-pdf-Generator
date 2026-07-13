from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle

from pdf_agent.models import ThemeSpec
from .elements.util import _tint_hex


def _light_card_background(theme: ThemeSpec) -> colors.Color:
    # Use a stronger light tint so the card background is visibly branded
    # while still staying soft enough for text-heavy layouts.
    return colors.HexColor(theme.table_row_even_bg or _tint_hex(theme.background_color, mix=0.82))


def _styles(theme: ThemeSpec):
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "StackedEntityTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12.0,
            leading=14.0,
            textColor=colors.HexColor(theme.primary_color),
        ),
        "metric": ParagraphStyle(
            "StackedEntityMetric",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13.0,
            leading=15.0,
            textColor=colors.HexColor(theme.accent_color),
        ),
        "body": ParagraphStyle(
            "StackedEntityBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12.5,
            textColor=colors.HexColor(theme.secondary_color),
        ),
        "label": ParagraphStyle(
            "StackedEntityLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=10.0,
            textColor=colors.HexColor(theme.secondary_color),
        ),
    }


def _rows_to_dicts(rows):
    if not rows or len(rows) < 2:
        return []

    headers = [str(cell).strip() for cell in rows[0]]
    data_rows = []
    for row in rows[1:]:
        if not isinstance(row, (list, tuple)):
            continue
        data_rows.append(
            {
                headers[i]: row[i]
                for i in range(min(len(headers), len(row)))
                if headers[i]
            }
        )
    return data_rows


def _count_data_rows(rows) -> int:
    if isinstance(rows, list) and rows and isinstance(rows[0], (list, tuple)):
        return max(0, len(rows) - 1)
    return len(rows) if isinstance(rows, list) else 0


def _is_compact_card(title: str, value: str, detail_keys: list[str], row: dict) -> bool:
    text_len = len(title.strip()) + len(value.strip())
    text_len += sum(len(str(row.get(key, ""))) for key in detail_keys)
    return text_len <= 90


def _build_card(theme: ThemeSpec, s, width: float, title: str, value_key: str, value: str, detail_keys: list[str], row: dict) -> Table:
    body_rows = [
        [Paragraph(str(key), s["label"]), Paragraph(str(row.get(key, "")), s["body"])]
        for key in detail_keys
    ]
    body_rows.append([Paragraph(value_key, s["label"]), Paragraph(value, s["metric"])])

    inner = Table(
        [[Paragraph(title, s["title"])]]
        + [[Table(body_rows, colWidths=[width * 0.28, width * 0.72])]],
        colWidths=[width],
    )
    inner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), _light_card_background(theme)),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor(theme.table_grid_color)),
                ("LINEBEFORE", (0, 0), (0, -1), 5, colors.HexColor(theme.accent_color)),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return inner


def render_stacked_entity_row(
    rows,
    theme: ThemeSpec,
    width: float,
    title_key: str,
    value_key: str,
    detail_keys: list[str] | None = None,
) -> Table:
    if not rows:
        return Table([[""]], colWidths=[width])

    if not title_key or not value_key:
        raise ValueError("render_stacked_entity_row requires title_key and value_key")

    # Support both the new table-style input:
    #   [[headers...], [row...], ...]
    # and the older dict-style input for backward compatibility.
    if isinstance(rows, list) and rows and isinstance(rows[0], (list, tuple)):
        rows = _rows_to_dicts(rows)

    detail_keys = detail_keys or []
    s = _styles(theme)
    cards = []
    data_row_count = _count_data_rows(rows)
    compact_mode = data_row_count >= 4
    card_width = width * 0.5 - 6 if compact_mode and width > 260 else width

    for row in rows:
        if not isinstance(row, dict):
            continue
        title = str(row.get(title_key, ""))
        value = str(row.get(value_key, ""))

        cards.append(
            _build_card(theme, s, card_width if card_width > 0 else width, title, value_key, value, detail_keys, row)
        )

    use_two_up = compact_mode and all(
        _is_compact_card(str(r.get(title_key, "")), str(r.get(value_key, "")), detail_keys, r)
        for r in rows
        if isinstance(r, dict)
    )

    if use_two_up:
        gap = 10
        pair_width = (width - gap) / 2
        rows_out = []
        for i in range(0, len(cards), 2):
            left = cards[i]
            right = cards[i + 1] if i + 1 < len(cards) else ""
            rows_out.append([left, right])

        wrapper = Table(rows_out, colWidths=[pair_width, pair_width], hAlign="LEFT")
        wrapper.setStyle(
            TableStyle(
                [
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("RIGHTPADDING", (0, 0), (0, -1), gap / 2),
                    ("LEFTPADDING", (1, 0), (1, -1), gap / 2),
                ]
            )
        )
        return wrapper

    wrapper = Table([[card] for card in cards], colWidths=[width])
    wrapper.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return wrapper
