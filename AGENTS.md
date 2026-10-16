# AGENTS.md — Universal Agent Operations Guide for Docwright AI Toolkits

> **Target Audience**: AI Agents, Code Assistants (Claude Code, Cursor, Windsurf, Codex, Antigravity, Roo Code, Cline), Python Developers, and Automated CI/CD Runners.  
> **Package**: `docwright-ai-toolkit`  
> **Executables**: `docwright` (Unified CLI) & `docwright-mcp` (Model Context Protocol STDIO Server)  
> **Python SDK**: `from doctools.api import ...` and `from doctools.operations import ...`

---

## 1. Three Ways to Use Docwright (51 Registered Tools)

**Docwright AI Toolkits** provides **51 schema-validated tools** across **2 core document modules** (`docx.*` — 19 tools, `xlsx.*` — 31 tools) and **1 utility module** (`common.compact_json` — 1 tool).

1. **Mode 1 — Direct MCP Server (`docwright-mcp`)**: Invoke any of the 51 tools directly as MCP tool calls (`docx.*` / `docx_*`, `xlsx.*` / `xlsx_*`, `common.compact_json`).
2. **Mode 2 — Python SDK Import (`doctools.api` & `doctools.operations`)**: Import tools and high-level faithful data models directly in Python scripts (`from doctools.api import load_workbook_model, read_table, xlsx_mutate_block` or `from doctools.operations.docx import docx_build_document`).
3. **Mode 3 — Unified CLI Dispatcher (`docwright`)**: Run tools and built-in utilities from the terminal:
   ```bash
   docwright list
   docwright schema docx.build_document
   docwright docx.build_document --spec payload.json
   docwright compact-json large_data.json --path tables.0 -o compact.json
   docwright profile-scaffold workbook.xlsx --output profile.yaml
   ```

---

## 2. Core Workflows & Best Practices

### Word Document Engineering (`docx.*` — 19 Tools)
- **Programmatic Generation (`docx.build_document`)**: Build multi-page `.docx` documents from a structured `DocSpec` JSON payload with automatic repeating table headers and row-split protection.
- **Jinja2 Template Rendering (`docx.normalize_template` -> `docx.render_template`)**: Consolidate split `{{ variable }}` tags across XML runs first, then inject JSON context while preserving corporate styles, headers, and footers.
- **Surgical Text Patching (`docx.patch`)**: Replace text inside existing documents while preserving original run font, size, color, and bold/italic formatting.
- **1:1 Scanned PDF Reconstruction (`docx.measure_pdf_layout` -> `docx.populate_layout_text` -> `docx.compile_layout_spec`)**: Measure table grid geometry from scanned PDFs, populate text by `cell_id` (`c0_0`), and compile into an editable Word document.
- **Validation (`docx.validate`)**: Verify OpenXML schema element ordering, table pagination locks, printable margins, and leftover placeholders.

### Spreadsheet Engineering (`xlsx.*` — 31 Tools)
- **3-Tier Faithful Reading (`xlsx.preflight` -> `xlsx.extract` -> `xlsx.query`)**: Inspect workbook structure and query targeted slices without overflowing LLM context windows.
- **2D Table Island Detection & Block Mutation (`xlsx.detect_tables` -> `xlsx.mutate_block`)**: Detect multiple independent tables on a single sheet, insert rows/columns, clone template row styles, and automatically shift downstream `=SUM(...)` and KPI formulas via AST parsing.
- **Recalculation & Quality Verification (`xlsx.recalc` -> `xlsx.validate`)**: Refresh cached formula evaluation values via headless LibreOffice and verify formula integrity, merged-cell borders, and embedded logos/shapes.

---

## 3. Universal Configuration Reference

| AI Agent / IDE | Configuration Path / Command | Server Entrypoint |
| :--- | :--- | :--- |
| **Claude Code CLI** | `claude mcp add docwright -- docwright-mcp` | `docwright-mcp` |
| **Cursor IDE** | `.cursor/mcp.json` | `docwright-mcp` |
| **Google Antigravity** | `.agents/mcp_config.json` | `docwright-mcp` |
| **Claude Desktop** | `claude_desktop_config.json` | `docwright-mcp` |
| **Windsurf / Codeium** | `~/.codeium/windsurf/mcp_config.json` | `docwright-mcp` |
| **Codex CLI / Shell Agents** | Direct Terminal CLI | `docwright <tool> --spec <file>` |
| **Continue.dev / Zed / Cline** | Standard MCP settings | `docwright-mcp` |
