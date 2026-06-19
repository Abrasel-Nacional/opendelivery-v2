# OpenAPI Artifacts

OpenAPI artifacts are implementation-facing contracts for REST APIs.
They are intended for Swagger UI visualization, client/server code generation, and automated validation.

OpenAPI does not replace protocol Specification.
Protocol pages remain the normative source of behavior and conformance obligations.

## Layering

1. Protocol Specification (`docs/protocol/**`): normative behavior (`MUST`, `SHOULD`, `MAY`).
2. REST/HTTP Binding (`docs/transport-bindings/**`): HTTP mapping of protocol rules.
3. OpenAPI (`docs/reference/**`): machine-readable API contract.

## v2 Artifacts

- Discovery endpoint: [rest-http-discovery.openapi.yaml](v2/rest-http-discovery.openapi.yaml)

## Authoring Rules

- Keep endpoint behavior aligned with protocol rules.
- Avoid duplicating protocol semantics in OpenAPI descriptions.
- Use references to protocol pages for semantic meaning.
- Prefer one OpenAPI file per bounded surface (for example: discovery, merchant, orders, logistics), then optionally aggregate later.
