# REST Binding — Merchant

Normative source: [Merchant Capability](./merchant.md).

This page defines the REST/HTTP transport contract for Merchant Capability operations.
Capability semantics are defined in the source document; this page covers transport behavior only.

## Base URL

Declared per participant in the discovery document under `capabilities[name=merchant].endpoint`.

## Endpoints

| Operation | Method | Path | Auth | Scope |
|---|---|---|---|---|
| `getMerchant` | `GET` | `/merchants/{merchantId}` | Required | `merchant.read` |
| `getMenu` | `GET` | `/merchants/{merchantId}/menus/{menuId}` | Required | `merchant.read` |
| `getMenuItem` | `GET` | `/merchants/{merchantId}/items/{itemId}` | Required | `merchant.read` |
| `updateMerchantStatus` | `POST` | `/merchants/{merchantId}/status` | Required | `merchant.write` |

## Request and Response Examples

### `getMerchant`

**Request:**

```
GET /merchants/merchant-001
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "id": "merchant-001",
  "name": "Burger House",
  "status": "ONLINE",
  "address": {
    "street": "Av. Paulista, 1000",
    "city": "São Paulo",
    "state": "SP",
    "country": "BR",
    "postalCode": "01310-100"
  }
}
```

### `getMenu`

**Request:**

```
GET /merchants/merchant-001/menus/menu-01
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "id": "menu-01",
  "merchantId": "merchant-001",
  "name": "Main Menu",
  "categories": [
    {
      "id": "cat-burgers",
      "name": "Burgers",
      "items": [
        {
          "id": "item-burger",
          "name": "Classic Burger",
          "price": 2500,
          "status": "AVAILABLE"
        }
      ]
    }
  ]
}
```

### `updateMerchantStatus`

**Request:**

```
POST /merchants/merchant-001/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "OFFLINE",
  "reason": "Closing early today"
}
```

**Response (202 Accepted):** No body.

## Error Codes

| Code | HTTP | Description |
|---|---|---|
| `MERCHANT_NOT_FOUND` | 404 | Merchant identifier not found |
| `MENU_NOT_FOUND` | 404 | Menu identifier not found |
| `INVALID_STATUS` | 422 | Status value not recognized |
