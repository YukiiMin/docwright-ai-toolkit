# Docwright AI Toolkits (`docwright-ai-toolkit`)

<p align="center">
  <strong>The AI-Native Office & Diagram Toolkit Plugin for AI Agents.</strong><br>
  <em>Schema-guaranteed, format-preserving, and zero-corruption execution for Word, Excel, and Technical Diagrams.</em>
</p>

<p align="center">
  <a href="#key-capabilities">Capabilities</a> &bull;
  <a href="#quickstart">Quickstart</a> &bull;
  <a href="#ai-ide-setup">AI IDE Setup</a> &bull;
  <a href="#architecture">Architecture</a> &bull;
  <a href="#tool-catalog">MCP Catalog</a> &bull;
  <a href="#license">License</a>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> | <a href="README.vi.md"><strong>Tiếng Việt</strong></a>
</p>

---

## The Problem: Why Standard AI Tools Fail at Office Documents

When modern Large Language Models (LLMs) generate or manipulate office documents using raw library scripts (`python-docx`, `openpyxl`), they frequently corrupt files:

- **Word / DOCX Corruption**: Missing `<w:p>` in empty cells violates ECMA-376 schema rules, triggering Microsoft Word's *"Word found unreadable content"* repair prompt.
- **Table Disruption**: Multi-page tables split across page boundaries because AI scripts omit `<w:cantSplit/>` and header repeat flags `<w:tblHeader/>`.
- **Excel Formula Invalidation**: Writing values directly breaks cell dependency graphs, overwrites live calculation formulas, and strips DrawingML logos and charts.
- **Style Stripping**: Mutating cell text destroys typography, runs, borders, and margins inherited from corporate templates.

**Docwright AI Toolkits** resolves this by introducing a strict, deterministic compilation layer between AI models and binary file formats.

---

## Key Capabilities

| Domain | Core Features | Deterministic Guarantees |
|---|---|---|
| **Word (DOCX)** | Dual-path compiler (Path A Jinja templates & Path B DocSpec DSL), Surgical Run Splicer, Document Vision Layout Measurer. | OpenXML ECMA-376 canonical tag ordering, zero table splitting, strict paragraph termination in every cell. |
| **Spreadsheets (XLSX)** | 2D Block Mutator, Table Island Detector, AST formula shifting, L1/L2/L3 Faithful Model, Recalc cache injector. | 13 Universal Quality Gates (`UG-01..13`), 100% formula preservation, DrawingML shape collision avoidance. |
| **Technical Diagrams** | Pure `mxGraphModel` generation for Draw.io, orthogonal auto-routing, dynamic geometry scaling. | Native XML element hierarchy, no rasterized hacks, high-DPI headless rendering. |
| **AI Integration** | Model Context Protocol (MCP) STDIO server, unified CLI dispatcher, Pydantic data contracts. | Parameter auto-adaptation, schema filtering, fail-closed diagnostic reporting. |

---

## Comparative Analysis

| Evaluation Metric | Generic AI Scripts (`python-docx` / `openpyxl`) | Generic MCP Document Servers | Docwright AI Toolkits |
|---|---|---|---|
| **OpenXML ECMA-376 Compliance** | None (ad-hoc tag generation) | Partial (library wrapper) | **100% Strict Canonical Ordering** |
| **Multi-page Table Integrity** | Splits rows randomly across pages | Often unsupported | **Guaranteed (`cantSplit` & `tblHeader`)** |
| **Excel Formula Shifts** | Hardcodes static numbers | Basic string substitution | **AST Tokenizer & 2D Block Shift** |
| **Corporate Template Logos & Shapes** | Often stripped upon resaving | Preserved only if untouched | **DrawingML Anchor & Collision Shield** |
| **Multi-column Scanned PDF Extraction** | Hallucinates table structure | Fails on complex layouts | **OpenCV Morphological Mesh Resolution** |
| **Validation & Diagnostic Gates** | None (silent corruptions) | Basic try-catch blocks | **13 Universal Quality Gates (Fail-Closed)** |

---

## Quickstart

### Installation

Install the package via `pip` or `uv`:

```bash
pip install docwright-ai-toolkit
```

Verify the installation:

```bash
docwright --version
```

### Inspecting Available Tools

Enumerate all registered MCP tools and their capabilities:

```bash
docwright list
```

Inspect the schema and parameter specifications for any tool:

```bash
docwright schema docx.build_document
```

---

## AI IDE & Agent Setup (Universal Integration)

Docwright communicates natively via the **Model Context Protocol (MCP)** using standard I/O (`stdio`), and provides a deterministic **CLI Engine** for terminal-based AI agents and headless pipelines.

### 1. Claude Code CLI (Anthropic)
Run the one-line CLI integration:
```bash
claude mcp add docwright -- docwright-mcp
```
Or add to your `.claude.json`:
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 2. Cursor IDE
Add to `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 3. Google Antigravity IDE
Add to `.agents/mcp_config.json`:
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 4. Claude Desktop
Add to `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 5. Windsurf / Codeium
Add to `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "docwright": {
      "command": "docwright-mcp"
    }
  }
}
```

### 6. OpenAI Codex CLI & Shell-Based AI Agents
For terminal-first agents (Codex CLI, Aider, CI/CD runners), invoke tools deterministically via CLI:
```bash
# Discover all 51 tools
docwright list

# Inspect exact contract & argument schema
docwright schema docx.build_document

# Execute via structured spec file
docwright docx.build_document --spec payload.json
```

### 7. Universal MCP Clients (Cline, Roo Code, Continue.dev, Zed)
Any client supporting the Model Context Protocol can connect via `docwright-mcp`. Pre-built JSON templates are available in [`configs/`](configs/).
- **Continue.dev**: [`configs/continue_mcp.json`](configs/continue_mcp.json)
- **Zed Editor**: [`configs/zed_settings.json`](configs/zed_settings.json)
- **Roo Code / Cline**: [`configs/universal_mcp.json`](configs/universal_mcp.json)

---

## Architecture Overview

Docwright enforces a 5-layer separation of concerns:

```
[ AI Agent / IDE (Cursor, Claude, Antigravity) ]
                       |
                 (MCP JSON-RPC)
                       v
[ Layer 5: Interfaces ] ──> CLI Dispatcher & Native MCP STDIO Server
                       |
[ Layer 4: Operations ] ──> Central ToolRegistry (Smart Parameter Adapter)
                       |
[ Layer 3: Contracts  ] ──> Pydantic Schemas (DocSpec, LayoutSpec, Envelope)
                       |
[ Layer 2: Verification ] ──> 13 Universal Gates (UG-01..13) & Diagnostic Envelopes
                       |
[ Layer 1: Core Engine ] ──> OpenXML TagOrderRegistry, 2D BlockMutator, OpenCV Measurer
```

- **Contracts (`contracts/`)**: Open Pydantic models allowing LLMs to inspect schemas, type hints, and documentation.
- **Engines (`core/`, `gates/`)**: High-performance, protected modules enforcing XML grammar, layout topology, and formula calculation.

---

## Core Tool Catalog

Docwright exposes 51 specialized tools organized by functional domain:

### Word Processing (`docx.*`)
- `docx.build_document`: Deterministically compiles structured `DocSpec` JSON into formatted Word documents with OpenXML guards.
- `docx.measure_pdf_layout`: Extracts physical table geometry, column ratios, and skew angles from scanned documents using morphological kernels.
- `docx.populate_layout_text`: Maps transcribed textual content into measured layout cells without manual coordinate calculations.
- `docx.compile_layout_spec`: Compiles physical geometric measurements into clean, normalized `DocSpec` representations.
- `docx.patch`: Executes surgical, format-preserving text replacements without destroying surrounding run styles.
- `docx.validate`: Evaluates document health against OpenXML structural invariants.

### Spreadsheet Engineering (`xlsx.*`)
- `xlsx.mutate_block`: Executes 2D rectangular block mutations with automatic horizontal and vertical formula shifting.
- `xlsx.detect_tables`: Detects independent table boundaries, whitespace corridors, and border matrices on shared sheets.
- `xlsx.extract`: Produces structured, lossless extractions stored via opaque references to prevent context overflow.
- `xlsx.query`: Performs targeted, paginated cell slice queries on extracted spreadsheet models.
- `xlsx.validate`: Audits workbooks against 13 Universal Quality Gates (`UG-01..13`).
- `xlsx.recalc`: Recalculates formula values and injects cached results into OpenXML structures.

### Technical Diagrams (`diagram.*`)
- `diagram.build`: Constructs clean, native Draw.io `mxGraphModel` XML structures from declarative topological specifications.
- `diagram.render_raster`: Headless, high-DPI rendering of technical diagrams to PNG format.
- `diagram.render_svg`: Headless vector export with crisp line-art representation.

---

## Standalone Binary Release

For non-developer environments without a pre-installed Python runtime, standalone executable releases are available in the [GitHub Releases](https://github.com/YukiiMin/docwright-ai-toolkit/releases) tab:

- Download `docwright-windows-amd64.exe`
- Configure your AI client to point directly to the binary executable:
  ```json
  {
    "mcpServers": {
      "docwright": {
        "command": "C:\\path\\to\\docwright.exe",
        "args": ["mcp"]
      }
    }
  }
  ```

---

## License & Commercial Terms

Docwright AI Toolkits is licensed under the **Business Source License 1.1 (BSL 1.1)**.

- **Non-Commercial & Development Use**: Free for personal use, internal corporate workflows, open-source projects, and integration with AI IDEs.
- **Commercial Restrictions**: You may not provide Docwright AI Toolkits as a hosted cloud service, managed API, or commercial SaaS product without an explicit commercial license.
- **Licensing Inquiries**: For enterprise licensing, custom integrations, or white-label partnerships, please contact the maintainers.
