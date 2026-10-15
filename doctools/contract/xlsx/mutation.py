"""
doctools.contract.xlsx.mutation — Spreadsheet Mutation Specification Contract (MutationSpec).
Complies with FR-05, FR-06, FR-09, D-02, E1..E14 of Foundation Plan v1.1.
Declares MutationSpec JSON schema controlling data injection,
prototype row cloning, range policies, and locked zone protection.
"""

from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class CellUpdate(BaseModel):
    """Direct value update for an individual cell."""
    model_config = ConfigDict(extra="ignore")

    sheet: str
    coordinate: str
    value: Any
    is_formula: bool = False


class TableExpansion(BaseModel):
    """Specification for expanding table rows and cloning prototype styles."""
    model_config = ConfigDict(extra="ignore")

    sheet: str
    start_row: Optional[int] = Field(
        default=None, description="Starting row for data injection (defaults after header or prototype_row)"
    )
    prototype_row: Optional[int] = Field(
        default=None, description="Prototype row used to clone 100% of formatting tokens (E1..E14)"
    )
    consume_prototype: bool = Field(
        default=True, description="Consume prototype row: overwrites prototype row with first data record"
    )
    rows_data: List[Union[Dict[str, Any], List[Any]]] = Field(
        ..., description="List of records to insert into table"
    )
    columns_mapping: Optional[Dict[str, Union[str, int]]] = Field(
        default=None, description="Mapping from record field keys to Excel columns (e.g. {'test_id': 'A', 'desc': 'B'})"
    )
    id_columns: List[Union[str, int]] = Field(
        default_factory=list, description="Identifier columns forced to text format '@' to preserve leading zeros"
    )
    range_policy: Literal["table_aware", "excel_native", "shrink_safe"] = Field(
        default="table_aware", description="Summary formula range expansion policy"
    )
    border_policy: Literal["preserve_exact", "inherit_prototype"] = Field(
        default="preserve_exact", description="Table border policy: preserve_exact or inherit_prototype"
    )


class MutationSpec(BaseModel):
    """
    MutationSpec JSON controlling spreadsheet mutation under strict schema validation.
    Engine rejects arbitrary AI-generated code or ad-hoc XML modifications;
    executes strictly according to MutationSpec.
    """
    model_config = ConfigDict(extra="ignore")

    template_ref_or_id: str = Field(
        ..., description="Registered template ID or FileRef/URI of template workbook"
    )
    border_policy: Literal["preserve_exact", "inherit_prototype"] = Field(
        default="preserve_exact", description="Global border policy: preserve_exact or inherit_prototype"
    )
    expansions: List[TableExpansion] = Field(
        default_factory=list, description="List of tables to expand with row records"
    )
    cell_updates: List[CellUpdate] = Field(
        default_factory=list, description="Direct cell updates (must be outside locked_zones)"
    )
    locked_zones: List[str] = Field(
        default_factory=list, description="Forbidden overwrite zones (e.g. ['Statistics!C12:I19', '*!A1:T8'])"
    )
    output_filename_hint: Optional[str] = Field(
        default=None, description="Suggested output filename hint"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Associated business metadata"
    )
