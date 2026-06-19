# General Rules

This section defines cross-capability protocol rules.

## Normative Keywords

The words `MUST`, `MUST NOT`, `SHOULD`, and `MAY` are normative.

## Interoperability Rules

1. Producers MUST include all required fields.
2. Consumers MUST validate required fields.
3. Consumers SHOULD tolerate unknown additive fields.
4. Participants MUST NOT infer unsupported state transitions.
5. Participants MUST process events idempotently.

## Payload Documentation Standard

Each protocol payload description MUST include:

1. Field table with `name`, `required`, and `description`.
2. Payload example.

Examples are illustrative protocol shapes, not transport contracts.

## Operation Documentation Standard

Each documented operation MUST declare:

1. Whether authentication is required.
2. Which scope or permission is required when authentication applies.
3. A reference to the Authentication and Authorization section.

This allows implementers to understand access requirements directly from the operation definition, without guessing from transport examples.

## Security Rules

- Authentication context MUST be merchant-scoped.
- Secrets MUST NOT be exposed in logs or traces.
- Callback trust validation MUST be enforced for asynchronous delivery.

## Compatibility Rules

- Existing required fields MUST NOT be removed in backward-compatible updates.
- Enum extensions SHOULD be additive.
- Breaking behavior changes MUST be version-signaled.
