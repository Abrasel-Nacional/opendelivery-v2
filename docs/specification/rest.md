# REST Transport Binding

This document defines the REST/HTTP transport binding for the Open Delivery Protocol.

Transport bindings define communication conventions. They do not redefine capability semantics.
All capability semantics are defined in the [Specification](../specification/overview.md).

## Overview

ODP uses HTTP/1.1 or higher with RESTful patterns.

- **Content-Type:** All requests and responses MUST use `application/json`.
- **Methods:** `GET` for retrieval; `POST` for mutations and lifecycle transitions.
- **Status codes:** Standard HTTP status codes apply (see below).
- **Security:** All endpoints MUST be served over HTTPS (TLS).

## Base URL

Each participant declares its base URL in the discovery document under the capability's
`endpoint` field:

```json
{
  "capabilities": [
    {
      "name": "orders",
      "endpoint": "https://api.myservice.com/opendelivery/v2"
    }
  ]
}
```

All capability paths are appended to the declared base URL:

```
POST https://api.myservice.com/opendelivery/v2/orders/{orderId}/confirm
```

## Standard Headers

| Header | Required | Description |
|---|---|---|
| `Authorization` | YES (protected endpoints) | `Bearer {token}` — OAuth2 access token |
| `Content-Type` | YES (with body) | Must be `application/json` |
| `Accept` | SHOULD | Expected `application/json` |
| `X-Request-Id` | SHOULD | Idempotency and correlation identifier |

## Status Codes

### Success

| Code | Meaning |
|---|---|
| `200 OK` | Resource returned (GET) or mutation result returned |
| `202 Accepted` | Mutation accepted for asynchronous processing |
| `204 No Content` | Operation succeeded with no response body |

### Client Errors

| Code | Meaning |
|---|---|
| `400 Bad Request` | Invalid or malformed request payload |
| `401 Unauthorized` | Missing or invalid credentials |
| `403 Forbidden` | Valid credentials but insufficient scope |
| `404 Not Found` | Resource not found |
| `409 Conflict` | Request conflicts with current state |
| `422 Unprocessable Entity` | Semantically invalid request |
| `429 Too Many Requests` | Rate limit exceeded |

### Server Errors

| Code | Meaning |
|---|---|
| `500 Internal Server Error` | Unexpected server error |
| `503 Service Unavailable` | Temporarily unable to serve; retry with backoff |

## Error Response Format

All error responses MUST include a machine-readable body:

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Order identifier is unknown for this merchant scope",
    "retryable": false
  }
}
```

## Capability Bindings

- [REST — Discovery](./rest-discovery.md)
- [REST — Merchant](./merchant-rest.md)
- [REST — Orders](./orders-rest.md)
- [REST — Indoor](./indoor-rest.md)
- [REST — Customer](./customer-rest.md)
- [REST — Loyalty](./loyalty-rest.md)
- [REST — Logistics](./logistics-rest.md)
