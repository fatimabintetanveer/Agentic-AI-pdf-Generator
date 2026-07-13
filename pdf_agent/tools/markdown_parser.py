from typing import List, Literal, Union, Dict, Any, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from pdf_agent.models import Document, DocBlock

from pdf_agent.schemas.parser_schema import (
    ParsedDocumentSchema, 
    HeaderBlockSchema,
    ListBlockSchema,
    ImageBlockSchema
)

# ==========================================
# LLM Parser Implementation
# ==========================================

def parse_markdown(md_text: str) -> Document:
    """
    Passes raw markdown to GPT-4o and forces it to extract the content 
    into a strict JSON array of strongly-typed DocBlocks.
    """
    client = OpenAI()
    
    import os
    
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "prompt",
        "markdown_parser.md"
    )
    with open(os.path.normpath(prompt_path), "r", encoding="utf-8") as f:
        prompt_template = f.read()
        
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": md_text}
        ],
        response_format=ParsedDocumentSchema,
    )
    
    parsed_data: ParsedDocumentSchema = response.choices[0].message.parsed
    
    # Map the Pydantic schema back to our internal Domain models
    domain_blocks = []
    for block_schema in parsed_data.blocks:
        b_type = block_schema.type
        b_content = block_schema.content
        b_metadata = {}
        
        # Extract specific properties into metadata for the domain model
        if isinstance(block_schema, HeaderBlockSchema):
            b_metadata["level"] = block_schema.level
        elif isinstance(block_schema, ListBlockSchema):
            b_metadata["ordered"] = block_schema.ordered
        elif isinstance(block_schema, ImageBlockSchema):
            # Prefer explicit caption field; fall back to alt text
            caption = block_schema.caption or block_schema.alt or ""
            b_metadata["alt"] = block_schema.alt
            b_metadata["caption"] = caption
            
        domain_blocks.append(DocBlock(
            type=b_type,
            content=b_content,
            metadata=b_metadata
        ))
        
    # Convert the strict cover/footer schema into plain dicts for the domain model
    cover_dict = parsed_data.cover.model_dump(exclude_none=True) if getattr(parsed_data, "cover", None) else {}
    metadata_dict = {}
    if cover_dict:
        metadata_items = cover_dict.get("metadata", []) or []
        metadata_dict = {
            item.get("key"): item.get("value")
            for item in metadata_items
            if item.get("key") and item.get("value") is not None
        }
    footer_dict = parsed_data.footer.model_dump(exclude_none=True) if getattr(parsed_data, "footer", None) else None

    return Document(
        title=parsed_data.title or cover_dict.get("title"),
        cover=cover_dict,
        footer=footer_dict,
        metadata=metadata_dict,
        blocks=domain_blocks
    )

def parse_markdown_file(file_path: str) -> Document:
    """Reads a markdown file and parses its contents using the LLM parser."""
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    return parse_markdown(md_content)
