---
template: redoc.html
openapi_spec: ../v2/customer.openapi.yaml
hide:
 - toc
 - navigation
---

!!! tip "Guide + contract"
    This page is the **API Spec** (endpoints, fields, errors, and examples) — enough to implement Customer (customer data, reviews, and loyalty).

    If you are new to the domain (capability `customer`, Software CRM, modules vs extensions, relationship-context orders), read first:

    - [Customer — overview](../protocol/customer.md)
    - [Reviews](../protocol/reviews.md)
    - [Loyalty](../protocol/loyalty.md)

    **Capability name:** always **Customer** (`customer`). There is no “CRM” capability. CRM software is the product class that uses Customer.

    **Reviews and Loyalty** are modules of the same capability — **not** extensions. Parties MAY implement reviews only or loyalty only.

    **Customer does not require Orders** for core data and reviews. Relationship-context orders use the **same shape** as [Orders](orders.md).

    **Contract language:** the API Spec is **always English**. Protocol guides are bilingual (PT/EN).
