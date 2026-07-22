# Migracao V1 -> V2

Este guia explica como migrar da V1 para a V2 com foco em impacto de implementacao.
A organizacao abaixo segue por capability para facilitar planejamento tecnico por squad.

Consulte o [Changelog](changelog.md) para historico de release.

!!! info "V1 continua ativa"
    A V1 permanece ativa durante a transicao. Novas integracoes devem priorizar V2.

---

## Como executar a migracao

Sequencia recomendada:

1. Migrar **Authentication** (modelo de credencial e escopos).
2. Publicar **Discovery** (manifesto obrigatorio da integracao).
3. Migrar capabilities de negocio na ordem de prioridade do produto (Merchant, Menu, Orders, Logistics, Customer, Indoor).
4. Rodar homologacao por capability com criterios de aceite objetivos.

---

## Authentication

### O que muda da V1 para a V2

- **Mudanca recomendada**: credencial por aplicacao (`client_id` unico por software) passa a ser o modelo preferencial para novas integracoes.
- **Compatibilidade legada**: credencial por merchant (`client_id` por loja) continua suportada para migracao gradual.
- **Breaking**: escopos passam a ser granulares por dominio (`od.orders`, `od.menu`, `od.logistics`, `od.crm`, `od.all`).
- **Melhoria**: suporte opcional ao `Authorization Code Flow` para casos que exigem autorizacao delegada de estabelecimento.

### Impacto no codigo

- Priorizar fluxo por aplicacao na camada de autenticacao.
- Manter fallback por merchant para parceiros ainda em legado.
- Atualizar emissao de token para incluir escopos adequados por fluxo.
- Revisar cache de token para uso por aplicacao (nao por loja).

```diff
# V1
POST /oauth/token
- client_id=credencial_loja_123
- client_secret=segredo_loja_123

# V2
POST /oauth/token
+ client_id=credencial_aplicacao
+ client_secret=segredo_aplicacao
+ scope=od.orders od.menu
```

Depois do token, a aplicacao resolve quais merchants estao autorizados via:

```
GET /merchants
Authorization: Bearer {token_da_aplicacao}
```

### Compatibilidade legada (importante)

- O modelo `by_merchant` (um `client_id` por loja) continua suportado na V2 para transicao.
- O modelo recomendado para novas integracoes e para evolucao gradual de stacks existentes e `by_app`.
- Se `authorization_code` for suportado, ele tambem deve ser declarado no discovery.

### Campos de Discovery que devem ser preenchidos

| Campo | Tipo | Obrigatorio | Uso na migracao |
|---|---|---|---|
| `authentication.supportedGrantTypes` | array[string] | SIM | Declarar `client_credentials` e, quando aplicavel, `authorization_code` |
| `authentication.clientIdGeneration` | array[string] | SIM | Declarar `by_app` (recomendado) e/ou `by_merchant` (legado) |

### Passo a passo de migracao

1. Criar armazenamento de credencial por aplicacao.
2. Atualizar cliente OAuth para enviar `scope` explicitamente.
3. Mapear rotas/acoes internas para escopos minimos.
4. Trocar fluxo de descoberta de lojas para `GET /merchants` com token da aplicacao.
5. Validar fallback de compatibilidade quando o parceiro ainda estiver em `by_merchant`.

### Criterios de aceite

- A aplicacao obtém token com escopos corretos.
- A aplicacao lista merchants autorizados sem usar credenciais por loja.
- Chamadas sem escopo necessario retornam erro esperado e observavel.

### Armadilhas comuns

- Reutilizar escopo amplo (`od.all`) em tudo e perder principio de menor privilegio.
- Manter cache de token por merchant sem necessidade.
- Esquecer renovacao de token para jobs assíncronos de longa duracao.

Referencias: [Protocolo Authentication](../protocol/authentication.md) · [API Authentication](../reference/authentication.md)

---

## Discovery

### O que muda da V1 para a V2

- **Breaking operacional**: `GET /.well-known/opendelivery` passa a ser obrigatorio para iniciar integracao.
- **Melhoria**: capabilities, versoes, auth models e modos de eventos ficam declarados em um manifesto unico.

### Campos de Discovery mais criticos na migracao

| Campo | Tipo | Obrigatorio | Por que importa |
|---|---|---|---|
| `openDelivery.supportedVersions` | array[string] | SIM | Garante compatibilidade de versao antes da integracao |
| `authentication.supportedGrantTypes` | array[string] | SIM | Define os fluxos OAuth permitidos |
| `authentication.clientIdGeneration` | array[string] | SIM | Define se o parceiro esta em `by_app`, `by_merchant` ou ambos |
| `capabilities.orders.originator.supportedEvents` | array[string] | Condicional | Define quais eventos de pedido sao realmente emitidos |
| `capabilities.orders.originator.supportsWebhook` | boolean | Condicional | Define se envio de eventos por webhook esta disponivel |
| `capabilities.orders.originator.supportsPolling` | boolean | Condicional | Define se consumo por polling esta disponivel |
| `capabilities.orders.receiver.supportedOperations` | array[string] | Condicional | Define quais operacoes de Orders podem ser chamadas |
| `capabilities.logistics.originator.supportedEvents` | array[string] | Condicional | Define eventos de logistics emitidos |
| `capabilities.logistics.receiver.supportedOperations` | array[string] | Condicional | Define operacoes de logistics aceitas |
| `capabilities.customer.maxBatchSize` | integer | Condicional | Controla tamanho de lote para sincronizacao |
| `capabilities.customer.requestsPerSecond` | integer | Condicional | Controla limite de taxa para consumo seguro |

### Impacto no codigo

- Adicionar cliente de bootstrap da integracao baseado no manifesto.
- Remover configuracoes fixas hardcoded de capability/baseUrl quando o manifesto estiver disponivel.
- Validar compatibilidade de versao antes de ativar chamadas de negocio.

### Passo a passo de migracao

1. Publicar endpoint `/.well-known/opendelivery`.
2. Declarar capabilities realmente suportadas e seus `baseUrl`.
3. Declarar modelo de autenticacao e modo de emissao/consumo de eventos.
4. Fazer o consumer carregar e validar o manifesto no onboarding.
5. Bloquear ativacao quando manifesto estiver ausente ou invalido.

### Criterios de aceite

- Integracao sobe apenas quando discovery retorna contrato valido.
- Versoes e capabilities lidas no discovery batem com o que a API expõe.
- Logs de bootstrap mostram capability habilitada/inabilitada de forma rastreavel.

### Armadilhas comuns

- Publicar capability no discovery sem endpoint correspondente implementado.
- Divergencia entre ambientes (homologacao publica algo diferente de producao).
- Tratar discovery como opcional e manter onboarding manual.

Referencias: [Protocolo Discovery](../protocol/discovery.md) · [API Discovery](../reference/discovery.md)

---

## Merchant

### Mudancas principais

- **Breaking**: `merchantId` passa a ser gerado pelo originador.
- **Breaking**: `merchantType` removido.
- **Breaking**: service deixa de ter id proprio e passa a ser identificado por tipo (`DELIVERY`, `TAKEOUT`, `INDOOR`).
- **Breaking**: shape de `Service` mudou na V2 (sem `id` de service; com `type` e `status` como base; horarios no bloco `operatingHours`).
- **Breaking**: endpoints legados de onboarding/status da V1 (`/v1/merchantOnboarding`, `/v1/merchantStatus`) nao fazem parte do contrato normativo de Merchant V2.

### O que adaptar

- Ajustar ownership do identificador em cadastro e sincronizacao.
- Garantir de/para interno via `externalCode` no Software Service.
- Atualizar validadores para novo modelo de services por tipo.
- Migrar consumidores para o novo shape de service (inclusive regras de status e horarios).
- Remover dependencia dos endpoints legados de onboarding/status e adotar discovery + operacoes normativas de Merchant.
- Tratar `GET .../snapshot` como caminho de bootstrap/reconciliacao e CRUD como caminho incremental.

### Campos de Discovery relevantes

| Campo | Tipo | Uso |
|---|---|---|
| `capabilities.merchant.supported` | boolean | Habilita capability Merchant na integracao |
| `capabilities.merchant.supportsPartialUpdate` | boolean | Define estrategia de atualizacao parcial vs payload completo |
| `capabilities.merchant.supportsFullGetByOriginator` | boolean | Define se reconciliacao por GET completo esta disponivel |

Referencias: [Protocolo Merchant](../protocol/merchant.md) · [API Merchant](../reference/merchant.md)

---

## Menu (modulo dentro da capability Merchant)

### Mudancas principais

- **Breaking**: fim do webhook monolitico `merchantUpdate`.
- **Breaking**: CRUD granular por entidade de catalogo.
- **Breaking**: `subtotal` em opcionais removido; `option_price` passa a ser obrigatorio.
- **Melhoria**: snapshot completo para sincronizacao.

### O que adaptar

- Separar pipeline de atualizacao por entidade (menu, categoria, itemOffer, optionGroup, option).
- Atualizar validacoes de preco para `option_price` e `unity_price`.
- Implementar reconciliacao por snapshot quando detectar drift de dados.

Referencias: [Protocolo Menu](../protocol/menu.md) · [API Merchant](../reference/merchant.md)

---

## Orders

### Mudancas principais

- **Breaking**: cancelamento do originador por handshake removido; permanece cancelamento mandatorio via `CANCELLED`.
- **Breaking**: evento `PICKED_UP` removido.
- **Breaking**: `Order.type` sai da raiz e vira `Order.fulfillment.orderType`.
- **Breaking**: `Order.delivery` / `Order.takeout` / `Order.indoor` movem para `Order.fulfillment.*`.
- **Breaking**: campos de preco de item/opcao passam a ficar agrupados em `pricing` dentro de `Order.items[*]` e `Order.items[*].options[*]`.
- **Breaking**: formato de preco volta ao modelo da V1 (`Price { value, currency }`) para item, opcao, descontos, taxas e totais.
- **Breaking**: `subtotalPrice` deixa de existir em item e opcao.
- **Breaking de consumo**: `Order.status` em `GET /orders/{id}` vira fonte de verdade.

### Regras de migracao essenciais

- Nao implementar `POST /orders` para entrada de pedido.
- Tratar eventos como notificacao; reconciliar estado via GET.
- Tratar operacao duplicada ja aplicada com `202` (sem nova transicao).

### Campos V2 de Orders que devem entrar no plano

| Campo | Tipo | Acao de migracao | Impacto |
|---|---|---|---|
| `Order.timing` | object | Migrar `orderTiming`, `schedule`, `preparationStartDateTime`, `orderPriority` para o bloco unificado | Quebra estrutural de payload |
| `Order.timing.schedule` | object | Validar obrigatoriedade quando `orderTiming = SCHEDULED` | Regra condicional obrigatoria |
| `Order.context.salesChannel` | string | Mapear canal de venda para `context.salesChannel` | Mudanca de local do campo |
| `Order.observations` | string | Separar observacao geral de pedido das observacoes de item/contexto | Novo campo funcional |
| `Order.items[*].itemOfferId` | string | Enviar referencia de oferta de catalogo quando existir | Novo campo opcional |
| `Order.items[*].observations` | string | Migrar de `specialInstructions` para `items[*].observations` | Renomeacao semantica |
| `Order.items[*].options[*].defaultQuantity` | integer | Informar quantidade incluida por padrao antes de adicional cobrado | Novo campo de precificacao |
| `Order.items[*].options[*].options` | array[OrderItemOption] | Suportar arvore de opcoes em multiplos niveis | Novo comportamento estrutural |
| `Order.customer.birthDate` | string(date) | Mapear quando disponivel para casos de CRM/Loyalty | Novo campo opcional |
| `Order.customer.gender` | string | Mapear quando disponivel para segmentacao/comunicacao | Novo campo opcional |
| `Order.customer` (quando `fulfillment.orderType = DELIVERY`) | object | Tornar obrigatorio para pedidos delivery | Quebra de validacao |

### Discovery para Orders (ponto critico)

Na V2, os eventos de Orders suportados pela contraparte devem ser lidos no discovery antes de ativar o fluxo.

| Campo | Tipo | Uso |
|---|---|---|
| `capabilities.orders.originator.supportedEvents` | array[string] | Lista os eventos que serao emitidos |
| `capabilities.orders.originator.unsupportedEvents` | array[string] | Lista eventos que nao devem ser esperados |
| `capabilities.orders.originator.supportsWebhook` | boolean | Define envio push de eventos |
| `capabilities.orders.originator.supportsPolling` | boolean | Define consumo pull de eventos |
| `capabilities.orders.receiver.supportedOperations` | array[string] | Lista operacoes de Orders aceitas pelo receiver |
| `capabilities.orders.receiver.unsupportedOperations` | array[string] | Lista operacoes indisponiveis para evitar chamadas invalidas |

```diff
# Antes
{
  "id": "order-123",
- "type": "DELIVERY",
  "delivery": { "address": { "city": "Sao Paulo" } }
}

# Depois
{
  "id": "order-123",
  "fulfillment": {
+   "orderType": "DELIVERY",
    "delivery": { "address": { "city": "Sao Paulo" } }
  }
}
```

Referencias: [Protocolo Orders](../protocol/orders.md) · [API Orders](../reference/orders.md) · [Convencoes](../reference/conventions.md#duplicidade-de-operacoes-de-ciclo-de-vida)

---

## Logistics

### Mudancas principais

- **Melhoria normativa**: consolidacao de semantica async-first com `202 Accepted` nas mutacoes de ciclo de vida.
- **Melhoria**: alinhamento com discovery para modo de acompanhamento (`push`/`pull`).

### O que adaptar

- Revisar consumidores para nao interpretar `202` como conclusao de estado.
- Ajustar rastreio para o modo declarado no discovery.

### Campos de Discovery relevantes

| Campo | Tipo | Uso |
|---|---|---|
| `capabilities.logistics.originator.supportedEvents` | array[string] | Define eventos de lifecycle emitidos |
| `capabilities.logistics.originator.supportsWebhook` | boolean | Define envio push |
| `capabilities.logistics.originator.supportsPolling` | boolean | Define consumo pull |
| `capabilities.logistics.receiver.supportedOperations` | array[string] | Define operacoes aceitas pelo receiver |

Referencias: [Protocolo Logistics](../protocol/logistics.md) · [API Logistics](../reference/logistics.md)

---

## Customer e Loyalty

### Mudancas principais

- **Novo**: capability Customer para dados de cliente, leads e reviews.
- **Novo**: Loyalty como modulo do dominio de relacionamento.

### O que adaptar

- Planejar onboarding separado por capability (nao assumir dependencia obrigatoria de Orders).
- Reaproveitar shape de dados de pedido quando aplicavel ao contexto de relacionamento.

### Campos de Discovery relevantes

| Campo | Tipo | Uso |
|---|---|---|
| `capabilities.customer.supported` | boolean | Habilita capability Customer |
| `capabilities.customer.supportsBatchGet` | boolean | Define disponibilidade de GET em lote |
| `capabilities.customer.supportsBatchPost` | boolean | Define disponibilidade de POST em lote |
| `capabilities.customer.maxBatchSize` | integer | Define tamanho maximo por lote |
| `capabilities.customer.maxGetPeriodDays` | integer | Define janela maxima de consulta |
| `capabilities.customer.requestsPerSecond` | integer | Define limite de taxa |

Referencias: [Protocolo Customer](../protocol/customer.md) · [API Customer](../reference/customer.md) · [Protocolo Loyalty](../protocol/loyalty.md)

---

## Indoor

### Mudancas principais

- **Novo**: capability para operacao de salao (mesa, comanda, balcao) com conta central.
- **Regra importante**: Indoor depende de Orders para lifecycle de pedido.

### O que adaptar

- Modelar fluxo de conta e pagamento sem criar atalho fora do lifecycle de Orders.
- Garantir consistencia entre pedido (`fulfillment.orderType: INDOOR`) e estado da conta.

### Campos de Discovery relevantes

| Campo | Tipo | Uso |
|---|---|---|
| `capabilities.indoor.supported` | boolean | Habilita capability Indoor |
| `capabilities.indoor.invoiceIssuer` | string | Define emissor fiscal (`pos`, `app`, `platform`) |
| `capabilities.indoor.invoiceIssueMoment` | string | Define momento de emissao fiscal |
| `capabilities.indoor.usesAccountId` | boolean | Define se o fluxo usa identificador de conta |

Referencias: [Protocolo Indoor](../protocol/indoor.md) · [API Indoor](../reference/indoor.md)

---

!!! abstract "Checklist final por capability"
  | Capability | Item de checklist |
  |---|---|
  | Authentication | Migrar para credencial por aplicacao com escopos corretos |
  | Authentication | Validar compatibilidade legada de autenticacao (`by_merchant`) quando necessario |
  | Authentication | Declarar Authorization Code no discovery quando suportado |
  | Discovery | Publicar e validar discovery no onboarding |
  | Orders + Discovery | Validar eventos e operacoes suportados de Orders a partir do discovery |
  | Merchant | Ajustar `merchantId` do originador e services por tipo |
  | Menu | Migrar de `merchantUpdate` para CRUD granular |
  | Orders | Migrar para `fulfillment.orderType` e status como fonte de verdade |
  | Logistics | Validar fluxo async-first com `202` |
  | Customer/Loyalty | Avaliar e planejar conforme roadmap de produto |
  | Indoor | Integrar com lifecycle de Orders |

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="changelog.md">Changelog</a> - historico completo de versoes</li>
    <li><a href="getting-started.md">Primeiros Passos</a> - caminho minimo V2</li>
    <li><a href="../protocol/authentication.md">Authentication</a> · <a href="../protocol/discovery.md">Discovery</a></li>
    <li><a href="../reference/index.md">Referencia da API</a></li>
  </ul>
</div>
