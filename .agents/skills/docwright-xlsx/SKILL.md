---
name: docwright-xlsx
description: Complete operational guide for all 31 Excel (xlsx.*) tools and doctools.api SDK across MCP, Python, and CLI.
---

# Docwright Spreadsheet (XLSX) Engineering Skill (31 Tools)

Use this skill whenever reading, creating, expanding, mutating, or validating Excel workbooks (`.xlsx`).

---

## 1. Core Spreadsheet Workflows

- **3-Tier Token-Safe Reading**:
  1. `xlsx.preflight` or `xlsx.detect_tables` to inspect sheets and locate independent 2D Table Islands.
  2. `xlsx.extract` or `xlsx.semantic_extract` to cache the faithful workbook model.
  3. `xlsx.query` to retrieve targeted cell ranges (`A1:G30`) without overflowing LLM context windows.
- **2D Block Insertion & Automatic Formula Shifting**:
  1. Use `xlsx.mutate_block` (`operation="insert_rows"` or `"insert_cols"`) to insert data blocks.
  2. The engine automatically clones row styles/borders and shifts all downstream `=SUM(...)`, `=AVERAGE(...)`, and KPI formula coordinates via AST parsing.
- **Recalculation & Quality Verification**:
  1. Run `xlsx.recalc` to refresh cached formula results (`<v>`) via headless LibreOffice.
  2. Run `xlsx.validate` to verify formula syntax, merged-cell border consistency, and DrawingML preservation.

---

## 2. Python SDK (`doctools.api`) & CLI Quick Examples

```python
from doctools.api import (
    load_workbook_model,
    read_table,
    get_key_values_by_labels,
    TableIslandDetector,
    xlsx_detect_tables,
    xlsx_mutate_block,
)
from doctools.operations.xlsx import xlsx_recalc, xlsx_validate
```

```bash
docwright schema xlsx.mutate_block
docwright xlsx.mutate_block --spec insert_rows.json
docwright compact-json extracted.json --path sheets.Summary -o compact.json
docwright profile-scaffold template.xlsx --output profile.yaml
```
