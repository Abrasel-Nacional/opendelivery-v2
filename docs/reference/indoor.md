---
template: redoc.html
openapi_spec: ../v2/indoor.openapi.yaml
hide:
 - toc
 - navigation
---

!!! tip "Guia + contrato"
    Esta página é a **especificação da API** (endpoints, campos, erros e exemplos) — o suficiente para implementar Indoor.

    Se você ainda não conhece o domínio (**conta × pedido**, pré-close, pagamentos parciais, canais e papéis), leia antes o [guia Indoor](../protocol/indoor.md).

    **Pré-requisito:** [Orders](orders.md) (`fulfillment.orderType: INDOOR`, entrada via evento `CREATED` — sem `POST /orders`). Indoor é extensão de Orders, não capability autônoma.

    **Conta:** nasce quando o Software Service processa um pedido INDOOR vindo de Orders; pedidos seguintes na mesma chave operacional acumulam itens na mesma conta.

    **Eventos Indoor:** são **webhook-only**. Esta capability não define polling para `ACCOUNT_*`, `PAYMENT_*` ou `FISCAL_*`.

    **Duplicidade de lifecycle:** se a mutação da conta já foi aplicada (ex.: `pre-close` com conta já `IN_PAYMENT`, `close` com conta já `CLOSED`), o host retorna **`202`** — não `409` só por repetição.

    **Idioma do contrato:** a especificação da API é **sempre em inglês**. O guia de protocolo é bilíngue (PT/EN).
