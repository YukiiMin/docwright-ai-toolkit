"""
doctools.contract.xlsx.preflight
Pydantic contracts for XLSX Preflight Scanner and Package Inventory (FR-01, FR-02).
Categorizes workbook components and selects the appropriate Fidelity Tier (T1..T4).
"""

from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

FidelityTier = Literal["T1", "T2", "T3", "T4"]


class SheetInventory(BaseModel):
    """Structural inventory of an individual worksheet in the workbook."""
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Worksheet name")
    visible_state: Literal["visible", "hidden", "veryHidden"] = Field(
        default="visible", description="Visibility state of worksheet"
    )
    max_row: int = Field(default=0, ge=0, description="Highest row index containing data")
    max_column: int = Field(default=0, ge=0, description="Highest column index containing data")
    formulas_count: int = Field(default=0, ge=0, description="Count of formula cells")
    merges_count: int = Field(default=0, ge=0, description="Count of merged cell ranges")
    has_autofilter: bool = Field(default=False, description="Whether AutoFilter is enabled")
    conditional_formats_count: int = Field(default=0, ge=0, description="Count of conditional formatting rules")
    data_validations_count: int = Field(default=0, ge=0, description="Count of data validation rules")


class PackageInventory(BaseModel):
    """
    Comprehensive package inventory mapping OpenXML parts and risk features.
    Provides ground truth (D-16) for fidelity preservation and quality gates.
    """
    model_config = ConfigDict(extra="forbid")

    file_name: str = Field(..., description="Spreadsheet file name")
    sheets: List[SheetInventory] = Field(default_factory=list, description="List of worksheet inventories")
    total_formulas: int = Field(default=0, ge=0, description="Total formulas across workbook")
    total_merges: int = Field(default=0, ge=0, description="Total merged ranges across workbook")
    has_drawingml: bool = Field(default=False, description="Contains DrawingML part (images, logos, shapes)")
    has_images: bool = Field(default=False, description="Contains image files in xl/media")
    has_charts: bool = Field(default=False, description="Contains chart parts in xl/charts")
    has_pivot_tables: bool = Field(default=False, description="Contains Pivot Tables")
    has_vba_macros: bool = Field(default=False, description="Contains VBA macro xl/vbaProject.bin")
    has_external_links: bool = Field(default=False, description="Contains external workbook links")
    has_slicers: bool = Field(default=False, description="Contains Slicers or Timelines")
    defined_names_count: int = Field(default=0, ge=0, description="Count of Defined Names in workbook")
    fidelity_tier: FidelityTier = Field(
        default="T1",
        description="Assigned Fidelity Tier: T1 (Pure openpyxl), T2 (Preserve XML parts), T3 (Warning), T4 (Macro rejected)"
    )
