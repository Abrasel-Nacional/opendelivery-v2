# REST Binding — Orders

Normative source: [Orders Capability](./orders.md).

This page defines the REST/HTTP transport contract for Orders Capability operations.
Capability semantics are defined in the source document; this page covers transport behavior only.

## Base URL

Declared per participant in the discovery document under `capabilities[name=orders].endpoint`.

## Endpoints

| Operation | Method | Path | Auth | Scope |
|---|---|---|---|---|
| `getOrder` | `GET` | `/orders/{orderId}` | Required | `orders.read` |
| `confirmOrder` | `POST` | `/orders/{orderId}/confirm` | Required | `orders.write` |
| `setPreparing` | `POST` | `/orders/{orderId}/preparing` | Required | `orders.write` |
| `setReadyForPickup` | `POST` | `/orders/{orderId}/readyForPickup` | Required | `orders.write` |
| `dispatchOrder` | `POST` | `/orders/{orderId}/dispatch` | Required | `orders.write` |
| `setDelivered` | `POST` | `/orders/{orderId}/delivered` | Required | `orders.write` |
| `cancelOrder` | `POST` | `/orders/{orderId}/cancel` | Required | `orders.write` |
| `concludeOrder` | `POST` | `/orders/{orderId}/conclude` | Required | `orders.write` |

## Headers

| Header | Required | Description |
|---|---|---|
| `Authorization` | YES | `Bearer {token}` |
| `Content-Type` | YES (with body) | `application/json` |
| `X-Request-Id` | SHOULD | Correlation identifier for idempotency |

## Response Contract

| Endpoint Type | Status | Meaning |
|---|---|---|
| `GET` | `200 OK` | Order snapshot returned |
| `POST` lifecycle | `202 Accepted` | Accepted for asynchronous processing |

## Request and Response Examples

### `getOrder`

**Request:**

```
GET /orders/order-abc123
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "id": "order-abc123",
  "merchantId": "merchant-001",
  "status": "CONFIRMED",
  "profile": "DELIVERY",
  "createdAt": "2026-06-01T12:00:00Z",
  "updatedAt": "2026-06-01T12:02:00Z",
  "items": [
    {
      "id": "li-1",
      "itemId": "item-burger",
      "name": "Classic Burger",
      "quantity": 2,
      "unitPrice": 2500,
      "totalPrice": 5000
    }
  ],
  "totals": {
    "subtotal": 5000,
    "deliveryFee": 500,
    "total": 5500
  },
  "customer": {
    "id": "cust-001",
    "name": "Maria Silva"
  }
}
```

### `confirmOrder`

**Request:**

```
POST /orders/order-abc123/confirm
Authorization: Bearer {token}
Content-Type: application/json

{
  "estimatedMinutes": 30
}
```

**Response (202 Accepted):** No body.

### `cancelOrder`

**Request:**

```
POST /orders/order-abc123/cancel
Authorization: Bearer {token}
Content-Type: application/json

{
  "cancellationCode": "OUT_OF_STOCK",
  "cancellationReason": "Item unavailable at this time",
  "cancelledBy": "MERCHANT"
}
```

**Response (202 Accepted):** No body.

## Error Codes

| Code | HTTP | Description |
|---|---|---|
| `ORDER_NOT_FOUND` | 404 | Order identifier not found for this merchant scope |
| `INVALID_TRANSITION` | 422 | Status transition not allowed from current state |
| `ORDER_ALREADY_CANCELLED` | 409 | Order is already in a cancelled state |
| `INVALID_CANCELLATION_CODE` | 422 | Cancellation code not recognized |
