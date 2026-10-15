"""
Unified CLI Dispatcher for doctools document and diagram engineering engines.
Provides a standardized CLI shell with strict exit codes and UTF-8 safe I/O.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

from doctools.contract.envelope import ResultEnvelope
from doctools.registry import ToolRegistry, get_default_registry

RESERVED_COMMANDS = {"list", "schema", "mcp", "help", "profile-scaffold", "compact-json"}



def _setup_io() -> None:
    """Set up UTF-8 safe encoding for standard streams inside main() to avoid import side-effects."""
    for stream in (sys.stdout, sys.stdin, sys.stderr):
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


class DoctoolsArgumentParser(argparse.ArgumentParser):
    """Custom ArgumentParser that exits with code 64 (EX_USAGE) on syntax/usage errors."""

    def error(self, message: str) -> None:
        sys.stderr.write(f"doctools: error: {message}\n")
        sys.exit(64)


def compute_exit_code(envelope: ResultEnvelope) -> int:
    """
    Compute exit code per enterprise QA rules:
    0: Clean (success=True, no errors or warnings)
    1: Warning-only (success=True, has warnings, no errors)
    2: Critical error / gate violation (success=False or has_errors=True)
    """
    if not envelope.success or (envelope.diagnostics and envelope.diagnostics.has_errors):
        return 2
    if envelope.diagnostics and len(envelope.diagnostics.warnings) > 0:
        return 1
    return 0


def resolve_spec_payload(spec_path: str) -> Dict[str, Any]:
    """Read spec file with utf-8-sig (handles PowerShell UTF-8 BOM) and resolve relative file_ref."""
    path = Path(spec_path).resolve()
    if not path.is_file():
        sys.stderr.write(f"doctools: error: Spec file not found: {spec_path}\n")
        sys.exit(64)

    try:
        content = path.read_text(encoding="utf-8-sig")
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"doctools: error: Invalid JSON in spec file: {exc}\n")
        sys.exit(64)

    if not isinstance(data, dict):
        sys.stderr.write("doctools: error: Spec JSON payload must be an object/dict.\n")
        sys.exit(64)

    # Resolve relative paths in file_ref against the spec file directory
    spec_dir = path.parent
    if "file_ref" in data and isinstance(data["file_ref"], str):
        fr = Path(data["file_ref"])
        if not fr.is_absolute():
            resolved = (spec_dir / fr).resolve()
            if resolved.exists():
                data["file_ref"] = str(resolved)

    return data


def create_parser(registry: ToolRegistry) -> DoctoolsArgumentParser:
    """Build parser with registered tools and built-in commands."""
    parser = DoctoolsArgumentParser(
        prog="doctools",
        description="Unified CLI Dispatcher for doctools document and diagram engineering engines.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands or tools")

    # Built-in subcommand: list
    subparsers.add_parser("list", help="List all registered tools")

    # Built-in subcommand: schema
    schema_p = subparsers.add_parser("schema", help="Show JSON schema and runnable example for a tool")
    schema_p.add_argument("tool", help="Tool name or alias (e.g. xlsx.inspect, xlsx_inspect)")

    # Built-in subcommand: mcp
    subparsers.add_parser("mcp", help="Start the doctools MCP (Model Context Protocol) stdio server")

    # Built-in shorthand: profile-scaffold
    scaffold_p = subparsers.add_parser(
        "profile-scaffold", help="Scaffold declarative YAML/JSON profile specification"
    )
    scaffold_p.add_argument("file", help="Path to Excel workbook (.xlsx)")
    scaffold_p.add_argument("--output", help="Target output file path")
    scaffold_p.add_argument("--format", default="yaml", choices=["yaml", "json"], help="Output format")
    scaffold_p.add_argument("--profile-name", dest="profile_name", help="Profile name")

    # Built-in shorthand: compact-json
    compact_p = subparsers.add_parser(
        "compact-json", help="Minify and compress JSON file/text for AI token efficiency"
    )
    compact_p.add_argument("file", help="Path to target JSON file or raw JSON text string")
    compact_p.add_argument("--path", "-p", dest="json_path", help="Optional dot/bracket path to isolate sub-tree")
    compact_p.add_argument("--max-depth", "-d", type=int, dest="max_depth", help="Optional max depth limit")
    compact_p.add_argument("--output", "-o", dest="output", help="Optional output file path")

    # Dynamic subcommands for tools and aliases

    for tool_info in registry.list_tools():
        tool_name = tool_info["name"]
        alias = tool_name.replace(".", "_")
        desc_help = (tool_info.get("description") or "").replace("%", "%%")
        for name in (tool_name, alias):
            t_parser = subparsers.add_parser(name, help=desc_help)
            t_parser.add_argument("--spec", help="Path to JSON spec file")
            t_parser.add_argument("--json", help="Direct JSON payload string")

    return parser


def main(argv: Optional[List[str]] = None, registry: Optional[ToolRegistry] = None) -> int:
    """Main CLI entrypoint."""
    _setup_io()

    reg = registry if registry is not None else get_default_registry()
    parser = create_parser(reg)

    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if not args.subcommand:
        parser.error("A subcommand or tool name is required.")

    if args.subcommand == "list":
        tools_data = reg.list_tools()
        print(json.dumps(tools_data, indent=2, ensure_ascii=False))
        return 0

    if args.subcommand == "schema":
        meta = reg.get_tool_metadata(args.tool)
        if not meta:
            sys.stderr.write(
                f"doctools: error: Unknown tool '{args.tool}'. Run 'doctools list' to view available tools.\n"
            )
            return 64
        schema_out = {
            "name": meta.name,
            "description": meta.description,
            "engine": meta.engine.value,
            "input_schema": meta.input_schema,
            "example": meta.example,
        }
        print(json.dumps(schema_out, indent=2, ensure_ascii=False))
        return 0

    if args.subcommand == "mcp":
        from doctools.mcp_server import main as mcp_main
        return mcp_main()

    if args.subcommand == "profile-scaffold":
        from doctools.core.xlsx.profiles.scaffolder import ProfileScaffolder
        try:
            res_text = ProfileScaffolder.scaffold(
                workbook_or_model=args.file,
                profile_name=args.profile_name,
                output_format=args.format,
                output_path=args.output,
            )
            if not args.output:
                print(res_text)
            else:
                print(f"Profile scaffolded successfully to: {args.output}")
            return 0
        except Exception as exc:
            sys.stderr.write(f"doctools: error: Scaffolding failed: {exc}\n")
            return 2

    if args.subcommand == "compact-json":
        from doctools.core.common.json_compactor import compact_json, compact_json_file
        try:
            if getattr(args, "output", None):
                out_path, stats = compact_json_file(
                    source_path=args.file,
                    output_path=args.output,
                    json_path=args.json_path,
                    max_depth=args.max_depth,
                )
                print(f"Compacted JSON written to: {out_path} ({stats['savings_percentage']}% saved, ~{stats['estimated_tokens_saved']} tokens saved)")
            else:
                compact_str, _ = compact_json(
                    source=args.file,
                    json_path=args.json_path,
                    max_depth=args.max_depth,
                )
                print(compact_str)
            return 0
        except Exception as exc:
            sys.stderr.write(f"doctools: error: JSON compaction failed: {exc}\n")
            return 2

    # Handle tool execution

    if getattr(args, "spec", None) and getattr(args, "json", None):
        parser.error("Cannot specify both --spec and --json.")

    payload: Dict[str, Any] = {}
    if getattr(args, "spec", None):
        payload = resolve_spec_payload(args.spec)
    elif getattr(args, "json", None):
        try:
            parsed = json.loads(args.json)
        except json.JSONDecodeError as exc:
            parser.error(f"Invalid JSON string in --json: {exc}")
        if not isinstance(parsed, dict):
            parser.error("Payload in --json must be a JSON object/dict.")
        payload = parsed

    envelope = reg.execute(args.subcommand, payload)
    print(json.dumps(envelope.model_dump(mode="json"), indent=2, ensure_ascii=False))
    return compute_exit_code(envelope)


if __name__ == "__main__":
    sys.exit(main())

