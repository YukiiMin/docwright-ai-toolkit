"""
Issue & Diagnostics Data Contract — Standardized fault and warning diagnostics
for all engines (DOCX, XLSX, DIAGRAM, INFRA) and MCP client triage.
"""

from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class Severity(str, Enum):
    """Severity classification of an Issue."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Engine(str, Enum):
    """Engine identifier originating the Issue."""
    DOCX = "docx"
    XLSX = "xlsx"
    DIAGRAM = "diagram"
    INFRA = "infra"
    COMMON = "common"


class FixableBy(str, Enum):
    """Entity authorized and capable of resolving the Issue."""
    ENGINE = "engine"
    AI = "ai"
    HUMAN = "human"


class Location(BaseModel):
    """Physical coordinate or structural location in document / diagram."""
    model_config = ConfigDict(extra="forbid")

    sheet: Optional[str] = Field(default=None, description="Sheet name in Excel workbook")
    cell: Optional[str] = Field(default=None, description="Excel cell coordinate (e.g. 'B7', 'D14')")
    range: Optional[str] = Field(default=None, description="Excel cell range (e.g. 'B7:H34')")
    part: Optional[str] = Field(default=None, description="OpenXML Part path (e.g. 'word/document.xml')")
    element: Optional[str] = Field(default=None, description="XML element tag (e.g. 'w:tc', 'w:tbl', 'mxCell')")
    node_id: Optional[str] = Field(default=None, description="Node/Cell ID in Draw.io diagram")
    edge_id: Optional[str] = Field(default=None, description="Edge/Connector ID in Draw.io diagram")
    line: Optional[int] = Field(default=None, ge=1, description="1-indexed line number in document / DSL")
    col: Optional[int] = Field(default=None, ge=1, description="1-indexed column number in document / DSL")


class Issue(BaseModel):
    """
    Detailed Issue record in diagnostics report.
    Complies with unified diagnostics schema across all 3 modules.
    """
    model_config = ConfigDict(extra="forbid")

    code: str = Field(
        ...,
        min_length=3,
        description="Standard identifier code (e.g. 'E-DOCX-OPENXML-TC-P', 'W-DEV-STYLE-MISMATCH')"
    )
    severity: Severity = Field(
        ...,
        description="Issue severity level ('error', 'warning', 'info')"
    )
    engine: Engine = Field(
        ...,
        description="Originating engine domain ('docx', 'xlsx', 'diagram', 'infra')"
    )
    message: str = Field(
        ...,
        min_length=1,
        description="Technical description and root cause context of the issue"
    )
    location: Optional[Location] = Field(
        default=None,
        description="Coordinate or structural component location of the issue"
    )
    fixable_by: Optional[FixableBy] = Field(
        default=None,
        description="Target entity capable of remediation ('engine', 'ai', 'human')"
    )
    suggested_action: Optional[str] = Field(
        default=None,
        description="Suggested remediation action for AI agent or engineer"
    )
    evidence: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Technical evidence payload supporting triage (e.g. AST diff, font values, bounding box)"
    )
