# General rules and conventions

!!! warning "Release Candidate (V2.0.0-rc)"
    Conventions for **V2.0.0-rc**, under ecosystem validation. Details: [Evolution](../protocol/evolution.md) · [Changelog](../guide/changelog.md).

This page summarizes **shared conventions** of the Open Delivery V2 REST/HTTP API.

**Normative source:** each API Spec spec under [API reference](index.md). If this summary and an API Spec file disagree, **API Spec wins**.

For domain mental models (roles, flows, status vs events), use the **Protocol** tab.

---

## Normative keywords

In API Specs (English), `MUST`, `MUST NOT`, `SHOULD`, and `MAY` follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

---

## Interoperability

Expected behavior across capabilities (details in API Specs):

1. Producers include all required schema fields.
2. Consumers validate required fields.
3. Consumers tolerate unknown additional fields (additive evolution).
4. Participants do not infer unsupported state transitions.
5. Events received more than once are **deduplicated** (by event / fact id) without re-applying business side effects.

---

## Security (overview)

- Authentication and scopes: [Authentication](authentication.md) and [Discovery](discovery.md).
- Secrets must not appear in logs or traces.
- Webhooks require signature verification when the contract requires it.

---

## Timestamps

Date-time fields use **ISO 8601** with an explicit timezone.

- Recommended (UTC): `2026-07-01T14:30:00Z`
- Offset accepted: `2026-07-01T11:30:00-03:00`
- Date-only values do not replace timestamps

---

## Identifiers

Entity identifiers (`id`) are typically:

- Opaque strings (no meaning derived from the value)
- UUID v4 recommended
- Unique within the declared scope
- Stable after creation

Resource-specific rules are in each capability API Spec.

---

## Pagination

List endpoints that return collections usually support pagination. Common pattern:

| parameter | type | description |
|---|---|---|
| `page` | integer | Page number (from 1) |
| `pageSize` | integer | Items per page |

Example metadata:

```json
{
 "pagination": {
 "page": 1,
 "pageSize": 20,
 "total": 150
 }
}
```

Exact parameters and defaults: see each API Spec operation.

---

## Duplicate lifecycle operations

<a id="duplicidade-de-operacoes-de-ciclo-de-vida"></a>

Rule aligned with the Architecture Committee (2026-03-26) and the Keeta case: repeated calls **must not break the flow** when the target state is **already reached**.

In V1, docs suggested `HTTP 422` for synchronous reprocessing of the same fact and, on the async path, re-presenting the event via polling. V2 is **async-first** (`202 Accepted`).

### Universal default (V2)

For order progression operations (and similar) that return `202`:

| Situation | HTTP response | Business effect |
|---|---|---|
| **Valid** transition not yet applied | `202 Accepted` | Accept processing; outcome via event / `GET` |
| Same operation **already applied** (e.g. `POST …/confirm` while order is already `CONFIRMED`) | **`202 Accepted`** | **No new transition**; receiver **MAY** re-present the corresponding event (webhook/polling) |
| **Invalid** transition (e.g. confirm a `CANCELLED` order) | Error `4xx` (e.g. `409` / `422` per the API Spec) | No state change |

Implementers **MUST NOT** treat a repeat of an **already successfully completed** operation as a business failure with `422`/`409` only because it “was already done”. That V1 anti-pattern broke POS stacks with double confirmation.

**Source of truth** remains queryable **status** and **events** — the HTTP response of the `POST` does not close business logic.

Normative detail: [Orders API Spec](orders.md) (and other capabilities using the same async pattern).

---

## Compatibility

- Existing required fields are not removed in backward-compatible releases
- Enum extensions should be additive; consumers tolerate unknown values when possible
- Breaking changes use versioning (see [Evolution](../protocol/evolution.md))

---

<div class="od-related">
  <p class="od-related__label">Related</p>
  <ul class="od-related__list">
    <li><a href="error-handling.md">Error handling</a> — envelope and HTTP codes</li>
    <li><a href="authentication.md">Authentication</a> — OAuth, scopes, webhooks</li>
    <li><a href="discovery.md">Discovery</a> — well-known manifest</li>
    <li><a href="index.md">API overview</a> — specs per capability</li>
  </ul>
</div>
