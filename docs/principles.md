# Design Principles

This section defines the foundational principles that guide the design, governance, and evolution of the Open Delivery Protocol v2.

These principles are **normative**.  
All specifications, protocol capabilities, and extensions MUST align with them.

---

## Protocol‑First

Open Delivery is designed as a **protocol**, not as an API, platform, or product.

The specification defines:
- Shared concepts
- Observable facts
- Clear responsibilities between independent systems

The protocol does NOT:
- Dictate internal workflows
- Prescribe implementation details
- Require specific technologies or vendors

Transport mechanisms, APIs, messaging patterns, and tooling are **implementation choices**, not part of the protocol itself.

---

## Decentralization and Autonomy

Open Delivery assumes a **decentralized ecosystem**.

- There is no central runtime
- There is no shared database
- There is no mandatory intermediary

Each participant:
- Remains autonomous
- Owns its internal state
- Applies its own business rules

The protocol exists to **coordinate systems**, not to control them.

---

## Clear Separation of Concerns

The protocol enforces a strict separation between:

- **Protocol rules** — what systems must agree on
- **Implementation logic** — how systems behave internally
- **Ecosystem services** — tooling and support for adoption

This separation ensures:
- Long‑term stability
- Multiple integration styles
- Freedom of architectural choice

---

## Orders as the Source of Coordination

The **Order** is the primary coordination entity in Open Delivery.

The protocol defines:
- The structure of an order
- Its possible states
- Events that represent meaningful facts

The protocol does NOT define:
- User interfaces
- Internal fulfillment steps
- Operational optimizations

Orders exist to synchronize systems, not to expose internal processes.

---

## Explicit Context via Order Profiles

Open Delivery introduces **Order Profiles** to represent different operational contexts.

An order profile:
- Expresses the nature of the transaction
- Defines expectations for interaction
- Determines event obligations

Examples include:
- `DELIVERY`
- `PICKUP`
- `ON_PREMISE`

Order profiles allow the protocol to remain generic while supporting diverse business models without fragmentation.

---

## Events Represent Facts, Not Workflow Steps

Events represent **facts that occurred**, not steps in a workflow.

An event:
- Is immutable
- Occurs at a specific point in time
- Communicates information to other systems

Events MUST NOT:
- Encode internal process steps
- Mirror internal state machines
- Implicitly describe how work is done

Only events relevant for **inter‑system coordination** are defined by the protocol.

---

## States Represent Current Condition

States represent the **current condition** of an order.

- States may change over time
- States describe what is known now
- States are descriptive, not prescriptive

Consumers MUST treat the order state as the **source of truth**, not the presence or absence of optional events.

---

## Normative, Conditional, and Optional Events

The protocol distinguishes between:

- **Normative events** — MUST be emitted in all relevant contexts
- **Conditional events** — MUST be emitted only in specific profiles
- **Optional events** — MAY be emitted to provide additional context

Optional events:
- Are never required for protocol correctness
- Must not be relied upon by consumers
- Exist to enrich integrations, not to guarantee behavior

---

## Profile‑Scoped Obligations

Event obligations are **scoped by order profile**, not global.

An event may be:
- Mandatory in one profile
- Optional in another
- Not applicable in a third

This avoids over‑specification and preserves protocol flexibility.

---

## Declared Support over Per‑Order Flags

Protocol behavior MUST NOT be controlled through per‑order dynamic flags.

Instead:
- Systems declare supported capabilities, profiles, and extensions explicitly
- Declared support remains stable across orders
- Orders contain only business data and context

This ensures predictable behavior and clean separation between business data and protocol support declarations.

---

## Tolerance and Resilience

Open Delivery assumes distributed systems with partial failures.

Implementations MUST:
- Tolerate missing optional events
- Handle duplicate events
- Accept out‑of‑order delivery
- Avoid reliance on timing guarantees

The protocol favors **eventual consistency** over strict synchronization.

---

## Transport and Technology Neutrality

The protocol is independent of:
- Transport protocols
- Serialization formats
- Authentication mechanisms
- Deployment models

Transport bindings MAY be defined separately without altering the protocol.

---

## Governance and Stewardship

Open Delivery is governed through a formal governance model.

Governance exists to:
- Ensure transparency and isonomy
- Preserve protocol neutrality
- Coordinate its evolution over time

Governance does NOT:
- Restrict adoption
- Impose commercial conditions
- Grant exclusive rights to any participant

---

## Institutional Coordination

The Open Delivery initiative is institutionally coordinated by Abrasel.

This coordination includes:
- Management of official repositories
- Publication of specifications
- Communication and outreach activities

Institutional coordination does NOT:
- Alter the open nature of the protocol
- Restrict access to the specification
- Impose mandatory participation or registration

---

## Principle of Minimalism

The protocol defines the **minimum necessary surface** to enable interoperability.

Anything that:
- Is purely internal
- Is implementation‑specific
- Is not required for coordination

SHOULD remain outside the protocol.

---

## Summary

These principles ensure that Open Delivery v2 remains:
- Stable
- Neutral
- Extensible
- Suitable for long‑term ecosystem growth

All future sections of this specification MUST conform to these principles.