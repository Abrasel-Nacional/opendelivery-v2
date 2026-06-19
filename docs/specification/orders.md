# Orders Capability

- **Capability name:** `orders`

## Overview

Orders Capability defines interoperable order lifecycle coordination across ordering, merchant
operation, and delivery participants.

### Key Concepts

- Order state is a current business condition and MUST be explicit.
- Order events are immutable lifecycle facts and MUST NOT be interpreted as commands.
- Profile-specific behavior MAY exist, but unsupported transitions MUST NOT be inferred.
- On-premise behavior MUST be modeled through the [Indoor Extension](./indoor.md), not as an
  independent capability.

### Scope

Orders Capability covers:

- Order creation and acceptance
- Preparation and readiness progression
- Dispatch and delivery progression (when applicable)
- Cancellation and logical closure

Orders Capability does not cover:

- On-premise account management details (Indoor extension)
- Merchant catalog publication structures
- Logistics orchestration policy internals

## Participants

| Participant | Provider | Consumer |
|---|---|---|
| **Software Service** | Exposes core order lifecycle operations | Consumes order requests and downstream acknowledgements |
| **Ordering Application** | Exposes callbacks and webhook targets when applicable | Calls order operations and consumes lifecycle updates |
| **Logistics Service** | Exposes delivery-progress updates when delegated | Consumes dispatch and order-delivery context |

## Data Model

### Order

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Unique order identifier |
| `merchantId` | string | YES | Merchant scope for this order |
| `status` | string | YES | Current order status (see lifecycle below) |
| `profile` | string | YES | Order profile (`DELIVERY`, `TAKEOUT`, `INDOOR`) |
| `createdAt` | string | YES | Order creation timestamp (RFC 3339) |
| `updatedAt` | string | YES | Last update timestamp (RFC 3339) |
| `items` | array[OrderItem] | YES | Line items in this order |
| `totals` | object | YES | Financial summary |
| `customer` | object | YES | Customer identification |
| `delivery` | object | NO | Delivery context (required for `DELIVERY` profile) |
| `indoor` | object | NO | Indoor context (required when Indoor extension is active) |

### OrderItem

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Line item identifier |
| `itemId` | string | YES | Catalog item reference |
| `name` | string | YES | Item name at order time |
| `quantity` | number | YES | Ordered quantity |
| `unitPrice` | number | YES | Unit price in minor units (cents) |
| `totalPrice` | number | YES | Total price for this line in minor units (cents) |
| `options` | array[object] | NO | Selected option references |
| `notes` | string | NO | Item-level special instructions |

### Order Status Lifecycle

```
PLACED → CONFIRMED → PREPARING → READY_FOR_PICKUP → DISPATCHED → DELIVERED → CONCLUDED
                                                               ↓
                                                           CANCELLED
```

| Status | Description |
|---|---|
| `PLACED` | Order created by Ordering Application; awaiting merchant confirmation |
| `CONFIRMED` | Merchant confirmed the order; preparation not yet started |
| `PREPARING` | Merchant started preparing the order |
| `READY_FOR_PICKUP` | Order is ready for pickup by courier or customer |
| `DISPATCHED` | Order handed off to courier or customer |
| `DELIVERED` | Order reached the customer |
| `CONCLUDED` | Order logically closed |
| `CANCELLED` | Order cancelled — terminal state |

### Cancellation

| Field | Type | Required | Description |
|---|---|---|---|
| `cancellationCode` | string | YES | Stable machine-readable cancellation reason |
| `cancellationReason` | string | NO | Human-readable description |
| `cancelledBy` | string | YES | Who initiated: `MERCHANT`, `ORDERING_APPLICATION`, `SYSTEM` |
| `cancelledAt` | string | YES | Cancellation timestamp (RFC 3339) |

## Operations

| Operation | Provider | Consumer | Description |
|---|---|---|---|
| `getOrder` | Software Service | Ordering Application | Retrieve current order snapshot |
| `confirmOrder` | Software Service | Ordering Application | Confirm order for processing |
| `setPreparing` | Software Service | Ordering Application | Signal order entered preparation |
| `setReadyForPickup` | Software Service | Ordering Application | Signal order is ready |
| `dispatchOrder` | Software Service | Ordering Application / Logistics Service | Signal order dispatched |
| `setDelivered` | Software Service | Ordering Application | Signal order delivered |
| `cancelOrder` | Software Service | Ordering Application | Resolve a cancellation |
| `concludeOrder` | Software Service or Ordering Application | Counterpart | Logically close the order |

Participants MUST preserve profile obligations and asynchronous interaction semantics.

For transport-specific details, see [REST Binding — Orders](./orders-rest.md).

## Example

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
