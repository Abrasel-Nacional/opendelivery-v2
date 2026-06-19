# Indoor Extension

!!! info "Extension"
    Indoor extends the [Orders Capability](./orders.md). It MUST NOT be used independently.

- **Capability name:** `indoor`
- **Extends:** `orders`

## Overview

Indoor enables on-premise order operations — table service, counter service, and tab management —
as an extension of the standard Orders lifecycle.

An **Indoor account** aggregates multiple orders placed at the same physical location into a single
financial unit, supporting incremental ordering, partial payments, and controlled closure.

### Scope

Indoor covers:

- On-premise identification via `operationMode` + `identifier` (table, tab, or counter token)
- Account-based aggregation of multiple orders
- Incremental account updates
- Partial payment registration and account closure
- Indoor account lifecycle events

Indoor does not cover:

- Reservation and waiting-list workflows
- Table occupancy or seating mapping
- Customer-calling UI/UX behavior
- Country-specific fiscal modules

## Participants

| Role | Description | Typical Participant |
|---|---|---|
| **Provider** | Exposes account interfaces; authoritative for account state and financial consistency | Software Service (POS/ERP) |
| **Consumer** | Initiates orders, queries account views, submits payment and close intents | Ordering Application (tablet, kiosk, QR app) |

## Data Model

### Account Lifecycle

| State | Description |
|---|---|
| `OPEN` | Account is active and accepts new orders and updates |
| `IN_PAYMENT` | Payment process started; account locked for new orders |
| `CLOSED` | Account finalized and immutable |

Closed accounts MUST NOT be updated or reopened.

### Indoor Order Context (`order.indoor`)

Attached to each order that belongs to an indoor account.

| Field | Type | Required | Description |
|---|---|---|---|
| `operationMode` | string | YES | `TABLE`, `TAB`, or `COUNTER` |
| `identifier` | string | YES | Operational key identifying the table/tab/counter |
| `accountId` | string | NO | Associated indoor account identifier |
| `sequence` | number | NO | Order sequence within the account |

### Indoor Account

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Account identifier |
| `merchantId` | string | YES | Merchant scope |
| `status` | string | YES | `OPEN`, `IN_PAYMENT`, or `CLOSED` |
| `operationMode` | string | YES | `TABLE`, `TAB`, or `COUNTER` |
| `identifier` | string | YES | Table/tab/counter identifier |
| `orderIds` | array[string] | YES | Orders aggregated under this account |
| `payments` | array[Payment] | NO | Registered partial payments |
| `totals` | object | YES | Account financial summary |
| `openedAt` | string | YES | Account open timestamp (RFC 3339) |
| `closedAt` | string | NO | Account closure timestamp (RFC 3339) |

### Payment Registration

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Payment identifier |
| `method` | string | YES | Payment method (open string; e.g., `CASH`, `CARD`, `PIX`) |
| `amount` | number | YES | Amount paid in minor units (cents) |
| `registeredAt` | string | YES | Registration timestamp (RFC 3339) |

## Operations

| Operation | Provider | Consumer | Description |
|---|---|---|---|
| `getAccount` | Software Service | Ordering Application | Retrieve current account snapshot |
| `updateAccount` | Software Service | Ordering Application | Append orders or update account state |
| `registerPayment` | Software Service | Ordering Application | Register a partial or full payment |
| `closeAccount` | Software Service | Ordering Application | Finalize and close the account |

For transport-specific details, see [REST Binding — Indoor](./indoor-rest.md).

## Example

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
