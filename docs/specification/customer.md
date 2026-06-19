# Customer Capability

- **Capability name:** `customer`

## Overview

Customer Capability defines interoperability for customer-centric CRM data exchange.
It covers customer records, leads, customer-context orders, reviews, and customer events.

This capability is transport-agnostic at semantic level and does not impose internal CRM
business policies (campaign engines, scoring algorithms, point rules, expiration rules).

### Scope

Customer Capability covers:

- Customer master and enrichment data exchange
- Lead ingestion and synchronization
- Order snapshots in CRM context
- Review ingestion and retrieval
- Customer-focused event exchange

Customer Capability does not cover:

- Fulfillment ownership and operational orchestration
- Loyalty internal accounting logic
- Campaign orchestration internals

Extension associated with Customer Capability:

- [Loyalty Extension](./loyalty.md)

## Participants

| Participant | Provider | Consumer |
|---|---|---|
| **Ordering Application / Origin Platform** | Exposes source customer, lead, order, and event data in pull mode | Sends customer, lead, order, review, and event payloads in push mode |
| **CRM Software Service** | Exposes customer intelligence interfaces and receives push payloads | Pulls source records for synchronization and enrichment |

## Schema Baseline (Aligned with Committee OpenAPI)

The table below lists the normative schemas exposed in the Customer capability contract.

| Schema | Type | Required | Description |
|---|---|---|---|
| `Customer` | object | YES | Core customer entity; only `identifier` is required |
| `CustomerIdentifier` | object | YES | Canonical identifier (`type`, `value`) |
| `CustomerDocument` | object | NO | Optional customer document block |
| `CustomerContacts` | object | NO | Optional phone/email collections |
| `CustomerPhone` | object | NO | Optional phone entry |
| `CustomerEmail` | object | NO | Optional email entry |
| `CustomerDemographics` | object | NO | Optional demographic data |
| `CustomerAddress` | object | NO | Optional customer address entry |
| `GeoCoordinates` | object | NO | Optional geographic coordinates |
| `CustomerExternalId` | object | NO | Optional cross-system identifier |
| `CustomerMetadata` | object | NO | Optional extensible metadata (`additionalProperties: true`) |
| `Lead` | object | NO | Lead entity in customer context |
| `Order` | object (`allOf`) | NO | Reuse of canonical Order schema from main OpenAPI |
| `Review` | object | NO | Review payload with overall rating and optional detailed questions |
| `CustomerEvent` | object | NO | Customer-focused event webhook payload |

## OpenAPI Traceability Matrix

This matrix maps Customer endpoints to request/response schemas from the committee OpenAPI.

| Endpoint | Method | Request Body Type | Response Type |
|---|---|---|---|
| `/customers` | GET | none | array[Customer] |
| `/customers` | POST | array[Customer] | status-only (`200`) |
| `/customers/{id}` | GET | none | Customer |
| `/leads` | GET | none | array[Lead] |
| `/leads` | POST | array[Lead] | status-only (`200`) |
| `/orders` | GET | none | array[Order] |
| `/orders` | POST | array[Order] | status-only (`201`) |
| `/orders/{id}` | GET | none | Order |
| `/reviews` | GET | none | array[Review] |
| `/reviews` | POST | Review | status-only (`201`) |
| `/customers/{customerId}/reviews` | GET | none | array[Review] |
| `/reviews/{id}` | GET | none | Review |
| `/customer/events` | GET | none | array[CustomerEvent] |
| `/customer/events` | POST | CustomerEvent | status-only (`202`) |

### Customer Normative Rules

| Rule | Type | Required | Description |
|---|---|---|---|
| `identifier` | object | YES | The only required field in `Customer` |
| `identifier.type` | string | YES | Canonical identifier type (`document`, `phone`, `email`, `external_id`, `custom`) |
| `identifier.value` | string | YES | Canonical identifier value |
| `document` | object | NO | MUST remain optional |
| `contacts` | object | NO | MUST remain optional |
| `externalIds` | array[object] | NO | MUST remain optional |
| `metadata` | object | NO | SHOULD be used for restrictions/blocks/custom rules |

### Review MVP Baseline

| Field | Type | Required | Description |
|---|---|---|---|
| `reviewType` | string | YES | Review context (`ORDER`, `MERCHANT_EXPERIENCE`, `EVENT`) |
| `overallRating.ratingStyle` | string | YES | Rating style (`STAR`, `THUMBS_UP_DOWN`, `NPS`, `OTHER`) |
| `overallRating.value` | number | YES | Main score value |
| `overallRating.comment` | string | NO | Optional textual feedback |
| `customer.customerId` | string | NO | Optional customer reference |
| `subject.orderId` | string | NO | Optional order reference |
| `reviewDate` | string | YES | RFC 3339 timestamp |

## Schema Examples

### Example: Customer (Minimal)

```json
{
  "identifier": {
    "type": "phone",
    "value": "+5511999999999"
  }
}
```

### Example: Customer (Enriched)

```json
{
  "identifier": {
    "type": "external_id",
    "value": "crm:customer:93821"
  },
  "name": "Maria Silva",
  "contacts": {
    "emails": [
      {
        "email": "maria.silva@example.com",
        "isPrimary": true
      }
    ]
  },
  "externalIds": [
    {
      "source": "PDV",
      "sourceName": "PDV Loja Centro",
      "key": "customerCode",
      "value": "C12345"
    }
  ],
  "metadata": {
    "restrictions": [
      "requiresManualReview"
    ],
    "customRules": {
      "requiresManualReview": true
    },
    "customTags": [
      "vip"
    ]
  }
}
```

### Example: Lead

```json
{
  "id": "lead-001",
  "name": "Ana Souza",
  "contact": "ana.souza@example.com",
  "externalIds": [
    {
      "source": "CRM",
      "sourceName": "CRM Core",
      "key": "leadCode",
      "value": "L-1020"
    }
  ]
}
```

### Example: Review

```json
{
  "reviewId": "rev-001",
  "reviewType": "ORDER",
  "overallRating": {
    "ratingStyle": "STAR",
    "value": 4,
    "comment": "Fast delivery and good food."
  },
  "subject": {
    "orderId": "ord-001",
    "merchantId": "merchant-01"
  },
  "customer": {
    "customerId": "cust-001",
    "email": "maria.silva@example.com"
  },
  "reviewDate": "2026-06-01T12:00:00Z",
  "source": {
    "system": "CRM",
    "channel": "DELIVERY_APP"
  }
}
```

### Example: CustomerEvent

```json
{
  "eventType": "ORDER_COMPLETED",
  "occurredAt": "2026-06-01T12:30:00Z",
  "customerId": "cust-001",
  "data": {
    "orderId": "ord-001",
    "totalAmount": 7990,
    "currency": "BRL"
  }
}
```

## Operations

| Operation | Provider | Consumer | Description |
|---|---|---|---|
| `listCustomers` | Origin Platform | CRM Software Service | Retrieve customers from source system |
| `upsertCustomer` | CRM Software Service | Origin Platform | Ingest/create/update customers (batch-capable) |
| `getCustomerById` | Origin Platform | CRM Software Service | Retrieve single customer by ID |
| `listLeads` | Origin Platform | CRM Software Service | Retrieve leads from source system |
| `upsertLead` | CRM Software Service | Origin Platform | Ingest/create/update leads (batch-capable) |
| `listOrders` | Origin Platform | CRM Software Service | Retrieve customer-context orders |
| `upsertOrders` | CRM Software Service | Origin Platform | Push orders to CRM (batch-capable) |
| `getOrderById` | Origin Platform | CRM Software Service | Retrieve single order by ID |
| `createReview` | CRM Software Service | Origin Platform | Send a review payload to CRM |
| `listReviews` | Origin Platform | CRM Software Service | Retrieve reviews |
| `listCustomerReviews` | Origin Platform | CRM Software Service | Retrieve reviews by customer |
| `getReviewById` | Origin Platform | CRM Software Service | Retrieve review by ID (optional endpoint) |
| `publishCustomerEvent` | CRM Software Service | Origin Platform | Send customer-focused events |
| `listCustomerEvents` | Origin Platform | CRM Software Service | Retrieve customer event history |

For transport-specific details, see [REST Binding - Customer](./customer-rest.md).
For loyalty-specific schemas and transport, see [Loyalty Extension](./loyalty.md) and
[REST Binding - Loyalty](./loyalty-rest.md).
