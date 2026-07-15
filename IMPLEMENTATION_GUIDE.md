# Implementation Guide: v1 to v2 Transition

This guide helps implementers who are familiar with Open Delivery v1 understand and implement the v2 protocol.

---

## Key Mental Shift

### v1 Thinking
"I need to implement these REST endpoints and handle events for order management."

### v2 Thinking
"I need to coordinate order state and events with other systems according to the Open Delivery domain model, implementing the published API Specs."

Domain narrative lives under Protocol; the implementable contract is API Spec (REST/HTTP).

---

## For a Merchant System (POS) Implementer

### What You Do in v1
1. Implement webhook endpoint: `POST /v1/orderUpdate` to receive orders
2. Implement endpoints: `POST /v1/orders/{id}/confirm`, `/preparing`, `/readyForPickup`, etc.
3. Implement webhook for merchant updates: `POST /v1/menuUpdated`
4. Handle order acknowledgment and errors

### What You Do in v2
1. **Understand your responsibility**: Implement the "Merchant System" actor role
2. **Handle all three profiles**: DELIVERY, PICKUP, ON_PREMISE (not just one)
3. **Emit normative events**: CONFIRMED, READY_FOR_PICKUP, DISPATCHED, DELIVERED (as applicable)
4. **Track state**, not workflow: The order state is truth, not your internal steps
5. **Implement the API Spec**: REST/HTTP as published in the API reference

### How Events Change

**v1:** Events were implementation details notifying state changes
- `ORDER_UPDATE` webhook contains status information
- You received events at arbitrary times
- Not all events were guaranteed

**v2:** Events are protocol-primary facts
- `ORDER_CONFIRMED` = Merchant accepted
- `ORDER_READY_FOR_PICKUP` = Order prepared
- `ORDER_DISPATCHED` = Order left location
- These are normative for DELIVERY profile (you MUST emit them)

### How State Changes

**v1:** You listened to events and updated your database
- "I got a webhook, so I update my POS"

**v2:** State is synchronized across systems
- Order in your system has state: PENDING, CONFIRMED, READY, DISPATCHED, DELIVERED
- This state is observable by other systems
- Events communicate state changes

### Migration Checklist

- [ ] Understand Orders Capability (your primary concern)
- [ ] Map your current endpoints to Orders Capability lifecycle
- [ ] Identify which order profiles you support (DELIVERY? PICKUP? ON_PREMISE?)
- [ ] Implement normative events for your profiles
- [ ] Implement the Orders (and related) API Specs
- [ ] Implement order state tracking (not just events)
- [ ] Test with multiple order profiles
- [ ] Review Principles (especially "tolerance and resilience")

---

## For an Ordering Application Implementer

### What You Do in v1
1. Query merchant endpoint: `GET /v1/merchant`
2. Send orders via webhook: `POST /v1/newEvent` (or polling receives them)
3. Poll for order events: `GET /v1/events:polling`
4. Call order action endpoints: `/confirm`, `/cancelled`, etc.
5. Receive merchant updates via webhook

### What You Do in v2
1. **Understand your responsibility**: Implement the "Originator" actor role
2. **Send complete orders**: Include all required information
3. **Manage order lifecycle**: Create → Track → Cancel if needed
4. **Receive normative events**: Understand which are mandatory vs. optional
5. **Create webhooks for merchant**: Send notification, receive updates
6. **Define order profiles**: Specify DELIVERY, PICKUP, or ON_PREMISE
7. **Implement the API Spec**: Follow the published REST/HTTP contracts

### How Order Creation Changes

**v1:**
```
POST /orders
{
 "merchant": {...},
 "items": [...],
 "delivery": {...}
}
→ Server responds with order ID
```

**v2:**
```
Same structure, but:
- MUST include "profile": "DELIVERY" | "PICKUP" | "ON_PREMISE"
- Order is created and exchanged per the Orders API Spec contract
```

### How Event Consumption Changes

**v1:**
```
GET /v1/events:polling → array of events
- Events may be incomplete
- No guarantee all events received
- You acknowledge each batch
```

**v2:**
```
Still get order events, but:
- Normative events are GUARANTEED for your profile
- Optional events MAY be present
- State is source of truth (not just events)
- You can poll OR use webhooks as declared in Discovery / API Spec
```

### Migration Checklist

- [ ] Understand Orders Capability (especially profiles and events)
- [ ] Implement all three order profiles (DELIVERY, PICKUP, ON_PREMISE)
- [ ] Map existing order creation to Orders Capability structure
- [ ] Add "profile" to your order data model
- [ ] Update merchant query to understand support declarations
- [ ] Handle normative events per profile
- [ ] Implement cancellation with reason codes
- [ ] Implement webhook / callback endpoints per the API Spec
- [ ] Implement webhook endpoint for merchant system updates

---

## For a Logistics Provider Implementer

### What You Do in v1
1. Receive delivery order: `POST /v1/logistics/delivery`
2. Accept/decline delivery
3. Emit tracking events: `POST /v1/newLogisticEvent`
4. Handle delivery problems, cancellations
5. Provide delivery pricing: `POST /v1/logistics/availability`

### What You Do in v2
1. **Understand your responsibility**: Implement the "Logistics Provider" actor role
2. **Understand delivery lifecycle**: States and events (parallel to order)
3. **Provide availability/pricing**: For orders with DELIVERY profile
4. **Emit delivery events**: PICKED_UP, IN_TRANSIT, DELIVERED (normative)
5. **Handle problems**: Problem reporting and resolution
6. **Choose transport**: Implement REST/HTTP binding OR alternative

### How Delivery Assignment Changes

**v1:**
```
POST /v1/logistics/delivery
{
 "orderId": "...",
 "pickup": {...},
 "delivery": {...}
}
→ Logistics provider accepts/declines
```

**v2:**
```
Same basic flow, but:
- Delivery is now a first-class entity (like Order)
- Delivery has its own state and lifecycle
- Delivery events are parallel to order events
- Normative events: PICKED_UP, DELIVERED (always)
```

### How Events Work

**v1:**
```
POST /v1/newLogisticEvent
{"status": "PICKED_UP", "orderId": "..."}
```

**v2:**
```
Same event, but understood as:
- DELIVERY_PICKED_UP (Logistics Capability)
- Aligns with ORDER_DISPATCHED (Orders Capability)
- Normative for DELIVERY profile
```

### Migration Checklist

- [ ] Understand Logistics Capability
- [ ] Map your current delivery states to Logistics Capability states
- [ ] Understand delivery events (normative vs. optional)
- [ ] Implement all normative delivery events
- [ ] Provide availability/pricing information
- [ ] Handle delivery problems with reason codes
- [ ] Implement delivery cancellation
- [ ] Choose REST/HTTP binding
- [ ] Test with integration platforms (they may use REST, you may use events)

---

## For an Integration Hub/Middleware Implementer

### Special Consideration

Hubs may implement BOTH roles simultaneously:
- **Originator role** (receiving from one system, sending to another)
- **Merchant System role** (or Logistics role)

### What Changes

**v1:** Hub translates between different API versions/styles
- Map endpoints
- Transform data structures
- Handle different event models

**v2:** Hub understands protocol capabilities
- Order lifecycle is consistent
- Events have clear semantics
- Profile-based obligations are explicit

### Migration Approach

1. **Implement Orders Capability understanding** (primary)
2. **Support all three profiles** (DELIVERY, PICKUP, ON_PREMISE)
3. **Map incoming to outgoing**: REST → REST, REST → Events, etc.
4. **Translate events**: Ensure normative events are always present
5. **Maintain state**: Track both sides' states
6. **Support both bindings**: REST + Events (if needed)

---

## Common Implementation Patterns

### Pattern 1: Merchant System (REST Binding)

```
Ordering App (REST client)
 ↓ POST /orders (with profile)
 Your Merchant System
 ↓ Implement
 ├── Accept/reject (emit CONFIRMED/REJECTED)
 ├── Track prep (emit PREPARING)
 ├── Ready event (emit READY_FOR_PICKUP)
 └── Dispatch event (emit DISPATCHED or DELIVERED)
 ↓ Webhook back to App
 Ordering App (receives events)
```

### Pattern 2: Logistics Provider (Mixed Binding)

```
Merchant (REST)
 ↓ POST /logistics/delivery (REST binding)
Your Logistics
 ↓ Implement
 ├── Accept/store delivery
 ├── Update via events (Event Stream binding)
 ├── Emit PICKED_UP event
 ├── Stream TRACKING_UPDATED events
 └── Emit DELIVERED event
 ↓ Webhooks or Event topics
Merchant + App (receive delivery updates)
```

### Pattern 3: Ordering App (Event Binding)

```
Merchants (Event Stream)
 ↓ Topic: orders/created
Your Ordering App
 ↓ Implement
 ├── Consume order created
 ├── Send to merchant system (REST or Events)
 ├── Consume merchant responses (REST webhooks or Events)
 ├── Emit order status updates (Events)
 └── Handle cancellations
 ↓ Events or webhooks
Customers (receive updates)
```

---

## Phased Migration Strategy

### Phase 1: Understand
- [ ] Read Principles
- [ ] Read Orders Capability
- [ ] Identify your role (Originator, Merchant, Logistics)
- [ ] Identify your order profiles (DELIVERY, PICKUP, etc.)

### Phase 2: Align Structure
- [ ] Map v1 data to v2 capability structure
- [ ] Add "profile" to order data
- [ ] Add "state" tracking (not just events)
- [ ] Identify normative events for your profile

### Phase 3: Implement API Specs
- [ ] Follow capability API Specs (API reference)
- [ ] Map endpoints to capability concepts
- [ ] Implement all normative events
- [ ] Implement error handling per conventions

### Phase 4: Handle Edge Cases
- [ ] Duplicate event handling
- [ ] Out-of-order events
- [ ] Cancellation as edge case
- [ ] Profile-specific behaviors

### Phase 5: Test & Validate
- [ ] Test all order profiles
- [ ] Verify normative events
- [ ] Test cancellation flows
- [ ] Test with other v2 implementers

---

## FAQ

### Q: Do I have to rewrite everything?
**A:** No. The capability concepts align with v1. You're adding structure (profiles, normative events) but the data is similar.

### Q: Can I still use REST APIs?
**A:** Yes. The V2 implementable contract **is** API Spec over REST/HTTP. Map your current endpoints to the published specs.

### Q: What if my order doesn't fit the three profiles?
**A:** The v2 design favors flexibility within profiles. If truly unique, consider:
1. Documenting how you map your scenario to a profile
2. Proposing a new profile for future versions
3. Using custom metadata

### Q: Do events have to be real-time?
**A:** No. Polling is fine when declared. Events represent facts; delivery mode (webhook vs poll) follows Discovery/API Spec.

### Q: How do I handle failure cases?
**A:** Principles cover tolerance and resilience—expect failures, handle idempotently, reconcile via state. See also API error conventions.

### Q: What about security/authentication?
**A:** See the Authentication API Spec and Protocol authentication pages (OAuth2, scopes, webhook signing).

---

## Getting Help

- **Domain / roles**: Protocol tab (Principles, capability pages)
- **Implementation**: API reference (API Spec)
- **Use Case Not Covered**: Open issue in GitHub repository

---
