---
title: API reference
---

# API reference

!!! warning "Release Candidate (V2.0.0-rc)"
    The API Specs below are **V2.0.0-rc**. They are published for **ecosystem validation** (company review and implementation pilots). They may still change based on feedback. A stable release will be published only after that phase; **V1 remains active** during the transition.

    Status and lifecycle: [Protocol evolution](../protocol/evolution.md) · [Changelog](../guide/changelog.md).

This section is the **normative implementation source** for Open Delivery V2: the **API Specs** (REST/HTTP) — endpoints, schemas, examples, and errors.

!!! note "Specification format"
    All API Specs are written in **[OpenAPI](https://www.openapis.org/)** (YAML). The site presents them in a readable form; the OpenAPI file is the canonical artifact for each capability.

!!! note "Contract language"
    API Specs are **English only**. Domain concepts and flows are in the **Protocol** tab (PT and EN).

The **Protocol** tab explains the domain; this tab defines the **implementable contract**. On conflict, the **API Spec wins**.

## Conventions

| Page | Description |
|---|---|
| [General rules](conventions.md) | Interoperability, timestamps, pagination, duplicate lifecycle ops |
| [Error handling](error-handling.md) | Error envelope and HTTP status codes |

## Infrastructure

Start here for every new integration.

| Spec | Description | Protocol |
|---|---|---|
| [Discovery](discovery.md) | Well-known endpoint and capability declaration | [Rules](../protocol/discovery.md) |
| [Authentication](authentication.md) | OAuth 2.0, token, webhook signing | [Rules](../protocol/authentication.md) |

## Capabilities

| Spec | Description | Protocol |
|---|---|---|
| [Orders](orders.md) | Lifecycle, status vs events, polling and webhooks | [Rules](../protocol/orders.md) |
| [Indoor](indoor.md) | Dine-in accounts (Orders extension), payments, fiscal | [Rules](../protocol/indoor.md) |
| [Merchant](merchant.md) | Establishment, catalog, services, availability | [Overview](../protocol/merchant.md) · [Store data](../protocol/merchant-store.md) · [Menus](../protocol/menu.md) |
| [Logistics](logistics.md) | Delivery coordination, tracking, problems | [Rules](../protocol/logistics.md) |
| [Customer](customer.md) | Customer data, leads, reviews, loyalty, events | [Customer](../protocol/customer.md) · [Reviews](../protocol/reviews.md) · [Loyalty](../protocol/loyalty.md) |
