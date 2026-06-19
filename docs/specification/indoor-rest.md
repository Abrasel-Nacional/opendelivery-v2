# REST Binding — Indoor

Normative source: [Indoor Extension](./indoor.md).

This page defines the REST/HTTP transport contract for Indoor Extension operations.
Capability semantics are defined in the source document; this page covers transport behavior only.

## Base URL

Declared per participant in the discovery document under `capabilities[name=indoor].endpoint`.

## Endpoints

| Operation | Method | Path | Auth | Scope |
|---|---|---|---|---|
| `getAccount` | `GET` | `/indoor/accounts/{accountId}` | Required | `indoor.read` |
| `updateAccount` | `POST` | `/indoor/accounts/{accountId}/update` | Required | `indoor.write` |
| `registerPayment` | `POST` | `/indoor/accounts/{accountId}/payments` | Required | `indoor.write` |
| `closeAccount` | `POST` | `/indoor/accounts/{accountId}/close` | Required | `indoor.write` |

## Request and Response Examples

### `getAccount`

**Request:**

```
GET /indoor/accounts/account-t5-001
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "id": "account-t5-001",
  "merchantId": "merchant-001",
  "status": "OPEN",
  "operationMode": "TABLE",
  "identifier": "T5",
  "orderIds": ["order-abc123", "order-abc456"],
  "totals": {
    "subtotal": 12000,
    "total": 12000
  },
  "openedAt": "2026-06-01T19:30:00Z"
}
```

### `registerPayment`

**Request:**

```
POST /indoor/accounts/account-t5-001/payments
Authorization: Bearer {token}
Content-Type: application/json

{
  "method": "CARD",
  "amount": 6000
}
```

**Response (202 Accepted):**

```json
{
  "id": "pay-001",
  "method": "CARD",
  "amount": 6000,
  "registeredAt": "2026-06-01T20:15:00Z"
}
```

### `closeAccount`

**Request:**

```
POST /indoor/accounts/account-t5-001/close
Authorization: Bearer {token}
Content-Type: application/json

{
  "reason": "Customer settled all payments"
}
```

**Response (202 Accepted):** No body.

## Error Codes

| Code | HTTP | Description |
|---|---|---|
| `ACCOUNT_NOT_FOUND` | 404 | Account identifier not found |
| `ACCOUNT_ALREADY_CLOSED` | 409 | Account is already in CLOSED state |
| `ACCOUNT_IN_PAYMENT` | 409 | Account is locked in IN_PAYMENT state |
| `INVALID_OPERATION_MODE` | 422 | Operation mode not recognized |
