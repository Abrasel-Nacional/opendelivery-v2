---
template: redoc.html
openapi_spec: ../v2/indoor.openapi.yaml
hide:
 - toc
 - navigation
---

!!! tip "Guide + contract"
    This page is the **API Spec** (endpoints, fields, errors, and examples) — enough to implement Indoor.

    If you are new to the domain (**account vs order**, pre-close, partial payments, channels, and roles), read the [Indoor guide](../protocol/indoor.md) first.

    **Prerequisite:** [Orders](orders.md) (`fulfillment.orderType: INDOOR`, entry via `CREATED` event — no `POST /orders`). Indoor is an extension of Orders, not a standalone capability.

    **Account:** it is created when the Software Service processes an INDOOR order coming from Orders; later orders on the same operational key accumulate items on the same account.

    **Indoor events:** they are **webhook-only**. This capability does not define polling for `ACCOUNT_*`, `PAYMENT_*`, or `FISCAL_*`.

    **Duplicate lifecycle calls:** if the account mutation was already applied (for example `pre-close` while already `IN_PAYMENT`, or `close` while already `CLOSED`), the host returns **`202`** — not `409` merely because it was repeated.

    **Contract language:** the API Spec is **always English**. Protocol guides are bilingual (PT/EN).
