import os
import sys
import json
from collections import Counter

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv()

from pdf_agent.tools.markdown_parser import parse_markdown_file
from pdf_agent.tools.layout_planner import plan_layout


INPUT_MD = "pdf_agent/sample_inputs/aqeel-test.md"
OUTPUT_DIR = "output/variety_step_by_step"


def summarize_layout(spec):
    counts = Counter()
    section_count = 0

    def walk(node):
        nonlocal section_count
        counts[node.type] += 1
        if node.type == "section":
            section_count += 1
        for child in node.children:
            walk(child)
        for child in node.children_left:
            walk(child)
        for child in node.children_right:
            walk(child)

    for section in spec.sections:
        walk(section)

    return {
        "section_count": section_count,
        "node_types": dict(counts),
        "has_two_column": counts["two_column"] > 0,
        "has_kpi_cards": counts["kpi_cards"] > 0,
        "has_highlight_cards": counts["highlight_cards"] > 0,
        "has_callout": counts["callout"] > 0,
        "has_timeline": counts["timeline"] > 0,
    }


def test_variety_step_by_step():
    if not os.path.exists(INPUT_MD):
        raise FileNotFoundError(f"Sample markdown not found: {INPUT_MD}")

    document = parse_markdown_file(INPUT_MD)

    scenarios = [
        ("balanced", "corporate_navy"),
        ("more_visual_variety", "cool_teal"),
        ("more_visual_variety", "warm_amber"),
    ]

    results = []
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for creativity_level, theme_name in scenarios:
        spec = plan_layout(
            document,
            preferred_theme=theme_name,
            creativity_level=creativity_level,
        )
        summary = summarize_layout(spec)
        results.append({
            "theme": theme_name,
            "creativity_level": creativity_level,
            "summary": summary,
            "theme_name": spec.theme.name,
        })

        output_path = os.path.join(OUTPUT_DIR, f"{theme_name}_{creativity_level}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    print(json.dumps(results, indent=2))

    assert len(results) == 3
    assert any(item["summary"]["has_two_column"] for item in results)


if __name__ == "__main__":
    test_variety_step_by_step()
