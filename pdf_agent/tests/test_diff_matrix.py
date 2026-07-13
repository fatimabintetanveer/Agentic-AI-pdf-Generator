import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from pdf_agent.components.diff_matrix import render_diff_matrix
from pdf_agent.models import ThemeSpec


def test_diff_matrix():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "diff_matrix_preview.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    theme = ThemeSpec(
        primary_color="#c75b12",
        secondary_color="#64748b",
        accent_color="#d97706",
        background_color="#fffaf3",
        table_header_bg="#f3e8d3",
        table_header_text="#7c2d12",
        table_row_even_bg="#fff8ee",
        table_row_odd_bg="#ffffff",
        table_grid_color="#e7d7bd",
    )

    story = [
        Paragraph("Presence / Absence Matrix", styles["Heading2"]),
        Spacer(1, 8),
        Paragraph(
            "Brand availability differs across retailers. The component should render a compact matrix with symbol-based cells.",
            styles["BodyText"],
        ),
        Spacer(1, 8),
        render_diff_matrix(
            row_labels=["GOODY", "TREVA", "LIBBY'S", "COFIQUE", "TIM HORTONS", "WELLO"],
            column_labels=["PANDA", "OTHAIM", "LULU", "CARREFOUR", "DANUBE", "TAMIMI"],
            cells=[
                ["present", "present", "present", "present", "present", "present"],
                ["present", "present", "present", "present", "present", "absent"],
                ["present", "present", "present", "present", "absent", "absent"],
                ["present", "present", "present", "present", "absent", "absent"],
                ["present", "present", "present", "absent", "absent", "absent"],
                ["present", "absent", "present", "absent", "absent", "absent"],
            ],
            theme=theme,
            width=A4[0] - 80,
            mode="presence_absence",
        ),
        Spacer(1, 18),
        Paragraph("Presence Evolution Matrix", styles["Heading2"]),
        Spacer(1, 8),
        Paragraph(
            "This version shows the same underlying change view with gains and losses rendered as arrows.",
            styles["BodyText"],
        ),
        Spacer(1, 8),
        render_diff_matrix(
            row_labels=["CARREFOUR", "LULU", "OTHAIM", "PANDA"],
            column_labels=["GOODY", "TREVA", "LIBBY'S", "COFIQUE", "TIM H.", "WELLO"],
            cells=[
                ["stable", "stable", "stable", "stable", "stable", "gain"],
                ["stable", "stable", "stable", "loss", "stable", "gain"],
                ["stable", "stable", "stable", "stable", "gain", "absent"],
                ["stable", "stable", "stable", "stable", "stable", "gain"],
            ],
            theme=theme,
            width=A4[0] - 80,
            mode="presence_evolution",
        ),
        Spacer(1, 18),
        Paragraph("Custom Diff Labels", styles["Heading2"]),
        Spacer(1, 8),
        Paragraph(
            "This case verifies the component can also accept a custom cell renderer for non-symbolic diff states.",
            styles["BodyText"],
        ),
        Spacer(1, 8),
        render_diff_matrix(
            row_labels=["Feature A", "Feature B", "Feature C"],
            column_labels=["Current", "Previous", "Status"],
            cells=[
                [{"state": "gain", "display": "added"}, {"state": "stable", "display": "same"}, {"state": "stable", "display": "up"}],
                [{"state": "loss", "display": "removed"}, {"state": "stable", "display": "same"}, {"state": "stable", "display": "down"}],
                [{"state": "stable", "display": "unchanged"}, {"state": "stable", "display": "same"}, {"state": "present", "display": "steady"}],
            ],
            theme=theme,
            width=A4[0] - 80,
            mode="status_diff",
        ),
    ]

    doc.build(story)
    print(f"Successfully generated: {pdf_path}")


if __name__ == "__main__":
    test_diff_matrix()
