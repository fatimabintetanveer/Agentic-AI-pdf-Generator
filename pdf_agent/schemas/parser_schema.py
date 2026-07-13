from typing import List, Literal, Union, Optional
from pydantic import BaseModel, Field

# ==========================================
# Strict JSON Schemas for LLM Output
# ==========================================

class HeaderBlockSchema(BaseModel):
    type: Literal["header"]
    content: str = Field(description="The text content of the header.")
    level: int = Field(description="The header level (1 for main title, 2 for section, 3 for subsection, etc.)")

class ParagraphBlockSchema(BaseModel):
    type: Literal["paragraph"]
    content: str = Field(description="The text content of the paragraph.")

class ListBlockSchema(BaseModel):
    type: Literal["list"]
    content: List[str] = Field(description="An array of list items as strings.")
    ordered: bool = Field(default=False, description="True if it's a numbered list, False if bulleted.")

class TableBlockSchema(BaseModel):
    type: Literal["table"]
    content: List[List[str]] = Field(description="A 2D array of strings representing the table rows and cells.")

class QuoteBlockSchema(BaseModel):
    type: Literal["quote"]
    content: str = Field(description="The text content of the quote or callout.")

class ImageBlockSchema(BaseModel):
    type: Literal["image"]
    content: str = Field(description="The file path or URL of the image.")
    alt: str = Field(default="", description="The alt text from the markdown image syntax ![alt](path).")
    caption: Optional[str] = Field(default=None, description="A caption for the image. Use the alt text if present. If the very next paragraph after the image tag reads like a figure caption (e.g. starts with 'Figure', 'Fig.', 'Source:', 'Note:'), absorb it here and do NOT create a separate paragraph block for it.")

# The LLM MUST select exactly one of these types for every piece of content
DocBlockSchema = Union[
    HeaderBlockSchema, 
    ParagraphBlockSchema, 
    ListBlockSchema, 
    TableBlockSchema, 
    QuoteBlockSchema, 
    ImageBlockSchema
]

class CoverMetadataItemSchema(BaseModel):
    key: str = Field(description="The metadata key inferred from the markdown, such as date, market, prepared_for, author, or department.")
    value: str = Field(description="The metadata value inferred from the markdown.")

class CoverPageSchema(BaseModel):
    title: Optional[str] = Field(
        ...,
        description="The main title to show on the cover page. Use the document's strongest top-level title if present, otherwise infer a title only when clearly supported by the markdown."
    )
    subtitle: Optional[str] = Field(
        ...,
        description="Optional subtitle or tagline under the cover title. Leave empty unless clearly supported by the markdown."
    )
    metadata: List[CoverMetadataItemSchema] = Field(
        ...,
        description="Flexible cover-page metadata as key-value entries. Only include items that are clearly supported by the markdown."
    )

class FooterSchema(BaseModel):
    text: Optional[str] = Field(
        ...,
        description="Optional footer text for the document. Leave empty unless the markdown clearly supports a footer."
    )

class ParsedDocumentSchema(BaseModel):
    title: Optional[str] = Field(
        ...,
        description="The main title of the document. Keep aligned with cover.title when present."
    )
    cover: CoverPageSchema = Field(
        ...,
        description="Structured cover page content inferred from the markdown."
    )
    footer: Optional[FooterSchema] = Field(
        ...,
        description="Optional footer text inferred from the markdown."
    )
    blocks: List[DocBlockSchema] = Field(
        ...,
        description="The sequential array of content blocks."
    )
