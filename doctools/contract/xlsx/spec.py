"""
doctools.contract.xlsx.spec — Spreadsheet Specification Contract (XlsxSpec Schema).
Complies with Path B (Spec Builder), FR-08, FR-15 of Foundation Plan v1.1:
- Declares XlsxSpec JSON schema allowing AI to construct workbooks from scratch.
- Supports cell specifications (CellSpec), tables (TableSpec), styling (StyleSpec), and charts (ChartSpec).
- Generates native openpyxl DrawingML charts without requiring reference templates.
"""

from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class StyleSpec(BaseModel):
    """Visual style specification for an individual cell."""
    model_config = ConfigDict(extra="ignore")

    font_name: Optional[str] = "Arial"
    font_size: Optional[float] = 11.0
    bold: Optional[bool] = False
    italic: Optional[bool] = False
    font_color: Optional[str] = None  # RGB Hex, e.g. "000000"
    fill_color: Optional[str] = None  # RGB Hex, e.g. "FFFF00"
    border_style: Optional[str] = None  # "thin", "medium", "double"
    border_color: Optional[str] = "000000"
    alignment_h: Optional[Literal["left", "center", "right", "justify"]] = None
    alignment_v: Optional[Literal["top", "center", "bottom"]] = "center"
    number_format: Optional[str] = None  # "@", "#,##0", "0.00%"


class CellSpec(BaseModel):
    """Specification for an individual spreadsheet cell."""
    model_config = ConfigDict(extra="ignore")

    coordinate: str = Field(..., description="Cell coordinate (e.g. 'A1')")
    value: Any = Field(default=None, description="Cell value")
    is_formula: bool = Field(default=False, description="Flag indicating value is a formula starting with '='")
    style: Optional[StyleSpec] = None


class TableSpec(BaseModel):
    """Specification for tabular block structures."""
    model_config = ConfigDict(extra="ignore")

    start_coordinate: str = Field(default="A1", description="Top-left anchor cell of table")
    headers: List[str] = Field(default_factory=list, description="Column header titles")
    rows: List[List[Any]] = Field(default_factory=list, description="Tabular data rows")
    id_columns: List[int] = Field(default_factory=list, description="Column indices forced to text format '@'")
    header_style: Optional[StyleSpec] = None
    row_style: Optional[StyleSpec] = None


class ChartSpec(BaseModel):
    """Native DrawingML chart specification."""
    model_config = ConfigDict(extra="ignore")

    chart_type: Literal["bar", "col", "line", "pie", "area", "doughnut"] = Field(
        ..., description="Chart type"
    )
    title: Optional[str] = None
    data_min_col: int
    data_min_row: int
    data_max_col: int
    data_max_row: int
    titles_from_data: bool = True
    categories_min_col: Optional[int] = None
    categories_min_row: Optional[int] = None
    categories_max_col: Optional[int] = None
    categories_max_row: Optional[int] = None
    anchor: str = Field(default="E2", description="Top-left anchor cell for chart placement")
    width_cm: float = 15.0
    height_cm: float = 8.0


class SheetSpec(BaseModel):
    """Worksheet specification within workbook."""
    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., description="Worksheet name")
    cells: List[CellSpec] = Field(default_factory=list, description="Individual cell specifications")
    tables: List[TableSpec] = Field(default_factory=list, description="Tabular block specifications")
    charts: List[ChartSpec] = Field(default_factory=list, description="DrawingML chart specifications")
    merged_ranges: List[str] = Field(default_factory=list, description="Merged ranges (e.g. ['A1:E1'])")
    column_widths: Dict[str, float] = Field(default_factory=dict, description="Column widths (e.g. {'A': 15.0})")
    freeze_panes: Optional[str] = Field(default=None, description="Freeze panes anchor cell (e.g. 'A3')")


class XlsxSpec(BaseModel):
    """Complete workbook specification contract (Path B XlsxSpec)."""
    model_config = ConfigDict(extra="ignore")

    title: Optional[str] = None
    sheets: List[SheetSpec] = Field(default_factory=list, description="List of worksheet specifications")
    output_filename_hint: Optional[str] = "generated_workbook.xlsx"
    metadata: Dict[str, Any] = Field(default_factory=dict)
