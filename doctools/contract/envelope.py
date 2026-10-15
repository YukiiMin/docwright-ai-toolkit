"""
ResultEnvelope & Diagnostics Contract — Unified response container
between MCP Server and AI Client / CLI Runner across all doctools engines.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator, ConfigDict

from .fileref import FileRef
from .issues import Engine, Issue, Severity


class Diagnostics(BaseModel):
    """
    Quality diagnostics report categorized into: errors, warnings, info.
    Supports helper methods to route issues automatically by severity.
    """
    model_config = ConfigDict(extra="forbid")

    engine: Engine = Field(..., description="Engine domain originating diagnostics report")
    errors: List[Issue] = Field(default_factory=list, description="Critical invariant violations")
    warnings: List[Issue] = Field(default_factory=list, description="Warnings (e.g. template divergence W-DEV-*)")
    info: List[Issue] = Field(default_factory=list, description="Informational and optimization observations")

    def add_issue(self, issue: Issue) -> None:
        """Add an issue and route to appropriate category."""
        if issue.severity == Severity.ERROR:
            self.errors.append(issue)
        elif issue.severity == Severity.WARNING:
            self.warnings.append(issue)
        else:
            self.info.append(issue)

    @property
    def has_errors(self) -> bool:
        """Check if any error-level issues exist."""
        return len(self.errors) > 0

    @property
    def total_count(self) -> int:
        """Total issue count."""
        return len(self.errors) + len(self.warnings) + len(self.info)


class Stats(BaseModel):
    """Operational metrics and resource consumption."""
    model_config = ConfigDict(extra="forbid")

    render_time_ms: Optional[float] = Field(default=None, ge=0.0, description="Execution duration in milliseconds")
    elements_processed: Optional[int] = Field(default=None, ge=0, description="Count of processed elements")
    memory_peak_mb: Optional[float] = Field(default=None, ge=0.0, description="Peak RAM usage in MB")
    extra: Optional[Dict[str, Any]] = Field(default=None, description="Module-specific extra metrics")


class ResultEnvelope(BaseModel):
    """
    Unified Result Envelope.
    Returned by all doctools MCP tool calls and operations.
    """
    model_config = ConfigDict(extra="forbid")

    success: bool = Field(..., description="Task success status")
    file_ref: Optional[FileRef] = Field(default=None, description="Opaque output FileRef reference if produced")
    diagnostics: Diagnostics = Field(..., description="Detailed diagnostics, warnings, and error block")
    guarantees_applied: List[str] = Field(
        default_factory=list,
        description="List of applied technical guards (e.g. 'cantSplit_enforced', 'AST_formula_shifted')"
    )
    stats: Optional[Stats] = Field(default=None, description="Execution performance statistics")

    @model_validator(mode="after")
    def validate_success_and_errors_consistency(self) -> ResultEnvelope:
        """Enforce invariant: success cannot be True if diagnostics contain errors."""
        if self.success and self.diagnostics.has_errors:
            raise ValueError(
                f"ResultEnvelope inconsistency: success=True is prohibited when diagnostics contain "
                f"{len(self.diagnostics.errors)} errors."
            )
        return self
