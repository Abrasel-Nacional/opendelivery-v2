# REST/HTTP Binding

This section defines how ODP protocol concepts are implemented over REST/HTTP.

Normative source for protocol behavior remains in Specification pages.
If any statement in this binding conflicts with protocol Specification, protocol Specification prevails.

## Scope

This binding specifies HTTP-level concerns only:

- HTTP methods
- URL patterns
- Headers and content types
- HTTP status codes
- Security transport requirements (HTTPS/TLS)
- OpenAPI artifact conventions

This binding does not redefine capability semantics, states, events, or role obligations.

## Rule Separation Model

Use this model to avoid duplication while keeping implementation clear:

1. Protocol Specification defines WHAT is required (`MUST`, `SHOULD`, `MAY`).
2. REST/HTTP Binding defines HOW to express those requirements over HTTP.
3. OpenAPI defines executable API contracts for implementers and tooling (Swagger UI, codegen, validation).

## Binding Pages

- Discovery endpoint binding: [REST/HTTP Discovery Binding](rest-http-discovery.md)

## OpenAPI Artifacts

- OpenAPI guidance and files: [OpenAPI Artifacts](../reference/openapi.md)

## Conformance Mapping Pattern

Each REST endpoint page should include a conformance mapping table:

| protocol rule ref | REST/HTTP implementation |
|---|---|
| `DISC-004` | URL MUST end with `/.well-known/opendelivery` |

This keeps protocol rules centralized while making REST implementation explicit.
