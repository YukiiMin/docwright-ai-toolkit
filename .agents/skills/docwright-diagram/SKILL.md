---
name: docwright-diagram
description: Operational guide and topological principles for Draw.io mxGraphModel diagram engineering.
---

# Docwright Technical Diagrams Engineering Skill

Use this skill whenever generating, editing, or rendering technical architecture diagrams for Draw.io (`.drawio`).

---

## 1. Core Topological Invariants

1. **Pure Native `<mxCell>` Hierarchy (`MX_INV_01`)**: All vertices and edges must be children of `parent="1"`. Never embed raw Mermaid or PlantUML inside XML tags.
2. **Orthogonal Routing (`MX_INV_04`)**: Use `edgeStyle=orthogonalEdgeStyle;` with standard perimeter ports (`exitX, exitY, entryX, entryY` at `0.0`, `0.5`, `1.0`).
3. **Dynamic Geometry Scaling (`MX_INV_05`)**: Node heights must scale based on field count ($H = 43 \times (N + 1)$). Maintain a minimum traffic corridor clearance of $\ge 60\text{px}$.
4. **Monochrome Line-Art (`MX_INV_07`)**: Default to academic black-and-white styling (`#ffffff` fill, `#000000` stroke).

---

## 2. Standard Diagram Generation Workflow

```
[ Step 1: Formulate Declarative Topology Spec (JSON) ]
                     ↓
[ Step 2: diagram.build (generates native .drawio file) ]
                     ↓
[ Step 3: diagram.render_raster (high-DPI PNG) or diagram.render_svg ]
```
