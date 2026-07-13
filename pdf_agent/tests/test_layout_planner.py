import os
import sys
import json
from dataclasses import asdict


# Auto-resolve and append the project root directory to Python's import search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv()

from pdf_agent.tools.markdown_parser import parse_markdown_file
from pdf_agent.tools.layout_planner import plan_layout
from pdf_agent.tools.pdf_generator import generate_pdf
from pdf_agent.themes import get_predefined_theme

def test_layout_planner():
    # 1. Setup sample document path
    input_md = "pdf_agent/sample_inputs/sample_report.md"
    if not os.path.exists(input_md):
        print(f"Error: Sample report markdown not found at {input_md}")
        return

    print("--- 1. Parsing Markdown File ---")
    document = parse_markdown_file(input_md)
    print(f"Document Title: '{document.title}'")
    print(f"Document Metadata: {document.metadata}")
    print(f"Number of content blocks: {len(document.blocks)}")
    
    print("\n--- Parsed Document Blocks (First 15 shown for brevity) ---")
    for idx, block in enumerate(document.blocks[:15]):
        content_preview = str(block.content).replace("\n", " ")
        if len(content_preview) > 80:
            content_preview = content_preview[:77] + "..."
        print(f"Block {idx:02d}: Type={block.type:<10} Metadata={block.metadata} Content={content_preview}")
    if len(document.blocks) > 15:
        print(f"... and {len(document.blocks) - 15} more blocks.")
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    print("\n--- 2. Invoking Layout Planner LLM (predefined theme only) ---")
    layout_spec = plan_layout(document)

    print("\n--- 3. Generated Layout Specification Output ---")
    spec_dict = asdict(layout_spec)
    print(json.dumps(spec_dict, indent=2))

    print("\n--- 5. Generating PDF ---")
    theme_names = ["cool_teal", "corporate_navy"]
    for theme_name in theme_names:
        themed_layout_spec = layout_spec
        themed_layout_spec.theme = get_predefined_theme(theme_name, font_style=layout_spec.theme.font_style)
        output_path = os.path.join(output_dir, f"test_layout_planner_output_{theme_name}.pdf")
        print(f"Rendering with theme: {theme_name}")
        generate_pdf(document, themed_layout_spec, output_path)
        print(f"PDF saved to: {output_path}")

if __name__ == "__main__":
    test_layout_planner()
