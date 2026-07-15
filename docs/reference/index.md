---
title: Referência da API
---

# Referência da API

!!! warning "Release Candidate (V2.0.0-rc)"
    As especificações da API abaixo são da **V2.0.0-rc**. Estão publicadas para **validação com o ecossistema** (revisão por empresas e pilotos de implementação). Podem ainda receber ajustes com base no feedback. A release estável será publicada somente após essa fase; a **V1 permanece ativa** na transição.

    Status e ciclo de vida: [Evolução do protocolo](../protocol/evolution.md) · [Changelog](../guide/changelog.md).

Esta seção é a **fonte normativa** de implementação do Open Delivery V2: as **especificações da API** (REST/HTTP) — endpoints, schemas, exemplos e erros.

!!! note "Formato das especificações"
    Todas as especificações da API são escritas em **[OpenAPI](https://www.openapis.org/)** (YAML). O site as apresenta de forma legível; o arquivo OpenAPI é o artefato canônico de cada capability.

!!! note "Idioma do contrato"
    As especificações da API estão **somente em inglês**. Conceitos e fluxos de domínio ficam na tab **Protocolo** (PT e EN).

A tab **Protocolo** explica o domínio; esta tab define o **contrato implementável**. Em divergência, **prevalece a especificação da API**.

## Convenções

| Página | Descrição |
|---|---|
| [Regras gerais](conventions.md) | Interoperabilidade, timestamps, paginação, duplicidade de ciclo de vida |
| [Tratamento de Erros](error-handling.md) | Envelope de erro e códigos HTTP |

## Infraestrutura

Comece por aqui em toda integração nova.

| Spec | Descrição | Protocolo |
|---|---|---|
| [Discovery](discovery.md) | Endpoint well-known e declaração de capabilities | [Regras](../protocol/discovery.md) |
| [Autenticação](authentication.md) | OAuth 2.0, token, assinatura de webhooks | [Regras](../protocol/authentication.md) |

## Capabilities

| Spec | Descrição | Protocolo |
|---|---|---|
| [Pedidos](orders.md) | Ciclo de vida, status × eventos, polling e webhooks | [Regras](../protocol/orders.md) |
| [Indoor](indoor.md) | Contas em salão (extensão de Orders), pagamentos e fiscal | [Regras](../protocol/indoor.md) |
| [Merchant](merchant.md) | Estabelecimento, catálogo, serviços e disponibilidade | [Visão geral](../protocol/merchant.md) · [Dados da Loja](../protocol/merchant-store.md) · [Menus](../protocol/menu.md) |
| [Logística](logistics.md) | Coordenação de entrega, rastreamento e problemas | [Regras](../protocol/logistics.md) |
| [Customer](customer.md) | Dados do cliente, leads, reviews, loyalty e eventos | [Customer](../protocol/customer.md) · [Reviews](../protocol/reviews.md) · [Loyalty](../protocol/loyalty.md) |
