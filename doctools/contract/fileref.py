"""
FileRef Contract — Opaque File Reference object.
Oversized binary payloads must never be transferred across chat stream;
exchanged strictly via opaque FileRef.
"""

from __future__ import annotations
import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

_SHA256_REGEX = re.compile(r"^[a-fA-F0-9]{64}$")


class FileRef(BaseModel):
    """
    Opaque File Reference contract across all doctools engines and MCP clients.
    """
    model_config = ConfigDict(extra="forbid", frozen=True)

    uri: str = Field(
        ...,
        description="Resource URI identifier (e.g. resource://docx/files/uuid-123 or file:///abs/path)"
    )
    sha256: str = Field(
        ...,
        description="SHA-256 hash containing exactly 64 hexadecimal characters verifying integrity"
    )
    size: int = Field(
        ...,
        ge=0,
        description="File size in bytes (>= 0)"
    )
    mime: str = Field(
        ...,
        min_length=3,
        description="Standard MIME type (e.g. application/vnd.openxmlformats-officedocument.wordprocessingml.document)"
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        description="TTL expiration timestamp in FileStore if applicable"
    )

    @field_validator("sha256")
    @classmethod
    def validate_sha256_hex(cls, v: str) -> str:
        clean_v = v.strip().lower()
        if not _SHA256_REGEX.match(clean_v):
            raise ValueError(f"sha256 must be exactly 64 hexadecimal characters, got: '{v}'")
        return clean_v

    @field_validator("uri")
    @classmethod
    def validate_uri_format(cls, v: str) -> str:
        clean_v = v.strip()
        if not clean_v:
            raise ValueError("uri cannot be empty")
        if not (clean_v.startswith("resource://") or clean_v.startswith("file://") or clean_v.startswith("/")):
            raise ValueError(f"uri must start with 'resource://', 'file://', or absolute path, got: '{v}'")
        return clean_v
