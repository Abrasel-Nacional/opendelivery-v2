# API Endpoints → Protocol Concepts Mapping

This reference maps Open Delivery v1 REST API endpoints to Open Delivery v2 protocol concepts.

Use this to understand which capability and concept each v1 endpoint corresponds to.

---

## MERCHANT ENDPOINTS

### GET /v1/merchant
**v1 Purpose:** Retrieve merchant data, menu, services, availability

**v2 Concept:** Merchant Capability - Information Exchange

**What It Is:**
- Merchant information exposure mechanism
- Merchant System provides this endpoint
- Originator calls it to update local cache

**v2 Equivalents:**
- Merchant Capability: Merchant Identity, Services, Menu Structure, Status
- Concept: Merchant information is provided via some binding (REST GET, or query via other mechanism)
- TTL: When to re-fetch merchant info (mentioned in Merchant Capability)

---

### POST /v1/menuUpdated (Webhook)
**v1 Purpose:** Notify Originator of merchant data changes

**v2 Concept:** Merchant Capability - Update Notifications

**What It Is:**
- Merchant System initiates notification
- Originator implements webhook endpoint
- Communicates that merchant data has changed

**v2 Equivalents:**
- Merchant Capability: Information Exchange - Optional notifications
- Transport Binding: Webhook pattern (defined in REST/HTTP binding)
- Resiliency: Originator should re-fetch merchant data when received

---

### GET /v1/merchant/{id}/status
**v1 Purpose:** Get merchant operational status

**v2 Concept:** Merchant Capability - Status

**What It Is:**
- Merchant's operational state (ACTIVE, CLOSED, PAUSED, etc.)
- Can be queried independently from full merchant data
- Useful for quick availability checks

**v2 Equivalents:**
- Merchant Capability: Status (ACTIVE, CLOSED, PAUSED, OFFLINE, DEACTIVATED)
- Support declaration mechanism
- Part of merchant information exposure

---

### PUT /v1/merchantOnboarding
**v1 Purpose:** Register merchant system endpoint with Originator

**v2 Concept:** Merchant Capability - Discovery/Registration

**What It Is:**
- Merchant System provides its base URL to Originator
- Originator stores this for future calls
- Establishes integration relationship

**v2 Equivalents:**
- Not explicitly covered in first version
- Relates to how systems declare their merchant endpoint location
- Implementation-specific (how you configure your system)

---

## ORDER ENDPOINTS

### GET /v1/events:polling
**v1 Purpose:** Retrieve pending order events from Originator

**v2 Concept:** Orders Capability - Event Consumption Pattern

**What It Is:**
- Merchant System polls for new order events
- Originator queues events for consumption
- Merchant acknowledges receipt

**v2 Equivalents:**
- Orders Capability: Event lifecycle and normative events
- Transport Binding (REST/HTTP): Polling pattern with acknowledgment
- Alternative: Event Stream binding (async delivery instead of polling)

---

### POST /v1/events/acknowledgment
**v1 Purpose:** Confirm receipt of events from polling

**v2 Concept:** Orders Capability - Event Acknowledgment

**What It Is:**
- Merchant System acknowledges it received and processed events
- Prevents re-sending same events in next poll

**v2 Equivalents:**
- Orders Capability: Event is processed
- Transport Binding: Acknowledgment pattern
- Idempotency: Events must be handled idempotently

---

### GET /v1/orders/{orderId}
**v1 Purpose:** Retrieve full order details

**v2 Concept:** Orders Capability - Order Structure

**What It Is:**
- System queries complete order data
- Order ID provided (from polling event or initial creation)
- Response includes items, pricing, delivery info, etc.

**v2 Equivalents:**
- Orders Capability: Order Structure (Required, Conditional, Optional information)
- Information needed: Items, pricing, customer, timing, profile-specific data
- Transport Binding: How to query (REST GET, or other mechanism)

---

### PATCH /v1/orders/{orderId}/details
**v1 Purpose:** Update order details (adjustments, special notes)

**v2 Concept:** Orders Capability - Order Modification

**What It Is:**
- Update order information after initial creation
- Typically for adjustments or clarifications
- Originator may issue, Merchant may request

**v2 Equivalents:**
- Orders Capability: Part of order lifecycle (before confirmation threshold)
- Concept: Order data can be refined before final confirmation
- Not explicitly modeled in first version; domain-specific

---

### POST /v1/orders/{orderId}/confirm
**v1 Purpose:** Merchant accepts and confirms order

**v2 Concept:** Orders Capability - State Transition (→ CONFIRMED)

**What It Is:**
- Merchant System explicitly accepts the order
- Order transitions from PENDING to CONFIRMED
- Time-critical: must happen within timeout period

**v2 Equivalents:**
- Orders Capability: Event `ORDER_CONFIRMED` (normative for all profiles)
- State: Order.state → CONFIRMED
- Responsibility: Merchant System must accept or reject within time limit
- Profiles: All profiles require this action

---

### POST /v1/orders/{orderId}/preparing
**v1 Purpose:** Notify order is being prepared

**v2 Concept:** Orders Capability - Optional state/event (PREPARING)

**What It Is:**
- Informational event; not strictly required
- Merchant notifies order work has started
- Used for customer updates, eta calculation

**v2 Equivalents:**
- Orders Capability: Event `ORDER_PREPARING` (optional for all profiles)
- State: IMPLIED state (order is active, being worked on)
- Classification: Optional/informational event
- Not required by protocol; enrichment only

---

### POST /v1/orders/{orderId}/readyForPickup
**v1 Purpose:** Notify order is ready to leave merchant

**v2 Concept:** Orders Capability - State Transition (→ READY_FOR_PICKUP) or State (→ READY)

**What It Is:**
- Order preparation complete
- Ready for customer pickup or dispatch
- Normative event across all profiles

**v2 Equivalents:**
- Orders Capability: Event `ORDER_READY_FOR_PICKUP` (normative for DELIVERY, PICKUP, ON_PREMISE)
- State: Order.state → READY_FOR_PICKUP
- Profiles: Different semantics per profile:
  - DELIVERY: Order ready for logistics pickup
  - PICKUP: Order ready for customer collection
  - ON_PREMISE: Order ready for table service

---

### POST /v1/orders/{orderId}/pickedUp
**v1 Purpose:** Confirm order was picked up (customer or logistics)

**v2 Concept:** Orders Capability - State Transition (→ PICKED_UP)

**What It Is:**
- Confirms order left merchant location
- Can be by customer (PICKUP) or logistics (DELIVERY)
- Signals preparation phase complete

**v2 Equivalents:**
- Orders Capability: Event `ORDER_PICKED_UP` (conditional for PICKUP profile)
- Logistics Capability: Event `DELIVERY_PICKED_UP` (normative for DELIVERY profile)
- State: Order/Delivery.state → PICKED_UP
- Profiles: Meaning varies:
  - DELIVERY: Logistics picked up from merchant
  - PICKUP: Customer collected from merchant
  - ON_PREMISE: Not applicable

---

### POST /v1/orders/{orderId}/dispatch
**v1 Purpose:** Notify order left merchant for delivery

**v2 Concept:** Orders Capability - State Transition (→ DISPATCHED)

**What It Is:**
- Order has left merchant premises
- For delivery orders, logistics is now in possession
- Signals start of delivery phase

**v2 Equivalents:**
- Orders Capability: Event `ORDER_DISPATCHED` (normative for DELIVERY profile)
- State: Order.state → DISPATCHED
- Profiles: DELIVERY profile only
- Relationship to Logistics: Order dispatch aligns with logistics pickup

---

### POST /v1/orders/{orderId}/delivered
**v1 Purpose:** Confirm order delivered to customer

**v2 Concept:** Orders Capability - State Transition (→ DELIVERED)

**What It Is:**
- Order reached final destination
- Customer has received order
- May require signature/confirmation

**v2 Equivalents:**
- Orders Capability: Event `ORDER_DELIVERED` (normative for DELIVERY profile, optional for others)
- State: Order.state → DELIVERED
- Profiles: 
  - DELIVERY: Customer received delivery
  - PICKUP: Customer already picked up (state reached at pickup)
  - ON_PREMISE: Staff delivered to table
- Logistics Capability: `DELIVERY_COMPLETED` aligns with this

---

### POST /v1/orders/{orderId}/validateCode
**v1 Purpose:** Verify delivery code for order acceptance

**v2 Concept:** Orders Capability - Delivery Confirmation (optional)

**What It Is:**
- Security mechanism: delivery person provides code
- Customer verifies code matches
- Proves correct recipient received

**v2 Equivalents:**
- Logistics Capability: `DELIVERY_CONFIRMATION_CODE_GENERATED` (optional event)
- Transport Binding: REST/HTTP specific mechanic
- Concept: Part of problem resolution and confirmation

---

### POST /v1/orders/{orderId}/tracking
**v1 Purpose:** Provide/receive delivery tracking information

**v2 Concept:** Logistics Capability - Tracking Information

**What It Is:**
- Merchant/Logistics provide delivery updates
- Location, ETA, status changes
- Real-time or periodic updates

**v2 Equivalents:**
- Logistics Capability: Tracking Information section
- Geolocation, routing, history
- Events: `DELIVERY_TRACKING_UPDATED` (optional, frequent)
- Transport Binding: REST binding may use POST for updates; Event binding uses streaming

---

## ORDER CANCELLATION ENDPOINTS

### POST /v1/orders/{orderId}/requestCancellation
**v1 Purpose:** Request cancellation of order

**v2 Concept:** Orders Capability - Cancellation Semantics

**What It Is:**
- Either party requests cancellation
- Reason code and explanation provided
- Request is asynchronous; response is separate

**v2 Equivalents:**
- Orders Capability: Cancellation Process (step 1: request)
- Event: `ORDER_CANCELLATION_REQUESTED` (conditional)
- Contents: Reason code (from defined list) + explanation
- Policies: Acceptance depends on timing, order state, rules

---

### POST /v1/orders/{orderId}/acceptCancellation
**v1 Purpose:** Accept cancellation request

**v2 Concept:** Orders Capability - Cancellation Response (Accept)

**What It Is:**
- Responding party agrees to cancel
- No longer will fulfill order
- Compensation/refund handled separately (Financial Domain)

**v2 Equivalents:**
- Orders Capability: Cancellation Handshake (response step: accept)
- Event: `ORDER_CANCELLED` (normative when accept)
- State: Order.state → CANCELLED
- Financial: Refund/compensation out of scope (Financial Capability)

---

### POST /v1/orders/{orderId}/denyCancellation
**v1 Purpose:** Reject cancellation request

**v2 Concept:** Orders Capability - Cancellation Response (Deny)

**What It Is:**
- Responding party refuses to cancel
- Order fulfillment continues
- Parties may need to negotiate further

**v2 Equivalents:**
- Orders Capability: Cancellation Handshake (response step: deny)
- Event: `ORDER_CANCELLATION_DENIED` (conditional)
- State: Order.state remains unchanged
- Next Action: Order fulfillment continues

---

## LOGISTICS ENDPOINTS

### POST /v1/logistics/availability
**v1 Purpose:** Check if delivery is possible to an address

**v2 Concept:** Logistics Capability - Delivery Availability and Pricing

**What It Is:**
- Query-only: can logistics serve this location?
- Returns availability, ETA, cost
- Pre-order decision support

**v2 Equivalents:**
- Logistics Capability: Availability and Pricing section
- Information: Service area, capacity, cost factors
- Transport Binding: REST binding defines query mechanism
- Alternative: May be discovery or declared-support based, not queried

---

### POST /v1/logistics/delivery
**v1 Purpose:** Create/assign new delivery to logistics provider

**v2 Concept:** Logistics Capability - Delivery Entity (creation)

**What It Is:**
- Originator or Merchant requests delivery
- Provides order and delivery information
- Logistics provider accepts or declines

**v2 Equivalents:**
- Logistics Capability: Delivery Entity and Lifecycle
- State: Delivery.state → PENDING
- Event: `DELIVERY_ASSIGNED` or `DELIVERY_DECLINED` (conditional)
- Responsibility: Logistics must respond within time limit

---

### GET /v1/logistics/delivery/{orderId}
**v1 Purpose:** Query delivery details/status

**v2 Concept:** Logistics Capability - Delivery Tracking and Details

**What It Is:**
- Retrieve current delivery state and information
- Full history and status
- Real-time snapshot

**v2 Equivalents:**
- Logistics Capability: Delivery states, tracking information
- Data: Current state, route, geolocations, events
- Transport Binding: Query mechanism (REST GET)

---

### POST /v1/logistics/readyForPickup/{orderId}
**v1 Purpose:** Notify logistics that order is ready for pickup

**v2 Concept:** Orders Capability (sync) + Logistics Capability - State alignment

**What It Is:**
- Merchant confirms order ready
- Notifies logistics provider
- Logistics should dispatch pickup

**v2 Equivalents:**
- Orders Capability: `ORDER_READY_FOR_PICKUP` (normative for DELIVERY)
- Logistics Capability: Implicit signal to start delivery phase
- Coordination: Order and Delivery states move together for DELIVERY profile

---

### POST /v1/logistics/orderPicked/{orderId}
**v1 Purpose:** Confirm logistics picked up order

**v2 Concept:** Logistics Capability - State Transition (→ PICKED_UP)

**What It Is:**
- Delivery person collected order from merchant
- Marks start of in-transit phase
- Signals end of merchant responsibility

**v2 Equivalents:**
- Logistics Capability: Event `DELIVERY_PICKED_UP` (normative for DELIVERY)
- State: Delivery.state → PICKED_UP
- Coordination: Aligns with Orders Capability `ORDER_DISPATCHED`

---

### POST /v1/logistics/finishDelivery/{orderId}
**v1 Purpose:** Confirm order delivered to customer

**v2 Concept:** Logistics Capability - State Transition (→ DELIVERED)

**What It Is:**
- Delivery person completed delivery
- Customer has received order
- End of delivery phase

**v2 Equivalents:**
- Logistics Capability: Event `DELIVERY_COMPLETED` (normative for DELIVERY)
- State: Delivery.state → DELIVERED
- Orders Capability: Aligns with `ORDER_DELIVERED`

---

### POST /v1/logistics/handleProblem/{orderId}
**v1 Purpose:** Report and manage delivery exceptions

**v2 Concept:** Logistics Capability - Problem Handling

**What It Is:**
- Logistics reports issue (address not found, customer unavailable, etc.)
- Merchant/Originator decides resolution
- Retry, return, escalate

**v2 Equivalents:**
- Logistics Capability: Problem Handling section
- Event: `DELIVERY_PROBLEM_OCCURRED` (conditional)
- Resolution: Designated outcomes (redeliver, return, refund)

---

### POST /v1/logistics/cancel/{orderId}
**v1 Purpose:** Cancel delivery

**v2 Concept:** Logistics Capability - Cancellation

**What It Is:**
- Delivery canceled (before or after pickup)
- Logistics ceases delivery attempt
- Financial implications handled separately

**v2 Equivalents:**
- Logistics Capability: Delivery cancellation
- State: Delivery.state → CANCELLED
- Orders Capability: May trigger `ORDER_CANCELLED`

---

## WEBHOOK ENDPOINTS (Initiated By Merchant/Logistics)

### POST /v1/newEvent (Webhook)
**v1 Purpose:** Merchant notifies Originator of order events

**v2 Concept:** Orders Capability - Event Notification

**What It Is:**
- Merchant System delivers order events to Originator webhook
- Alternative to polling
- Faster, more real-time

**v2 Equivalents:**
- Orders Capability: All normative/conditional events
- Transport Binding (REST/HTTP): Webhook pattern
- Alternative: Event Stream binding (topic-based instead of webhook)
- Events: `ORDER_CONFIRMED`, `ORDER_READY_FOR_PICKUP`, `ORDER_CANCELLED`, etc.

---

### POST /v1/newLogisticEvent (Webhook)
**v1 Purpose:** Logistics notifies Merchant/Originator of delivery events

**v2 Concept:** Logistics Capability - Delivery Event Notification

**What It Is:**
- Logistics Provider delivers events (instead of query)
- Real-time delivery status updates
- Faster than polling

**v2 Equivalents:**
- Logistics Capability: All normative/conditional delivery events
- Transport Binding: Webhook pattern (or Event Stream alternative)
- Events: `DELIVERY_PICKED_UP`, `DELIVERY_IN_TRANSIT`, `DELIVERY_COMPLETED`, etc.

---

### POST /v1/confirmationCode (Webhook)
**v1 Purpose:** Logistics sends delivery confirmation code

**v2 Concept:** Logistics Capability - Delivery Confirmation

**What It Is:**
- Delivery person provides code
- Merchant/Originator receives for customer verification
- Security mechanism

**v2 Equivalents:**
- Logistics Capability: Optional event `DELIVERY_CONFIRMATION_CODE_GENERATED`
- Transport Binding: Webhook to notify
- Usage: Customer verification, proof of delivery

---

## Authentication Endpoint

### POST /oauth/token
**v1 Purpose:** Obtain authentication token

**v2 Concept:** Transport Binding (not protocol)

**What It Is:**
- OAuth2 token exchange
- Standard Web API authentication

**v2 Equivalents:**
- Transport Binding (REST/HTTP): OAuth2 authentication section
- Security: Handled by binding, not protocol
- Protocol is auth-agnostic

---

## Summary Table

| v1 Endpoint | v1 Purpose | v2 Domain | v2 Concept |
|---|---|---|---|
| GET /merchant | Merchant info | Merchant | Entity structure, services, menu |
| POST /menuUpdated | Merchant update | Merchant | Update notification |
| GET /merchant/status | Merchant status | Merchant | Status/capabilities |
| PUT /merchantOnboarding | Register | Merchant | Integration setup |
| GET /events:polling | Order events | Orders | Event consumption (polling) |
| POST /events/acknowledgment | Ack events | Orders | Event processing |
| GET /orders/{id} | Order details | Orders | Order structure |
| PATCH /orders/{id}/details | Edit order | Orders | Order modification |
| POST /orders/{id}/confirm | Accept order | Orders | State: CONFIRMED |
| POST /orders/{id}/readyForPickup | Ready | Orders | State: READY_FOR_PICKUP |
| POST /orders/{id}/dispatch | Dispatch | Orders | State: DISPATCHED |
| POST /orders/{id}/delivered | Delivered | Orders | State: DELIVERED |
| POST /orders/{id}/requestCancellation | Cancel request | Orders | Cancellation process |
| POST /orders/{id}/acceptCancellation | Accept cancel | Orders | Cancellation: accept |
| POST /orders/{id}/denyCancellation | Deny cancel | Orders | Cancellation: deny |
| POST /logistics/availability | Check delivery | Logistics | Availability query |
| POST /logistics/delivery | Create delivery | Logistics | Delivery creation |
| GET /logistics/delivery/{id} | Delivery details | Logistics | Delivery tracking |
| POST /logistics/readyForPickup | Ready for delivery | Orders + Logistics | State sync |
| POST /logistics/orderPicked | Picked up | Logistics | State: PICKED_UP |
| POST /logistics/finishDelivery | Delivered | Logistics | State: DELIVERED |
| POST /logistics/handleProblem | Problem report | Logistics | Problem handling |
| POST /logistics/cancel | Cancel delivery | Logistics | Cancellation |
| POST /oauth/token | Auth token | Transport | OAuth2 (binding) |

---

## Migration Order

**Phase 1:** Understand mapping (this document)

**Phase 2:** Implement concepts (Orders → Merchant → Logistics)

**Phase 3:** Choose transport binding (REST is simplest)

**Phase 4:** Implement normative events

**Phase 5:** Handle edge cases (cancellation, problems, idempotency)

---
