---
title: Referência da API
---

# Referência da API

Esta seção contém as especificações **OpenAPI** normativas para cada capability do Open Delivery V2.
Cada página renderiza o contrato REST completo com **ReDoc** — endpoints, schemas, exemplos de requisição/resposta e códigos de erro.

Para explicações conceituais, fluxos e orientações de implementação, consulte a seção **Protocolo**.

<div class="od-api-callout">
  <p>Não conhece o modelo híbrido? Leia Protocolo vs Binding antes de implementar.</p>
  <a href="../PROTOCOL_VS_BINDING/">Entender protocolo vs API →</a>
</div>

## Infraestrutura

Comece por aqui em toda integração nova.

| Spec | Descrição | Protocolo |
|---|---|---|
| [Discovery](discovery.md) | Endpoint well-known e declaração de capabilities | [Regras](../protocol/discovery.md) |
| [Autenticação](authentication.md) | OAuth 2.0, token, assinatura de webhooks | [Regras](../protocol/authentication.md) |

## Capabilities

| Spec | Descrição | Protocolo |
|---|---|---|
| [Merchant](merchant.md) | Estabelecimento, catálogo, serviços e disponibilidade | [Visão geral](../protocol/merchant.md) · [Dados da Loja](../protocol/merchant-store.md) · [Menus](../protocol/menu.md) |
| [Pedidos](orders.md) | Ciclo de vida de pedidos, estados e eventos | [Regras](../protocol/orders.md) |
| [Logística](logistics.md) | Coordenação de entrega, rastreamento e problemas | [Regras](../protocol/logistics.md) |
| [Customer & Fidelidade](customer.md) | CRM, leads, reviews, loyalty e eventos | [Customer](../protocol/customer.md) · [Reviews](../extensions/reviews.md) · [Loyalty](../extensions/loyalty.md) |
| [Indoor](indoor.md) | Contas em salão, pedidos, pagamentos e fiscal | [Regras](../protocol/indoor.md) |
