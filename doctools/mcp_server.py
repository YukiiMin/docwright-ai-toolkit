"""
Model Context Protocol (MCP) Stdio Server for doctools.
Exposes all 32 registered DOCX and XLSX engineering tools to AI clients.
"""
from __future__ import annotations

import asyncio
import sys
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

from doctools.contract.envelope import ResultEnvelope
from doctools.registry import ToolRegistry, get_default_registry


def create_mcp_server(registry: Optional[ToolRegistry] = None) -> Server:
    """Create and configure an MCP Server instance bound to the given registry."""
    reg = registry if registry is not None else get_default_registry()
    server = Server("doctools")

    @server.list_tools()
    async def list_tools() -> List[types.Tool]:
        tools: List[types.Tool] = []
        for t in reg.list_tools():
            # Antigravity IDE and major LLM clients require ^[a-zA-Z0-9_-]{1,64}$.
            # Replace dot notation with underscore notation for strict client compatibility.
            mcp_tool_name = t["name"].replace(".", "_")
            tools.append(
                types.Tool(
                    name=mcp_tool_name,
                    description=t.get("description", ""),
                    inputSchema=t.get("inputSchema", {"type": "object", "properties": {}}),
                )
            )
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> types.CallToolResult:
        # Strip potential client prefix if present (e.g., mcp_doctools_xlsx_preflight -> xlsx_preflight)
        clean_name = name
        if clean_name.startswith("mcp_doctools_"):
            clean_name = clean_name[len("mcp_doctools_"):]
        elif clean_name.startswith("doctools_"):
            clean_name = clean_name[len("doctools_"):]

        resolved_name = reg.resolve_tool_name(clean_name)
        if resolved_name is None:
            resolved_name = reg.resolve_tool_name(name)

        if resolved_name is None:
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=f"Error: Unknown tool '{name}'")],
                isError=True,
            )

        envelope: ResultEnvelope = reg.execute(resolved_name, arguments or {})
        text_payload = envelope.model_dump_json(indent=2)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=text_payload)],
            isError=not envelope.success,
        )

    return server


async def run_stdio_server(registry: Optional[ToolRegistry] = None) -> None:
    """Run the MCP server over standard I/O (JSON-RPC 2.0)."""
    server = create_mcp_server(registry)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="doctools",
                server_version="2.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main() -> int:
    """Entry point for running doctools MCP server."""
    for stream in (sys.stdout, sys.stdin, sys.stderr):
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

    try:
        asyncio.run(run_stdio_server())
        return 0
    except (KeyboardInterrupt, SystemExit):
        return 0
    except Exception as exc:
        sys.stderr.write(f"doctools-mcp: fatal error: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
