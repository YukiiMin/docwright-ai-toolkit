# AGENTS.md — Universal Agent Operations Guide for Docwright AI Toolkits

> **Target Audience**: AI Agents, Code Assistants (Claude Code, Cursor, Windsurf, Codex, Antigravity, Roo Code, Cline), and Automated CI/CD Runners.  
> **Package**: `docwright-ai-toolkit`  
> **Executable**: `docwright` (CLI) & `docwright-mcp` (Model Context Protocol STDIO Server)

---

## 1. Operating Mental Model

You have access to **Docwright AI Toolkits**, an industrial-grade engine designed to eliminate corruption in Word (`.docx`), Excel (`.xlsx`), and Diagrams (`.drawio`).

### The Cardinal Rule (No Ad-Hoc Scripts)
**NEVER** write or run unmanaged raw library scripts (`python -c "import openpyxl..."`, `python -c "import docx..."`). Raw scripts bypass OpenXML tag order validation, strip DrawingML corporate logos, disrupt cell merge topologies, and break Excel calculation chains.

All document and diagram modifications **MUST** route through:
1. **Tier 1 (Preferred)**: MCP Tool Calls (`docx.*`, `xlsx.*`, `diagram.*`).
2. **Tier 2 (CLI Alternative)**: `docwright <tool_name> --spec <spec.json>`.

---

## 2. Tool Discovery & Self-Inspection

If you need to discover available capabilities or examine required arguments, execute:

```bash
# List all 51 registered tools across DOCX, XLSX, and DIAGRAM
docwright list

# Inspect exact Pydantic schema, parameter types, and docstrings
docwright schema docx.build_document
docwright schema xlsx.mutate_block
docwright schema xlsx.validate
```

---

## 3. Core Execution Invariants

### Word Processing (`docx.*`)
- **The Last Paragraph Invariant**: Every table cell (`<w:tc>`) MUST terminate with at least one `<w:p>`. Empty cells corrupt Word documents.
- **Table Integrity**: Multi-page tables must include `<w:cantSplit/>` on data rows and `<w:tblHeader/>` on header rows.
- **Surgical Run Splicing**: Mutate text within runs without destroying font styling, bold/italic, color, or paragraph margins.

### Spreadsheet Engineering (`xlsx.*`)
- **2D Block Mutation**: Use `xlsx.mutate_block` to insert or shift rows/columns. It automatically adjusts formula coordinate references using AST tokenization.
- **DrawingML Shield**: Never resave workbooks using blank templates; preserve existing logos, shapes, and charts.
- **13 Universal Gates (`UG-01..13`)**: Every spreadsheet operation automatically verifies against structural gates (zero formula breakage, no merged-cell corruption, no style stripping).

### Technical Diagrams (`diagram.*`)
- **Pure Native Hierarchy**: All nodes and edges must be native `<mxCell>` elements inside a clean `mxGraphModel`. No raster hacks or embedded Markdown wrappers.
- **Orthogonal Routing**: Use `edgeStyle=orthogonalEdgeStyle;` with standard anchor ports (`0.0`, `0.5`, `1.0`).

---

## 4. Universal Configuration Reference

| AI Agent / IDE | Configuration Path | Command |
|---|---|---|
| **Cursor IDE** | `.cursor/mcp.json` | `docwright-mcp` |
| **Claude Desktop** | `claude_desktop_config.json` | `docwright-mcp` |
| **Claude Code CLI** | `claude mcp add docwright -- docwright-mcp` | `docwright-mcp` |
| **Windsurf / Codeium** | `~/.codeium/windsurf/mcp_config.json` | `docwright-mcp` |
| **Google Antigravity** | `.agents/mcp_config.json` | `docwright-mcp` |
| **Codex CLI / Shell Agents** | Direct Terminal CLI | `docwright <tool> --spec <file>` |
| **Continue.dev** | `.continue/config.json` | `docwright-mcp` |
| **Zed Editor** | `settings.json` (`context_servers`) | `docwright-mcp` |
| **Cline / Roo Code** | MCP Settings Panel | `docwright-mcp` |
