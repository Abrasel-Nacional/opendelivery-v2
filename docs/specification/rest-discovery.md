# REST Binding — Discovery

Normative source: [Specification — Discovery](./overview.md#discovery).

This page defines the REST/HTTP transport contract for the ODP Discovery endpoint.

## Endpoint

```
GET /.well-known/opendelivery
```

## Request

No request body. No authentication required.

### Headers

| Header | Required | Description |
|---|---|---|
| `Accept` | SHOULD | `application/json` |

## Response

### Success (200 OK)

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

### Response Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `participantId` | string | YES | Unique participant identifier |
| `protocolVersion` | string | YES | Protocol version string |
| `capabilities` | array | YES | List of supported capabilities |
| `capabilities[].name` | string | YES | Capability name |
| `capabilities[].role` | string | YES | `ORIGINATOR`, `RECEIVER`, or `BOTH` |
| `capabilities[].operations` | array[string] | YES | Supported operation identifiers |
| `capabilities[].extensions` | array[string] | NO | Active extension names |
| `capabilities[].endpoint` | string | NO | Base URL for this capability's REST endpoints |
| `compatibility` | string | NO | Compatibility statement |

## Requirements

- MUST be publicly accessible without authentication.
- MUST use HTTPS.
- MUST NOT redirect (3xx).
- MUST return `Content-Type: application/json`.
- SHOULD return `Cache-Control: public, max-age=60` or higher.
- MUST include CORS headers when accessed from browser contexts.
