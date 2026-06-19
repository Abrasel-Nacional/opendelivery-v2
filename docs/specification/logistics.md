# Logistics Capability

- **Capability name:** `logistics`

## Overview

Logistics Capability defines delivery coordination primitives linked to an order context.

Delivery coordination MUST reference an existing order identifier.

### Scope

Logistics covers:

- Delivery request and delivery context exchange
- Delivery progression tracking
- Delivery problem and incident signaling
- Delivery cancellation and completion outcomes
- Availability and pricing declarations

Logistics does not cover:

- Core order fulfillment status ownership
- Merchant catalog publication
- Customer CRM and loyalty behavior

## Participants

| Participant | Provider | Consumer |
|---|---|---|
| **Logistics Service** | Exposes delivery quote, tracking, and status interfaces | Consumes dispatch and order-delivery context |
| **Software Service** | Exposes merchant operational delivery context interfaces | Consumes delivery progression and incident events |
| **Ordering Application** | Exposes optional webhook targets when agreed | Consumes delivery status and ETA updates |

## Data Model

### Delivery Request

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Delivery request identifier |
| `orderId` | string | YES | Source order reference |
| `merchantId` | string | YES | Merchant scope |
| `pickup` | Address | YES | Pickup location |
| `dropoff` | Address | YES | Delivery destination |
| `requestedAt` | string | YES | Request timestamp (RFC 3339) |
| `scheduledFor` | string | NO | Scheduled pickup time (RFC 3339) |

### Delivery Status

| Field | Type | Required | Description |
|---|---|---|---|
| `deliveryId` | string | YES | Delivery identifier |
| `orderId` | string | YES | Source order reference |
| `status` | string | YES | Current delivery status (see lifecycle) |
| `eta` | string | NO | Estimated arrival time (RFC 3339) |
| `updatedAt` | string | YES | Last update timestamp (RFC 3339) |

### Delivery Status Lifecycle

| Status | Description |
|---|---|
| `REQUESTED` | Delivery request received |
| `ACCEPTED` | Logistics provider accepted the delivery |
| `REJECTED` | Logistics provider rejected the delivery |
| `ASSIGNED` | Courier assigned to the delivery |
| `AT_PICKUP` | Courier arrived at pickup location |
| `PICKED_UP` | Order collected by courier |
| `IN_TRANSIT` | Order in transit to customer |
| `AT_DROPOFF` | Courier arrived at delivery address |
| `DELIVERED` | Order delivered to customer |
| `FAILED` | Delivery failed — see incident details |
| `CANCELLED` | Delivery cancelled |

### Delivery Incident

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Incident identifier |
| `deliveryId` | string | YES | Affected delivery |
| `type` | string | YES | Incident type (`CUSTOMER_ABSENT`, `ADDRESS_NOT_FOUND`, `ITEM_DAMAGED`, `OTHER`) |
| `description` | string | NO | Human-readable description |
| `occurredAt` | string | YES | Incident timestamp (RFC 3339) |

### Quote

| Field | Type | Required | Description |
|---|---|---|---|
| `quoteId` | string | YES | Quote identifier |
| `merchantId` | string | YES | Merchant scope |
| `fee` | number | YES | Delivery fee in minor units (cents) |
| `eta` | string | YES | Estimated delivery time (RFC 3339) |
| `validUntil` | string | YES | Quote expiration timestamp (RFC 3339) |

## Operations

| Operation | Provider | Consumer | Description |
|---|---|---|---|
| `requestQuote` | Logistics Service | Software Service / Ordering Application | Request delivery fee and ETA quote |
| `requestDelivery` | Logistics Service | Software Service / Ordering Application | Submit a delivery request |
| `getDeliveryStatus` | Logistics Service | Software Service / Ordering Application | Retrieve current delivery status |
| `cancelDelivery` | Logistics Service | Software Service / Ordering Application | Cancel a delivery request |
| `reportIncident` | Logistics Service | Software Service | Report a delivery incident |

For transport-specific details, see [REST Binding — Logistics](./logistics-rest.md).

## Example

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
