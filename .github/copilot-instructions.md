---
applyTo: "**"
---

## Project rules (see AGENTS.md)

- **OpenAPI / ReDoc contracts are always English** (`docs/reference/v2/*.openapi.yaml`).
- **Guides are bilingual:** Portuguese default (`page.md`) + English (`page.en.md`).
- Technical identifiers (schemas, fields, enums, events, paths) stay English in all locales.
- Capability model: Guide = helper; OpenAPI = self-contained normative contract. Cross-link both ways.

## Orders domain (extra)

- Treat orders as coordination entities, not workflows.
- Do not assume synchronous behavior.
- Do not infer event order unless explicitly defined.
- Separate states from events clearly.
- Always reference order profiles when discussing obligations.
