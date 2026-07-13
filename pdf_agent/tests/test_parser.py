import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv

load_dotenv()

from pdf_agent.tools.markdown_parser import parse_markdown_file


ROOT = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
INPUT_MD = ROOT / "pdf_agent" / "sample_inputs" / "aqeel-test.md"


def main():
    if not INPUT_MD.exists():
        print(f"Error: Sample report markdown not found at {INPUT_MD}")
        return

    print("--- 1. Parsing Markdown File ---")
    document = parse_markdown_file(str(INPUT_MD))
    print(f"Document Title: '{document.title}'")
    print(f"Document Cover: {document.cover}")
    print(f"Document Footer: {document.footer}")
    print(f"Document Metadata: {document.metadata}")
    print(f"Number of content blocks: {len(document.blocks)}")

    print("\n--- Parsed Document Blocks (First 15 shown for brevity) ---")
    for idx, block in enumerate(document.blocks[:]):
        content_preview = str(block.content).replace("\n", " ")
        if len(content_preview) > 80:
            content_preview = content_preview[:77] + "..."
        print(f"Block {idx:02d}: Type={block.type:<10} Metadata={block.metadata} Content={content_preview}")
    if len(document.blocks) > 15:
        print(f"... and {len(document.blocks) - 15} more blocks.")


if __name__ == "__main__":
    main()
