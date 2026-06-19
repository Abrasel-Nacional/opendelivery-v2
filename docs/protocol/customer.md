# Customer Capability

## 1. Overview

Customer Capability defines interoperability for customer-related data and events with focus on CRM, relationship, and engagement scenarios.

This capability standardizes customer, lead, review, and customer-linked order exchanges without taking ownership of operational fulfillment lifecycle.

## 2. Scope and Extensions

Customer Capability covers:

- Customer master and enrichment data exchange
- Lead ingestion and qualification context
- Customer-centric order views for CRM analytics
- Customer relationship events (consent and engagement)
- Review ingestion model (draft under discussion)

Customer Capability does not cover:

- Kitchen, fulfillment, dispatch, or operational order transitions
- Campaign orchestration internals
- Reward catalog and loyalty business policy internals

Extension associated with Customer Capability:

- [Loyalty Extension (Customer)](../extensions/loyalty.md)

CRM systems MUST be treated as consumers of customer intelligence context and MUST NOT alter operational order state ownership.

## 3. Players

- `ORDERING_APPLICATION`: origin channels such as first-party app, marketplace, POS/PDV, digital menu, or indoor interface
- `CRM_SOFTWARE_SERVICE`: CRM, marketing automation, loyalty/couponing backends

`CRM_SOFTWARE_SERVICE` is a specialized software-service role for customer relationship use cases.

### Provider/Consumer Mapping

| participant | typical role as Provider | typical role as Consumer |
|---|---|---|
| `ORDERING_APPLICATION` | Exposes customer/order/event data interfaces in pull mode | Sends ingest payloads and consumes CRM outcomes in push mode |
| `CRM_SOFTWARE_SERVICE` | Exposes customer intelligence interfaces when pulling from ordering systems is not used | Consumes customer/order/event data from origin channels |

## 4. Interaction Between Players

Supported interaction patterns:

1. Push: `ORDERING_APPLICATION` sends customers/orders/events to CRM.
2. Pull: `CRM_SOFTWARE_SERVICE` fetches customers/orders from origin system.
3. Hybrid: push for selected entities and pull for others.

The protocol MUST NOT assume a single authoritative source for customer data, and external identifiers MUST be supported for deduplication/reconciliation.

## 5. Flows (Statuses and Events)

### Customer States

- `lead`: person in acquisition stage
- `active`: customer with active relationship
- `inactive`: customer without recent interaction

### Events

- `customer.created`
- `customer.updated`
- `customer.opted_in`
- `customer.opted_out`
- `lead.created`
- `order.created`
- `order.completed`
- `order.canceled`
- `review.created` (draft)

Flow/event principles:

- Events MUST represent business facts, not commands.
- Events SHOULD be emitted when they enable meaningful downstream action.
- Customer data MAY be incomplete as long as semantic structure remains valid.

## 6. Discovery / Well-Known Configuration

Participants exposing Customer Capability MUST declare capability name `customer` in discovery.

Discovery declaration SHOULD include:

- Supported integration mode(s): push, pull, hybrid
- Supported operation groups (customer, lead, order-view, event, review)
- Extension support metadata for loyalty/couponing when available

Each integration MUST explicitly declare supported mode(s) through discovery before operational exchange starts.

## 7. Authorization

Customer operations require authenticated requests with scope validation according to [Authentication and Authorization](authentication.md).

Recommended scope families by operation group:

- `customer.read`, `customer.write`
- `orders.crm.read`, `orders.crm.write`
- `customer.events.write`
- `lead.write`
- `review.write` (draft)

## 8. Operations

### `ingestCustomer`

- Provider: `CRM_SOFTWARE_SERVICE`
- Consumer: `ORDERING_APPLICATION`
- Originator: `ORDERING_APPLICATION`
- Receiver: `CRM_SOFTWARE_SERVICE`
- Authentication: Required
- Required scope: `customer.write`
- See: [Authentication and Authorization](authentication.md)

### `getCustomers`

- Provider: `ORDERING_APPLICATION`
- Consumer: `CRM_SOFTWARE_SERVICE`
- Originator: `CRM_SOFTWARE_SERVICE`
- Receiver: `ORDERING_APPLICATION`
- Authentication: Required
- Required scope: `customer.read`
- See: [Authentication and Authorization](authentication.md)

### `ingestOrdersForCRM`

- Provider: `CRM_SOFTWARE_SERVICE`
- Consumer: `ORDERING_APPLICATION`
- Originator: `ORDERING_APPLICATION`
- Receiver: `CRM_SOFTWARE_SERVICE`
- Authentication: Required
- Required scope: `orders.crm.write`
- See: [Authentication and Authorization](authentication.md)

### `getOrdersForCRM`

- Provider: `ORDERING_APPLICATION`
- Consumer: `CRM_SOFTWARE_SERVICE`
- Originator: `CRM_SOFTWARE_SERVICE`
- Receiver: `ORDERING_APPLICATION`
- Authentication: Required
- Required scope: `orders.crm.read`
- See: [Authentication and Authorization](authentication.md)

### `receiveCustomerEvent`

- Provider: `CRM_SOFTWARE_SERVICE`
- Consumer: `ORDERING_APPLICATION`
- Originator: `ORDERING_APPLICATION`
- Receiver: `CRM_SOFTWARE_SERVICE`
- Authentication: Required
- Required scope: `customer.events.write`
- See: [Authentication and Authorization](authentication.md)

### `ingestLead`

- Provider: `CRM_SOFTWARE_SERVICE`
- Consumer: `ORDERING_APPLICATION`
- Originator: `ORDERING_APPLICATION` (or lead source integrated through it)
- Receiver: `CRM_SOFTWARE_SERVICE`
- Authentication: Required
- Required scope: `lead.write`
- See: [Authentication and Authorization](authentication.md)

### Draft Operation: `ingestReview` (Under Discussion)

- Provider: `CRM_SOFTWARE_SERVICE`
- Consumer: `ORDERING_APPLICATION`
- Originator: `ORDERING_APPLICATION`
- Receiver: `CRM_SOFTWARE_SERVICE`
- Authentication: Required
- Required scope: `review.write`
- See: [Authentication and Authorization](authentication.md)

### Customer Fields

| name | type | required | description |
|---|---|---|---|
| `customer.id` | string | YES | Logical customer identifier |
| `customer.externalIds[]` | array[string] | YES | External identifiers for deduplication/reconciliation |
| `customer.name` | string | YES | Customer display name |
| `customer.contacts` | object | YES | Contact channels (phone, email) |
| `customer.document` | string | NO | National identity document (for example CPF) |
| `customer.birthDate` | string | NO | Birth date (`YYYY-MM-DD`) |
| `customer.gender` | string | NO | Optional demographic enrichment |
| `customer.consent` | object | YES | Consent metadata (opt-in/opt-out, legal basis) |
| `customer.createdAt` | string | YES | Creation timestamp (ISO 8601 date-time) |
| `customer.updatedAt` | string | YES | Update timestamp (ISO 8601 date-time) |

### Lead Fields

| name | type | required | description |
|---|---|---|---|
| `lead.id` | string | YES | Lead identifier |
| `lead.source` | string | YES | Lead source channel |
| `lead.status` | string | YES | Lead stage/status |
| `lead.customerRef` | string | NO | Optional customer link |

### Customer-Centric Order Fields

| name | type | required | description |
|---|---|---|---|
| `order.orderId` | string | YES | Reference to ODP order id |
| `order.customerId` | string | YES | Linked customer identifier |
| `order.salesChannel` | string | YES | Sales channel context |
| `order.timestamps` | object | YES | Minimal lifecycle markers for CRM analytics |

### Event Fields

| name | type | required | description |
|---|---|---|---|
| `event.eventType` | string | YES | Event classification |
| `event.entityType` | string | YES | Entity type (`customer`, `order`, `lead`, `review`) |
| `event.occurredAt` | string | YES | Business occurrence time (ISO 8601 date-time) |
| `event.payload` | object | YES | Event-specific payload |

### Draft Review Fields (Under Discussion)

| name | type | required | description |
|---|---|---|---|
| `review.id` | string | YES | Review identifier |
| `review.referenceType` | string | YES | Review reference type (`order`, `store`, `experience`) |
| `review.score` | number | YES | Numeric rating |
| `review.comment` | string | NO | Free-text comment |

## Pending Topics (Non-Normative)

- Final payload structure for reviews
- Detailed loyalty modeling (points, cashback, catalog, redemption)
- Formal separation between CRM and loyalty events
- Standard enums (`salesChannel`, `lead.status`, `lead.source`)
- Event versioning strategy
- Mandatory vs optional sensitive fields under LGPD guidance

## Out of Scope

- Campaign execution logic
- Loyalty business rules
- Reward catalog specifics
- CRM-to-CRM synchronization
- Real-time operational orchestration
- UI/UX or internal workflow definitions
