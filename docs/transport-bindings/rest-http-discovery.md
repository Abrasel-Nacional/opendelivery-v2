# Discovery Endpoint

Normative source: [Discovery and Well-Known](../protocol/discovery.md).

This page defines the REST/HTTP transport contract for the ODP discovery endpoint.
It does not redefine protocol rules — only their HTTP-level implementation.

## Endpoint

| field | type | value |
|---|---|---|
| method | string | `GET` |
| url suffix | string | `/.well-known/opendelivery` |
| authentication | string | `none` — public endpoint, no credentials required |
| transport security | string | `HTTPS` required |
| response content type | string | `application/json` |

The discovery URL MUST end with `/.well-known/opendelivery`.
The participant MAY use any host or path prefix as long as the suffix is preserved.

Valid examples:

- `https://dominio.com/.well-known/opendelivery` (recommended)
- `https://api.dominio.com/.well-known/opendelivery`
- `https://dominio.com/api/.well-known/opendelivery`

## Request

### Headers

| name | type | required | description |
|---|---|---|---|
| `Accept` | string | NO | Preferred response media type. Recommended: `application/json`. |

### Example

```http
GET /.well-known/opendelivery HTTP/1.1
Host: dominio.com
Accept: application/json
```

## Successful Response

### Status: `200 OK`

### Headers

| name | type | required | description |
|---|---|---|---|
| `Content-Type` | string | YES | Must be `application/json`. |
| `Cache-Control` | string | NO | Recommended: `no-store`. |
| `Access-Control-Allow-Origin` | string | NO | Required if browser access is supported. |

### Body Fields

| name | type | required | description |
|---|---|---|---|
| `discovery.participantId` | string | YES | Unique participant identifier |
| `discovery.protocolVersion` | string | YES | Protocol version string |
| `discovery.capabilities[].name` | string | YES | Capability name: `merchant`, `orders`, `customer`, or `logistics` |
| `discovery.capabilities[].role` | string | YES | Participant role: `ORIGINATOR`, `RECEIVER`, or `BOTH` |
| `discovery.capabilities[].operations[]` | array[string] | YES | Supported operation identifiers |
| `discovery.capabilities[].profiles[]` | array[string] | NO | Supported profiles or variants |
| `discovery.compatibility` | string | NO | Compatibility statement |
| `discovery.notes` | string | NO | Informative notes |

### Example

```json
{
 "discovery": {
 "participantId": "software-service-123",
 "protocolVersion": "v2.0.0-draft",
 "capabilities": [
 {
 "name": "merchant",
 "role": "ORIGINATOR",
 "operations": ["publishMerchant", "notifyMerchantUpdate"]
 },
 {
 "name": "orders",
 "role": "RECEIVER",
 "operations": ["receiveOrder", "acknowledgeOrderEvent", "resolveCancellation"]
 },
 {
 "name": "logistics",
 "role": "BOTH",
 "operations": ["quoteDelivery", "createDelivery", "publishDeliveryEvent"]
 }
 ],
 "compatibility": "backward-compatible"
 }
}
```

## Error Responses

| status | when | body |
|---|---|---|
| `400 Bad Request` | Malformed request | ODP error model |
| `404 Not Found` | Endpoint not configured or path not found | ODP error model |
| `406 Not Acceptable` | Unsupported `Accept` header value | ODP error model |
| `500 Internal Server Error` | Unexpected server failure | ODP error model |

Error payloads SHOULD follow the [Error Model](../protocol/error-handling.md).

## Protocol Rules Applied

!!! info "Normative source: [Discovery and Well-Known](../protocol/discovery.md)"
    - Participant MUST publish discovery before capability coordination.
    - Endpoint MUST be public — no authentication.
    - Endpoint MUST use HTTPS (SSL/TLS).
    - URL MUST end with `/.well-known/opendelivery`.
    - Full URL MUST be communicated to partner before operations.
    - Payload MUST include all required fields and MUST NOT declare unsupported behaviors.

## especificação da API Artifact

- Download: [discovery.openapi.yaml](../reference/v2/discovery.openapi.yaml)
