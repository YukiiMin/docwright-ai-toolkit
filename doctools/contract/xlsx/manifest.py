"""
doctools.contract.xlsx.manifest — Manifest and Profile Contract for XLSX Templates.
Specifies schema for template manifests in accordance with v1.1 standards.
Supports locked zones (locked_zones), reference sheet (reference_sheet),
semantic anchors, id_columns, calc_policy, and range_policy.
"""

from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class AnchorConfig(BaseModel):
    """Semantic anchor configuration for tables or headers."""
    model_config = ConfigDict(extra="ignore")

    kind: Literal["header", "data_start", "summary", "custom"] = "header"
    keyword: Optional[str] = None
    keywords: Optional[List[str]] = None
    match: Literal["exact", "contains", "regex"] = "exact"
    scope: Literal["first_table", "sheet", "all"] = "first_table"
    scan_rows: int = Field(default=150, ge=1, le=10000)
    or_formula: Optional[str] = None


class RequiredPackageConfig(BaseModel):
    """Preservation policy for OOXML package components."""
    model_config = ConfigDict(extra="ignore")

    images: Literal["preserve", "ignore", "forbid"] = "preserve"
    charts: Literal["preserve_relink", "preserve", "ignore"] = "preserve_relink"
    data_validations: Literal["preserve_shift", "ignore"] = "preserve_shift"
    conditional_formats: Literal["preserve_shift", "ignore"] = "preserve_shift"
    defined_names: Literal["preserve_shift", "ignore"] = "preserve_shift"


class CalcPolicyConfig(BaseModel):
    """Recalculation and caching policy."""
    model_config = ConfigDict(extra="ignore")

    recalc: Literal["oracle_verify", "headless", "none"] = "oracle_verify"
    cache: Literal["write", "skip"] = "write"
    calc_on_open: Literal["auto", "always", "never"] = "auto"


class XlsxTemplateManifest(BaseModel):
    """
    Manifest declaring rules, locked zones, and structural specifications of an XLSX Template.
    Complies with section 4.5 of Foundation Plan v1.1.
    """
    model_config = ConfigDict(extra="ignore")

    template_id: str = Field(..., min_length=1, description="Unique template identifier")
    version: int = Field(default=1, ge=1, description="Template version integer")
    description: Optional[str] = Field(default=None, description="Template purpose description")
    reference_sheet: str = Field(..., min_length=1, description="Ground truth reference sheet for formatting tokens")
    sibling_sheets: List[str] = Field(default_factory=list, description="Symmetrically structured sibling sheets (E5)")
    anchors: Dict[str, Union[AnchorConfig, str, Dict[str, Any]]] = Field(
        default_factory=dict, description="Semantic anchors mapping"
    )
    prototype_rows: Dict[str, int] = Field(
        default_factory=dict, description="Prototype rows used for cloning styling tokens per sheet"
    )
    locked_zones: List[str] = Field(
        default_factory=list, description="Forbidden overwrite zones (e.g. Statistics!C12:I19, *!A1:T8)"
    )
    id_columns: List[Union[str, int]] = Field(
        default_factory=list, description="Identifier columns forced to text format '@' (e.g. ['Test ID'])"
    )
    calc_policy: CalcPolicyConfig = Field(default_factory=CalcPolicyConfig)
    range_policy: Literal["table_aware", "excel_native", "shrink_safe"] = "table_aware"
    gates_profile: Optional[str] = Field(default="unit_test_matrix", description="Quality verification gate profile")
    required_package: RequiredPackageConfig = Field(default_factory=RequiredPackageConfig)
    placeholders: Dict[str, List[str]] = Field(
        default_factory=lambda: {"forbid_unreplaced": ["{{", "<...>"]},
        description="Unreplaced placeholder detection rules",
    )
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional business metadata")
