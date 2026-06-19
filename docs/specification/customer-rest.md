# Customer - REST Binding

This document specifies the HTTP/REST binding for the [Customer Capability](./customer.md).

## Protocol Fundamentals

### Discovery

Participants advertise Customer REST availability through the protocol discovery document,
including capability name, transport (`rest`), and endpoint base URL.

### Authentication

All endpoints require `bearerAuth` (HTTP Bearer JWT).

### Content Type

- Request content type: `application/json`
- Response content type: `application/json`

### Base URL

Example base URL from committee draft:

`https://api.opendelivery.io/v2`

## Operations

| Operation | Method | Path | Entity | Description |
|---|---|---|---|---|
| [List Customers](#list-customers) | GET | `/customers` | Customer | Retrieve all customers |
| [Upsert Customers](#upsert-customers) | POST | `/customers` | Customer | Create or update customers in batch |
| [Get Customer By ID](#get-customer-by-id) | GET | `/customers/{id}` | Customer | Retrieve a specific customer by identifier |
| [List Leads](#list-leads) | GET | `/customers/leads` | Lead | Retrieve all leads |
| [Upsert Leads](#upsert-leads) | POST | `/customers/leads` | Lead | Create or update leads in batch |
| [List Orders](#list-orders) | GET | `/customers/orders` | Order | Retrieve all orders |
| [Upsert Orders](#upsert-orders) | POST | `/customers/orders` | Order | Create or update orders in batch |
| [Get Order By ID](#get-order-by-id) | GET | `/customers/orders/{id}` | Order | Retrieve a specific order by identifier |
| [Create Review](#create-review) | POST | `/customers/reviews` | Review | Create a new review |
| [List Reviews](#list-reviews) | GET | `/customers/reviews` | Review | Retrieve all reviews |
| [List Customer Reviews](#list-customer-reviews) | GET | `/customers/{customerId}/reviews` | Review | Retrieve reviews for a specific customer |

### List Customers

Method and path: `GET /customers`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| query params | object | No | Optional implementation-specific filters |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Customer] | Yes | Customer list |

#### Example

=== "Request"
    ```http
    GET /customers HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    [
      {
        "identifier": {
          "type": "phone",
          "value": "+5511999999999"
        },
        "name": "Maria Silva"
      }
    ]
    ```

### Upsert Customers

Method and path: `POST /customers`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Customer] | Yes | Customers to create/update |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| status | integer | Yes | `200` on success |

#### Example

=== "Request"
    ```http
    POST /customers HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Content-Type: application/json

    [
      {
        "identifier": {
          "type": "external_id",
          "value": "crm:customer:93821"
        },
        "name": "Maria Silva"
      }
    ]
    ```

=== "Response (200)"
    ```text
    No body
    ```

### Get Customer By ID

Method and path: `GET /customers/{id}`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Customer identifier |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | Customer | Yes | Customer payload |

#### Example

=== "Request"
    ```http
    GET /customers/cust-001 HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    {
      "identifier": {
        "type": "external_id",
        "value": "cust-001"
      },
      "name": "Maria Silva"
    }
    ```

### List Leads

Method and path: `GET /customers/leads`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| query params | object | No | Optional implementation-specific filters |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Lead] | Yes | Lead list |

#### Example

=== "Request"
    ```http
    GET /customers/leads HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    [
      {
        "id": "lead-001",
        "name": "Ana Souza",
        "contact": "ana.souza@example.com"
      }
    ]
    ```

### Upsert Leads

Method and path: `POST /customers/leads`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Lead] | Yes | Leads to create/update |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| status | integer | Yes | `200` on success |

#### Example

=== "Request"
    ```http
    POST /customers/leads HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Content-Type: application/json

    [
      {
        "id": "lead-001",
        "name": "Ana Souza",
        "contact": "ana.souza@example.com"
      }
    ]
    ```

=== "Response (200)"
    ```text
    No body
    ```

### List Orders

Method and path: `GET /customers/orders`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| query params | object | No | Optional implementation-specific filters |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Order] | Yes | Order list |

#### Example

=== "Request"
    ```http
    GET /customers/orders HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    [
      {
        "id": "ord-001",
        "status": "CONFIRMED",
        "customer": {
          "id": "cust-001"
        }
      }
    ]
    ```

### Upsert Orders

Method and path: `POST /customers/orders`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Order] | Yes | Orders to ingest |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| status | integer | Yes | `201` on success |

#### Example

=== "Request"
    ```http
    POST /customers/orders HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Content-Type: application/json

    [
      {
        "id": "ord-001",
        "status": "CONFIRMED",
        "customer": {
          "id": "cust-001"
        }
      }
    ]
    ```

=== "Response (201)"
    ```text
    No body
    ```

### Get Order By ID

Method and path: `GET /customers/orders/{id}`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Order identifier |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | Order | Yes | Order payload |

#### Example

=== "Request"
    ```http
    GET /customers/orders/ord-001 HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    {
      "id": "ord-001",
      "status": "DELIVERED",
      "customer": {
        "id": "cust-001"
      }
    }
    ```

### Create Review

Method and path: `POST /customers/reviews`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | Review | Yes | Review payload |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| status | integer | Yes | `201` on success |

#### Example

=== "Request"
    ```http
    POST /customers/reviews HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Content-Type: application/json

    {
      "reviewId": "rev-001",
      "reviewType": "ORDER",
      "overallRating": {
        "ratingStyle": "STAR",
        "value": 5,
        "comment": "Great experience"
      },
      "subject": {
        "orderId": "ord-001"
      },
      "customer": {
        "customerId": "cust-001"
      },
      "reviewDate": "2026-06-01T12:00:00Z"
    }
    ```

=== "Response (201)"
    ```text
    No body
    ```

### List Reviews

Method and path: `GET /customers/reviews`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| query params | object | No | Optional implementation-specific filters |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Review] | Yes | Review list |

#### Example

=== "Request"
    ```http
    GET /customers/reviews HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    [
      {
        "reviewId": "rev-001",
        "reviewType": "ORDER",
        "overallRating": {
          "ratingStyle": "STAR",
          "value": 5
        },
        "reviewDate": "2026-06-01T12:00:00Z"
      }
    ]
    ```

### List Customer Reviews

Method and path: `GET /customers/{customerId}/reviews`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `customerId` | string | Yes | Customer identifier |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Review] | Yes | Reviews for the customer |

#### Example

=== "Request"
    ```http
    GET /customers/cust-001/reviews HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    [
      {
        "reviewId": "rev-001",
        "reviewType": "ORDER",
        "overallRating": {
          "ratingStyle": "STAR",
          "value": 4
        },
        "customer": {
          "customerId": "cust-001"
        },
        "reviewDate": "2026-06-01T12:00:00Z"
      }
    ]
    ```

## Error Handling

UCP-style two-layer interpretation applies: transport-level failures use HTTP status,
while business semantics are expressed by endpoint responses and payloads.

### Transport Errors

| HTTP | Description |
|---|---|
| `400` | Bad request (defined in committee OpenAPI) |
| `401` | Unauthorized (auth policy) |
| `403` | Forbidden (authz policy) |
| `404` | Not found (resource path/ID resolution) |
| `500` | Internal server error |

### Business Outcomes

Business outcomes are represented by endpoint-specific success responses (`200`, `201`)
and response payloads (`Customer`, `Lead`, `Order`, `Review`).

## Entities

### Customer Collection Response

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Customer] | Yes | Customer list response |

### Lead Collection Response

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Lead] | Yes | Lead list response |

### Order Collection Response

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Order] | Yes | Order list response |

### Review Collection Response

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Review] | Yes | Review list response |

### Error Response (`BadRequest`)

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string | No | Machine-readable error code |
| `message` | string | No | Human-readable error message |

## Conformance

A conforming Customer REST implementation MUST:

1. Implement all advertised Customer operations in discovery metadata.
2. Enforce Bearer authentication on all operations.
3. Accept and return JSON payloads as defined by Customer and related schemas.
4. Support batch payloads where defined (`POST /customers`, `POST /leads`, `POST /orders`).
5. Return status codes consistent with this binding and committee OpenAPI.

For loyalty transport under Customer scope, see [Loyalty - REST Binding](./loyalty-rest.md).
