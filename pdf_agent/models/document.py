from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DocBlock:
    """
    Represents an isolated content element extracted from the Markdown document.
    This separates document content from visual representation.
    """
    type: str  # Type identifier: 'header', 'paragraph', 'list', 'table', 'quote', 'image', 'kpis'
    content: Any  # Content payload (e.g., text string, grid lists, dicts)
    metadata: Dict[str, Any] = field(default_factory=dict)  # Stores context like list ordered/unordered, header level, image paths

@dataclass
class Document:
    """
    Stores the full parsed contents and high-level metadata of a document.
    """
    title: Optional[str] = None
    cover: Dict[str, Any] = field(default_factory=dict)
    footer: Optional[Dict[str, Any]] = None
    blocks: List[DocBlock] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)  # Document-wide variables (e.g., author, date, department)
