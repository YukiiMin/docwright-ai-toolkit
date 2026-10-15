"""
doctools.contract.docx
Pydantic contracts and schemas for DOCX operations, templates, DocSpec, and Patch.
"""

from doctools.contract.docx.manifest import (
    LayoutPolicy,
    TemplateManifest,
    VariableDef,
)
from doctools.contract.docx.docspec import (
    CalloutBlock,
    DocBlock,
    DocSpec,
    DocumentMode,
    HeadingBlock,
    ImageBlock,
    ListBlock,
    PageBreakBlock,
    PageSetupSpec,
    ParagraphBlock,
    RunSpec,
    TableBlock,
    TableCellSpec,
)
from doctools.contract.docx.fidelity_report import (
    FidelityMetrics,
    FidelityReport,
    FidelityValidationSummary,
)
from doctools.contract.docx.patch import (
    PatchOp,
    PatchSpec,
)
from doctools.contract.docx.layout_spec import (
    AmbiguityState,
    BoundingBox,
    EvidenceOrigin,
    FieldProvenance,
    LayoutCellSpec,
    LayoutSpec,
    LayoutTableSpec,
    PageGeometrySpec,
    ResolutionStatus,
)

__all__ = [
    "LayoutPolicy",
    "TemplateManifest",
    "VariableDef",
    "CalloutBlock",
    "DocBlock",
    "DocSpec",
    "DocumentMode",
    "HeadingBlock",
    "ImageBlock",
    "ListBlock",
    "PageBreakBlock",
    "PageSetupSpec",
    "ParagraphBlock",
    "RunSpec",
    "TableBlock",
    "TableCellSpec",
    "FidelityMetrics",
    "FidelityReport",
    "FidelityValidationSummary",
    "PatchOp",
    "PatchSpec",
    "AmbiguityState",
    "BoundingBox",
    "EvidenceOrigin",
    "FieldProvenance",
    "LayoutCellSpec",
    "LayoutSpec",
    "LayoutTableSpec",
    "PageGeometrySpec",
    "ResolutionStatus",
]
