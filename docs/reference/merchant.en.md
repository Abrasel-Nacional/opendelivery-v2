---
template: redoc.html
openapi_spec: ../v2/merchant.openapi.yaml
hide:
 - toc
 - navigation
---

!!! tip "Guide + contract"
    This page is the **API Spec** (endpoints, fields, errors, and examples) — enough to implement Merchant (store + catalog).

    If you do not yet know the domain (originator-owned `merchantId`, CRUD vs `merchantUpdate`, service-by-type, pause, snapshot), read first:

    - [Merchant overview](../protocol/merchant.md)
    - [Store data](../protocol/merchant-store.md)
    - [Menus](../protocol/menu.md)

    **Merchant does not require Orders.** It may be implemented alone.

    **Contract language:** the API Spec is **always English**. Protocol guides are bilingual (PT/EN).
