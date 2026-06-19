# Discovery and Well-Known

This section defines how participants publish discoverable protocol support before productive coordination.

In The Open Delivery Protocol (ODP), Discovery is a mandatory protocol mechanism, not a capability.
It allows one participant to understand another participant before any capability operation.
Discovery always uses a REST endpoint, even when capability operations use other transport bindings.

## What Discovery Is For

Discovery allows participants to determine:

- Whether a participant supports a given capability
- Which operations are available inside that capability
- Which side originates or receives each operation
- Which protocol version/profile is supported

## Well-Known Endpoint

ODP uses a REST well-known endpoint for discovery in the same general spirit seen in standards such as OAuth, OpenAPI-related ecosystem conventions, and UCP.

The reason is practical: discovery must be simple, predictable, and retrievable before any participant-specific transport assumptions are made.

This means the protocol has two layers:

- A mandatory REST well-known endpoint for discovery
- One or more transport bindings for capability operations

Before any productive capability coordination, a participant MUST publish a machine-readable discovery document in this endpoint.

**Required URL suffix:**

```
/.well-known/opendelivery
```

Every discovery URL MUST end with this suffix.

Using the domain root is recommended for consistency, but not mandatory.

A participant MAY expose discovery at any HTTPS-accessible host or path prefix, as long as the URL keeps the mandatory suffix.

- The exact URL **MUST** be communicated to the other participant through out-of-band channels (e.g., configuration, registration, or manual setup) before any capability operation begins.
- The endpoint **MUST** be publicly accessible without authenticated requests.
- The endpoint **MUST** use HTTPS (SSL/TLS).
- The endpoint response **MUST** include proper CORS headers if accessed from browser contexts.

Accepted examples:

- `https://dominio.com/.well-known/opendelivery` (recommended)
- `https://api.dominio.com/.well-known/opendelivery`
- `https://dominio.com/api/.well-known/opendelivery`

Transport-specific implementation details are defined in [REST/HTTP Discovery Binding](../transport-bindings/rest-http-discovery.md).

## Discovery Fields

A valid discovery payload MUST include all fields marked as `YES` and MUST NOT declare operations or behaviors the participant cannot execute.
When `discovery.compatibility` is provided, it SHOULD include backward-compatibility guidance.

| name | type | required | description |
|---|---|---|---|
| `discovery.participantId` | string | YES | Unique participant identifier |
| `discovery.protocolVersion` | string | YES | Protocol version string |
| `discovery.capabilities[].name` | string | YES | Capability name (`orders`, `merchant`, `customer`, `logistics`) |
| `discovery.capabilities[].operations[]` | array[string] | YES | Supported operation identifiers in that capability |
| `discovery.capabilities[].role` | string | YES | Participant role in operations (`ORIGINATOR`, `RECEIVER`, `BOTH`) |
| `discovery.capabilities[].profiles[]` | array[string] | NO | Supported profiles/variants for that capability |
| `discovery.compatibility` | string | NO | Compatibility statement |
| `discovery.notes` | string | NO | Informative notes |

## Discovery Example

```json
{
  "discovery": {
    "participantId": "software-service-123",
    "protocolVersion": "v1.7.0",
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
        "name": "customer",
        "role": "BOTH",
        "operations": ["ingestCustomer", "getCustomers", "receiveCustomerEvent"]
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

## Normative Statements

- Participant MUST publish a machine-readable discovery document before productive capability coordination.
- Discovery endpoint MUST be public — no authentication required.
- Discovery endpoint MUST use HTTPS (SSL/TLS).
- Discovery endpoint URL MUST end with `/.well-known/opendelivery`.
- Participant MUST communicate the full discovery URL to partners before capability operations.
- Discovery payload MUST include all required fields and MUST NOT declare unsupported behaviors.
- If `discovery.compatibility` is present, it SHOULD include backward-compatibility guidance.

!!! tip "Implementation Checklist"
    - Publish a machine-readable discovery document before productive coordination.
    - Use a public HTTPS endpoint for discovery.
    - Ensure the discovery URL ends with `/.well-known/opendelivery`.
    - Communicate the full discovery URL to partners before any capability operation.
    - Declare supported capabilities, operations, and participant role per operation.
    - Do not declare behaviors that are not actually supported.
    - If provided, include backward-compatibility guidance in `discovery.compatibility`.

    Conformance requirements are defined in `Well-Known Endpoint` and `Discovery Fields`.
    For REST/HTTP mapping and OpenAPI artifact, see `transport-bindings/rest-http-discovery.md` and `reference/v2/rest-http-discovery.openapi.yaml`.
