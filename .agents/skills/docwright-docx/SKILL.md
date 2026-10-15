---
name: docwright-docx
description: Complete operational guide and decision tree for Word (DOCX) engineering via Docwright AI Toolkits.
---

# Docwright DOCX Engineering Skill

Use this skill whenever creating, modifying, patching, or reconstructing Microsoft Word documents (`.docx`).

---

## 1. Decision Tree: Choosing the Compilation Path

```
Does the user have an existing .docx corporate template with Jinja tags?
├── YES ──> Use Path A: docx.render_template
└── NO  ──> Use Path B: docx.build_document (DocSpec DSL)
```

### Path A: Template Rendering (`docx.render_template`)
- Load existing template containing `{{ variable_name }}` or `{% for row in rows %}`.
- Provide JSON context dictionary.
- The engine sanitizes run boundaries and preserves all corporate header/footer styling.

### Path B: Algorithmic Synthesis (`docx.build_document`)
- Define page layout (`orientation`, `margin_*_cm`).
- Define blocks:
  - `heading` (level 1-3)
  - `paragraph` (typed `runs` with `bold`, `italic`, `underline`, `font_size_pt`)
  - `table` (`headers`, `col_widths`, `rows`)
- Automatically receives `<w:cantSplit/>` on rows and `<w:tblHeader/>` on header rows.

---

## 2. Scanned PDF 1:1 Reconstruction Pipeline

When converting a scanned paper form or PDF into Word:
1. `docx.measure_pdf_layout`: Extract physical table geometry and column ratios.
2. `docx.populate_layout_text`: Map extracted text into physical cell IDs (`c0_0`).
3. `docx.compile_layout_spec`: Compile to normalized `DocSpec`.
4. `docx.build_document`: Generate the final pixel-accurate Word document.
