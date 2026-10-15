---
name: docwright-xlsx
description: Operational guide and decision tree for Excel spreadsheet engineering, 2D block mutation, and formula shifts.
---

# Docwright XLSX Engineering Skill

Use this skill whenever reading, creating, expanding, repairing, or mutating Excel spreadsheets (`.xlsx`).

---

## 1. Golden Rules of Spreadsheet Engineering

1. **Never write static numbers into summary cells**: Always generate dynamic formulas (`=SUM(B5:B20)`, `=COUNTIF(...)`).
2. **Never create blank `Workbook()` from scratch when modifying**: Load the existing template with `data_only=False` to preserve corporate logos and DrawingML shapes.
3. **Handle merged cells safely**: Assign values strictly to the Top-Left cell of a merged range and synchronize perimeter borders.

---

## 2. Standard 2D Block Mutation Workflow

When inserting or updating rows/columns in an existing sheet:

```
[ Step 1: xlsx.inspect / xlsx.detect_tables ]
                     ↓
[ Step 2: xlsx.mutate_block (with shift_direction='down') ]
                     ↓
[ Step 3: xlsx.recalc (recalculates formula cache <v>) ]
                     ↓
[ Step 4: xlsx.validate (audits 13 Universal Gates UG-01..13) ]
```

- `xlsx.mutate_block` tokenizes dependent formulas using an AST parser and shifts row indices automatically.
- `xlsx.validate` checks formula validity (`#REF!`), border synchronization, and DrawingML collision before saving.
