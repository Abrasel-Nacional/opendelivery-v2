# Primeiros Passos

O Open Delivery é um **protocolo aberto**, não um produto. Ele define como sistemas independentes do ecossistema de food tech — aplicações de pedido, sistemas de gestão de restaurantes, operadores de logística e plataformas de CRM — se comunicam de forma interoperável, sem integrações bilaterais customizadas.

Este guia cobre o mínimo necessário para começar uma integração.

<div class="od-api-callout">
  <p>Prefere um caminho por tipo de produto? Use as trilhas por papel.</p>
  <a href="by-role/">Abrir trilhas por papel →</a>
</div>

---

## 1. Entenda seu papel no ecossistema

O protocolo define quatro papéis. Um sistema pode desempenhar mais de um.

| Papel | Quem é | O que faz |
|---|---|---|
| **Originador** | Aplicação de pedido, marketplace, totem | Cria o pedido; recebe atualizações de ciclo de vida |
| **Software Service (PDV)** | Sistema de gestão do restaurante | Aceita pedidos; gerencia cardápio, conta, fiscal |
| **Logística** | Operador de entrega, frota própria | Executa a entrega; emite eventos de rastreamento |
| **CRM** | Plataforma de fidelidade, dados de cliente | Consome dados de pedidos e clientes; gerencia programas de fidelidade |

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

=== "CRM"
    1. **Discovery** — publique seu endpoint Well-Known
    2. **Customer** — gerencie dados de clientes
    3. **Loyalty** — gerencie programas de fidelidade e resgate

---

## 5. Referências

| Documento | Descrição |
|---|---|
| [Conceitos](../documentation/core-concepts.md) | Arquitetura, entidades e modelo de interação |
| [Papéis e Responsabilidades](../protocol/roles-and-responsibilities.md) | Obrigações de cada papel no protocolo |
| [Autenticação](../protocol/authentication.md) | Modelos OAuth 2.0 e escopos |
| [Discovery](../protocol/discovery.md) | Endpoint Well-Known e estrutura do manifesto |
| [Guidelines](../protocol/guidelines.md) | Convenções de datas, paginação, idempotência |
| [Tratamento de Erros](../protocol/error-handling.md) | Formato padrão de erros e códigos HTTP |
| [Migração V1→V2](migration-v1-v2.md) | Breaking changes e guia de migração |
| [Referência da API](../reference/index.md) | OpenAPI specs interativas |
