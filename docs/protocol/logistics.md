# Logistics Capability

## 1. Overview

Logistics Capability defines delivery coordination primitives linked to an order context.

Delivery coordination MUST reference an existing order identifier.

## 2. Scope and Extensions

Logistics Capability covers:

- Delivery request and delivery context exchange
- Delivery progression tracking
- Delivery problem and incident signaling
- Delivery cancellation and completion outcomes
- Availability and pricing declarations

Logistics Capability does not cover:

- Core order fulfillment status ownership
- Merchant catalog publication
- Customer CRM/loyalty behavior

Current extension set: no Logistics extensions are defined in this version.

## 3. Players

- `ORDERING_APPLICATION`: sends delivery demand and receives tracking updates
- `SOFTWARE_SERVICE`: coordinates merchant-side delivery context
- `DELIVERY_PLATFORM`: executes or orchestrates delivery progression

### Provider/Consumer Mapping

| participant | typical role as Provider | typical role as Consumer |
|---|---|---|
| `DELIVERY_PLATFORM` | Exposes delivery quote/tracking/status interfaces | Consumes dispatch and order-delivery context |
| `SOFTWARE_SERVICE` | Exposes merchant operational delivery context interfaces | Consumes delivery progression and incident events |
| `ORDERING_APPLICATION` | Exposes optional callback/webhook targets when agreed | Consumes delivery status and ETA updates |

## 4. Interaction Between Players

Typical interaction model:

1. Order context is mapped to delivery context.
2. Delivery participant accepts/rejects service and returns estimates.
3. Delivery progression updates are exchanged asynchronously.
4. Delivery exceptions and cancellation are communicated explicitly.

Cancellation of delivery MUST be explicit and auditable.

## 5. Flows (Statuses and Events)

Logistics progression MUST expose explicit delivery facts/states.

Expected flow includes:

- Dispatch or assignment
- Pickup readiness and pickup completion
- In-transit progression
- Delivered or canceled terminal state
- Problem reporting with history continuity

Problem reporting MUST preserve problem history context to support traceability.

## 6. Discovery / Well-Known Configuration

Participants exposing logistics behavior MUST declare capability name `logistics` in discovery.

Discovery declaration SHOULD include:

- Service coverage and operation mode support
- Pricing/availability endpoint references
- Tracking and event callback/polling support

Availability and pricing declarations SHOULD be deterministic for the same input context.

## 7. Authorization

Logistics operations require authenticated calls with scope validation.

Implementations MUST enforce scope-based authorization according to [Authentication and Authorization](authentication.md).

Recommended minimum scope families:

- `logistics.read`
- `logistics.write`
- `logistics.events.write`

## 8. Operations

Reference operations include quote/availability, dispatch coordination, tracking updates, incident reporting, and cancellation. Final endpoint contracts are defined in REST API Binding pages.

### Delivery Fields (Top Level)

| name | type | required | description |
|---|---|---|---|
| `delivery.id` | string | YES | Delivery coordination identifier |
| `delivery.orderId` | string | YES | Related order identifier |
| `delivery.merchant` | object | YES | Merchant context |
| `delivery.pickup` | object | YES | Pickup context |
| `delivery.dropoff` | object | YES | Destination context |
| `delivery.vehicle` | object | NO | Vehicle context |
| `delivery.price` | object | NO | Delivery pricing context |
| `delivery.eta` | string | NO | Estimated delivery timing (ISO 8601 date-time) |

### Delivery Example

```json
{
  "delivery": {
    "id": "delivery-001",
    "orderId": "order-123",
    "merchant": {"id": "merchant-123"},
    "pickup": {},
    "dropoff": {}
  }
}
```
