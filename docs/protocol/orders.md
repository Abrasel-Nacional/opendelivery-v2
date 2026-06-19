# Orders Capability

* Capability Name: `orders`

## Overview

Orders Capability defines interoperable order lifecycle coordination across ordering, merchant operation, and delivery participants.

### Key Concepts

- Order state is a current business condition and MUST be explicit.
- Order events are immutable lifecycle facts and MUST NOT be interpreted as commands.
- Profile-specific behavior MAY exist, but unsupported transitions MUST NOT be inferred.
- Indoor behavior MUST be modeled through [Indoor Extension (Orders)](../extensions/indoor.md), not as an independent capability.

## Data Model

Orders Capability models the order as a lifecycle entity with transport-neutral semantics.

### Scope Boundary

Orders Capability covers:

- Order creation and acceptance
- Preparation and readiness progression
- Dispatch and delivery progression (when applicable)
- Cancellation and logical closure

Orders Capability does not cover:

- On-premise account management details (Indoor extension)
- Merchant catalog publication structures
- Logistics orchestration policy internals

### Participants

- `ORDERING_APPLICATION`: originates and tracks order lifecycle interactions
- `SOFTWARE_SERVICE`: merchant operational source of truth for order execution
- `DELIVERY_PLATFORM` (optional): provides delivery lifecycle updates when logistics is externalized

Participants MUST preserve profile obligations and asynchronous interaction semantics.

#### Provider/Consumer Mapping

| participant | typical role as Provider | typical role as Consumer |
|---|---|---|
| `ORDERING_APPLICATION` | Exposes order-origin context or callbacks when applicable | Calls order operations and consumes lifecycle updates |
| `SOFTWARE_SERVICE` | Exposes core order lifecycle operations and state updates | Consumes order requests and downstream acknowledgements |
| `DELIVERY_PLATFORM` | Exposes delivery-progress updates when delegated | Consumes dispatch/order-delivery context |

## Schema

### Order (Top Level)

| name | type | required | description |
|---|---|---|---|
| `order.id` | string | YES | Order identifier |
| `order.displayId` | string | YES | Human-readable code |
| `order.createdAt` | string | YES | Creation timestamp (ISO 8601 date-time) |
| `order.orderTiming` | string | YES | Timing mode |
| `order.merchant` | object | YES | Merchant reference |
| `order.items` | array[object] | YES | Ordered items |
| `order.total` | object | YES | Total amount |
| `order.customer` | object | NO | Customer context |
| `order.payments` | array[object] | NO | Payment context |
| `order.metadata` | object | NO | Additional context |

## Example

```json
{
  "order": {
    "id": "order-123",
    "displayId": "A123",
    "createdAt": "2026-03-17T12:00:00Z",
    "orderTiming": "INSTANT",
    "merchant": {"id": "merchant-123"},
    "items": [],
    "total": {"value": 0, "currency": "BRL"}
  }
}
```

## Operations

Logical operations in this capability are profile-dependent and mapped by transport bindings.

| operation | provider | consumer | intent |
|---|---|---|---|
| `createOrder` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | Create order lifecycle entity |
| `confirmOrder` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | Accept order for processing |
| `updateOrderLifecycle` | `SOFTWARE_SERVICE` or `DELIVERY_PLATFORM` | `ORDERING_APPLICATION` | Publish lifecycle progression facts |
| `cancelOrder` | `SOFTWARE_SERVICE` | `ORDERING_APPLICATION` | Resolve cancellation request |
| `concludeOrder` | `SOFTWARE_SERVICE` or `ORDERING_APPLICATION` (profile-dependent) | `ORDERING_APPLICATION` or counterpart | Mark logical completion |

Transport-specific contracts are documented in REST Binding pages.

## Events

Event consumers MUST deduplicate by event identifier.
Event producers SHOULD include monotonic timestamps.
Participants MUST support asynchronous delivery and MUST NOT assume strict delivery ordering.

### Event and Status Matrix - DELIVERY Profile

| Event | Action Origin | Endpoint | Requirement | Projected Status | Notes |
|---|---|---|---|---|---|
| `CREATED` | ORIGINATOR | - | MUST | `CREATED` | Order created by the customer |
| `CONFIRMED` | POS | `/confirm` | MUST | `CONFIRMED` | Merchant acceptance |
| `PREPARATION_REQUESTED` | ORIGINATOR | - | MAY | (unchanged) | Requests/authorizes preparation start |
| `PREPARING` | POS | `/preparing` | MAY | `PREPARING` | Preparation started |
| `READY_FOR_PICKUP` | POS | `/readyForPickup` | MAY | `READY` | Order ready |
| `PICKUP_ONGOING` | ORIGINATOR | - | MAY | `READY` | Courier assigned |
| `RIDER_ARRIVED_AT_STORE` | ORIGINATOR | - | MAY | `READY` | Courier arrived at store |
| `DISPATCHED` | POS | `/dispatch` | MAY | `IN_DELIVERY` | Order dispatched |
| `ORDER_COLLECTED` | ORIGINATOR | - | MAY | `IN_DELIVERY` | Order left store custody |
| `DELIVERY_ONGOING` | ORIGINATOR | - | MAY | `IN_DELIVERY` | In transit |
| `ARRIVED_AT_CUSTOMER` | ORIGINATOR | - | MAY | `IN_DELIVERY` | Arrival at customer location |
| `DELIVERED` | POS or ORIGINATOR | `/delivered` | MUST | `DELIVERED` | Customer received the order |
| `CANCELLED` | ORIGINATOR | - | MUST | `CANCELLED` | Final cancellation |
| `CONCLUDED` | ORIGINATOR | - | MUST | `CONCLUDED` | Closure by originator |

### Event and Status Matrix - TAKEOUT Profile

| Event | Action Origin | Endpoint | Requirement | Projected Status | Notes |
|---|---|---|---|---|---|
| `CREATED` | ORIGINATOR | - | MUST | `CREATED` | Order created by the customer |
| `CONFIRMED` | POS | `/confirm` | MUST | `CONFIRMED` | Acceptance |
| `PREPARATION_REQUESTED` | ORIGINATOR | - | MAY | (unchanged) | Requests preparation |
| `PREPARING` | POS | `/preparing` | MAY | `PREPARING` | Optional |
| `READY_FOR_PICKUP` | POS | `/readyForPickup` | MUST | `READY` | Awaiting pickup |
| `PICKUP_ONGOING` | ORIGINATOR | - | MUST NOT | `READY` | Courier assigned |
| `RIDER_ARRIVED_AT_STORE` | ORIGINATOR | - | MUST NOT | `READY` | Courier arrived at store |
| `ORDER_COLLECTED` | - | `/pickedUp` | MUST NOT | - | No logistics pickup exists |
| `DELIVERED` | POS | `/delivered` | MUST | `DELIVERED` | Customer picked up at counter |
| `DELIVERY_ONGOING` | - | - | MUST NOT | - | No delivery stage |
| `ARRIVED_AT_CUSTOMER` | - | - | MUST NOT | - | No delivery stage |
| `CANCELLED` | ORIGINATOR | - | MUST | `CANCELLED` | Cancellation |
| `CONCLUDED` | ORIGINATOR | - | MUST | `CONCLUDED` | Closure by originator |

### Event and Status Matrix - INDOOR Profile

| Event | Action Origin | Endpoint | Requirement | Projected Status | Notes |
|---|---|---|---|---|---|
| `CREATED` | ORIGINATOR | - | MUST | `CREATED` | Order created |
| `CONFIRMED` | POS | `/confirm` | MUST | `CONFIRMED` | Acceptance |
| `PREPARATION_REQUESTED` | ORIGINATOR | - | MAY | (unchanged) | On-demand flow |
| `PREPARING` | POS | `/preparing` | MAY | `PREPARING` | Optional |
| `READY_FOR_PICKUP` | POS | `/readyForPickup` | MAY | `READY` | Ready to serve |
| `PICKUP_ONGOING` | ORIGINATOR | - | MUST NOT | `READY` | Courier assigned |
| `RIDER_ARRIVED_AT_STORE` | ORIGINATOR | - | MUST NOT | `READY` | Courier arrived at store |
| `ORDER_COLLECTED` | - | `/pickedUp` | MUST NOT | - | No logistics stage |
| `DELIVERED` | POS | `/delivered` | MAY | `DELIVERED` | Order delivered to customer in-store |
| `DELIVERY_ONGOING` | - | - | MUST NOT | - | No delivery stage |
| `ARRIVED_AT_CUSTOMER` | - | - | MUST NOT | - | No delivery stage |
| `CANCELLED` | ORIGINATOR | - | MUST | `CANCELLED` | Cancellation |
| `CONCLUDED` | ORIGINATOR | - | MUST | `CONCLUDED` | Logical closure |

Rows marked as `MUST NOT` indicate events/operations that are forbidden for that profile and MUST NOT be emitted or accepted.

## Capability Discovery

Implementations exposing Orders Capability MUST declare capability name `orders` through discovery.

Capability declaration SHOULD include:

- Supported interaction mode (`push`, `pull`, or `hybrid`)
- Binding endpoint references
- Supported extensions (including Indoor when available)

Order interactions MUST only be assumed after counterpart discovery metadata is validated.

## Authorization

All Orders operations require authenticated access.

Implementations MUST enforce scope-based authorization per [Authentication and Authorization](authentication.md).

Recommended minimum scope families:

- `orders.read`
- `orders.write`
- `orders.events.write`

## Conformance

Participants implementing Orders Capability:

- MUST preserve lifecycle semantics defined in this specification across all bindings.
- MUST treat event payloads as authoritative lifecycle facts at publication time.
- SHOULD prioritize event-driven updates and use polling for reconciliation/fallback.
