# REST Binding — Logistics

Normative source: [Logistics Capability](./logistics.md).

This page defines the REST/HTTP transport contract for Logistics Capability operations.

## Base URL

Declared per participant in the discovery document under `capabilities[name=logistics].endpoint`.

## Endpoints

| Operation | Method | Path | Auth | Scope |
|---|---|---|---|---|
| `requestQuote` | `POST` | `/logistics/quotes` | Required | `logistics.write` |
| `requestDelivery` | `POST` | `/logistics/deliveries` | Required | `logistics.write` |
| `getDeliveryStatus` | `GET` | `/logistics/deliveries/{deliveryId}` | Required | `logistics.read` |
| `cancelDelivery` | `POST` | `/logistics/deliveries/{deliveryId}/cancel` | Required | `logistics.write` |
| `reportIncident` | `POST` | `/logistics/deliveries/{deliveryId}/incidents` | Required | `logistics.write` |

## Request and Response Examples

### `requestQuote`

**Request:**

```
POST /logistics/quotes
Authorization: Bearer {token}
Content-Type: application/json

{
  "orderId": "order-abc123",
  "merchantId": "merchant-001",
  "pickup": {
    "street": "Av. Paulista, 1000",
    "city": "São Paulo",
    "state": "SP",
    "postalCode": "01310-100"
  },
  "dropoff": {
    "street": "Rua Augusta, 500",
    "city": "São Paulo",
    "state": "SP",
    "postalCode": "01305-100"
  }
}
```

**Response (200 OK):**

```json
{
  "quoteId": "quote-001",
  "merchantId": "merchant-001",
  "fee": 800,
  "eta": "2026-06-01T12:45:00Z",
  "validUntil": "2026-06-01T12:15:00Z"
}
```

### `getDeliveryStatus`

**Request:**

```
GET /logistics/deliveries/delivery-001
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "id": "delivery-001",
  "orderId": "order-abc123",
  "merchantId": "merchant-001",
  "status": "IN_TRANSIT",
  "eta": "2026-06-01T12:45:00Z",
  "updatedAt": "2026-06-01T12:30:00Z"
}
```

## Error Codes

| Code | HTTP | Description |
|---|---|---|
| `DELIVERY_NOT_FOUND` | 404 | Delivery identifier not found |
| `QUOTE_EXPIRED` | 422 | Quote no longer valid |
| `DELIVERY_AREA_NOT_COVERED` | 422 | Dropoff outside service area |
| `DELIVERY_ALREADY_CANCELLED` | 409 | Delivery is already cancelled |
