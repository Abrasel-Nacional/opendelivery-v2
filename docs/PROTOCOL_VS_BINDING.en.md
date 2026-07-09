# Protocol vs. Transport Binding: Understanding the Separation

<div class="od-api-callout">
  <p>Protocolo vs transporte. Continue a jornada ou abra o contrato técnico.</p>
  <a href="reference/">Referência OpenAPI →</a>
</div>

This document clarifies the distinction between the **Open Delivery Protocol** and **Transport Bindings**, and how they work together.

---

## The Core Distinction

### The Protocol (What)
Defines **what systems must coordinate on**:
- Concepts (Order, Merchant, Delivery)
- Entity states and transitions
- Events that represent facts
- Actor responsibilities
- Obligations (normative/conditional/optional)

**Protocol is technology-agnostic.**

**Example:**
> "When a Merchant System receives an order with profile `DELIVERY`, it MUST emit either `ORDER_CONFIRMED` or `ORDER_REJECTED` within 60 seconds."

### Transport Binding (How)
Defines **how to carry protocol concepts** over a specific technology:
- Standardized paths/topics
- Serialization format
- Method/operation names
- Headers and authentication
- Request/response schemas

**Transport Binding is technology-specific.**

**Example (REST/HTTP Binding):**
```
POST /v1/orders/{orderId}/confirm
Content-Type: application/json
Authorization: Bearer {token}
X-Merchant-Id: {id}

{
  "metadata": {...}
}

→ 200 OK
{
  "orderId": "...",
  "state": "CONFIRMED",
  "timestamp": "..."
}
```

---

## Three Levels of Specification

```
Level 1: PROTOCOL (Conceptual)
┌────────────────────────────────────────┐
│ Orders Capability                      │
│ ├── Order entity                       │
│ ├── States: CREATED, CONFIRMED, ...    │
│ ├── Event: ORDER_CONFIRMED (normative) │
│ ├── Actor: Merchant System             │
│ └── Rule: MUST emit within 60 seconds  │
└────────────────────────────────────────┘
         ↓ (What needs to happen)
         
Level 2: TRANSPORT BINDING (Standardized)
┌────────────────────────────────────────┐
│ REST/HTTP Binding v1.0                 │
│ ├── Endpoint: POST /v1/orders/{id}/... │
│ ├── Headers: X-Merchant-Id, Content... │
│ ├── Request: {metadata: ...}           │
│ ├── Response: {state: "CONFIRMED", ...}│
│ └── Status: 200 OK, 202 Accepted, ...  │
└────────────────────────────────────────┘
         ↓ (How to transport it in HTTP)
         
Level 3: IMPLEMENTATION (Specific)
┌────────────────────────────────────────┐
│ Your Merchant System (Python/Go/Node)  │
│ ├── HTTP server listening on port 8080 │
│ ├── Endpoint handler registration      │
│ ├── Database state update               │
│ ├── Event emission/webhook delivery    │
│ └── Error handling & logging            │
└────────────────────────────────────────┘
```

---

## Mapping: Protocol Concept → Binding → Endpoint

### Example 1: Order Confirmation

**Protocol Level (from Orders Capability):**
```
Concept: ORDER_CONFIRMED event
Trigger: Merchant accepts the order
Obligation: MUST be emitted for all profiles
Contains: orderId, timestamp, metadata (optional)
```

**REST/HTTP Binding Level:**
```
Operation: Confirm order
Endpoint: POST /v1/orders/{orderId}/confirm
Headers: 
  - X-Merchant-Id (required)
  - Authorization (required)
  - Content-Type: application/json
Request:
  {
    "metadata": {
      "preparedBy": "John",
      "notes": "..."
    }
  }
Response (200 OK):
  {
    "orderId": "...",
    "state": "CONFIRMED",
    "timestamp": "2026-03-09T...",
    "profile": "DELIVERY"
  }
Response (202 Accepted):
  - Request accepted, processing async
Response (400 Bad Request):
  - Invalid orderId or state
Response (404 Not Found):
  - Order not found
```

**Implementation Level (Merchant System):**
```python
@app.post("/v1/orders/{orderId}/confirm")
async def confirm_order(orderId: str, request: ConfirmRequest):
    # 1. Validate request (header checks, signature)
    merchant_id = request.headers.get("X-Merchant-Id")
    if not merchant_id:
        return 400, {"error": "Missing X-Merchant-Id"}
    
    # 2. Find order in database
    order = db.order.find(orderId)
    if not order:
        return 404, {"error": "Order not found"}
    
    # 3. Validate state transition
    if order.state not in ["CREATED", "PENDING"]:
        return 400, {"error": "Cannot confirm order in state " + order.state}
    
    # 4. Update state
    order.state = "CONFIRMED"
    order.timestamp = now()
    db.order.save(order)
    
    # 5. Emit event (internal or webhook)
    emit_event(OrderConfirmedEvent(orderId=orderId, ...))
    
    # 6. Return response
    return 200, {
        "orderId": orderId,
        "state": "CONFIRMED",
        "timestamp": order.timestamp,
        "profile": order.profile
    }
```

---

### Example 2: Order Ready for Pickup

**Protocol Level (from Orders Capability):**
```
Concept: ORDER_READY_FOR_PICKUP event
Trigger: Order preparation complete
Obligation: MUST be emitted for all profiles
Semantics varies by profile:
  - DELIVERY: Ready for logistics pickup
  - PICKUP: Ready for customer collection
  - ON_PREMISE: Ready for table service
Contains: orderId, timestamp, optional pickupArea (PICKUP profile)
```

**REST/HTTP Binding Level:**
```
Operation: Mark order ready for pickup
Endpoint: POST /v1/orders/{orderId}/readyForPickup
Headers: 
  - X-Merchant-Id (required)
  - Authorization (required)
  - Content-Type: application/json
Request:
  {
    "pickupArea": "COUNTER_A",  // Only for PICKUP profile
    "estimatedWaitTime": 5
  }
Response (200 OK):
  {
    "orderId": "...",
    "state": "READY_FOR_PICKUP",
    "timestamp": "...",
    "profile": "DELIVERY"
  }
```

**Implementation Level:**
```typescript
// POST /v1/orders/{orderId}/readyForPickup
async function markOrderReady(req: Request, res: Response) {
  const { orderId } = req.params;
  const { pickupArea, estimatedWaitTime } = req.body;
  
  try {
    const order = await Order.findById(orderId);
    
    // Validate profile-specific requirements
    if (order.profile === "PICKUP" && !pickupArea) {
      return res.status(400).json({
        error: "pickupArea required for PICKUP profile"
      });
    }
    
    // Update state
    order.state = "READY_FOR_PICKUP";
    order.pickupArea = pickupArea;
    await order.save();
    
    // Emit event
    await EventEmitter.emit("order:ready", {
      orderId,
      profile: order.profile,
      timestamp: new Date()
    });
    
    // Notify external systems (webhook or polling)
    await notifyOriginatorViaWebhook(order);
    
    res.status(200).json({
      orderId,
      state: "READY_FOR_PICKUP",
      timestamp: order.timestamp,
      profile: order.profile
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

---

## Why This Separation Matters

### 1. Protocol Stability
- Protocol concepts don't change when transport technology evolves
- Can implement REST and Events bindings side-by-side
- Old implementations aren't immediately obsolete

### 2. Multiple Valid Implementations
- Same protocol, different bindings:
  - **REST/HTTP**: Web applications, traditional APIs
  - **Event Streams**: Asynchronous, high-volume systems
  - **gRPC**: High-performance, internal services
  - **Custom**: Domain-specific bindings

### 3. Clear Responsibility
- **Protocol**: "What must happen?"
- **Binding**: "How do we standardize it?"
- **Implementation**: "How do we make it work?"

### 4. Interoperability
- Systems using REST can talk to systems using Events (via gateway/adapter)
- Binding evolution doesn't break protocol implementations

---

## REST/HTTP Binding Development Roadmap

The REST/HTTP binding will provide:

**Phase 1: Endpoint Definitions** (Current)
- [ ] List all endpoints
- [ ] Define HTTP methods
- [ ] Describe path/query parameters
- [ ] Map to protocol concepts

**Phase 2: Request/Response Schemas** (Next)
- [ ] JSON schema for each request
- [ ] JSON schema for each response
- [ ] Error response format
- [ ] Validation rules

**Phase 3: Implementation Guidance** (Then)
- [ ] Code examples (multiple languages)
- [ ] Security patterns
- [ ] Error handling strategies
- [ ] Testing approaches

**Phase 4: OpenAPI Specification** (Future)
- [ ] Machine-readable OpenAPI 3.0 spec
- [ ] Swagger UI for interactive documentation
- [ ] SDK generation support

---

## REST/HTTP Binding Endpoint Summary

### Authentication
- `POST /oauth/token` – OAuth2 token exchange

### Merchant Endpoints
- `GET /v1/merchant/{id}` – Retrieve merchant data
- `GET /v1/merchant/{id}/status` – Check merchant status
- `PUT /v1/merchantOnboarding` – Register merchant

### Order Endpoints
- `POST /v1/orders` – Create order
- `GET /v1/orders/{orderId}` – Get order details
- `PATCH /v1/orders/{orderId}/details` – Update details
- `POST /v1/orders/{orderId}/confirm` – Confirm order
- `POST /v1/orders/{orderId}/preparing` – Order preparing (optional)
- `POST /v1/orders/{orderId}/readyForPickup` – Ready for pickup
- `POST /v1/orders/{orderId}/dispatch` – Dispatch order
- `POST /v1/orders/{orderId}/delivered` – Mark delivered
- `POST /v1/orders/{orderId}/requestCancellation` – Request cancel
- `POST /v1/orders/{orderId}/acceptCancellation` – Accept cancel
- `POST /v1/orders/{orderId}/denyCancellation` – Deny cancel

### Event Endpoints
- `GET /v1/events:polling` – Poll for events
- `POST /v1/events/acknowledgment` – Acknowledge events

### Logistics Endpoints
- `POST /v1/logistics/availability` – Check availability
- `POST /v1/logistics/delivery` – Create delivery
- `GET /v1/logistics/delivery/{orderId}` – Get delivery details
- `POST /v1/logistics/readyForPickup/{orderId}` – Notify ready
- `POST /v1/logistics/orderPicked/{orderId}` – Confirm picked up
- `POST /v1/logistics/finishDelivery/{orderId}` – Confirm delivered
- `POST /v1/logistics/handleProblem/{orderId}` – Report problem
- `POST /v1/logistics/cancel/{orderId}` – Cancel delivery

### Webhook Endpoints (Receiver Implements)
- `POST /v1/orderUpdate` – Order events webhook
- `POST /v1/deliveryUpdate` – Delivery events webhook
- `POST /v1/merchantUpdate` – Merchant update webhook

---

## How Protocol Principles Apply to Binding

### Principle: Events Represent Facts
**Protocol:** Order events are immutable facts
**REST Binding:** Each `POST` to `confirm`, `readyForPickup`, etc. generates an event
**Implementation:** Event object created with timestamp, metadata preserved

### Principle: Order Profile Determines Obligations
**Protocol:** Profile determines which events are normative
**REST Binding:** All profiles use same endpoints, but obligations differ
**Implementation:** Validate profile before accepting request, emit appropriate responses

### Principle: Tolerance and Resilience
**Protocol:** Systems must handle duplicate events, out-of-order delivery
**REST Binding:** No guaranteed delivery; retry + idempotency required
**Implementation:** Check event IDs, use idempotency keys, implement exponential backoff

### Principle: Decentralization
**Protocol:** No central authority, point-to-point communication
**REST Binding:** Direct HTTP calls between systems; optional webhook callbacks
**Implementation:** Use the mandatory REST well-known discovery endpoint, no hardcoded server lists

---

## Next Steps

1. **Continue Protocol Development** – Refine domain specifications
2. **Develop REST/HTTP Binding** – Define detailed endpoint specs and schemas
3. **Develop Alternate Bindings** – Event Stream, gRPC, etc.
4. **Create Implementation Guide** – Step-by-step for developers
5. **Build Validation Tools** – OpenAPI spec, schema validators
6. **Gather Feedback** – Community testing and real-world adoption

---
