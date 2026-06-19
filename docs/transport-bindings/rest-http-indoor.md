# Indoor Endpoints (REST/HTTP Binding)

> Protocol specification: [Indoor Extension](../extensions/indoor.md)
> This document defines the REST/HTTP transport contract for Indoor operations. It does not redefine protocol semantics.

## Fundamentals

- **Base URL**: relative to the Provider base URL advertised via discovery
- **Content type**: `application/json` for all requests and responses
- **Transport**: all endpoints MUST be served over HTTPS
- **Authentication**: OAuth2 Bearer token, required on every request

## Operations

| operation | method | endpoint | scope |
|---|---|---|---|
| Create or Receive Indoor Order | `POST` | `/v1/orders/indoor` | `orders.indoor.write` |
| Query Indoor Account | `GET` | `/v1/orders/indoor/accounts` | `orders.indoor.read` |
| Update Indoor Account | `PATCH` | `/v1/orders/indoor/accounts` | `orders.indoor.write` |
| Register Partial Payment | `POST` | `/v1/orders/indoor/accounts/payments` | `orders.indoor.payment.write` |
| Close Indoor Account | `POST` | `/v1/orders/indoor/accounts/close` | `orders.indoor.close.write` |

Mutation operations (`POST`, `PATCH`) MUST return `202 Accepted`.
Query operations (`GET`) MUST return `200 OK` with the account snapshot.

## HTTP Headers

| header | required | description |
|---|---|---|
| `Authorization` | YES | `Bearer <token>` with the required operation scope |
| `Content-Type` | YES (body) | `application/json` |
| `Accept` | SHOULD | `application/json` |
| `X-Request-Id` | SHOULD | Correlation identifier for tracing and idempotency |

## Error Status Codes

| status | when |
|---|---|
| `400 Bad Request` | Malformed payload or invalid parameters |
| `401 Unauthorized` | Missing or invalid credentials |
| `403 Forbidden` | Valid credentials but insufficient scope |
| `404 Not Found` | Account or order not found |
| `409 Conflict` | State or version conflict (e.g., update to a closed account) |
| `422 Unprocessable Entity` | Invalid state transition or business rule violation |
| `500 Internal Server Error` | Unexpected server failure |

Error responses SHOULD follow the [Error Model](../protocol/error-handling.md).

---

## Create or Receive Indoor Order

```http
POST /v1/orders/indoor HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
X-Request-Id: req-001

{
  "order": {
    "id": "order-9001",
    "indoor": {
      "operationMode": "TABLE",
      "identifier": "A12",
      "originChannel": "WAITER_TABLET",
      "consumptionType": "ON_PREMISE",
      "notifyOriginator": true
    }
  }
}
```

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{
  "status": "accepted",
  "operation": "createOrReceiveIndoorOrder"
}
```

---

## Query Indoor Account

```http
GET /v1/orders/indoor/accounts?operationMode=TABLE&identifier=A12 HTTP/1.1
Authorization: Bearer <token>
Accept: application/json
X-Request-Id: req-002
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "account": {
    "operationMode": "TABLE",
    "identifier": "A12",
    "accountId": "acc-301",
    "status": "OPEN",
    "items": [
      { "id": "item-1", "name": "Burger", "quantity": 1 }
    ]
  }
}
```

---

## Update Indoor Account

```http
PATCH /v1/orders/indoor/accounts HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
X-Request-Id: req-003

{
  "account": {
    "operationMode": "TABLE",
    "identifier": "A12",
    "items": [
      { "id": "item-2", "name": "Fries", "quantity": 1 }
    ]
  }
}
```

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{
  "status": "accepted",
  "operation": "updateIndoorAccount"
}
```

---

## Register Partial Payment

```http
POST /v1/orders/indoor/accounts/payments HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
X-Request-Id: req-004

{
  "account": {
    "operationMode": "TABLE",
    "identifier": "A12"
  },
  "payment": {
    "amount": { "value": 45.00, "currency": "BRL" },
    "method": "CREDIT_CARD",
    "items": ["item-1", "item-2"]
  }
}
```

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{
  "status": "accepted",
  "operation": "registerPartialPayment"
}
```

---

## Close Indoor Account

```http
POST /v1/orders/indoor/accounts/close HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
X-Request-Id: req-005

{
  "account": {
    "operationMode": "TABLE",
    "identifier": "A12"
  }
}
```

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{
  "status": "accepted",
  "operation": "closeIndoorAccount"
}
```

---

## Conformance

**Provider MUST:**

- Return `202 Accepted` for all mutation operations (`POST`, `PATCH`)
- Return `200 OK` with account snapshot for `GET` queries
- Serve all endpoints over HTTPS
- Enforce scope-based authorization on every request
- Return `409 Conflict` when a Consumer attempts to update a `CLOSED` account
- Return `404 Not Found` when account lookup yields no result

**Consumer MUST:**

- Send a valid `Authorization: Bearer <token>` header on every request
- Send `Content-Type: application/json` on all requests with a body
- Use `operationMode` + `identifier` as the primary lookup key on initial access

## OpenAPI Artifact

- Download: [rest-http-indoor.openapi.yaml](../reference/v2/rest-http-indoor.openapi.yaml)
