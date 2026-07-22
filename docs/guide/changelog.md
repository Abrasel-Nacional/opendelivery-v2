# Changelog

Historico de versoes do Open Delivery Protocol.

<div class="od-version-banner">
 <span class="od-version-banner__ver">V2.0.0-rc</span>
 <span class="od-version-banner__meta">Release Candidate · Julho 2026 · V1 permanece ativa na transicao</span>
</div>

## Como ler este changelog

Este changelog esta organizado por capability/modulo para facilitar implementacao e migracao.

Legenda usada:

- **Breaking**: exige ajuste de contrato ou comportamento.
- **Novo**: capability ou bloco funcional novo na V2.
- **Melhoria**: esclarecimento, reforco normativo ou evolucao sem quebra direta de contrato.

---

## V2.0.0-rc - Julho 2026

Primeira versao **Release Candidate** da V2. Esta release abre fase de validacao com o ecossistema; a V1 continua ativa durante a transicao.

### Status: validacao com o ecossistema

A publicacao do RC inicia um periodo de **validacao**, nao a release estavel. Nesta fase:

1. **Revisao** - empresas e implementadores revisam a documentacao (guia, protocolo e especificacoes da API).
2. **Piloto** - algumas empresas implementam trechos da especificacao em ambientes controlados e validam fluxos reais.
3. **Feedback** - ajustes e esclarecimentos podem ser incorporados com base nos resultados da revisao e dos pilotos.
4. **Release** - somente apos essa validacao a V2 sera promovida a versao estavel.

Ate la, a **V1 permanece ativa** e continua sendo referencia para integracoes em producao.

### Mudancas por capability

#### Discovery

- **Melhoria**: `/.well-known/opendelivery` passa a ser obrigatorio para declarar capabilities, versoes e modos de integracao antes da ativacao da integracao.

Referencias: [Protocolo Discovery](../protocol/discovery.md) · [API Discovery](../reference/discovery.md)

#### Authentication

- **Breaking**: autenticacao por aplicacao, com um `client_id` por software (nao por loja).
- **Melhoria**: padronizacao de escopos por dominio (`od.orders`, `od.menu`, `od.logistics`, `od.crm`, `od.all`).
- **Melhoria**: `Authorization Code Flow` suportado opcionalmente para casos avancados.

Referencias: [Protocolo Authentication](../protocol/authentication.md) · [API Authentication](../reference/authentication.md)

#### Merchant

- **Breaking**: `merchantId` passa a ser gerado pelo originador; PDV usa `externalCode` para correlacao interna.
- **Breaking**: `merchantType` removido.
- **Breaking**: servicos passam a ser identificados por tipo (`DELIVERY`, `TAKEOUT`, `INDOOR`), sem id separado.
- **Breaking**: shape de `Service` foi simplificado (sem `id` de service; foco em `type` + `status`; `operatingHours` no lugar do modelo antigo de horarios).
- **Breaking**: endpoints legados de onboarding/status da V1 (`/v1/merchantOnboarding`, `/v1/merchantStatus`) deixam de compor o contrato normativo de Merchant V2.
- **Melhoria**: pausa por servico explicita no modelo da capability.
- **Melhoria**: bootstrap e reconciliacao de catalogo por `GET .../snapshot`; `merchantUpdate/menuUpdated` deixa de ser caminho central.

Referencias: [Protocolo Merchant](../protocol/merchant.md) · [API Merchant](../reference/merchant.md)

#### Menu (modulo dentro da capability Merchant)

- **Breaking**: fim do webhook monolitico `merchantUpdate` da V1.
- **Breaking**: adocao de CRUD granular por entidade de catalogo.
- **Breaking**: `subtotal` em opcionais removido; usar `option_price` (obrigatorio) e `unity_price`.
- **Melhoria**: opcionais recursivos com OptionGroups aninhados.
- **Melhoria**: `quantity_available` em ItemOffer para disponibilidade operacional.

Referencias: [Protocolo Menu](../protocol/menu.md) · [API Merchant](../reference/merchant.md)

#### Orders

- **Breaking**: handshake de cancelamento do originador (`ORDER_CANCELLATION_REQUEST` + accept/deny) removido; cancelamento mandatorio via `CANCELLED`.
- **Breaking**: evento `PICKED_UP` removido.
- **Breaking**: `Order.type` removido da raiz; perfil passa para `Order.fulfillment.orderType`.
- **Breaking**: `Order.delivery`, `Order.takeout` e `Order.indoor` movidos para `Order.fulfillment.*`.
- **Breaking**: bloco de tempo foi unificado em `Order.timing` (`orderTiming`, `schedule`, `preparationStartDateTime`, `orderPriority`) e `schedule` passa a ser obrigatorio quando `orderTiming = SCHEDULED`.
- **Breaking**: campos de preco de item/opcao foram agrupados em `pricing` dentro de `Order.items[*]` e `Order.items[*].options[*]`, mantendo formato da V1 (`Price { value, currency }`).
- **Breaking**: `subtotalPrice` foi removido de item e opcao em Orders V2.
- **Breaking**: `Order.status` vira campo autoritativo em `GET /orders/{id}`.
- **Breaking**: para pedidos `DELIVERY`, `Order.customer` passa a ser obrigatorio no payload.
- **Novo**: metadados de origem no pedido com `Order.context.salesChannel` e observacoes gerais em `Order.observations`.
- **Novo**: `Order.items[*].itemOfferId`, `Order.items[*].options[*].defaultQuantity` e suporte a opcoes aninhadas (`Order.items[*].options[*].options`).
- **Novo**: dados opcionais de CRM/Loyalty em cliente (`Order.customer.birthDate` e `Order.customer.gender`).
- **Melhoria**: separacao explicita entre status e eventos.
- **Melhoria**: repeticao de operacao ja aplicada segue padrao async com `202 Accepted` (sem transicao adicional).

Referencias: [Protocolo Orders](../protocol/orders.md) · [API Orders](../reference/orders.md) · [Convencoes](../reference/conventions.md#duplicidade-de-operacoes-de-ciclo-de-vida)

#### Logistics

- **Melhoria**: consolidacao de semantica async-first (`202 Accepted`) para operacoes de ciclo de vida na integracao de entrega.
- **Melhoria**: alinhamento com discovery para modos de acompanhamento (push/pull) no contexto de rastreio.

Referencias: [Protocolo Logistics](../protocol/logistics.md) · [API Logistics](../reference/logistics.md)

#### Customer

- **Novo**: capability de dados de cliente, leads e reviews na V2.

Referencias: [Protocolo Customer](../protocol/customer.md) · [API Customer](../reference/customer.md)

#### Loyalty

- **Novo**: capability/modulo de loyalty (pontos, cashback, cupons e recompensas), dentro do dominio de CRM/Customer.

Referencias: [Protocolo Loyalty](../protocol/loyalty.md)

#### Indoor

- **Novo**: capability de operacoes de salao (mesa, comanda e balcao), com conta central e comportamento assincrono.

Referencias: [Protocolo Indoor](../protocol/indoor.md) · [API Indoor](../reference/indoor.md)

### Mudancas transversais

- **Melhoria**: modelo V2 reforca integracao assincrona como padrao (`202 Accepted` para mutacoes).
- **Melhoria**: separacao mais nitida entre narrativa de dominio (Protocolo) e contrato implementavel (API Spec).

---

## V1.7.0

A V1 permanece ativa durante a transicao.

Para diferencas e migracao, consulte: [Guia de Migracao V1->V2](migration-v1-v2.md).

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="../migration-v1-v2/">Migracao V1->V2</a> - breaking changes e checklist</li>
    <li><a href="../../documentation/roadmap/">Roadmap</a> - trabalho em andamento</li>
    <li><a href="../getting-started/">Primeiros Passos</a> · <a href="../../reference/index/">Referencia da API</a></li>
  </ul>
</div>
