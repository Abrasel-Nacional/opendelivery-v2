# REST API Binding

This section defines how The Open Delivery Protocol (ODP) is implemented over REST/HTTP.

The protocol itself is transport-agnostic: it defines roles, capabilities, operations, and behavioral obligations without assuming a specific communication mechanism. A binding translates those protocol concepts into concrete transport details.

At this stage, ODP supports one binding:

- **REST/HTTP** — the primary and only currently supported binding

Other bindings such as MCP (Model Context Protocol) may be introduced in future versions of the protocol. When a new binding is added, it will appear as a new section here and will follow the same documentation pattern as REST/HTTP.

## What a Binding Defines

A binding does not redefine protocol semantics. It defines only:

- HTTP methods and URL patterns
- Request and response headers
- Payload structure and content types
- HTTP status codes
- Transport security requirements (HTTPS/TLS)
- Download link for the corresponding OpenAPI artifact

If any binding statement conflicts with the protocol Specification, the Specification prevails.

## Layering Model

| layer | source | defines |
|---|---|---|
| Protocol Specification | `docs/protocol/**` | Normative rules (`MUST`, `SHOULD`, `MAY`), roles, capabilities, fields, behavior |
| REST/HTTP Binding | this section | HTTP methods, paths, headers, status codes, transport security |
| OpenAPI Artifact | `docs/reference/v2/**` | Machine-readable contract for code generation, validation, and tooling |

## Documentation Pattern

Every binding endpoint page in this section follows this structure:

1. Endpoint contract (method, path, auth, transport security, content type)
2. Request (headers, path/query parameters if any, body fields and example)
3. Successful response (status, headers, body fields and example)
4. Error responses (status codes, when each applies)
5. Protocol rule references (DISC-*, AUTH-*, etc.) with links to Specification
6. OpenAPI artifact download link

## REST/HTTP Binding Pages

- [Discovery Endpoint](transport-bindings/rest-http-discovery.md)
- [Orders Endpoints](transport-bindings/rest-http-orders.md)
- [Indoor Endpoints (Orders Extension)](transport-bindings/rest-http-indoor.md)
- [Customer Endpoints](transport-bindings/rest-http-customer.md)
