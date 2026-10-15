"""
BaseSpec — Abstract foundation for JSON specifications across all 3 modules:
DocSpec (Word), MutationSpec / XlsxSpec (Excel), and DiagramSpec (Draw.io).
"""

from __future__ import annotations
from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T", bound="BaseSpec")


class BaseSpec(BaseModel):
    """
    Abstract base class for all JSON Specifications in doctools.
    Rules:
    - extra="forbid": Prohibits foreign fields outside schema to guarantee determinism.
    - Provides standardized serialization and deserialization helpers.
    """
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    version: str = Field(
        default="2.0",
        description="Standard specification version (default '2.0')"
    )
    title: Optional[str] = Field(
        default=None,
        description="Document, workbook, or diagram title"
    )
    description: Optional[str] = Field(
        default=None,
        description="Brief description of the specification scope"
    )
    meta: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Controlled metadata dictionary"
    )

    def to_json(self, indent: int = 2) -> str:
        """Serialize specification to pretty-printed JSON string."""
        return self.model_dump_json(indent=indent)

    def to_dict(self) -> Dict[str, Any]:
        """Convert specification to primitive Python dictionary."""
        return self.model_dump()

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """Parse and validate specification from JSON string."""
        return cls.model_validate_json(json_str)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Parse and validate specification from dictionary."""
        return cls.model_validate(data)
