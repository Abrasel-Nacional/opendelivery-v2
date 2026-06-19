# Core Concepts

The Open Delivery Protocol (ODP) is an open standard designed to improve communication and
interoperability across food and retail delivery ecosystems.

Different systems usually run disconnected models, payloads, and operational rules. ODP provides a
shared language so these systems can coordinate merchant data, order lifecycles, customer
relationships, and delivery tracking without custom one-off integrations for each partner.

This page explains ODP at a conceptual level. Normative behavior is described in the
[Specification](../specification/overview.md).

## High-Level Architecture

ODP is a coordination protocol between independent participants.

There is no central host required by the protocol. Each participant runs its own infrastructure and
exchanges protocol information through agreed transport bindings.

At a high level, the protocol coordinates four streams of information:

- **Merchant context** — identity, operational services, catalog
- **Order context** — events, states, cancellation outcomes
- **Customer context** — CRM, loyalty-related facts, customer-centric analytics
- **Delivery context** — quote, dispatch, tracking, problem handling

## Roles and Participants

ODP defines four primary participant roles:

- **Ordering Application** — Consumer-facing surface where users browse menus and place orders. Consumes merchant information and coordinates order interactions.
- **Software Service** — Merchant-side system that publishes merchant data and processes order lifecycle updates.
- **Logistics Service** — Delivery platform that receives delivery requests, returns quotes, and sends tracking/problem updates.
- **CRM Software Service** — CRM, marketing automation, loyalty, and couponing backends.

A single company can fulfill multiple roles depending on the integration context.

## Capabilities

Capabilities are the primary functional areas of the protocol. They represent the main coordination
problems ODP solves.

| Capability | Description |
|---|---|
| **Merchant** | Merchant identity, catalog, services, and operational context |
| **Orders** | Order lifecycle, state management, and coordination |
| **Indoor** | On-premise order operations — table service, counter, tab |
| **Customer** | CRM, leads, customer events, and customer-linked order views |
| **Loyalty** | Loyalty identity, accrual, redemption, and coupon validation |
| **Logistics** | Delivery coordination, tracking, and problem handling |

## Extensions

Extensions are optional protocol modules that augment a base capability without redefining it.
An extension is always declared alongside its parent capability and MUST NOT be used independently.

| Extension | Parent Capability | Description |
|---|---|---|
| **Indoor** | Orders | On-premise account aggregation, incremental ordering, partial payments |
| **Loyalty** | Customer | Loyalty account, accrual, redemption, and coupon/voucher validation |

## Transport Bindings

Transport bindings define the communication layer used to exchange ODP messages between
participants. ODP currently specifies one transport binding:

- **REST/HTTP** — RESTful HTTP endpoints with JSON payloads

Transport bindings are defined separately from capability semantics. The same capability
semantics apply regardless of transport.

## Discovery

Before any capability operation, participants MUST publish a machine-readable discovery document
at a well-known endpoint:

```
GET /.well-known/opendelivery
```

This document declares the participant's identity, supported capabilities, and the transport
endpoints available for each capability.

See [Specification — Discovery](../specification/overview.md#discovery) for normative rules.
