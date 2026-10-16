<p align="center">
  <img src="https://raw.githubusercontent.com/YukiiMin/docwright-ai-toolkit/main/assets/docwright-ai-toolkit-icon.png" width="128" height="128" alt="Docwright AI Toolkits Icon" />
</p>

# Docwright AI Toolkits (`docwright-ai-toolkit`)

<p align="center">
  <strong>Deterministic Word (DOCX) &amp; Excel (XLSX) Engineering Toolkit for AI Agents, Python Developers, and CLI Pipelines.</strong><br>
  <em>Build, inspect, patch, and validate enterprise documents and spreadsheets across 51 schema-validated tools — via MCP Server, Python SDK, or CLI.</em>
</p>

<p align="center">
  <a href="https://docwright-ai-toolkit.vercel.app/"><img src="https://img.shields.io/badge/docs-vercel_live-000000?style=for-the-badge&logo=vercel" alt="Documentation" /></a>
  <a href="https://pypi.org/project/docwright-ai-toolkit/"><img src="https://img.shields.io/pypi/v/docwright-ai-toolkit?style=for-the-badge&color=38bdf8" alt="PyPI Version" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-BSL--1.1-blue?style=for-the-badge" alt="License" /></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python Version" />
</p>

<p align="center">
  <a href="https://docwright-ai-toolkit.vercel.app/"><strong>📖 Official Documentation Portal</strong></a> &bull;
  <a href="#quickstart">Quickstart</a> &bull;
  <a href="#3-ways-to-use-docwright">3 Usage Modes</a> &bull;
  <a href="#1-click-ai-ide-setup">AI IDE Setup</a> &bull;
  <a href="#complete-51-tool-catalog">51-Tool Catalog</a> &bull;
  <a href="#license--commercial-terms">License</a>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> | <a href="README.vi.md"><strong>Tiếng Việt</strong></a>
</p>

<div align="center">

```bash
pip install docwright-ai-toolkit
```

👉 **[Get Started with Installation & AI IDE Setup](https://docwright-ai-toolkit.vercel.app/getting-started/installation/)**

</div>

---

## What Docwright Solves

**Docwright AI Toolkits** provides a deterministic engineering layer for creating, reading, modifying, and validating **Microsoft Word (`.docx`)** and **Microsoft Excel (`.xlsx`)** files:

1. **Multi-Page Word Table Pagination Protection**: Automatically locks table rows against mid-row page splits, repeats table headers at the top of every page, and binds section banners (`keep_with_next`) to their data rows.
2. **Jinja2 Template Healing & Style-Preserving Patching**: Consolidates split `{{ variable }}` tags across XML runs before rendering, and splices text updates into existing `.docx` files while preserving fonts, sizes, colors, and corporate formatting.
3. **1:1 Scanned PDF to Editable Word Reconstruction**: Uses computer-vision grid measurement (`docx.measure_pdf_layout`) to extract exact column ratios and cell coordinates (`c0_0`, `c0_1`, ...), populates text by cell ID, and compiles editable Word forms.
4. **Token-Safe Spreadsheet Reading & 2D Block Mutation**: Extracts multi-sheet workbooks into a queryable 3-tier model without overflowing LLM context windows, detects independent **2D Table Islands** on shared sheets, and inserts rows/columns while automatically shifting downstream `=SUM(...)` and KPI formula ranges via AST parsing.

---

## Core Modules Overview (51 Tools)

| Module Namespace | Tool Count | Key Capabilities |
| :--- | :--- | :--- |
| **Word Module (`docx.*`)** | **19 Tools** | Declarative `DocSpec` document builder, Jinja2 template normalization & rendering, surgical style-preserving text patching, 2-tier faithful extraction, scanned PDF layout reconstruction, and 8 structural validation checks. |
| **Excel Module (`xlsx.*`)** | **31 Tools** | 3-tier faithful extraction (`extract`/`query`), 2D Table Island detection (`detect_tables`), block insertion with automatic AST formula range shifting (`mutate_block`), headless LibreOffice recalculation (`recalc`), and 13 quality validation checks. |
| **Common Module (`common.*`)** | **1 Tool** | Token-efficient JSON minification and subtree pruning (`common.compact_json`) for large extracted payloads. |

---

## Quickstart

```bash
# 1. Install from PyPI
pip install docwright-ai-toolkit

# 2. List all 51 registered tools (19 docx.*, 31 xlsx.*, 1 common.*)
docwright list

# 3. Inspect the JSON input schema and runnable example for any tool
docwright schema docx.build_document
docwright schema xlsx.mutate_block
```

---

## 3 Ways to Use Docwright

### Mode 1: Direct MCP Server (`docwright-mcp`) for AI Agents
Connect `docwright-mcp` to your AI IDE (Claude Code, Cursor, Google Antigravity, Claude Desktop, Windsurf). Your AI agent can call any of the 51 tools directly using either dot notation (`docx.build_document`) or underscore aliases (`docx_build_document`).

### Mode 2: Python SDK Import (`doctools.api` & `doctools.operations`)
Import Docwright directly inside your Python applications, backend services, or automation scripts:

```python
from doctools.api import (
    load_workbook_model,
    read_table,
    TableIslandDetector,
    xlsx_detect_tables,
    xlsx_mutate_block,
    compact_json,
)
from doctools.operations.docx import docx_build_document, docx_patch, docx_validate
from doctools.operations.xlsx import xlsx_recalc, xlsx_validate

# Example: Insert 2 rows into an Excel table and automatically shift =SUM(...) formulas
res = xlsx_mutate_block(
    file_ref="data/quarterly_budget.xlsx",
    output_path="data/quarterly_budget_q4.xlsx",
    sheet_name="Summary",
    operation="insert_rows",
    start_row=5,
    count=2,
    data=[
        ["AI Compute Cluster", 14500, 16000],
        ["Automated QA Pipeline", 3200, 3500],
    ],
)
print("Success:", res.success)
```

### Mode 3: Unified CLI Dispatcher (`docwright`)
Execute tools and built-in utilities directly from your terminal or CI/CD workflows:

```bash
# Execute any tool with a JSON spec file or inline --json payload
docwright docx.build_document --spec report_spec.json
docwright docx.validate --json '{"file_ref": "output/report.docx"}'

# Built-in CLI utilities for token compaction and profile scaffolding
docwright compact-json extracted_model.json --path sheets.Summary --max-depth 3 -o compact.json
docwright profile-scaffold template.xlsx --output profile.yaml
```

---

## 1-Click AI IDE Setup

### 1. Claude Code CLI (Anthropic)
```bash
claude mcp add docwright -- docwright-mcp
```

### 2. Cursor IDE (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp",
      "args": []
    }
  }
}
```

### 3. Google Antigravity IDE (`.agents/mcp_config.json`)
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp",
      "args": []
    }
  }
}
```

### 4. Claude Desktop (`claude_desktop_config.json`) & Windsurf (`~/.codeium/windsurf/mcp_config.json`)
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp",
      "args": []
    }
  }
}
```

Pre-made configuration templates for all clients (including **Continue.dev**, **Zed Editor**, **Cline / Roo Code**, and **Codex CLI**) are available in the [`configs/`](configs/) folder.

---

## Complete 51-Tool Catalog

### 1. Word Module (`docx.*` — 19 Tools)
| # | Tool Name | Summary |
| :--- | :--- | :--- |
| 1 | `docx.inspect_structure` | Inspect paragraphs, tables, styles, sections, and page setup of a `.docx` file. |
| 2 | `docx.validate` | Run 8 structural and OpenXML schema checks on a `.docx` document. |
| 3 | `docx.extract_media` | Extract embedded images and media assets from a Word document. |
| 4 | `docx.to_markdown` | Convert a Word document into clean Markdown for read-only analysis and summarization. |
| 5 | `docx.render_template` | Populate a corporate Jinja2 `.docx` template with a structured JSON context. |
| 6 | `docx.build_document` | Build a formatted `.docx` document from a declarative `DocSpec` JSON specification. |
| 7 | `docx.patch` | Perform style-preserving surgical text replacements across runs and tables. |
| 8 | `docx.merge` | Combine multiple `.docx` documents while preserving sections and styles. |
| 9 | `docx.lint_template` | Check a Jinja2 `.docx` template for split tags or syntax issues before rendering. |
| 10 | `docx.normalize_template` | Heal and consolidate fragmented `{{ ... }}` Jinja tags across XML runs. |
| 11 | `docx.register_template` | Register a validated `.docx` template into the local template catalog. |
| 12 | `docx.list_templates` | List all registered `.docx` templates and their metadata. |
| 13 | `docx.get_template_manifest` | Retrieve required variables and schema manifest for a registered Word template. |
| 14 | `docx.update_fields` | Refresh Word document fields (such as Table of Contents and page numbers). |
| 15 | `docx.extract` | Extract a 2-tier faithful structural representation of a Word document into `FileStore`. |
| 16 | `docx.query` | Query specific sections, paragraphs, or tables from an extracted Word document. |
| 17 | `docx.measure_pdf_layout` | Measure physical table grids, column ratios, and cell bounding boxes from a scanned PDF. |
| 18 | `docx.populate_layout_text` | Map transcribed text into measured `LayoutSpec` cells by deterministic `cell_id` (`c0_0`). |
| 19 | `docx.compile_layout_spec` | Compile a populated `LayoutSpec` into an editable 1:1 `.docx` document. |

### 2. Spreadsheet Module (`xlsx.*` — 31 Tools)
| # | Tool Name | Summary |
| :--- | :--- | :--- |
| 20 | `xlsx.preflight` | Rapidly scan sheet names, dimensions, merged ranges, and formula counts. |
| 21 | `xlsx.inspect` | Inspect detailed sheet metadata, headers, and structure of an Excel workbook. |
| 22 | `xlsx.coverage_report` | Generate a cell population and formula coverage report across sheets. |
| 23 | `xlsx.analyze_formulas` | Analyze formula dependency chains, functions used, and cross-sheet references. |
| 24 | `xlsx.describe_formats` | Extract font, fill, border, and number format tokens from reference cells. |
| 25 | `xlsx.function_catalog` | List supported Excel functions and formula validation rules. |
| 26 | `xlsx.mutate` | Apply cell-level value and formula updates while preserving template styles and logos. |
| 27 | `xlsx.recalc` | Recalculate live formula values via headless LibreOffice and update XML caches (`<v>`). |
| 28 | `xlsx.validate` | Audit an Excel workbook against all 13 spreadsheet quality gates. |
| 29 | `xlsx.diff` | Compare two Excel workbooks and report cell value, formula, and structural diffs. |
| 30 | `xlsx.export_legacy_xls` | Convert or export spreadsheet data for legacy `.xls` compatibility workflows. |
| 31 | `xlsx.build` | Build a new multi-sheet `.xlsx` workbook from a declarative specification. |
| 32 | `xlsx.repair` | Repair common structural issues such as desynchronized merged-cell borders. |
| 33 | `xlsx.register_template` | Register a reference `.xlsx` template into the template catalog. |
| 34 | `xlsx.lint_template` | Audit an Excel template for hardcoded totals or broken references. |
| 35 | `xlsx.list_templates` | List all registered Excel templates in the catalog. |
| 36 | `xlsx.set_format` | Apply fonts, fills, borders, alignment, and number formats to target cell ranges. |
| 37 | `xlsx.set_validation` | Configure Excel data validation dropdowns and constraints on target ranges. |
| 38 | `xlsx.set_conditional_format` | Add conditional formatting rules (color scales, highlights) to cell ranges. |
| 39 | `xlsx.copy_sheet` | Duplicate a worksheet within a workbook while preserving styles and print setup. |
| 40 | `xlsx.extract` | Extract a 3-tier faithful workbook model into `FileStore` to prevent token overflow. |
| 41 | `xlsx.query` | Query targeted sheet slices or cell ranges from an extracted workbook model. |
| 42 | `xlsx.verify_extract` | Verify extraction completeness against fast column hash checksums. |
| 43 | `xlsx.classify_layout` | Classify worksheet layout archetypes (matrix, key-value form, multi-island). |
| 44 | `xlsx.profile_scaffold` | Generate a reusable YAML/JSON extraction profile from a reference workbook. |
| 45 | `xlsx.semantic_extract` | Extract tables, key-value pairs, and topology using semantic layout detection. |
| 46 | `xlsx.detect_tables` | Detect independent 2D Table Islands, headers, and bounding boxes on a sheet. |
| 47 | `xlsx.mutate_block` | Insert or update 2D blocks of rows/columns with automatic AST formula range shifting. |
| 48 | `xlsx.shift_block` | Shift a rectangular cell block horizontally or vertically and update dependent formulas. |
| 49 | `xlsx.batch_interact` | Execute a transactional sequence of multiple spreadsheet operations in a single pass. |
| 50 | `xlsx.bulk_ingest` | High-throughput streaming ingestion of large tabular datasets into Excel templates. |

### 3. Common Utility Module (`common.*` — 1 Tool)
| # | Tool Name | Summary |
| :--- | :--- | :--- |
| 51 | `common.compact_json` | Minify JSON payloads and isolate specific sub-paths to save LLM context tokens. |

---

## License & Commercial Terms

Docwright AI Toolkits is licensed under the **Business Source License 1.1 (BSL 1.1)**.
- **Free for Non-Commercial & Development Use**: Free for individual developers, internal corporate workflows, academic research, open-source projects, and direct integration with AI IDEs/Agents.
- **Commercial SaaS Restriction**: Commercial hosting of the core engine as a paid third-party multi-tenant SaaS service requires a separate commercial license from the maintainer.
