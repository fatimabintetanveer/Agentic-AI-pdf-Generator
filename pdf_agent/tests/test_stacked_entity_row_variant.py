import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate

from pdf_agent.components import render_stacked_entity_row
from pdf_agent.models import ThemeSpec


def test_stacked_entity_row_variant_renders_pdf():
    theme = ThemeSpec()
    width = A4[0] - 80

    data = [
        {
            "Retailer": "OTHAIM",
            "Active Brands": "GOODY, TREVA, COFIQUE",
            "worth": "12,115,392",
            "Monthly Value Sales": "12,115,392",
        },
        {
            "Retailer": "PANDA",
            "Active Brands": "GOODY, TREVA, COFIQUE, LIBBY'S",
            "worth": "9,896,884",
            "Monthly Value Sales": "9,896,884",
        },
        {
            "Retailer": "LULU",
            "Active Brands": "GOODY, TREVA, COFIQUE, LIBBY'S, TIM HORTONS",
            "worth": "2,336,393",
            "Monthly Value Sales": "2,336,393",
        },
    ]

    table = render_stacked_entity_row(
        data,
        theme,
        width,
        title_key="Retailer",
        value_key="Monthly Value Sales",
        detail_keys=["Active Brands", "worth"],
    )
    assert table is not None

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "stacked_entity_row_variant.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    doc.build([table])
    print(f"Stacked entity row variant PDF generated at: {pdf_path}")


def test_stacked_entity_row_variant_supports_table_row_format():
    theme = ThemeSpec()
    width = A4[0] - 80

    data = [
        ["Retailer", "Active Brands", "Monthly Value Sales"],
        ["OTHAIM", "GOODY, TREVA, COFIQUE", "12,115,392"],
        ["PANDA", "GOODY, TREVA, COFIQUE, LIBBY'S", "9,896,884"],
        ["CARREFOUR", "GOODY, TREVA, COFIQUE, LIBBY'S", "9,876,884"],
        ["HYPERSTAR", "GOODY, TREVA, COFIQUE, LIBBY'S", "9,876,880"],
        ["LULU", "GOODY, TREVA, COFIQUE, LIBBY'S, TIM HORTONS", "2,336,393"],
    ]

    table = render_stacked_entity_row(
        data,
        theme,
        width,
        title_key="Retailer",
        value_key="Monthly Value Sales",
        detail_keys=["Active Brands"],
    )
    assert table is not None

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "stacked_entity_row_table_row_format.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    doc.build([table])
    print(f"Stacked entity row table-row format PDF generated at: {pdf_path}")


def test_stacked_entity_row_variant_supports_value_in_second_column():
    theme = ThemeSpec()
    width = A4[0] - 80

    table = render_stacked_entity_row(
        [
            {
                "Retailer": "OTHAIM",
                "Monthly Value Sales": "12,115,392",
            },
            {
                "Retailer": "PANDA",
                "Monthly Value Sales": "9,896,884",
            },
        ],
        theme,
        width,
        title_key="Retailer",
        value_key="Monthly Value Sales",
    )

    assert table is not None

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "stacked_entity_row_value_in_second_column.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    doc.build([table])

    print(f"Stacked entity row second-column value PDF generated at: {pdf_path}")


if __name__ == "__main__":
    test_stacked_entity_row_variant_supports_table_row_format()

