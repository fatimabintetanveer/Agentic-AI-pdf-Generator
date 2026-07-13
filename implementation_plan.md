# Unified Design Planner Implementation

Based on your feedback, we are shifting from the "Separate Graphic Designer" architecture to a **Unified Design Planner**. 

Your rationale is completely correct: layout and graphic design are tightly coupled. A bold cover choice dictates a colored band, which influences margin widths, table styles, etc. A single, holistic LLM pass allows the AI to make cohesive decisions across both structure and aesthetics simultaneously, exactly like a human designer.

We will rename the current `Layout Planner` to the **`Design Planner`**.

## Proposed Architecture

```text
Markdown
      ↓
Markdown Parser (LLM)
      ↓
Parsed Document (Content only)
      ↓
Design Planner (LLM) 
      ├── Chooses structural layout (sections, columns, component types)
      └── Chooses visual styles (colors, fonts, decorations, variants)
      ↓
Design Specification (Structured JSON)
      ↓
ReportLab Renderer (Deterministic Execution)
      ↓
PDF
```

## Step-by-Step Implementation Plan

### Phase 1: Establish the Visual Style Catalog (Data Models & Schemas)

Before the LLM can compose styles, we must define the catalog of available primitives in our Python schemas.

1.  **Define Style Enums:** In `pdf_agent/models/style.py`, we will define strict `Enum` or `Literal` types for all the variants you listed:
    -   `CoverStyle` (Centered, Split layout, Hero image, etc.)
    -   `SectionHeaderStyle` (Underline, Colored strip, Ribbon, etc.)
    -   `TableStyleVariant` (Minimal, Zebra, Corporate, etc.)
    -   `CalloutStyleVariant` (Left border, Filled box, Quote, etc.)
    -   `DividerStyleVariant` (Thin line, Double line, Wave, etc.)
    -   `DecorationType` (Top band, Corner triangles, Geometric polygons, etc.)
2.  **Update the `DesignSpec` Schema:** In `pdf_agent/schemas/layout_schema.py` (which we will rename to `design_schema.py`), we will expand the Pydantic models so the LLM can output these specific style choices alongside the structural layout.

### Phase 2: Build the Component Style Renderers

We need to implement the visual logic in ReportLab for each of the new style variants. We will do this iteratively, testing each component as we go.

1.  **Page Decorations:** We've already started this in `pdf_agent/components/decorations.py`. We will integrate these parameterized canvas drawing functions into the main `pdf_generator.py` so they render behind the text based on the `DesignSpec`.
2.  **Cover Pages:** Build the different cover compositions in `pdf_agent/components/cover.py`.
3.  **Component Variants:** Update `elements.py`, `structures.py`, `callout.py`, etc., to conditionally render different ReportLab layouts depending on the chosen variant (e.g., if `table_style == "zebra"`, use alternating background colors).

### Phase 3: The Design Planner Agent

1.  **Rename and Refactor:** Rename `layout_planner.py` to `design_planner.py`.
2.  **Update the Prompt:** Overhaul `pdf_agent/prompt/layout_planner.md` (renamed to `design_planner.md`). 
    - Instruct the LLM to act as a holistic professional graphic designer.
    - Provide it with the catalog of available style primitives.
    - Give it rules for cohesive design (e.g., "If using a bold, dark theme, pair it with minimal table styles to prevent visual clutter").
3.  **Integrate:** Ensure the pipeline flows from Parser -> Design Planner -> PDF Generator.

## Open Questions

> [!IMPORTANT]
> - For Phase 2 (Building Component Style Renderers), which components would you like to start testing first? We have a lot of options (Cover Pages, Tables, Section Headers, Callouts). 
> - I suggest we start by integrating the Page Decorations we just built, followed immediately by Cover Page styles. Does that sound good?

## Verification
- We will write isolated test scripts (like `test_page_decorations.py`) for each new component style to ensure it looks beautiful in ReportLab before wiring it up to the LLM.
