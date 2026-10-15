"""
doctools — AI-Native Office Document & Technical Diagram Toolkit.
Modular 5-layer architecture supporting DOCX, XLSX, and DIAGRAM engines.
"""

__version__ = "1.0.0"


def __getattr__(name: str):
    if name in ("ToolRegistry", "ToolDefinition", "default_registry"):
        try:
            from .registry import ToolRegistry, ToolDefinition, default_registry
            mapping = {
                "ToolRegistry": ToolRegistry,
                "ToolDefinition": ToolDefinition,
                "default_registry": default_registry,
            }
            return mapping[name]
        except ImportError as exc:
            raise AttributeError(
                f"doctools core engine is not installed. Run 'pip install docwright-ai-toolkit' to install: {exc}"
            )
    raise AttributeError(f"module 'doctools' has no attribute '{name}'")


__all__ = [
    "__version__",
    "ToolRegistry",
    "ToolDefinition",
]
