# Open Delivery v2 — Agent instructions

Permanent project rules for documentation and specs. Follow these on every change.

## Language policy (mandatory)

| Layer | Language | Files |
|-------|----------|--------|
| **API Spec (OpenAPI YAML)** | **English only** | `docs/reference/v2/*.openapi.yaml`; short shells under `docs/reference/` |
| **Protocol / Guide** | **Bilingual (PT + EN)** | `docs/protocol/**`, `docs/guide/**`, `docs/documentation/**`, landing, etc. |

### Rules

1. **API Specs are always English.** User-facing prose says “especificação da API” / “API Spec”; the **format** is OpenAPI (YAML). Do not mention ReDoc in published text (it is only the site renderer). Descriptions, summaries, examples, tag names, `info`, and error messages in specs MUST be English — never Portuguese inside OpenAPI YAML.
2. **Guides are bilingual.** Default locale is Portuguese (`page.md`). English is `page.en.md` (mkdocs-static-i18n suffix). When you create or substantially rewrite a guide page, update **both** PT and EN (or add the missing `.en.md`).
3. **Technical identifiers stay English everywhere:** schemas, fields, enums, events, paths, operationIds, JSON examples keys/values that are protocol tokens (`IN_USE`, `ACCOUNT_OPENED`, etc.).
4. **API reference shell notes** (`docs/reference/*.md`) may be short and bilingual (PT default + `.en.md`), but the **contract body** is the English OpenAPI file.
5. Do **not** treat Indoor or any capability as an exception to English API Specs.

## Documentation model: Guide · Protocol · API Spec

| Layer | Role |
|-------|------|
| **Guide** (`docs/guide/…`, landing, concepts) | Onboarding: getting started, roles paths, migration, changelog. Non-normative. |
| **Protocol** (`docs/protocol/…`) | Domain narrative: concepts, flows, responsibilities. Helper for humans — **not** the field-level normative source. |
| **API Spec** (`docs/reference/v2/…`) | Self-contained **normative** contract: endpoints, fields, MUST/MAY, errors, JSON examples. Enough to implement alone. |

There is **no transport-binding layer**. Do not reintroduce “protocol vs binding”, multi-binding roadmaps, or transport-agnostic protocol-as-separate-spec language.

Cross-link Protocol ↔ API Spec (`externalDocs` + guide callouts). See `STRUCTURE.md` for the full checklist.

## Other

- Committee minutes under `docs/reference/v2/comites/` are reference only; do not invent normative rules without committee basis.
- `docs/transport-bindings/**` is legacy and excluded from the published site — do not link it from published docs.
- Prefer `python -m mkdocs build --strict` after doc/spec changes.
