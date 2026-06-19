# Core Concepts

The Open Delivery Protocol (ODP) is an open standard created to improve communication and interoperability across food and retail delivery ecosystems.

In practice, different systems usually run disconnected models, payloads, and operational rules. ODP provides a shared language so these systems can coordinate merchant data, order lifecycles, and delivery tracking without custom one-off integrations for each partner.

This page explains ODP at a conceptual level. Detailed normative behavior is described in each capability page.

## High-Level Architecture

ODP is a coordination protocol between independent participants.

There is no central host required by the protocol. Each participant runs its own infrastructure and exchanges protocol information through agreed transport bindings.

At a high level, the protocol coordinates three streams of information:

- Merchant context (identity, services, catalog)
- Order context (events, statuses, cancellation outcomes)
- Customer context (CRM, loyalty-related facts, customer-centric analytics)
- Delivery context (quote, dispatch, tracking, problem handling)

## Key Goals

- **Interoperability**: enable platforms and systems to integrate using a common model.
- **Operational clarity**: keep merchant, order, and delivery coordination understandable and predictable.
- **Discovery-driven integration**: allow participants to expose what they support before operations begin.
- **Asynchronous resilience**: support both polling and push flows in real-world delivery operations.
- **Extensibility**: evolve capabilities independently without redesigning the whole protocol.

## Roles and Participants

ODP defines three primary roles:

- **Ordering Application**
	Consumer-facing surface where users browse menus and place orders.
	It consumes merchant information and coordinates order interactions.

- **Software Service**
	Merchant-side system that publishes merchant data and processes order lifecycle updates.

- **Logistics Service**
	Delivery platform that receives delivery requests, returns quote/availability, and sends tracking/problem updates.

A single company can play multiple roles depending on the integration context.

## Core Concepts Summary

ODP revolves around three fundamental constructs that define how participants interact.

### Capabilities

Capabilities are the primary functional areas of the protocol. They represent the main coordination problems ODP solves.

Current core capabilities are:

- `Merchant Capability`
- `Orders Capability`
- `Customer Capability`
- `Logistics Capability`

Each capability includes its own concepts, data structures, operations, and interaction expectations.

### Extensions

Extensions are optional protocol modules that refine or augment a base capability without redefining it completely.

They are useful when a coordination need is real, but not universal across every implementation.

Examples of future ODP extensions might include profile-specific variations, vertical-specific rules, or optional operational flows built on top of a core capability.

### Transport Bindings

Transport bindings are the lower-level communication layers used to exchange ODP information between participants.

To avoid confusion with the `service` entity inside the Merchant capability, ODP uses the term `transport binding` instead of `service` for this concept.

ODP is transport-agnostic at the protocol level, but practical interoperability depends on shared bindings.

For now, ODP documentation is focused on:

- `REST/HTTP`

## Discovery

Before any capability interaction starts, participants MUST discover each other through a mandatory REST well-known endpoint.
This endpoint exposes supported capabilities, operations, roles, and protocol version. Full details are specified in the **Discovery and Well-Known** section of Specification.

## Authentication

Most operations are protected by authentication and access control based on merchant scope.
The shared authentication model, token flow, and authorization rules are normatively defined in the **Authentication and Authorization** section of Specification.

## Operations and Interaction Responsibilities

Capabilities are not only data groupings. They also define what can happen between participants.

Examples of operation groups:

- **Merchant**: publish merchant context, notify updates, synchronize structure changes.
- **Orders**: receive new order events, update order lifecycle, resolve cancellations.
- **Customer**: ingest customer/lead records, exchange customer events, synchronize customer-linked order view for CRM.
- **Logistics**: quote delivery, request dispatch, send tracking and delivery outcomes.

Each declared operation is associated with a participant role in the interaction:

- `ORIGINATOR`: who starts the operation
- `RECEIVER`: who receives/processes it
- `BOTH`: when a participant can act in both directions

Operations are also expected to declare their access model, including whether authentication is required and which scope is used when the operation is protected.

## Interaction Patterns

ODP supports both pull and push communication styles.

- **Pull**: periodic retrieval of new events (for example, polling)
- **Push**: direct event notifications (for example, webhooks)

Real integrations often use both, depending on reliability, latency, and operational policy.

## States and Events

Two concepts are central across capabilities:

- **State**: the current condition of an entity (order, delivery, merchant availability context)
- **Event**: a fact that happened and is exchanged between participants

This distinction helps keep lifecycle coordination consistent, especially in asynchronous flows.

## Transport and Binding Boundary

Core protocol documentation defines meaning and behavior.

Binding documentation defines transport details such as URLs, headers, status codes, and retry mechanics.

This separation allows ODP to stay transport-agnostic while still supporting practical implementations through shared bindings.

## Practical Reading Guide

When reading ODP documentation, start here, then proceed to Specification:

1. **Core Concepts** (this page): Understand roles, architecture, and design rationale.
2. **Specification**:
   - **General Rules**: Common normative requirements across the protocol.
   - **Discovery and Well-Known**: Mandatory REST entry point and participant capability exposition.
   - **Authentication and Authorization**: Merchant-scoped credentials and access control model.
3. **Capability Pages**: Understand specific capability models (Merchant, Orders, Customer, Logistics).
4. **Transport Binding** (when available): Map protocol operations to REST endpoints, headers, status codes.

