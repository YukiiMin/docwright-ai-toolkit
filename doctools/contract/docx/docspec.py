"""
doctools.contract.docx.docspec
Pydantic contracts for Path B DocSpec-driven document generation.
Allows AI agents and workflows to generate documents from scratch via structured JSON.
"""

from __future__ import annotations
from typing import Annotated, Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class RunSpec(BaseModel):
    """Specification for an inline run of text."""
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="String character content")
    bold: Optional[bool] = Field(default=None, description="Bold styling flag")
    italic: Optional[bool] = Field(default=None, description="Italic styling flag")
    underline: Optional[bool] = Field(default=None, description="Underline styling flag")
    color: Optional[str] = Field(default=None, description="HEX color code (e.g. 'FF0000')")
    font_name: Optional[str] = Field(default=None, description="Font family name (e.g. 'Times New Roman')")
    size_pt: Optional[float] = Field(default=None, gt=0, description="Font size in points (e.g. 11.0)")


class ParagraphBlock(BaseModel):
    """A standard body paragraph with text or rich runs."""
    model_config = ConfigDict(extra="forbid")

    type: Literal["paragraph"] = "paragraph"
    text: Optional[str] = Field(default=None, description="Plain text string")
    runs: Optional[List[RunSpec]] = Field(default=None, description="List of detailed styled runs")
    style: Optional[str] = Field(default=None, description="Style name in base template")
    align: Optional[Literal["left", "center", "right", "justify"]] = Field(
        default=None, description="Paragraph horizontal alignment"
    )
    space_before_pt: Optional[float] = Field(
        default=None, ge=0.0, description="Space before paragraph in points"
    )
    space_after_pt: Optional[float] = Field(
        default=None, ge=0.0, description="Space after paragraph in points"
    )
    line_spacing: Optional[float] = Field(
        default=None, ge=0.0, description="Line spacing multiple (e.g. 1.08)"
    )
    keep_with_next: Optional[bool] = Field(
        default=None, description="Keep with next paragraph (w:keepNext)"
    )


class HeadingBlock(BaseModel):
    """A heading element from level 1 to 6."""
    model_config = ConfigDict(extra="forbid")

    type: Literal["heading"] = "heading"
    text: str = Field(..., min_length=1, description="Heading title text")
    level: int = Field(default=1, ge=1, le=6, description="Heading hierarchy level (1..6)")
    style: Optional[str] = Field(default=None, description="Custom heading style name")


class ListBlock(BaseModel):
    """An unordered or ordered list."""
    model_config = ConfigDict(extra="forbid")

    type: Literal["list"] = "list"
    items: List[str] = Field(..., min_length=1, description="List of item strings")
    ordered: bool = Field(default=False, description="True for ordered/numbered list")
    style: Optional[str] = Field(default=None, description="Custom list style name")


class TableCellSpec(BaseModel):
    """Specification for a rich table cell supporting styled runs, paragraphs, and merging."""
    model_config = ConfigDict(extra="forbid")

    text: Optional[str] = Field(default=None, description="Plain text content")
    runs: Optional[List[RunSpec]] = Field(default=None, description="List of styled runs")
    paragraphs: Optional[List[ParagraphBlock]] = Field(default=None, description="List of paragraphs inside cell")
    col_span: Optional[int] = Field(default=1, ge=1, description="Grid span (number of columns to merge)")
    row_span: Optional[int] = Field(default=1, ge=1, description="Vertical span (number of rows to merge via w:vMerge)")
    align: Optional[Literal["left", "center", "right", "justify"]] = Field(
        default=None, description="Default horizontal alignment for cell paragraphs"
    )
    bg_color: Optional[str] = Field(default=None, description="Cell background fill HEX color (e.g. 'F2F2F2')")
    valign: Optional[Literal["top", "center", "bottom"]] = Field(default=None, description="Vertical alignment")
    cell_padding_cm: Optional[Union[float, Dict[str, float]]] = Field(default=None, description="Inner cell margins/padding in cm")
    borders: Optional[Dict[str, Any]] = Field(default=None, description="Granular cell borders (e.g. {'bottom': 'double'})")
    keep_with_next: Optional[bool] = Field(default=None, description="Lock keep_with_next on cell paragraphs (w:keepNext)")


DocumentMode = Literal["template_driven", "source_reconstruction", "new_document"]


class TableBlock(BaseModel):
    """A data table with optional headers and cells."""
    model_config = ConfigDict(extra="forbid")

    type: Literal["table"] = "table"
    headers: Optional[List[str]] = Field(default=None, description="Column header label strings")
    rows: List[List[Union[str, TableCellSpec]]] = Field(..., description="Matrix of row and cell values or specs")
    style: Optional[str] = Field(default="Table Grid", description="Table style name")
    table_width_mode: Literal["template_native", "fill_available", "proportional", "measured"] = Field(
        default="fill_available", description="Table width determination mode"
    )
    col_widths: Optional[List[float]] = Field(default=None, description="Column widths in cm")
    col_widths_ratio: Optional[List[float]] = Field(
        default=None, description="Normalized column width ratios (e.g. [0.2, 0.5, 0.3])"
    )
    row_heights: Optional[List[float]] = Field(default=None, description="Row heights in cm (w:hRule='atLeast')")
    header_row_count: int = Field(
        default=0, ge=0, description="Number of header rows to repeat on subsequent pages with w:tblHeader"
    )
    cant_split_policy: Literal["allow", "prevent", "inherit"] = Field(
        default="prevent", description="Row split prevention policy"
    )
    alignment: Optional[Literal["left", "center", "right"]] = Field(
        default=None, description="Table alignment"
    )
    cell_padding_cm: Optional[Union[float, Dict[str, float]]] = Field(default=None, description="Default cell padding in cm")
    borders: Optional[Dict[str, Any]] = Field(default=None, description="Default borders for table cells")


class ImageBlock(BaseModel):
    """An image element reference."""
    model_config = ConfigDict(extra="forbid")

    type: Literal["image"] = "image"
    source: str = Field(..., min_length=1, description="File path, FileRef URI, or base64")
    caption: Optional[str] = Field(default=None, description="Image caption text")
    width_cm: Optional[float] = Field(default=None, gt=0, description="Image width in cm (dynamic geometry)")


class CalloutBlock(BaseModel):
    """A highlighted callout box for notes, warnings, or tips."""
    model_config = ConfigDict(extra="forbid")

    type: Literal["callout"] = "callout"
    text: str = Field(..., min_length=1, description="Callout body text")
    title: Optional[str] = Field(default=None, description="Callout title text")
    kind: Literal["info", "warning", "tip", "note"] = Field(default="info", description="Callout style kind")


class PageBreakBlock(BaseModel):
    """Explicit page break."""
    model_config = ConfigDict(extra="forbid")

    type: Literal["page_break"] = "page_break"


DocBlock = Annotated[
    Union[
        ParagraphBlock,
        HeadingBlock,
        ListBlock,
        TableBlock,
        ImageBlock,
        CalloutBlock,
        PageBreakBlock,
    ],
    Field(discriminator="type"),
]


class PageSetupSpec(BaseModel):
    """Page geometry and margins."""
    model_config = ConfigDict(extra="forbid")

    orientation: Literal["portrait", "landscape"] = Field(default="portrait", description="Page orientation")
    margin_top_cm: Optional[float] = Field(default=2.54, ge=0.5, le=10.0)
    margin_bottom_cm: Optional[float] = Field(default=2.54, ge=0.5, le=10.0)
    margin_left_cm: Optional[float] = Field(default=2.54, ge=0.5, le=10.0)
    margin_right_cm: Optional[float] = Field(default=2.54, ge=0.5, le=10.0)
    page_width_cm: Optional[float] = Field(default=None, gt=0, le=100.0, description="Page width in cm")
    page_height_cm: Optional[float] = Field(default=None, gt=0, le=100.0, description="Page height in cm")


class DocSpec(BaseModel):
    """
    Root specification for Path B document generation.
    Deterministic JSON description of document blocks, theme, and layout.
    """
    model_config = ConfigDict(extra="forbid")

    docspec_version: str = Field(default="1.1", description="DocSpec schema version")
    document_mode: DocumentMode = Field(default="new_document", description="Document engineering mode")
    title: Optional[str] = Field(default=None, description="Document title")
    base_template: Optional[str] = Field(default=None, description="Registered template ID or template path")
    default_font: Optional[str] = Field(default=None, description="Default document font family (None = inherit template)")
    default_font_size_pt: Optional[float] = Field(default=None, gt=0, description="Default document font size in points")
    page_setup: Optional[PageSetupSpec] = Field(default=None, description="Page setup configuration")
    blocks: List[DocBlock] = Field(default_factory=list, description="Ordered document content blocks")
