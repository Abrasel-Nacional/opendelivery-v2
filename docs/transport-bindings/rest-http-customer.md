# Customer Endpoints

Normative source: [Customer Capability](../protocol/customer.md).

This page defines the REST/HTTP transport contract for Customer Capability operations.
It does not redefine protocol semantics.

## Endpoint Catalog

| operation | method | path | authentication | scope |
|---|---|---|---|---|
| `ingestCustomer` | `POST` | `/v1/customer/customers:ingest` | required | `customer.write` |
| `getCustomers` | `GET` | `/v1/customer/customers` | required | `customer.read` |
| `ingestOrdersForCRM` | `POST` | `/v1/customer/orders:ingest` | required | `orders.crm.write` |
| `getOrdersForCRM` | `GET` | `/v1/customer/orders` | required | `orders.crm.read` |
| `receiveCustomerEvent` | `POST` | `/v1/customer/events` | required | `customer.events.write` |
| `ingestLead` | `POST` | `/v1/customer/leads:ingest` | required | `lead.write` |
| `ingestReview` (draft) | `POST` | `/v1/customer/reviews:ingest` | required | `review.write` |

All endpoints in this binding MUST use HTTPS and `application/json` payloads.

## Request Payload Fields

### Customer Ingestion (`ingestCustomer`)

| name | type | required | description |
|---|---|---|---|
| `customer.id` | string | YES | Logical customer identifier |
| `customer.externalIds[]` | array[string] | YES | External identifiers for deduplication |
| `customer.name` | string | YES | Customer display name |
| `customer.contacts` | object | YES | Contact channels |
| `customer.consent` | object | YES | Consent metadata |
| `customer.createdAt` | string | YES | Creation timestamp (ISO 8601 date-time) |
| `customer.updatedAt` | string | YES | Update timestamp (ISO 8601 date-time) |

### Lead Ingestion (`ingestLead`)

| name | type | required | description |
|---|---|---|---|
| `lead.id` | string | YES | Lead identifier |
| `lead.source` | string | YES | Lead source |
| `lead.status` | string | YES | Lead stage |
| `lead.customerRef` | string | NO | Linked customer id |

### Customer Event (`receiveCustomerEvent`)

| name | type | required | description |
|---|---|---|---|
| `event.eventType` | string | YES | Business fact type |
| `event.entityType` | string | YES | `customer`, `order`, `lead`, or `review` |
| `event.occurredAt` | string | YES | Occurrence timestamp (ISO 8601 date-time) |
| `event.payload` | object | YES | Event payload |

## Payload Examples

### `ingestCustomer`

```json
{
  "customer": {
    "id": "customer-123",
    "externalIds": ["app:123", "crm:ABC-9"],
    "name": "Maria Souza",
    "contacts": {
      "email": "maria@example.com",
      "phone": "+55-11-99999-0000"
    },
    "consent": {
      "marketing": true,
      "updatedAt": "2026-03-24T12:00:00Z"
    },
    "createdAt": "2026-03-01T10:00:00Z",
    "updatedAt": "2026-03-24T12:00:00Z"
  }
}
```

### `receiveCustomerEvent`

```json
{
  "event": {
    "eventType": "customer.updated",
    "entityType": "customer",
    "occurredAt": "2026-03-24T12:00:00Z",
    "payload": {
      "customerId": "customer-123",
      "changedFields": ["contacts.email", "consent.marketing"]
    }
  }
}
```

## Response Contract

### Successful Status Codes

| endpoint type | status | meaning |
|---|---|---|
| Ingestion endpoints (`POST`) | `202 Accepted` | Accepted for asynchronous processing |
| Query endpoints (`GET`) | `200 OK` | Data returned successfully |

### Error Status Codes

| status | when | body |
|---|---|---|
| `400 Bad Request` | malformed payload/params | ODP error model |
| `401 Unauthorized` | missing/invalid credentials | ODP error model |
| `403 Forbidden` | missing required scope | ODP error model |
| `404 Not Found` | endpoint/resource not found | ODP error model |
| `409 Conflict` | duplicate or version conflict | ODP error model |
| `500 Internal Server Error` | unexpected server failure | ODP error model |

Error payloads SHOULD follow [Error Model](../protocol/error-handling.md).

## Protocol Rules Applied

!!! info "Normative source: [Customer Capability](../protocol/customer.md)"
    - CRM software MUST be consumer-oriented and MUST NOT control operational order lifecycle.
    - Ordering Applications MUST expose declared customer and customer-linked order operations.
    - Events MUST represent business facts.
    - External identifiers MUST be supported for deduplication.
    - Customer-centric order view MUST NOT replace operational order lifecycle semantics.

## OpenAPI Artifact

- Download: [customer.openapi.yaml](../reference/v2/customer.openapi.yaml)
