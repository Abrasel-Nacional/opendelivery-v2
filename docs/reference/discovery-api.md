# Discovery API

This page presents the Discovery API in a documentation style native to MkDocs.

Normative behavior remains defined in [Discovery and Well-Known](../protocol/discovery.md).
HTTP transport rules remain defined in [REST/HTTP Discovery Binding](../transport-bindings/rest-http-discovery.md).
The machine-readable contract remains defined in [discovery.openapi.yaml](v2/discovery.openapi.yaml).

## Endpoint Summary

| field | type | value |
|---|---|---|
| method | string | `GET` |
| url suffix | string | `/.well-known/opendelivery` |
| authentication | string | `none` |
| transport security | string | `HTTPS` |
| request content type | string | none |
| response content type | string | `application/json` |

The final URL MUST end with `/.well-known/opendelivery`.
The endpoint MAY be exposed under any host or path prefix, as long as the suffix is preserved.

Examples:

- `https://dominio.com/.well-known/opendelivery`
- `https://api.dominio.com/.well-known/opendelivery`
- `https://dominio.com/api/.well-known/opendelivery`

## Request

### Headers

| name | type | required | description |
|---|---|---|---|
| `Accept` | string | NO | Preferred response media type. Recommended value: `application/json`. |
| `Host` | string | YES | Target host, following HTTP semantics. |

### Example

```http
GET /.well-known/opendelivery HTTP/1.1
Host: dominio.com
Accept: application/json
```

## Successful Response

### Status

| status | description |
|---|---|
| `200 OK` | Discovery metadata returned successfully |

### Headers

| name | type | required | description |
|---|---|---|---|
| `Content-Type` | string | YES | Response media type. Expected value: `application/json`. |
| `Cache-Control` | string | NO | Cache behavior for clients and intermediaries. Recommended value: `no-store`. |
| `Access-Control-Allow-Origin` | string | NO | Required when browser access is supported. |

### Body Fields

| name | type | required | description |
|---|---|---|---|
| `discovery.participantId` | string | YES | Unique participant identifier |
| `discovery.protocolVersion` | string | YES | Protocol version string |
| `discovery.capabilities[].name` | string | YES | Capability name (`merchant`, `orders`, `customer`, `logistics`) |
| `discovery.capabilities[].role` | string | YES | Participant role in that capability (`ORIGINATOR`, `RECEIVER`, `BOTH`) |
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
        "operations": ["receiveOrder", "acknowledgeOrderEvent"]
      }
    ],
    "compatibility": "backward-compatible"
  }
}
```

## Error Responses

| status | body | description |
|---|---|---|
| `400 Bad Request` | ODP error model | Malformed request |
| `404 Not Found` | ODP error model | Endpoint not found |
| `406 Not Acceptable` | ODP error model | Unsupported `Accept` header |
| `500 Internal Server Error` | ODP error model | Unexpected server failure |

Error payloads SHOULD follow [Error Model](../protocol/error-handling.md).

## Conformance Links

| concern | source |
|---|---|
| Protocol rules | [Discovery and Well-Known](../protocol/discovery.md) |
| HTTP transport details | [REST/HTTP Discovery Binding](../transport-bindings/rest-http-discovery.md) |
| OpenAPI contract | [discovery.openapi.yaml](v2/discovery.openapi.yaml) |
