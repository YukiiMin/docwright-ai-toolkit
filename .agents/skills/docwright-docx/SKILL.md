---
name: docwright-docx
description: Complete operational guide for all 19 Word (docx.*) tools across MCP, Python SDK, and CLI.
---

# Docwright Word (DOCX) Engineering Skill (19 Tools)

Use this skill whenever creating, templating, patching, extracting, or reconstructing Microsoft Word documents (`.docx`).

---

## 1. Choosing the Right Word Workflow

- **Building New Documents from Scratch**: Call `docx.build_document` with a structured `DocSpec` JSON (`page_setup`, `headings`, `paragraphs`, `tables`). Tables automatically receive repeating header rows and row-split locks across pages.
- **Populating Corporate Jinja Templates**:
  1. Run `docx.normalize_template` to heal split `{{ variable }}` tags across XML runs.
  2. Run `docx.render_template` with your JSON `context`.
- **Updating Text in Existing Documents**: Run `docx.patch` to replace specific strings while preserving original run font, size, color, and bold/italic formatting.
- **Reading Long Documents Without Context Overflow**: Run `docx.extract` followed by `docx.query`, or `docx.to_markdown` for read-only summarization.
- **Reconstructing Scanned PDFs into 1:1 Editable Word Forms**:
  1. `docx.measure_pdf_layout`: Measure table grid geometry and cell IDs (`c0_0`, `c0_1`, ...).
  2. `docx.populate_layout_text`: Map transcribed text to each `cell_id` (supports `row_span` and `col_span`).
  3. `docx.compile_layout_spec`: Compile into an editable `.docx` file.
- **Quality Verification**: Always run `docx.validate` on the output file.

---

## 2. Python SDK & CLI Quick Examples

```python
from doctools.operations.docx import (
    docx_build_document,
    docx_normalize_template,
    docx_render_template,
    docx_patch,
    docx_validate,
)
```

```bash
docwright schema docx.build_document
docwright docx.build_document --spec spec.json
docwright docx.validate --json '{"file_ref": "output/report.docx"}'
```
