# Indoor Extension

> Extends: [Orders Capability](../protocol/orders.md) · Extension name: `indoor`
> REST/HTTP binding: [Indoor Endpoints](../transport-bindings/rest-http-indoor.md)

## Overview

Indoor enables on-premise order operations — table service, counter, tab — as an extension of the standard Orders lifecycle.
An **Indoor account** aggregates multiple orders placed at the same physical location into a single financial unit, supporting incremental ordering, partial payments, and controlled closure.

Indoor is **not** an independent capability. It extends Orders semantics and MUST NOT replace them.

What Indoor covers:

- On-premise identification via `operationMode` + `identifier` (table/tab/counter token)
- Account-based aggregation of multiple orders
- Incremental account updates
- Partial payment registration and account closure
- Indoor account lifecycle events

What Indoor does **not** cover:

- Reservation and waiting-list workflows
- Table occupancy or seating mapping
- Customer-calling UI/UX behavior
- Messaging technology requirements
- Country-specific fiscal modules

## Participants

| interaction role | description | likely participant types |
|---|---|---|
| `Provider` | Exposes account interfaces and is authoritative for account state and financial consistency. | `SOFTWARE_SERVICE` (POS/ERP) |
| `Consumer` | Initiates orders, queries account views, and submits payment and close intents. | `ORDERING_APPLICATION` (tablet, kiosk, QR app) |

The same participant MAY act as both Provider and Consumer for different operations (e.g., a `SOFTWARE_SERVICE` that initiates a payment on a shared account). The roles above reflect the typical and expected configuration.

## Data Model

### Account Lifecycle

An indoor account moves through three states:

| state | description |
|---|---|
| `OPEN` | Account is active and accepts new orders and updates |
| `IN_PAYMENT` | Payment process has started; account is locked for new orders |
| `CLOSED` | Account has been finalized and is immutable |

Closed accounts MUST NOT be updated or reopened.
Formal state machine and transition guards are PENDING.

### Indoor Order Context (`order.indoor`)

Attached to each order that belongs to an indoor account.

| field | type | required | description |
|---|---|---|---|
| `operationMode` | string | YES | `TABLE`, `TAB`, or `COUNTER` |
| `identifier` | string | YES | Operational key identifying the table/tab/counter |
| `originChannel` | string | YES | Source channel (`KIOSK`, `TABLET`, `APP`, `POS`, etc.) |
| `consumptionType` | string | NO | `ON_PREMISE` or `TAKEAWAY` |
| `deliveryLocation` | object | NO | Indoor destination reference (e.g., seat or zone) |
| `callMethod` | string | NO | Customer-calling method |
| `notifyOriginator` | boolean | NO | Whether to notify the originator when order is ready |

### Account (`account`)

The account is the root entity for all indoor operations.

| field | type | required | description |
|---|---|---|---|
| `operationMode` | string | YES | Must match the `order.indoor.operationMode` used in associated orders |
| `identifier` | string | YES | Same operational key used in indoor order context |
| `accountId` | string | NO | Opaque technical identifier assigned by the Provider |
| `items[]` | array[object] | NO | Aggregated item list across all orders in this account |
| `payments[]` | array[object] | NO | Registered partial or full payments |
| `status` | string | NO | Current account state (`OPEN`, `IN_PAYMENT`, `CLOSED`) |

`accountId` MUST NOT be required for initial operations. The primary key for account lookup is always `operationMode` + `identifier`.

## Operations

| operation | description | responsibility |
|---|---|---|
| Create or Receive Indoor Order | Creates a new order with an indoor context and correlates it to an account. | `Provider` |
| Query Indoor Account | Returns the current account snapshot for a given indoor context. | `Provider` |
| Update Indoor Account | Applies an incremental update to an existing account. | `Provider` |
| Register Partial Payment | Registers a partial or full payment against the account. | `Provider` |
| Close Indoor Account | Finalizes the account and transitions it to `CLOSED`. | `Provider` |

---

### Create or Receive Indoor Order

Creates a new order with an indoor context, or receives one from an external originator, and correlates it to an account identified by `operationMode` + `identifier`.

The Provider MUST create or locate the corresponding account automatically.
The Provider MUST NOT require a pre-existing `accountId` for this operation.

**Inputs**

| field | type | required | description |
|---|---|---|---|
| `order.id` | string | YES | Order identifier |
| `order.indoor.operationMode` | string | YES | `TABLE`, `TAB`, or `COUNTER` |
| `order.indoor.identifier` | string | YES | Operational key (table/tab/counter token) |
| `order.indoor.originChannel` | string | YES | Source channel |
| `order.indoor.consumptionType` | string | NO | `ON_PREMISE` or `TAKEAWAY` |
| `order.indoor.notifyOriginator` | boolean | NO | Notify originator when order is ready |

**Outputs**

The Provider acknowledges receipt. The operation is processed asynchronously.

---

### Query Indoor Account

Returns the current account snapshot for a given indoor context. The primary lookup key is `operationMode` + `identifier`. `accountId` MAY be used as an alternative once known.

**Inputs**

| field | type | required | description |
|---|---|---|---|
| `operationMode` | string | YES | Indoor operation mode |
| `identifier` | string | YES | Table/tab/counter identifier |
| `accountId` | string | NO | Optional: use if `identifier` is ambiguous |

**Outputs**

Returns the full account snapshot, including current `status`, aggregated `items[]`, and registered `payments[]`.

---

### Update Indoor Account

Applies an incremental update to an existing account. Updates MAY be partial — only the fields provided are applied.
The Provider MUST correlate the account using `operationMode` + `identifier`.

**Inputs**

| field | type | required | description |
|---|---|---|---|
| `account.operationMode` | string | YES | Indoor operation mode |
| `account.identifier` | string | YES | Operational account key |
| `account.items[]` | array[object] | NO | Item delta to apply |
| `account.status` | string | NO | New account status |

**Outputs**

The Provider acknowledges the update. Conflicts in state or version MUST be reported to the Consumer.

---

### Register Partial Payment

Registers a partial or full payment against the account. Multiple payments MAY be registered for the same account. Item-level mapping is optional.

**Inputs**

| field | type | required | description |
|---|---|---|---|
| `account.operationMode` | string | YES | Indoor operation mode |
| `account.identifier` | string | YES | Operational account key |
| `payment.amount.value` | number | YES | Payment value |
| `payment.amount.currency` | string | YES | ISO 4217 currency code |
| `payment.method` | string | YES | Payment method |
| `payment.items[]` | array[string] | NO | Optional item IDs this payment covers |

**Outputs**

The Provider acknowledges the payment registration. State or business rule violations MUST be reported to the Consumer.

---

### Close Indoor Account

Finalizes the account and transitions it to `CLOSED`. A closed account is immutable and MUST NOT receive further updates or orders.

**Inputs**

| field | type | required | description |
|---|---|---|---|
| `account.operationMode` | string | YES | Indoor operation mode |
| `account.identifier` | string | YES | Operational account key |
| `account.accountId` | string | NO | Optional technical identifier |

**Outputs**

The Provider acknowledges the closure. Attempting to close an already-closed account MUST result in a conflict response.

---

## Events

Indoor account changes are communicated through the following events:

| event | triggered when |
|---|---|
| `ACCOUNT_CREATED` | An indoor account is created for the first time |
| `ACCOUNT_UPDATED` | An incremental update is applied to an open account |
| `ACCOUNT_PAYMENT_REGISTERED` | A payment is registered against the account |
| `ACCOUNT_CLOSED` | The account transitions to `CLOSED` |

Event rules:

- Events MUST NOT define a specific messaging technology or transport.
- Events MUST NOT imply synchronous execution or strict timing guarantees.
- Events MUST preserve Orders lifecycle integrity.
- Consumers SHOULD prefer events as the primary synchronization channel; polling MUST remain available as fallback.

Illustrative account lifecycle:

```
Create Indoor Order          →  Account: OPEN
Update Indoor Account        →  Account: OPEN  (more orders added)
Register Partial Payment     →  Account: IN_PAYMENT
Close Indoor Account         →  Account: CLOSED
```

## Authorization

All Indoor operations require OAuth2 Bearer token authentication. Scopes are per-operation:

| operation | required scope |
|---|---|
| Create or Receive Indoor Order | `orders.indoor.write` |
| Query Indoor Account | `orders.indoor.read` |
| Update Indoor Account | `orders.indoor.write` |
| Register Partial Payment | `orders.indoor.payment.write` |
| Close Indoor Account | `orders.indoor.close.write` |

Authorization decisions MUST be enforced by the Provider.
See [Authentication and Authorization](../protocol/authentication.md) for token issuance and validation rules.

## Discovery

Indoor support MUST be declared through Orders capability metadata.
A Provider supporting Indoor SHOULD advertise:

- Supported `operationMode` values (`TABLE`, `TAB`, `COUNTER`)
- Supported payment models (partial, full, item-level)
- Event delivery capabilities

No fixed discovery endpoint path is mandated by this extension.
See [Discovery and Well-Known](../protocol/discovery.md) for the discovery protocol.

## Conformance

**Provider MUST:**

- Correlate accounts using `operationMode` + `identifier` as the primary key
- Accept initial create and query operations without requiring `accountId`
- Enforce scope-based authorization for every operation
- Reject updates to `CLOSED` accounts
- Preserve Orders capability semantics for all indoor orders

**Consumer MUST:**

- Use `operationMode` + `identifier` for initial account access (never assume `accountId`)
- Treat polling as fallback only; prefer event-driven synchronization when available

## Pending

- Formal account state machine and transition guards
- Final account payload model (item and payment schemas)
- Mandatory vs optional operation set per integration profile
- Partial payment by item semantics
- Fiscal treatment within account lifecycle
