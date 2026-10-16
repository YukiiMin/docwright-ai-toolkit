# Rule: Docwright AI Toolkits — Execution & Document Integrity Standards

> **Scope**: Applies to AI Agents (Cursor, Claude Code, Antigravity, Windsurf, Codex) operating on Word (`.docx`) and Excel (`.xlsx`) files in this workspace.  

---

## 1. Preferred Execution Interfaces (3 Modes)

Always use registered **Docwright** interfaces to ensure OpenXML schema compliance, multi-page table protection, DrawingML preservation, and automatic Excel formula range shifting:

1. **Mode 1 — Direct MCP Tools (`docwright-mcp`)**: Invoke `docx.*` (19 tools), `xlsx.*` (31 tools), and `common.compact_json` (1 tool) directly via MCP.
2. **Mode 2 — Python SDK (`doctools.api` & `doctools.operations`)**: When writing Python scripts, import official SDK functions (`from doctools.api import load_workbook_model, read_table, xlsx_mutate_block` or `from doctools.operations.docx import docx_build_document`).
3. **Mode 3 — Unified CLI (`docwright`)**:
   ```bash
   docwright list
   docwright schema <tool_name>
   docwright <tool_name> --spec payload.json
   ```

---

## 2. Verification & Diagnostics Protocol

- Always validate generated or modified files with `docx.validate` or `xlsx.validate` before completing a task.
- Inspect `res.diagnostics.errors` and `res.diagnostics.warnings` in the returned `ResultEnvelope`.
- If a tool call returns an error, check the parameter schema via `docwright schema <tool_name>` and correct the payload.
