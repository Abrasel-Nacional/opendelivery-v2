---
template: redoc.html
openapi_spec: ../v2/customer.openapi.yaml
hide:
 - toc
 - navigation
---

!!! tip "Guia + contrato"
    Esta página é a **especificação da API** (endpoints, campos, erros e exemplos) — o suficiente para implementar Customer (dados do cliente, reviews e loyalty).

    Se você ainda não conhece o domínio (capability `customer`, Software CRM, módulos vs extensões, pedidos no contexto de relacionamento), leia antes:

    - [Customer — visão geral](../protocol/customer.md)
    - [Reviews](../protocol/reviews.md)
    - [Loyalty](../protocol/loyalty.md)

    **Nome da capability:** sempre **Customer** (`customer`). Não existe capability “CRM”. Software CRM é o tipo de produto que usa Customer.

    **Reviews e Loyalty** são módulos da mesma capability — **não** extensões. É permitido implementar só reviews ou só loyalty.

    **Customer não exige Orders** para o núcleo e reviews. Pedidos no contexto de relacionamento usam o **mesmo shape** de [Orders](orders.md).

    **Idioma do contrato:** a especificação da API é **sempre em inglês**. Os guias de protocolo são bilíngues (PT/EN).
