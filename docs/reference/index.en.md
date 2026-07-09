---
title: API reference
---

# API reference

This section contains the normative **OpenAPI** specifications for each Open Delivery V2 capability.
Each page renders the full REST contract with **ReDoc** — endpoints, schemas, request/response examples, and error codes.

!!! note "Contract language"
    OpenAPI specs are **English only**. Conceptual rules and flows are in the **Protocol** section (available in PT and EN).

For conceptual explanations, flows, and implementation guidance, see **Protocol**.

<div class="od-api-callout">
  <p>New to the hybrid model? Read Protocol vs binding first.</p>
  <a href="../PROTOCOL_VS_BINDING/">Understand protocol vs API →</a>
</div>

## Infrastructure

Start here for every new integration.

| Spec | Description | Protocol |
|---|---|---|
| [Discovery](discovery.md) | Well-known endpoint and capability declaration | [Rules](../protocol/discovery.md) |
| [Authentication](authentication.md) | OAuth 2.0, token, webhook signing | [Rules](../protocol/authentication.md) |

## Capabilities

| Spec | Description | Protocol |
|---|---|---|
| [Merchant](merchant.md) | Establishment, catalog, services, availability | [Overview](../protocol/merchant.md) · [Store data](../protocol/merchant-store.md) · [Menus](../protocol/menu.md) |
| [Orders](orders.md) | Order lifecycle, states, and events | [Rules](../protocol/orders.md) |
| [Logistics](logistics.md) | Delivery coordination, tracking, problems | [Rules](../protocol/logistics.md) |
| [Customer & Loyalty](customer.md) | CRM, leads, reviews, loyalty, events | [Customer](../protocol/customer.md) · [Reviews](../extensions/reviews.md) · [Loyalty](../extensions/loyalty.md) |
| [Indoor](indoor.md) | Dine-in accounts, orders, payments, fiscal | [Rules](../protocol/indoor.md) |
