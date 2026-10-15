"""
doctools.contract.docx.fidelity_report
Machine-readable fidelity report contract for DOCX visual & structural verification.
"""

from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

from doctools.contract.envelope import Issue


class FidelityValidationSummary(BaseModel):
    """Status across independent verification channels."""
    model_config = ConfigDict(extra="forbid")

    structural: Literal["passed", "failed"] = "passed"
    geometry: Literal["passed", "failed", "not_verified"] = "not_verified"
    xml_font_intent: Literal["passed", "failed", "not_specified"] = "not_specified"
    rendered_font_evidence: Literal["passed", "failed", "not_verified"] = "not_verified"
    glyph_coverage: Literal["passed", "failed", "not_verified"] = "not_verified"
    preservation: Literal["passed", "failed", "not_verified"] = "not_verified"


class FidelityMetrics(BaseModel):
    """Quantitative measurement metrics with strict tolerance tracking."""
    model_config = ConfigDict(extra="forbid")

    table_topology_mismatches: int = 0
    grid_width_mismatches: int = 0
    unmatched_edges_count: int = 0
    max_edge_error_mm: Optional[float] = None
    unexpected_blank_pages: int = 0
    page_count_delta: Optional[int] = None


class FidelityReport(BaseModel):
    """
    Standard machine-readable audit report emitted after document generation,
    patching, or conformance validation.
    """
    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0"
    document_mode: Literal["template_driven", "source_reconstruction", "new_document"] = "new_document"
    source_hash: Optional[str] = None
    template_hash: Optional[str] = None
    engine_version: str = "doctools-1.4"
    renderer_profile: Optional[Literal["word_visual", "libreoffice_visual", "structural_ci"]] = "structural_ci"
    validation: FidelityValidationSummary = Field(default_factory=FidelityValidationSummary)
    metrics: FidelityMetrics = Field(default_factory=FidelityMetrics)
    issues: List[Issue] = Field(default_factory=list)
    unsupported_regions: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
