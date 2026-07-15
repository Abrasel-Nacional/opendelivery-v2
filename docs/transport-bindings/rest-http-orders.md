# Orders Capability - REST Binding

This document specifies the REST/HTTP binding for [Orders Capability](../protocol/orders.md).
It defines transport behavior and does not redefine capability semantics.

## Protocol Fundamentals

### Discovery

Order endpoint support MUST be discoverable through the `orders` capability metadata.
Participants MUST validate counterpart discovery data before invoking operations.

### Base URL

All order endpoints are relative to the provider base URL advertised in discovery.

### Content Types

- Requests: `application/json`
- Responses: `application/json`

### Transport Security

All endpoints in this binding MUST be served over HTTPS.

## Operations

| operation | provider | consumer | method | endpoint | description |
|---|---|---|---|---|---|
| `getOrder` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | `GET` | `/v1/orders/{orderId}` | Retrieve current order snapshot |
| `confirmOrder` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | `POST` | `/confirm` | Confirm order for processing |
| `setPreparing` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | `POST` | `/preparing` | Mark order as preparing |
| `setReadyForPickup` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | `POST` | `/readyForPickup` | Mark order as ready |
| `dispatchOrder` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` or `DELIVERY_PLATFORM` | `POST` | `/dispatch` | Mark order as dispatched |
| `setDelivered` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | `POST` | `/delivered` | Mark order as delivered |
| `cancelOrder` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | `POST` | `/cancel` | Resolve cancellation |
| `concludeOrder` | `SOFTWARE_SERVICE` or `ORDERING_APPLICATION` | counterpart participant | `POST` | `/conclude` | Mark logical closure |

Endpoint naming MAY vary by profile agreement, but lifecycle semantics MUST match [Orders Capability](../protocol/orders.md).

## HTTP Headers

| header | required | description |
|---|---|---|
| `Authorization` | YES | OAuth2 Bearer token |
| `Content-Type` | YES (for body) | Must be `application/json` |
| `Accept` | SHOULD | Expected `application/json` |

## Response Contract

### Success Status Codes

| endpoint type | status | meaning |
|---|---|---|
| Query endpoint (`GET`) | `200 OK` | Order snapshot returned |
| Mutation endpoints (`POST`) | `202 Accepted` | Accepted for asynchronous processing |

### Error Status Codes

| status | when | body |
|---|---|---|
| `400 Bad Request` | invalid payload/params | ODP error model |
| `401 Unauthorized` | missing/invalid credentials | ODP error model |
| `403 Forbidden` | missing required scope | ODP error model |
| `404 Not Found` | order not found | ODP error model |
| `409 Conflict` | state/version conflict | ODP error model |
| `422 Unprocessable Entity` | invalid transition/business rule violation | ODP error model |
| `500 Internal Server Error` | unexpected server failure | ODP error model |

Error payloads SHOULD follow [Error Model](../protocol/error-handling.md).

## Conformance

Platforms and ordering applications implementing this binding:

- MUST authenticate requests and include required scopes.
- MUST treat webhook/event updates as primary synchronization channel when supported.
- SHOULD use polling/query endpoints for reconciliation and fallback.

Software services implementing this binding:

- MUST preserve Orders lifecycle semantics from the capability specification.
- MUST reject invalid lifecycle transitions.
- MUST provide deterministic status projection per profile rules.

## Related Bindings

- [Indoor Endpoints (Orders Extension)](rest-http-indoor.md)
