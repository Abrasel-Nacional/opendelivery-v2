# Roles and Responsibilities

## Cross-Capability Interaction Roles

To standardize capability documentation, every operation uses these cross-cutting roles:

- `Provider`: participant that exposes the operation interface (endpoint, tool, or event channel).
- `Consumer`: participant that invokes, subscribes to, or otherwise consumes that interface.

Normative guidance:

- Every operation MUST declare a Provider and a Consumer.
- A participant MAY act as Provider in one operation and Consumer in another.
- Provider/Consumer classification is operation-specific and MUST NOT be treated as a global system identity.

## Ordering Application

Responsibilities:

- Consume merchant context.
- Create and track order coordination.
- Consume order and delivery events.
- Trigger lifecycle actions when applicable.

## Software Service

Responsibilities:

- Publish merchant context.
- Receive and process order coordination.
- Emit order progression facts.
- Coordinate with logistics participants when needed.

## Logistics Service

Responsibilities:

- Accept or deny delivery coordination.
- Emit delivery progress and delivery problem facts.
- Provide delivery status and availability context.

## Hub/Intermediary Model

A hub MAY act as Ordering Application in one integration side and as Software Service in another side.

Implementations MUST preserve role-specific behavior for each role they assume.
