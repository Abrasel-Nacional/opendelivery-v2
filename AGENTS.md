# Open Delivery v2 — Agent instructions

Permanent project rules for documentation and specs. Follow these on every change.

## Language policy (mandatory)

| Layer | Language | Files |
|-------|----------|--------|
| **OpenAPI / ReDoc contract** | **English only** | `docs/reference/v2/*.openapi.yaml`, ReDoc pages under `docs/reference/` |
| **Protocol / Guide** | **Bilingual (PT + EN)** | `docs/protocol/**`, `docs/guide/**`, `docs/documentation/**`, landing, etc. |

### Rules

1. **OpenAPI is always English.** Descriptions, summaries, examples labels, tag names, `info`, error messages in examples, and ReDoc narrative blocks MUST be English. Do not publish Portuguese (or any other language) inside OpenAPI YAML.
2. **Guides are bilingual.** Default locale is Portuguese (`page.md`). English is `page.en.md` (mkdocs-static-i18n suffix). When you create or substantially rewrite a guide page, update **both** PT and EN (or add the missing `.en.md`).
3. **Technical identifiers stay English everywhere:** schemas, fields, enums, events, paths, operationIds, JSON examples keys/values that are protocol tokens (`IN_USE`, `ACCOUNT_OPENED`, etc.).
4. **ReDoc shell notes** (`docs/reference/*.md`) may be short and bilingual (PT default + `.en.md`), but the **contract body** is the English OpenAPI file.
5. Do **not** treat Indoor or any capability as an exception to OpenAPI-in-English.

## Capability model: Guide ↔ OpenAPI

| Layer | Role |
|-------|------|
| **Guide** (`docs/protocol/…`) | Helper for newcomers: concepts, roles, flows, checklists. Not the field-level normative source. |
| **OpenAPI** (`docs/reference/v2/…`) | Self-contained normative contract: endpoints, fields, MUST/MAY, errors, JSON examples. Enough to implement alone. |

Cross-link both ways (`externalDocs` + guide callouts). See `STRUCTURE.md` for the full checklist.

## Other

- Committee minutes under `docs/reference/v2/comites/` are reference only; do not invent normative rules without committee basis.
- `docs/transport-bindings/**` is legacy and excluded from the published site.
- Prefer `python -m mkdocs build --strict` after doc/spec changes.
