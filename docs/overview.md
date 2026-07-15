# Protocol Overview

This section provides a high‑level overview of the Open Delivery Protocol v2, describing its actors, responsibilities, interaction model, and capability architecture.

The goal of this overview is to establish a shared mental model for implementers before introducing capability-specific specifications.

---

## High‑Level Concept

Open Delivery defines a **protocol for interoperability**, enabling independent systems to exchange information about food service transactions without requiring tight coupling or shared infrastructure.

The protocol focuses on **coordination between systems**, not on internal workflows or user interfaces.

Each participant remains autonomous, implementing the protocol according to its own architecture and business rules.

---

## Actors

The Open Delivery ecosystem involves multiple independent actors. The protocol does not impose a hierarchy among them.

### Originator

The **Originator** is the system that creates an order.

Examples include:
- Consumer‑facing applications
- Marketplaces
- Ordering platforms
- Kiosks or self‑service systems

The Originator is responsible for:
- Creating the order
- Providing all required order data
- Receiving updates about the order lifecycle

---

### Merchant System

The **Merchant System** is the system operated by or on behalf of the restaurant or store responsible for fulfilling the order.

Examples include:
- Point of Sale (POS) systems
- Order management systems
- Kitchen management systems

The Merchant System is responsible for:
- Accepting or rejecting orders
- Managing preparation and fulfillment
- Emitting relevant order events

---

### Logistics Provider (Optional)

A **Logistics Provider** is an optional participant responsible for delivery execution.

Examples include:
- Third‑party delivery services
- Fleet management systems
- Courier platforms

The Logistics Provider may:
- Receive delivery‑related information
- Emit delivery status events
- Operate independently from both Originator and Merchant

---

## Interaction Model

Open Delivery follows a **point‑to‑point interaction model**.

- Systems communicate directly
- No central broker is required
- No shared state is enforced

Each interaction is governed by:
- The protocol specification
- The order profile
- The declared support of each participant

---

## Orders as the Central Entity

The **Order** is the central entity in the protocol.

An order:
- Is created by an Originator
- Is fulfilled by a Merchant
- May involve a Logistics Provider
- Has a defined lifecycle

The protocol defines:
- Order structure
- Allowed states
- Events that represent observable facts

The protocol does **not** define:
- Internal processing steps
- Timing guarantees beyond event semantics
- Business rules such as pricing or commissions

---

## Order Profiles

Open Delivery introduces the concept of **Order Profiles** to represent different operational contexts.

Examples include:
- `DELIVERY`
- `PICKUP`
- `ON_PREMISE`

An order profile:
- Defines the expected interaction pattern
- Determines which events are required, optional, or not applicable
- Allows the protocol to remain generic while supporting diverse business models

---

## Events and States

Open Delivery distinguishes clearly between **events** and **states**.

### States

A state represents the current condition of an order.

States:
- Are descriptive
- May change over time
- Represent the latest known status

---

### Events

An event represents a **fact that occurred**.

Events:
- Are immutable
- Occur at a specific point in time
- Communicate information between systems

The protocol defines a limited set of events to ensure interoperability while allowing implementations to remain flexible.

---

## Event Obligations

Not all events are mandatory in all contexts.

The protocol defines:
- **Normative events** that MUST be emitted in all relevant profiles
- **Conditional events** that MUST be emitted only in specific profiles
- **Optional events** that MAY be emitted to provide additional context

Consumers MUST NOT rely on optional events for protocol correctness and MUST treat the order state as the source of truth.

---

## Implementation contract (API Spec)

Open Delivery V2 is implemented through the published **API Specs** (REST/HTTP + JSON) under [API reference](reference/index.md).

There is no separate “transport binding” layer and no parallel official bindings. Domain explanation lives under **Protocol**; implementable obligations live in **API Spec**.

Shared HTTP conventions: [General rules](reference/conventions.md) · [Error handling](reference/error-handling.md).

---

## Security and Authorization Model (Protocol Perspective)

The protocol assumes authentication at the **software** level rather than per-merchant credentials.

Core security directives:

- Authentication is associated with the integrating software/system.
- Access is scoped by functional service area (e.g., orders, menus, logistics).
- Request / webhook signing is used as an integrity mechanism where declared.
- Authorization between software and merchant is explicit; onboarding details may be bilateral, while Discovery declares supported models.

Normative auth operations and headers are defined in the [Authentication API Spec](reference/authentication.md).

---

## Governance and Documentation

Open Delivery v2 is governed through transparent, ongoing review.

- GitHub is the canonical source for issues, decisions, and change tracking.
- The specification is under continuous weekly review by the technical committees.
- Documentation presentation tooling is an implementation detail and may change without affecting the protocol.

---

## Version Lifecycle and Migration Model

Open Delivery v2 is expected to become the official Open Delivery documentation from a defined effective date.

The transition model is:

- v2 becomes the canonical specification for new evolution
- v1 remains active for a transition period as a legacy specification
- both versions may be maintained in parallel for a limited time
- v1 is deprecated after the transition period ends

From a specification perspective, v2 starts from the functional baseline established by v1.

The main change is not a wholesale behavioral reset, but a reorganization of the standard into:

- clear documentation layers: Guide · Protocol · API Spec
- protocol capabilities and extensions instead of a monolithic API surface
- explicit state and event semantics
- a single implementable contract: API Spec (REST/HTTP)

Migration documentation should therefore focus on differences, additions, and changed obligations, rather than reproducing the full legacy reference inside the v2 specification.

---

## Work In Progress

The following items are actively being refined:

- Final event model for orders (separating status vs. logistics facts)
- Discovery contract and well-known endpoint for partner onboarding
- Documentation tooling selection

---

## Extensibility

The protocol is designed to evolve over time.

Extensibility is achieved through:
- Explicit versioning
- Service separation
- Order profiles
- Capability declarations

This approach allows new features to be introduced without breaking existing integrations.

---

## Summary

At a high level, Open Delivery v2:

- Defines how systems coordinate around orders
- Preserves autonomy of participants
- Avoids centralized control
- Supports multiple business models
- Prioritizes clarity and long‑term stability

Subsequent sections expand this overview: Protocol pages for domain narrative, and API Spec for the implementable contract.

<div class="od-related">
  <p class="od-related__label">Related</p>
  <ul class="od-related__list">
    <li><a href="guide/getting-started.md">Getting started</a> — minimum integration path</li>
    <li><a href="protocol/principles.md">Design principles</a> — how the domain is organized</li>
    <li><a href="documentation/core-concepts.md">Core concepts</a> — capabilities and extensions</li>
    <li><a href="reference/index.md">API reference</a> — implementable contracts</li>
  </ul>
</div>