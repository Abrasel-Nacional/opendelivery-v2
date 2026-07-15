---
template: redoc.html
openapi_spec: ../v2/orders.openapi.yaml
hide:
 - toc
 - navigation
---

!!! tip "Guia + contrato"
    Esta página é a **especificação da API** (endpoints, campos, erros e exemplos) — o suficiente para implementar Orders.

    Se você ainda não conhece o domínio (**status × eventos**, perfis, **dois caminhos de cancelamento**, polling/webhook), leia antes o [guia Orders](../protocol/orders.md).

    **Cancelamento:** merchant → `requestCancellation` (handshake mantido). Originador → só `CANCELLED` mandatório (sem accept/deny).

    **Breaking de payload:** `Order.type` saiu da raiz. Use `fulfillment.orderType` como discriminador (`DELIVERY`, `TAKEOUT`, `INDOOR`).
    **Breaking de payload:** `delivery`, `takeout` e `indoor` também saíram da raiz e agora ficam em `fulfillment.delivery`, `fulfillment.takeout` e `fulfillment.indoor`.
    **Breaking de consumo:** trate `order.status` no `GET /orders/{orderId}` como fonte de verdade. Na V1 era comum inferir estado só por evento/`lastEvent`.

    **Não existe `POST /orders`.** O pedido entra via evento `CREATED` + `GET /orders/{orderId}`.

    **Indoor** é a única capability que **exige** Orders. Merchant, Logistics e Customer podem operar sozinhas.

    **Idioma do contrato:** a especificação da API é **sempre em inglês**. O guia de protocolo é bilíngue (PT/EN).
