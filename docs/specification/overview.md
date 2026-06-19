# Open Delivery Protocol — Official Specification

## Overarching Guidelines

The key words `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, `SHOULD NOT`, `RECOMMENDED`, `MAY`, and
`OPTIONAL` in this document are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html).

Schema notes:

- Date/time format: always [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) unless stated otherwise
- Monetary amounts: minor units (cents) as defined by ISO 4217
- Identifiers: stable strings, opaque to consumers unless otherwise specified

## Discovery

Before any capability operation, participants MUST publish a machine-readable discovery document
at a well-known endpoint.

### Well-Known Endpoint

```
GET /.well-known/opendelivery
```

Every discovery URL MUST end with this suffix. Using the domain root is recommended:

```
https://yourdomain.com/.well-known/opendelivery
```

The exact URL MUST be communicated to the other participant through out-of-band channels (e.g.,
configuration, registration, or manual setup) before any capability operation begins.

### Discovery Rules

- The endpoint MUST be publicly accessible without authentication.
- The endpoint MUST use HTTPS (TLS).
- The endpoint MUST include proper `CORS` headers when accessed from browser contexts.
- The endpoint MUST NOT redirect (3xx).
- The endpoint response SHOULD include a `Cache-Control` header with a reasonable `max-age`.

### Discovery Document

A valid discovery document MUST include all required fields and MUST NOT declare capabilities or
operations the participant cannot execute.

| Field | Type | Required | Description |
|---|---|---|---|
| `participantId` | string | YES | Unique participant identifier |
| `protocolVersion` | string | YES | Protocol version string (e.g., `v2`) |
| `capabilities` | array | YES | List of supported capability declarations |
| `capabilities[].name` | string | YES | Capability name (`orders`, `merchant`, `customer`, `logistics`) |
| `capabilities[].role` | string | YES | Participant role: `ORIGINATOR`, `RECEIVER`, or `BOTH` |
| `capabilities[].operations` | array[string] | YES | Supported operation identifiers |
| `capabilities[].extensions` | array[string] | NO | Active extension names for this capability |
| `capabilities[].endpoint` | string | NO | Base URL for REST transport binding |
| `compatibility` | string | NO | Compatibility statement |

### Discovery Example

```json
{
  "participantId": "my-service-001",
  "protocolVersion": "v2",
  "capabilities": [
    {
      "name": "orders",
      "role": "RECEIVER",
      "operations": ["confirmOrder", "setPreparing", "setReadyForPickup", "cancelOrder"],
      "extensions": [],
      "endpoint": "https://api.myservice.com/opendelivery/v2"
    },
    {
      "name": "merchant",
      "role": "RECEIVER",
      "operations": ["getMerchant", "getMenu"],
      "endpoint": "https://api.myservice.com/opendelivery/v2"
    }
  ]
}
```

Transport-specific details are defined in
[REST Binding — Discovery](../specification/rest-discovery.md).

---

## Identity and Authentication

Authentication is a protocol-wide mechanism that accompanies capability operations. It is not a
capability.

### Normative Rules

1. Implementations MUST support a merchant-scoped credential model.
2. Implementations MUST NOT share one credential set across unrelated merchants.
3. Authentication material MUST be protected in transit and at rest.
4. Access scopes MUST be explicit and auditable.
5. Event callbacks MUST use an authenticated trust mechanism.

### Merchant-Scoped Credentials

All operations on behalf of a specific merchant MUST be authenticated with credentials scoped to
that merchant. Credentials MUST NOT be reused across different merchant scopes.

### Operation-Level Authentication

Each capability operation explicitly declares:

- Whether the operation is public or protected
- Which scope is required when the operation is protected
- Which participant presents the credential
- Which trust rule applies to callbacks or asynchronous notifications

### Authentication Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `credential.merchantId` | string | YES | Merchant scope for the credential |
| `credential.clientId` | string | YES | Client identifier |
| `credential.scope` | string | YES | Granted protocol scope |
| `credential.expiresAt` | string | NO | Credential expiration timestamp (RFC 3339) |

---

## Transport Layer

ODP currently defines one transport binding: **REST/HTTP**.

### REST Transport

- All endpoints MUST use HTTPS.
- `Content-Type` MUST be `application/json` for all request and response bodies.
- Implementations MUST use standard HTTP verbs (`GET` for retrieval, `POST` for mutations).
- Implementations MUST use standard HTTP status codes.

For endpoint conventions and headers, see [REST Transport Binding](../specification/rest.md).

---

## Error Model

### Error Rules

1. Error responses MUST be machine-readable.
2. Error classification MUST preserve semantic meaning for automation.
3. Producers MUST NOT emit success fields when processing failed.
4. Cancellation-specific failures MUST be explicitly distinguishable from general errors.

### Error Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `error.code` | string | YES | Stable machine-readable error code |
| `error.message` | string | YES | Human-readable description |
| `error.details` | object | NO | Additional structured context |
| `error.retryable` | boolean | NO | Whether a retry is safe |
| `error.timestamp` | string | NO | Emission timestamp (RFC 3339) |

### Error Example

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Order identifier is unknown for this merchant scope",
    "retryable": false
  }
}
```

---

## Capabilities

ODP defines the following capabilities:

| Capability | Description |
|---|---|
| [Merchant](./merchant.md) | Merchant identity, catalog, services, and operational context |
| [Orders](./orders.md) | Order lifecycle, state management, and coordination |
| [Indoor](./indoor.md) | On-premise order operations as an extension of Orders |
| [Customer](./customer.md) | CRM, leads, customer events, and customer-linked order views |
| [Loyalty](./loyalty.md) | Loyalty identity, accrual, redemption, and coupon validation |
| [Logistics](./logistics.md) | Delivery coordination, tracking, and problem handling |

---

## Roles and Responsibilities

### Cross-Capability Roles

Every operation declares a **Provider** and a **Consumer**:

- **Provider** — participant that exposes the operation interface (endpoint or event channel)
- **Consumer** — participant that invokes or subscribes to that interface

A participant MAY act as Provider in one operation and Consumer in another.

### Participant Types

| Role | Responsibilities |
|---|---|
| **Ordering Application** | Consume merchant context; create and track orders; consume delivery events |
| **Software Service** | Publish merchant context; receive and process orders; emit lifecycle events |
| **Logistics Service** | Accept delivery requests; emit tracking and incident events |
| **CRM Software Service** | Consume customer and order data for CRM, loyalty, and marketing |

---

## Versioning

### Version Format

ODP uses semantic version strings (e.g., `v2`). Breaking changes MUST increment the major version.

### Backwards Compatibility

The following MAY be introduced without a new version:

- Adding new optional fields to responses
- Adding new optional parameters to requests
- Adding new operations or endpoints
- Adding new enum values

The following MUST NOT be introduced without a version increment:

- Removing or renaming existing fields
- Changing field types or semantics
- Making optional fields required
- Removing operations or endpoints
- Changing authentication requirements
- Modifying existing lifecycle state machines

---

## General Interoperability Rules

1. Producers MUST include all required fields.
2. Consumers MUST validate required fields.
3. Consumers SHOULD tolerate unknown additive fields.
4. Participants MUST NOT infer unsupported state transitions.
5. Participants MUST process events idempotently.
6. Secrets MUST NOT be exposed in logs or traces.
7. Callback trust validation MUST be enforced for asynchronous delivery.
