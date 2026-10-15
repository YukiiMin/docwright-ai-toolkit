"""
AuditLogger — Task lifecycle logging and audit trail system (Traceability).
Maintains end-to-end request_id context via ContextVar across cross-module operation chains.
"""

from __future__ import annotations
import json
import os
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict

_REQUEST_ID_CTX: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


def get_request_id() -> str:
    """Retrieve the current context request_id; generates one if unset."""
    req_id = _REQUEST_ID_CTX.get()
    if req_id is None:
        req_id = f"req-{uuid.uuid4().hex[:12]}"
        _REQUEST_ID_CTX.set(req_id)
    return req_id


def set_request_id(request_id: Optional[str] = None) -> str:
    """Explicitly set request_id for the current task context."""
    new_id = request_id or f"req-{uuid.uuid4().hex[:12]}"
    _REQUEST_ID_CTX.set(new_id)
    return new_id


class AuditEvent(BaseModel):
    """Structured JSON audit event record."""
    model_config = ConfigDict(extra="forbid")

    request_id: str = Field(..., description="Unique request identifier across pipeline")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp of recorded event")
    engine: str = Field(..., description="Engine domain ('docx', 'xlsx', 'diagram', 'infra')")
    action: str = Field(..., description="Action name executed")
    success: bool = Field(..., description="Whether action succeeded")
    duration_ms: Optional[float] = Field(default=None, description="Execution duration in ms")
    file_uri: Optional[str] = Field(default=None, description="Relevant FileRef URI if any")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Extended metadata dict")


class AuditLogger:
    """
    Manages audit log persistence in JSON Lines (audit.jsonl)
    and maintains an in-memory ring buffer for immediate inspection.
    """

    def __init__(self, log_file: Optional[Path] = None, max_in_memory: int = 100) -> None:
        self.log_file = log_file
        self.max_in_memory = max_in_memory
        self._history: List[AuditEvent] = []

        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        engine: str,
        action: str,
        success: bool,
        duration_ms: Optional[float] = None,
        file_uri: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditEvent:
        """Record an audit event."""
        event = AuditEvent(
            request_id=get_request_id(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            engine=engine,
            action=action,
            success=success,
            duration_ms=duration_ms,
            file_uri=file_uri,
            details=details,
        )

        self._history.append(event)
        if len(self._history) > self.max_in_memory:
            self._history.pop(0)

        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(event.model_dump_json() + "\n")
            except OSError:
                pass

        return event

    def get_recent_events(self, limit: int = 50) -> List[AuditEvent]:
        """Retrieve recent in-memory audit events."""
        return self._history[-limit:]
