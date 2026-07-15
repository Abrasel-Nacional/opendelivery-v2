---
template: redoc.html
openapi_spec: ../v2/merchant.openapi.yaml
hide:
 - toc
 - navigation
---

!!! tip "Guia + contrato"
    Esta página é a **especificação da API** (endpoints, campos, erros e exemplos) — o suficiente para implementar Merchant (loja + catálogo).

    Se você ainda não conhece o domínio (`merchantId` do originador, CRUD vs `merchantUpdate`, services por tipo, pause, snapshot), leia antes:

    - [Merchant — visão geral](../protocol/merchant.md)
    - [Dados da Loja](../protocol/merchant-store.md)
    - [Menus](../protocol/menu.md)

    **Merchant não exige Orders.** Pode ser implementada sozinha.

    **Idioma do contrato:** a especificação da API é **sempre em inglês**. Os guias de protocolo são bilíngues (PT/EN).
