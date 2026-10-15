# Rule: Docwright AI Sovereignty & Office Document Integrity

> **Scope**: Mandatory for any AI Agent (Cursor, Claude Code, Antigravity, Windsurf, Codex) operating on office documents (`.docx`, `.xlsx`, `.drawio`) in this workspace.  
> **Status**: Non-Negotiable Hard Constraint.

---

## 1. Zero Ad-Hoc Library Scripting (Strict Prohibition)

- **NEVER** write ad-hoc Python one-liner scripts or scratch scripts (`python -c "import openpyxl..."`, `python -c "import docx..."`) to inspect, modify, or generate office files.
- Bypassing Docwright strips DrawingML logos, violates ECMA-376 canonical XML schemas, destroys formula dependency trees, and causes silent file corruption.
- All operations MUST route through registered **Docwright MCP Tools** or the **Unified CLI Dispatcher** (`docwright <tool> --spec <file.json>`).

---

## 2. Execution Hierarchy

1. **Tier 1 (Preferred)**: MCP Tools (`docx.*`, `xlsx.*`, `diagram.*`) via `docwright-mcp`.
2. **Tier 2 (CLI Fallback)**: Unified CLI Dispatcher:
   ```bash
   # 1. Discover tool schema
   docwright schema <tool_name>

   # 2. Execute via structured spec
   docwright <tool_name> --spec payload.json
   ```

---

## 3. Fail-Closed Protocol

- If a command fails or raises an unhandled exception:
  1. Attempt a MAXIMUM of 1 schema-compliant correction.
  2. If failure persists, **STOP IMMEDIATELY**, report the raw traceback, and await user feedback.
  3. NEVER synthesize gate passes (`UG-*`) or claim files are valid without tool verification logs.
