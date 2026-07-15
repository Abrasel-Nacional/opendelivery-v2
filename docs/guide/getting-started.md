# Primeiros Passos

!!! warning "Release Candidate (V2.0.0-rc)"
    Esta documentação está em **Release Candidate**. O conteúdo foi consolidado nos comitês técnicos e agora passa por um período de **validação com o ecossistema**: revisão por empresas e **pilotos de implementação**.

    Durante essa fase a especificação ainda pode receber ajustes com base no feedback. A versão **estável (release)** será publicada somente após a conclusão da validação. A **V1 permanece ativa** e é a referência em produção na transição.

    Envie feedback pelo [repositório no GitHub](https://github.com/Abrasel-Nacional/opendelivery-v2/issues). Detalhes no [changelog](changelog.md).

O Open Delivery é um **protocolo aberto**, não um produto. Ele define como sistemas independentes do ecossistema de food tech — aplicações de pedido, sistemas de gestão de restaurantes, operadores de logística e plataformas de CRM — se comunicam de forma interoperável, sem integrações bilaterais customizadas.

Este guia cobre o mínimo necessário para começar uma integração.

---

## 1. Entenda seu papel no ecossistema

O protocolo define quatro papéis. Um sistema pode desempenhar mais de um.

| Papel | Quem é | O que faz |
|---|---|---|
| **Originador** | Aplicação de pedido, marketplace, totem | Cria o pedido; recebe atualizações de ciclo de vida |
| **Software Service (PDV)** | Sistema de gestão do restaurante | Aceita pedidos; gerencia cardápio, conta, fiscal |
| **Logística** | Operador de entrega, frota própria | Executa a entrega; emite eventos de rastreamento |
| **Software CRM** | Plataforma de dados do cliente / fidelidade | Consome a capability **Customer** (e módulos Reviews/Loyalty); não altera o ciclo operacional do pedido |

Antes de qualquer coisa, identifique qual papel — ou quais papéis — seu sistema desempenha. Isso define quais capabilities você precisa implementar.

Guia detalhado: **[Trilhas por papel](by-role.md)**.

---

## 2. Autentique-se

O Open Delivery V2 usa **OAuth 2.0** com autenticação por aplicação: um único `client_id` para todas as lojas que seu sistema integra.

Três modelos são suportados:

| Modelo | Identificador | Recomendação |
|---|---|---|
| Client Credentials por aplicação | `client_credentials` + `by_app` | **Recomendado para novas integrações** |
| Client Credentials por loja | `client_credentials` + `by_merchant` | Compatibilidade com V1 |
| Authorization Code | `authorization_code` | Casos de uso avançados |

Para obter um token de acesso:

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id={seu_client_id}
&client_secret={seu_client_secret}
&scope=od.orders od.menu
```

O token retornado deve ser incluído no header `Authorization: Bearer {token}` em todas as requisições.

!!! note "Escopos disponíveis"
    `od.orders` · `od.menu` · `od.logistics` · `od.crm` · `od.all`

Para mais detalhes, consulte a [documentação de autenticação](../protocol/authentication.md) e a [referência da API de autenticação](../reference/authentication.md).

---

## 3. Declare suas capacidades via Discovery

O primeiro passo obrigatório de qualquer integração é publicar um endpoint de Discovery no padrão Well-Known:

```
GET /.well-known/opendelivery
```

Este endpoint declara publicamente quais capabilities seu sistema implementa, quais versões do protocolo suporta, e como os parceiros devem se autenticar. **Nenhuma integração pode prosseguir sem que o Discovery esteja disponível.**

Exemplo mínimo de resposta:

```json
{
 "appId": "550e8400-e29b-41d4-a716-446655440000",
 "openDelivery": {
 "currentVersion": "2.0",
 "supportedVersions": ["2.0"]
 },
 "discovery": { "version": "1.0.0" },
 "authentication": {
 "supportedGrantTypes": ["client_credentials"],
 "clientIdGeneration": ["by_app"]
 },
 "capabilities": {
 "orders": { "endpoint": "https://api.suaempresa.com/v2" }
 }
}
```

Para mais detalhes, consulte a [documentação de Discovery](../protocol/discovery.md) e a [referência da API de Discovery](../reference/discovery.md).

---

## 4. Escolha qual capability implementar primeiro

Dependendo do seu papel:

=== "Originador"
 1. **Discovery** — publique seu endpoint Well-Known
 2. **Orders** — crie pedidos e consuma eventos de ciclo de vida
 3. **Merchant** — consulte cardápio e status das lojas

=== "Software Service (PDV)"
 1. **Discovery** — publique seu endpoint Well-Known
 2. **Merchant** — exponha cardápio, horários e pausas
 3. **Orders** — aceite e processe pedidos recebidos
 4. **Indoor** — se suportar salão/comanda/totem

=== "Logística"
 1. **Discovery** — publique seu endpoint Well-Known
 2. **Logistics** — receba solicitações de entrega e emita eventos de rastreamento

=== "Software CRM"
 1. **Discovery** — publique seu endpoint Well-Known
 2. **Customer** — capability de dados do cliente (módulos Reviews e/ou Loyalty conforme necessidade)
 3. **Loyalty** (módulo) — programas de fidelidade e resgate, se aplicável

---

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="by-role.md">Trilhas por papel</a> — o que implementar conforme o produto</li>
    <li><a href="../documentation/core-concepts.md">Conceitos</a> — arquitetura e entidades</li>
    <li><a href="../protocol/discovery.md">Discovery</a> · <a href="../protocol/authentication.md">Autenticação</a></li>
    <li><a href="../reference/conventions.md">Regras gerais</a> · <a href="../reference/error-handling.md">Tratamento de Erros</a></li>
    <li><a href="migration-v1-v2.md">Migração V1→V2</a> · <a href="../reference/index.md">Referência da API</a></li>
  </ul>
</div>
