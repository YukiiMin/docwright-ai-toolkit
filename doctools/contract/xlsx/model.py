"""
Faithful Lossless Intermediate Representation (L1) Contracts for XLSX Engine.
Document ID: SPEC-XLSX-FAITHFUL-MODEL-002 v2.1
"""

from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from doctools.contract.issues import Issue


class ReaderFidelity(str, Enum):
    """Fidelity tier for reading Excel workbooks."""
    FULL_DOM = "FULL_DOM"          # 100% L1 IR: styles, formulas, merged cells, dimensions (Two-Pass DOM)
    FAST_TABULAR = "FAST_TABULAR"  # Fast flat table extraction via python-calamine or tabular iterator
    METADATA_ONLY = "METADATA_ONLY"# Fast structure scan (sheet names, dimensions) without cell parsing


class StyleModel(BaseModel):
    """Deduplicated Style Palette."""
    model_config = ConfigDict(extra="ignore")

    style_id: str = Field(..., description="Unique style identity hash")
    font_name: Optional[str] = None
    font_size: Optional[float] = None
    bold: bool = False
    italic: bool = False
    underline: bool = False
    font_color_rgb: Optional[str] = None
    font_color_theme: Optional[int] = None
    fill_type: Optional[str] = None
    fill_fg_color_rgb: Optional[str] = None
    fill_fg_color_theme: Optional[int] = None
    border_top_style: Optional[str] = None
    border_top_color: Optional[str] = None
    border_bottom_style: Optional[str] = None
    border_bottom_color: Optional[str] = None
    border_left_style: Optional[str] = None
    border_left_color: Optional[str] = None
    border_right_style: Optional[str] = None
    border_right_color: Optional[str] = None
    horizontal_align: Optional[str] = None
    vertical_align: Optional[str] = None
    wrap_text: bool = False
    shrink_to_fit: bool = False
    text_rotation: int = 0
    number_format: str = "General"


class ColumnDimensionModel(BaseModel):
    """Column width and visibility dimensions."""
    model_config = ConfigDict(extra="ignore")

    col_letter: str
    width: Optional[float] = None
    hidden: bool = False
    best_fit: bool = False


class RowDimensionModel(BaseModel):
    """Row height and visibility dimensions."""
    model_config = ConfigDict(extra="ignore")

    row_index: int
    height: Optional[float] = None
    hidden: bool = False


class HyperlinkModel(BaseModel):
    """Hyperlink model (internal or external) from a source cell."""
    model_config = ConfigDict(extra="ignore")

    source_cell: str
    target: Optional[str] = None
    location: Optional[str] = None
    display: Optional[str] = None
    is_external: bool = False


class CellModel(BaseModel):
    """Cell model storing formula syntax and cached evaluation value."""
    model_config = ConfigDict(extra="ignore")

    coordinate: str
    row: int
    col: int
    data_type: str = "s"
    raw_value: Any = None
    formula_text: Optional[str] = None
    cached_value: Any = None
    style_id: Optional[str] = None
    is_merged: bool = False
    merge_top_left: Optional[str] = None
    is_hidden: bool = False
    comment: Optional[str] = None
    hyperlink: Optional[HyperlinkModel] = None


class SheetModel(BaseModel):
    """Worksheet model representing sparse cell structure and geometry."""
    model_config = ConfigDict(extra="ignore")

    name: str
    visible_state: str = "visible"
    max_row: int = 0
    max_column: int = 0
    cells: Dict[str, CellModel] = Field(default_factory=dict)
    merged_ranges: List[str] = Field(default_factory=list)
    hyperlinks: List[HyperlinkModel] = Field(default_factory=list)
    column_dimensions: Dict[str, ColumnDimensionModel] = Field(default_factory=dict)
    row_dimensions: Dict[int, RowDimensionModel] = Field(default_factory=dict)
    freeze_panes: Optional[str] = None
    show_grid_lines: bool = True
    print_area: Optional[List[str]] = None
    data_validations_count: int = 0
    conditional_formattings_count: int = 0
    has_charts: bool = False
    has_images: bool = False


class WorkbookModel(BaseModel):
    """Lossless Intermediate Representation (L1 IR) of an entire Workbook."""
    model_config = ConfigDict(extra="ignore")

    schema_version: str = "1.0"
    engine_version: str = "2.0.0"
    file_name: str
    source_sha256: str
    file_size_bytes: int
    date1904: bool = False
    reader_fidelity: ReaderFidelity = ReaderFidelity.FULL_DOM
    styles: Dict[str, StyleModel] = Field(default_factory=dict)
    sheets: Dict[str, SheetModel] = Field(default_factory=dict)
    defined_names: Dict[str, str] = Field(default_factory=dict)
    issues: List[Issue] = Field(default_factory=list)
