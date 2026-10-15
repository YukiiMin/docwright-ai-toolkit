"""
doctools.api — Public AI-Native Document Engineering SDK Facade.
Provides official Python SDK interface for AI agents and human developers.
Complies with < 300 lines/file limit and Document ID: SPEC-XLSX-FAITHFUL-MODEL-002 v2.1.
"""

from __future__ import annotations

from doctools.contract.xlsx.model import (
    CellModel,
    ColumnDimensionModel,
    HyperlinkModel,
    ReaderFidelity,
    RowDimensionModel,
    SheetModel,
    StyleModel,
    WorkbookModel,
)
from doctools.core.xlsx.export.jsonl_streamer import (
    export_workbook_to_jsonl,
    query_jsonl_stream,
)
from doctools.core.xlsx.model.cache import ModelCache, get_default_model_cache
from doctools.core.xlsx.model.helpers import (
    get_key_values_by_labels,
    read_table,
    resolve_sheet_name,
)
from doctools.core.xlsx.model.loader import load_workbook_model
from doctools.core.xlsx.model.raw_access import open_raw_readonly
from doctools.core.xlsx.profiles import BaseProfile, UnitTestMatrixProfile
from doctools.core.xlsx.profiles.classifier import (
    ClassificationResult,
    LayoutArchetype,
    LayoutClassifier,
)
from doctools.core.xlsx.profiles.scaffolder import ProfileScaffolder
from doctools.gates.xlsx.fast_verifier import ColumnHashReport, FastColumnHashVerifier
from doctools.core.common.json_compactor import compact_json, compact_json_file
from doctools.operations.common.compact_ops import common_compact_json
from doctools.core.xlsx.extraction import MediaExtractor, SemanticExtractor, TopologyMapper
from doctools.operations.xlsx import (
    xlsx_semantic_extract,
    xlsx_detect_tables,
    xlsx_mutate_block,
    xlsx_batch_interact,
    xlsx_bulk_ingest,
)
from doctools.core.xlsx.mutate import (
    TableIsland,
    TableIslandDetector,
    BlockMutator,
    BatchInteractionManager,
    BulkIngestionEngine,
)

__version__ = "2.0.0"


def get_profile(name: str) -> BaseProfile:
    """Retrieve an instantiated profile by registered name."""
    if name == "unit_test_matrix":
        return UnitTestMatrixProfile()
    raise ValueError(f"Unknown profile: {name}")


__all__ = [
    # L1 Faithful Model
    "WorkbookModel",
    "ReaderFidelity",
    "SheetModel",
    "CellModel",
    "StyleModel",
    "HyperlinkModel",
    "ColumnDimensionModel",
    "RowDimensionModel",
    "load_workbook_model",
    # L2 General Helpers
    "read_table",
    "get_key_values_by_labels",
    "resolve_sheet_name",
    # L3 Template Profiles
    "BaseProfile",
    "UnitTestMatrixProfile",
    "get_profile",
    # Controlled Raw Access Escape Hatch
    "open_raw_readonly",
    # Enterprise Model Cache
    "ModelCache",
    "get_default_model_cache",
    # Streaming & Large Dataset Export
    "export_workbook_to_jsonl",
    "query_jsonl_stream",
    # Fast Verification
    "FastColumnHashVerifier",
    "ColumnHashReport",
    # Layout Topology Classification & Scaffolding
    "LayoutClassifier",
    "LayoutArchetype",
    "ClassificationResult",
    "ProfileScaffolder",
    # Token-Efficient JSON Compaction
    "compact_json",
    "compact_json_file",
    "common_compact_json",
    # Enterprise Semantic Extraction & Topology
    "MediaExtractor",
    "SemanticExtractor",
    "TopologyMapper",
    "xlsx_semantic_extract",
    # Enterprise 2D Table Island & Block Mutation Architecture
    "TableIsland",
    "TableIslandDetector",
    "xlsx_detect_tables",
    "BlockMutator",
    "xlsx_mutate_block",
    "BatchInteractionManager",
    "xlsx_batch_interact",
    "BulkIngestionEngine",
    "xlsx_bulk_ingest",
]
