"""
doctools.contract.docx.layout_spec
Pydantic v2 schemas for raw layout measurement, field-level provenance,
and geometric layout representation (Phase 1.5 - DOCX-GAP-04).
"""

from __future__ import annotations
from enum import Enum
import math
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class EvidenceOrigin(str, Enum):
    """Origin of data in LayoutSpec (SSOT D-31)."""
    OBSERVED = "observed"      # Directly measured via computer vision or PDF vector
    INFERRED = "inferred"      # Interpreted via Multimodal Vision LLM or heuristic
    REQUESTED = "requested"    # Explicitly requested by user in prompt / spec


class ResolutionStatus(str, Enum):
    """Lifecycle resolution status of an individual data field (SSOT D-31)."""
    PENDING = "pending"        # Pending review / unverified
    ACCEPTED = "accepted"      # Verified and accepted for DocSpec emission
    REJECTED = "rejected"      # Rejected due to rule or boundary violation
    NEEDS_REVIEW = "needs_review"  # Ambiguous or low confidence, flagged for review


class AmbiguityState(str, Enum):
    """Geometric mesh ambiguity state (SSOT D-32)."""
    MEASURED = "measured"          # Clean closed rectangular grid with valid intersections
    AMBIGUOUS = "ambiguous"        # Broken lines, conflicting clusters, or multiple valid column cuts
    UNMEASURABLE = "unmeasurable"  # Borderless table, heavy warp, or insufficient line segments


class FieldProvenance(BaseModel):
    """
    Field-level provenance and audit metadata.
    Enforces Authority Matrix and prevents hallucinated styles or blind mutations (DG-12).
    """
    model_config = ConfigDict(extra="ignore")

    origin: EvidenceOrigin = Field(..., description="Source origin of the value")
    status: ResolutionStatus = Field(
        default=ResolutionStatus.PENDING,
        description="Lifecycle validation status",
    )
    source_ref: Optional[str] = Field(
        default=None,
        description="Referenced bounding box ID, token span ID, or prompt rule",
    )
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score [0.0, 1.0]",
    )


class BoundingBox(BaseModel):
    """Normalized bounding box coordinates in [0.0, 1.0] relative to page dimensions."""
    model_config = ConfigDict(extra="ignore")

    x_norm: float = Field(..., ge=0.0, le=1.0, description="Normalized X coordinate of top-left corner")
    y_norm: float = Field(..., ge=0.0, le=1.0, description="Normalized Y coordinate of top-left corner")
    w_norm: float = Field(..., ge=0.0, le=1.0, description="Normalized width")
    h_norm: float = Field(..., ge=0.0, le=1.0, description="Normalized height")

    @model_validator(mode="after")
    def validate_bounds(self) -> BoundingBox:
        if self.x_norm + self.w_norm > 1.0001:
            raise ValueError(f"x_norm ({self.x_norm}) + w_norm ({self.w_norm}) exceeds 1.0")
        if self.y_norm + self.h_norm > 1.0001:
            raise ValueError(f"y_norm ({self.y_norm}) + h_norm ({self.h_norm}) exceeds 1.0")
        return self

    def to_mm(self, page_width_mm: float, page_height_mm: float) -> Tuple[float, float, float, float]:
        """Convert normalized coordinates to absolute millimeters (x, y, w, h)."""
        return (
            round(self.x_norm * page_width_mm, 2),
            round(self.y_norm * page_height_mm, 2),
            round(self.w_norm * page_width_mm, 2),
            round(self.h_norm * page_height_mm, 2),
        )

    def to_pixels(self, dpi: int, page_width_mm: float, page_height_mm: float) -> Tuple[int, int, int, int]:
        """Convert normalized coordinates to integer pixel coordinates at target DPI."""
        mm_to_px = dpi / 25.4
        return (
            int(round(self.x_norm * page_width_mm * mm_to_px)),
            int(round(self.y_norm * page_height_mm * mm_to_px)),
            int(round(self.w_norm * page_width_mm * mm_to_px)),
            int(round(self.h_norm * page_height_mm * mm_to_px)),
        )


class LayoutCellSpec(BaseModel):
    """Specification of an individual table cell in a measured layout."""
    model_config = ConfigDict(extra="ignore")

    cell_id: Optional[str] = Field(default=None, description="Unique cell identifier (e.g. 'c0_0')")
    row_idx: int = Field(..., ge=0, description="0-indexed row position")
    col_idx: int = Field(..., ge=0, description="0-indexed column position")
    row_span: int = Field(default=1, ge=1, description="Vertical span (vMerge)")
    col_span: int = Field(default=1, ge=1, description="Horizontal span (gridSpan)")
    bbox: Optional[BoundingBox] = Field(default=None, description="Optional bounding box of the cell")
    text: Optional[str] = Field(default=None, description="Transcribed or extracted cell text")
    provenance: FieldProvenance = Field(..., description="Field-level provenance and confidence")


class LayoutTableSpec(BaseModel):
    """Specification of a detected table island on a document page."""
    model_config = ConfigDict(extra="ignore")

    table_id: str = Field(..., description="Unique table identifier (e.g. 'tbl_p0_0')")
    page_idx: int = Field(..., ge=0, description="0-indexed page number")
    bbox: BoundingBox = Field(..., description="Outer bounding box encompassing the entire table")
    column_ratios: List[float] = Field(
        default_factory=list,
        description="Relative column width ratios [r_1, ..., r_k] with sum ~= 1.0",
    )
    row_heights_ratio: List[float] = Field(
        default_factory=list,
        description="Relative row height ratios",
    )
    ambiguity: AmbiguityState = Field(
        default=AmbiguityState.MEASURED,
        description="Mesh ambiguity classification",
    )
    cells: List[LayoutCellSpec] = Field(default_factory=list, description="List of table cells")
    provenance: FieldProvenance = Field(..., description="Table-level measurement provenance")

    @field_validator("column_ratios")
    @classmethod
    def validate_ratios(cls, v: List[float]) -> List[float]:
        if not v:
            return v
        for r in v:
            if r <= 0.0:
                raise ValueError(f"Column ratio must be strictly positive, got {r}")
        total = sum(v)
        if not math.isclose(total, 1.0, abs_tol=0.05):
            raise ValueError(f"Sum of column ratios must approximate 1.0, got {total}")
        return v


class PageGeometrySpec(BaseModel):
    """Physical and digital page geometry specifications."""
    model_config = ConfigDict(extra="ignore")

    page_idx: int = Field(..., ge=0, description="0-indexed page index")
    dpi: int = Field(default=300, ge=72, le=1200, description="Rendering raster DPI")
    physical_width_mm: float = Field(default=210.0, gt=0.0, description="Physical page width in mm (default A4)")
    physical_height_mm: float = Field(default=297.0, gt=0.0, description="Physical page height in mm (default A4)")
    rotation: int = Field(default=0, description="Native page rotation (0, 90, 180, 270)")
    skew_angle_deg: float = Field(default=0.0, description="Estimated scan skew angle in degrees")
    crop_box: Optional[List[float]] = Field(default=None, description="PDF crop box [x0, y0, x1, y1]")
    calibration_status: str = Field(default="calibrated", description="Geometry calibration state")


class LayoutSpec(BaseModel):
    """
    Standard contract schema representing complete measured document layout.
    Serves as input to docx.compile_layout_spec (Phase 1.5 SSOT).
    """
    model_config = ConfigDict(extra="ignore")

    version: str = Field(default="1.0", description="LayoutSpec schema version")
    source_file: str = Field(..., description="Source PDF or image file path")
    pages: List[PageGeometrySpec] = Field(default_factory=list, description="Page geometry records")
    tables: List[LayoutTableSpec] = Field(default_factory=list, description="Detected table islands")
    review_required: bool = Field(default=False, description="Flag indicating human review is required")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary engine or job metadata")

    def get_table(self, table_id: str) -> Optional[LayoutTableSpec]:
        """Retrieve table by unique identifier."""
        for tbl in self.tables:
            if tbl.table_id == table_id:
                return tbl
        return None

    def get_page_geometry(self, page_idx: int) -> Optional[PageGeometrySpec]:
        """Retrieve page geometry for specified page index."""
        for pg in self.pages:
            if pg.page_idx == page_idx:
                return pg
        return None

    def has_unresolved_reviews(self) -> bool:
        """Check whether any table or cell carries a NEEDS_REVIEW status."""
        if self.review_required:
            return True
        for tbl in self.tables:
            if tbl.provenance.status == ResolutionStatus.NEEDS_REVIEW or tbl.ambiguity != AmbiguityState.MEASURED:
                return True
            for c in tbl.cells:
                if c.provenance.status == ResolutionStatus.NEEDS_REVIEW:
                    return True
        return False
