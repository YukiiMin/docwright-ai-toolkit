"""
doctools.registry — Central Tool Registry & MCP Protocol Dispatcher.
Features:
- Explicit namespace routing: docx.*, xlsx.*, diagram.*, infra.*.
- Name Collision Guard & alias mapping (e.g. xlsx_inspect -> xlsx.inspect).
- Unhandled exception wrapping into standardized ResultEnvelope.
- AuditLogger integration with request_id traceability.
- Model Context Protocol (MCP) tool schema catalog generation.
"""

from __future__ import annotations
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, Type
from pydantic import BaseModel

from .contract.envelope import Diagnostics, ResultEnvelope, Stats
from .contract.issues import Engine, Issue, Severity
from .infra.audit import AuditLogger, get_request_id
from .infra.file_store import FileStore

VALID_NAMESPACES = {
    "docx": Engine.DOCX,
    "xlsx": Engine.XLSX,
    "diagram": Engine.DIAGRAM,
    "infra": Engine.INFRA,
    "common": Engine.COMMON,
    "util": Engine.COMMON,
}

COMMON_PARAM_ALIASES: Dict[str, List[str]] = {
    "file_ref": ["file_path", "path", "filepath", "file", "file_ref_or_path", "document_path", "workbook_path"],
    "file_path": ["file_ref", "path", "filepath", "file", "file_ref_or_path", "document_path", "workbook_path"],
    "file_ref_or_path": ["file_ref", "file_path", "path", "filepath", "file"],
    "pdf_path": ["file_path", "file_ref", "path", "pdf_file"],
    "template_ref": ["template_path", "template_file", "template", "file_ref", "file_path"],
    "template_ref_or_id": ["template_ref", "template_id", "template_path", "template"],
    "base_ref": ["base_path", "file_ref", "file_path"],
    "original_ref": ["original_path", "original_file", "file_ref", "file_path"],
    "modified_ref": ["modified_path", "modified_file"],
    "model_ref": ["file_ref", "file_path", "model_file", "json_ref"],
    "layout_spec": ["spec", "layout_spec_path", "spec_path"],
    "docspec": ["spec", "docspec_path"],
    "spec": ["layout_spec", "docspec"],
}


def adapt_tool_arguments(
    handler: Callable[..., Any],
    raw_args: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Intelligently maps argument aliases and filters unexpected arguments to prevent
    TypeError crashes when AI clients pass common parameter synonyms.
    """
    try:
        sig = inspect.signature(handler)
    except (ValueError, TypeError):
        return raw_args

    has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
    adapted = dict(raw_args)

    for target_param in sig.parameters.keys():
        if target_param not in adapted:
            aliases = COMMON_PARAM_ALIASES.get(target_param, [])
            for alias in aliases:
                if alias in adapted:
                    adapted[target_param] = adapted[alias]
                    break

    if not has_var_keyword:
        return {k: v for k, v in adapted.items() if k in sig.parameters}

    return adapted


class ToolDefinition(BaseModel):
    """Metadata definition of an MCP tool."""
    name: str
    description: str
    engine: Engine
    input_schema: Dict[str, Any]
    handler_name: str
    example: Optional[Dict[str, Any]] = None


class ToolRegistry:
    """Central registry managing and routing all MCP tools in doctools."""

    def __init__(
        self,
        file_store: Optional[FileStore] = None,
        audit_logger: Optional[AuditLogger] = None,
    ) -> None:
        self.file_store = file_store or FileStore()
        self.audit_logger = audit_logger or AuditLogger()
        self._tools: Dict[str, Callable[..., ResultEnvelope]] = {}
        self._metadata: Dict[str, ToolDefinition] = {}
        self._input_models: Dict[str, Optional[Type[BaseModel]]] = {}
        self._alias_map: Dict[str, str] = {}

    def resolve_tool_name(self, name_or_alias: str) -> Optional[str]:
        """Resolve canonical tool name or underscore alias (e.g. xlsx_inspect -> xlsx.inspect)."""
        if name_or_alias in self._tools:
            return name_or_alias
        return self._alias_map.get(name_or_alias)

    def register(
        self,
        name: str,
        description: str,
        input_model: Optional[Type[BaseModel]] = None,
        example: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Callable[..., ResultEnvelope]], Callable[..., ResultEnvelope]]:
        """Decorator registering a tool into Registry with strict namespace checking."""
        parts = name.split(".", 1)
        if len(parts) != 2 or parts[0] not in VALID_NAMESPACES:
            valid_list = ", ".join(f"'{ns}.*'" for ns in VALID_NAMESPACES)
            raise ValueError(f"Invalid tool name '{name}'. Tools must use strict prefix: {valid_list}.")

        engine = VALID_NAMESPACES[parts[0]]
        if name in self._tools:
            raise ValueError(f"Tool collision: Tool '{name}' is already registered in registry.")

        alias = name.replace(".", "_")
        if alias in self._alias_map and self._alias_map[alias] != name:
            raise ValueError(f"Ambiguous alias collision: '{alias}' maps to both '{self._alias_map[alias]}' and '{name}'.")
        self._alias_map[alias] = name

        input_schema = input_model.model_json_schema() if input_model is not None else {"type": "object", "properties": {}}

        def decorator(handler: Callable[..., ResultEnvelope]) -> Callable[..., ResultEnvelope]:
            self._tools[name] = handler
            self._input_models[name] = input_model
            self._metadata[name] = ToolDefinition(
                name=name,
                description=description.strip(),
                engine=engine,
                input_schema=input_schema,
                handler_name=handler.__name__,
                example=example,
            )
            return handler

        return decorator

    def execute(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> ResultEnvelope:
        """Executes a registered tool with error handling, timing, and audit logging."""
        args = arguments or {}
        req_id = get_request_id()

        resolved_name = self.resolve_tool_name(tool_name)
        if resolved_name is None:
            diag = Diagnostics(engine=Engine.INFRA)
            diag.add_issue(
                Issue(
                    code="E-REGISTRY-TOOL-NOT-FOUND",
                    severity=Severity.ERROR,
                    engine=Engine.INFRA,
                    message=f"Tool '{tool_name}' is not registered in doctools registry.",
                    suggested_action=f"Available tools: {list(self._tools.keys())}",
                )
            )
            env = ResultEnvelope(success=False, diagnostics=diag)
            self.audit_logger.log(
                engine="infra",
                action=f"call:{tool_name}",
                success=False,
                details={"error": "Tool not found", "request_id": req_id},
            )
            return env

        handler = self._tools[resolved_name]
        meta = self._metadata[resolved_name]
        start_time = time.perf_counter()

        adapted_args = adapt_tool_arguments(handler, args)
        try:
            result = handler(**adapted_args)
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            if result.stats is None:
                result.stats = Stats(render_time_ms=round(duration_ms, 2))
            elif result.stats.render_time_ms is None:
                result.stats.render_time_ms = round(duration_ms, 2)

            file_uri = result.file_ref.uri if result.file_ref else None
            self.audit_logger.log(
                engine=meta.engine.value,
                action=tool_name,
                success=result.success,
                duration_ms=result.stats.render_time_ms,
                file_uri=file_uri,
                details={"guarantees": result.guarantees_applied, "request_id": req_id},
            )
            return result

        except Exception as err:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            diag = Diagnostics(engine=meta.engine)
            diag.add_issue(
                Issue(
                    code="E-SYS-UNCAUGHT-EXCEPTION",
                    severity=Severity.ERROR,
                    engine=meta.engine,
                    message=f"Unhandled exception in tool '{tool_name}': {type(err).__name__}: {str(err)}",
                    evidence={"exception_type": type(err).__name__, "args": repr(args)},
                    suggested_action="Check input arguments and engine logs.",
                )
            )

            env = ResultEnvelope(
                success=False,
                diagnostics=diag,
                stats=Stats(render_time_ms=round(duration_ms, 2)),
            )

            self.audit_logger.log(
                engine=meta.engine.value,
                action=tool_name,
                success=False,
                duration_ms=round(duration_ms, 2),
                details={"error": str(err), "request_id": req_id},
            )
            return env

    def list_tools(self, engine: Optional[Engine] = None) -> List[Dict[str, Any]]:
        """List registered tools formatted for MCP tool enumeration."""
        tools_list: List[Dict[str, Any]] = []
        for name, meta in self._metadata.items():
            if engine is not None and meta.engine != engine:
                continue
            tools_list.append({
                "name": meta.name,
                "description": meta.description,
                "inputSchema": meta.input_schema,
            })
        return tools_list

    def get_tool_metadata(self, tool_name: str) -> Optional[ToolDefinition]:
        """Retrieve tool metadata definition (supports aliases)."""
        resolved = self.resolve_tool_name(tool_name)
        return self._metadata.get(resolved) if resolved else None

    def get_tool_model(self, tool_name: str) -> Optional[Type[BaseModel]]:
        """Retrieve tool Pydantic input model (supports aliases)."""
        resolved = self.resolve_tool_name(tool_name)
        return self._input_models.get(resolved) if resolved else None

    def is_registered(self, tool_name: str) -> bool:
        """Check whether tool is registered (supports aliases)."""
        return self.resolve_tool_name(tool_name) is not None

    def get_system_instructions(self) -> str:
        """Returns standard MCP Server instructions for connected LLM clients (Zero-Shot Guidance)."""
        return (
            "DOCTOOLS MCP SERVER OPERATING INSTRUCTIONS:\n"
            "1. FAIL-CLOSED DISCIPLINE: Never hand-write openpyxl/pandas scripts to edit workbooks. All mutations must pass through xlsx.* tools.\n"
            "2. THE 7-STEP LOOP: preflight -> inspect -> plan -> mutate -> recalc -> validate/diff -> deliver.\n"
            "3. FAITHFUL EXTRACTION LOOP: For reading data/tables without LLM context bloat: call xlsx_extract (dumps to FileStore) then xlsx_query (targeted slice). In Python SDK: import doctools.api.\n"
            "4. DIAGNOSTICS: When issues arise, read 'fixable_by' and 'suggested_action'. Never silence warnings by deleting formulas or writing 0.\n"
            "5. OPERATOR PLAYBOOK: Refer to .agents/skills/xlsx-engine-operator/SKILL.md and AGENTS.md for complete rules."
        )


def get_default_registry() -> ToolRegistry:
    """Instantiate and populate default ToolRegistry with all doctools tools."""
    reg = ToolRegistry()

    # Register XLSX tools
    try:
        from doctools.operations.xlsx import (
            register_preflight_ops, register_xlsx_inspect_tools, register_xlsx_mutate_tools,
            register_xlsx_recalc_tools, register_xlsx_validate_tools, register_xlsx_export_tools,
            register_xlsx_build_tools, register_xlsx_repair_tools, register_xlsx_template_tools,
            register_xlsx_write_catalog_tools, register_xlsx_extract_tools,
            register_xlsx_verify_tools, register_xlsx_profile_tools,
            register_xlsx_semantic_extract_tools,
            register_xlsx_detect_tables_tools,
            register_xlsx_block_mutate_tools,
            register_xlsx_batch_interaction_tools,
            register_xlsx_bulk_ingest_tools,
        )
        for reg_fn in (
            register_preflight_ops, register_xlsx_inspect_tools, register_xlsx_mutate_tools,
            register_xlsx_recalc_tools, register_xlsx_validate_tools, register_xlsx_export_tools,
            register_xlsx_build_tools, register_xlsx_repair_tools, register_xlsx_template_tools,
            register_xlsx_write_catalog_tools, register_xlsx_extract_tools,
            register_xlsx_verify_tools, register_xlsx_profile_tools,
            register_xlsx_semantic_extract_tools,
            register_xlsx_detect_tables_tools,
            register_xlsx_block_mutate_tools,
            register_xlsx_batch_interaction_tools,
            register_xlsx_bulk_ingest_tools,
        ):
            reg_fn(reg)
    except Exception:
        pass


    # Register DOCX tools
    try:
        from doctools.operations.docx.inspect_ops import register_inspect_ops
        from doctools.operations.docx.build_ops import register_build_ops
        from doctools.operations.docx.patch_ops import register_patch_ops
        from doctools.operations.docx.merge_ops import register_merge_ops
        from doctools.operations.docx.template_ops import register_template_ops
        from doctools.operations.docx.field_ops import register_field_ops
        from doctools.operations.docx.extract_ops import register_docx_extract_tools
        from doctools.operations.docx.layout_ops import register_layout_ops

        for reg_fn in (
            register_inspect_ops, register_build_ops, register_patch_ops,
            register_merge_ops, register_template_ops, register_field_ops,
            register_docx_extract_tools, register_layout_ops,
        ):
            reg_fn(reg)
    except Exception:
        pass

    # Register Common / Util tools
    try:
        from doctools.operations.common.compact_ops import register_common_tools
        register_common_tools(reg)
    except Exception:
        pass

    return reg
