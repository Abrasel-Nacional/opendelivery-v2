# Error handling

This page describes the shared **HTTP error model** used by Open Delivery V2 API Specs.

**Normative source:** error responses and schemas in each [API Spec](index.md). This summary guides implementers; on conflict, **API Spec wins**.

---

## Principles

1. Error responses are machine-readable (stable `code`).
2. Classification preserves meaning for automation (retry, UX, audit).
3. Producers do not emit business success when processing failed.
4. Cancellation and state-transition failures are distinguishable by code.

---

## Error envelope (common shape)

| field | type | required | description |
|---|---|---|---|
| `error.code` | string | YES | Stable machine-readable code |
| `error.message` | string | YES | Human-readable message |
| `error.details` | object | NO | Additional structured context |
| `error.retryable` | boolean | NO | Whether retry is safe |
| `error.timestamp` | string | NO | ISO 8601 instant |

### Example

```json
{
 "error": {
 "code": "ORDER_NOT_FOUND",
 "message": "Unknown order identifier for this merchant scope",
 "retryable": false
 }
}
```

---

## HTTP status codes (typical use)

| status | when |
|---|---|
| `400 Bad Request` | Malformed payload or invalid parameters |
| `401 Unauthorized` | Missing or invalid credentials |
| `403 Forbidden` | Valid credentials, insufficient scope |
| `404 Not Found` | Resource not found |
| `409 Conflict` | State or version conflict |
| `422 Unprocessable Entity` | Invalid transition or business rule |
| `429 Too Many Requests` | Rate limit |
| `500 Internal Server Error` | Unexpected internal failure |
| `202 Accepted` | Accepted for async processing (**not an error**) |

Many ODP V2 mutations are **async-first** (`202`). Confirm outcomes via events or `GET`, per capability.

---

## Retries

When `error.retryable` is `true`, the client may retry after a delay.

Recommendation: exponential backoff with jitter (e.g. 1s → 2s → 4s; about 3 attempts max).

- On async mutations (`202`), **repeating an already applied operation** (e.g. a second `confirm` while the order is already `CONFIRMED`) is **not an error** — see [duplicate lifecycle operations](conventions.md#duplicate-lifecycle-operations).
- Do not confuse that with an **invalid** transition (incompatible state), which does return `4xx`.

---

## State transition errors

Return an error **only** when the transition is **impossible** in the current state (e.g. confirm an order that is already `CANCELLED`). An order **already in the operation’s target state** is **not** an error — return `202` (see conventions).

Example of an invalid transition:

```json
{
 "error": {
 "code": "INVALID_STATE_TRANSITION",
 "message": "Cannot confirm an order in CANCELLED status",
 "retryable": false,
 "details": {
 "currentStatus": "CANCELLED",
 "attemptedTransition": "confirm"
 }
 }
}
```

Exact codes and HTTP status: capability API Spec.

---

<div class="od-related">
  <p class="od-related__label">Related</p>
  <ul class="od-related__list">
    <li><a href="conventions.md">General conventions</a> — dates, pagination, duplicate lifecycle ops</li>
    <li><a href="authentication.md">Authentication</a> — OAuth, scopes, webhook signing</li>
    <li><a href="../protocol/principles.md">Protocol principles</a> — domain mental model</li>
  </ul>
</div>
