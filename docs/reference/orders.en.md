---
template: redoc.html
openapi_spec: ../v2/orders.openapi.yaml
hide:
 - toc
 - navigation
---

!!! tip "Guide + contract"
    This page is the **API Spec** (endpoints, fields, errors, and examples) — enough to implement Orders.

    If you do not yet know the domain (**status vs events**, profiles, **two cancellation paths**, polling/webhook), read the [Orders guide](../protocol/orders.md) first.

    **Cancellation:** merchant → `requestCancellation` (handshake kept). Originator → mandatory `CANCELLED` only (no accept/deny).

    **Payload breaking change:** root `Order.type` was removed. Use `fulfillment.orderType` as the discriminator (`DELIVERY`, `TAKEOUT`, `INDOOR`).
    **Payload breaking change:** `delivery`, `takeout`, and `indoor` were also moved out of order root to `fulfillment.delivery`, `fulfillment.takeout`, and `fulfillment.indoor`.
    **Consumer breaking change:** treat `order.status` on `GET /orders/{orderId}` as source of truth. In V1, many flows inferred state only from event/`lastEvent`.

    **There is no `POST /orders`.** Orders enter via a `CREATED` event + `GET /orders/{orderId}`.

    **Indoor** is the only capability that **requires** Orders. Merchant, Logistics, and Customer can stand alone.

    **Contract language:** the API Spec is **always English**. The protocol guide is bilingual (PT/EN).
