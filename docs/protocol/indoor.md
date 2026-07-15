# Indoor / Salão

<p class="od-meta">
 <span class="od-badge od-badge--ext">Extensão</span>
 <span class="od-badge od-badge--code">indoor</span>
 <span class="od-badge">pai: Orders</span>
 <span class="od-badge od-badge--new">Novo na V2</span>
</p>

!!! note "Especificação da API"
    O contrato implementável (endpoints, campos, erros e exemplos) está na **[especificação de Indoor](../reference/indoor.md)** — somente em inglês.

A capability **Indoor** padroniza as operações de consumo no local — mesa, comanda e balcão — cobrindo tanto atendimento mediado por garçom quanto **autoatendimento completo** via totem, QR Code ou tablet. Ela cobre o ciclo completo de uma sessão de salão: agrupar os pedidos numa **conta**, registrar pagamentos (inclusive parciais), emitir documento fiscal e fechar a conta — tudo sincronizado entre o sistema de gestão do restaurante e a aplicação de pedido.

Esta página é o **guia de leitura**: conceitos, papéis, **conta x pedido**, fluxos e checklists. O contrato de campos e endpoints está na especificação da API (nota acima).

!!! note "Chamada repetida no ciclo da conta"
    Se a operação **já foi aplicada** (ex.: pre-close com conta já `IN_PAYMENT`, close com conta já `CLOSED`), o host **retorna `202`** — não `409` só por duplicidade. Ver [Convenções](../reference/conventions.md#duplicidade-de-operacoes-de-ciclo-de-vida) e [especificação Indoor](../reference/indoor.md).

---

## Para que serve

No delivery tradicional, um pedido nasce e morre como uma unidade isolada: é criado, preparado, entregue, encerrado. No salão a realidade é outra. Uma conta abre — numa mesa, numa comanda ou num balcão de autoatendimento — e recebe **vários pedidos ao longo do tempo**, possivelmente vindos de canais diferentes (garçom com tablet, cliente pelo QR Code, totem). Itens são cancelados ou transferidos para outra conta, o total é dividido, pago em partes, e só então a conta é fechada com emissão fiscal.

Sem um padrão, cada integração entre PDV e aplicação de salão precisava negociar bilateralmente como representar esse acúmulo: onde fica o total, como cancelar um item sem cancelar o pedido inteiro, quando emitir a nota, como tratar pagamento parcial. O Indoor elimina essa negociação ao definir a **conta** como entidade central e um conjunto fixo de operações e eventos sobre ela.

---

## O que muda da V1 para a V2

!!! important "Breaking - leia antes de migrar"
    O Indoor da V2 transforma um conjunto comum de integrações bilaterais em um contrato normativo. Se a sua empresa já opera salao com fluxos proprietarios, estes sao os pontos mais importantes para migracao.

| Tema | V1 / integracoes legadas | V2 |
|---|---|---|
| **Modelo da capability** | Normalmente proprietario ou acoplado ao PDV | Capability **Indoor** explicita, com contrato normativo |
| **Entrada de itens** | Muitas vezes descrita como abertura local de conta | Sempre via **Orders**: evento `CREATED` + `GET /orders/{id}` com `fulfillment.orderType: INDOOR` |
| **Entidade central** | Pedido, conta ou ticket variavam por integrador | **Conta** e a entidade operacional para agrupamento, pagamento, fechamento e fiscal |
| **Eventos da conta** | Formato e transporte proprietarios | Eventos `ACCOUNT_*`, `PAYMENT_*` e `FISCAL_*` padronizados |
| **Entrega de eventos** | Polling, webhook ou integracoes proprietarias | **Webhook-only** |
| **Mutacao repetida** | Repeticao de `pre-close` / `close` frequentemente tratada como erro | **`202`** se o estado alvo ja tiver sido aplicado |
| **Momento do pagamento** | Frequentemente acoplado ao checkout final | Pagamento pode acontecer em `IN_USE` ou `IN_PAYMENT` |

Nao existe `POST /orders` para criar pedido no protocolo - nem para Indoor. O pedido nasce em Orders e a conta nasce a partir dele.

---

## Pré-requisito: protocolo de Orders

!!! warning "Indoor é uma extensão de Orders, não uma capability autônoma"
    Ambas as partes **DEVEM** implementar o **protocolo de Orders** antes de Indoor. A **conta de salão é aberta a partir de um pedido**: quando o Software Service processa um pedido com `fulfillment.orderType: INDOOR` (evento `CREATED` + `GET /orders/{id}` — **não há `POST /orders`**) para uma chave operacional sem conta aberta, cria a conta. Pedidos INDOOR seguintes na mesma chave só acumulam itens.

    Detalhes de ciclo de vida e eventos do **pedido** ficam só em Orders — não se redefinem aqui. Implementações sem Orders ativo **não podem** usar esta capability.

    - Guia: [Orders](orders.md)
    - Contrato: [especificação Orders](../reference/orders.md)

O pedido é o **canal de entrada de itens**; a conta é o **agrupador operacional** desses pedidos para fins de pagamento, fechamento e integração fiscal.

---

## Papeis

| Papel | Responsabilidade |
|---|---|
| **Software Service** | Sistema de gestão do restaurante. **Hospeda e implementa** todos os endpoints desta spec e **emite** os eventos do ciclo de vida da conta. |
| **Ordering Application** | Aplicação de pedido (totem, tablet do garçom, app do cliente, frente de caixa). **Consome** os endpoints e **recebe** os eventos via webhook para manter-se sincronizada. |

Em todas as operações desta capability o Software Service é o servidor e a Ordering Application é o cliente.

---

## Conta vs eventos

Este é o ponto mais importante para não misturar Indoor com Orders.

| Conceito | O que é | Onde está a verdade |
|---|---|---|
| **Pedido INDOOR** | Canal de entrada dos itens | [Orders](orders.md) |
| **Conta** | Agrupador operacional da sessão | `GET /accounts` / `GET /accounts/{accountId}` |
| **Evento da conta** | Fato imutável notificado sobre a conta | Webhook `accountEvent` |

**Regras:**

1. O pedido continua seguindo o lifecycle de Orders; Indoor **não** redefine `order.status`.
2. A conta é a fonte de verdade para agrupamento, pagamentos, lock e fechamento.
3. `202 Accepted` nas mutações de conta não significa resultado final; a confirmação de negócio fecha com evento e/ou reconciliação por GET.
4. Eventos de conta são notificações, não comandos.
5. Deduplique por `eventId` e não assuma ordenação estrita de entrega.

---

## Discovery

Participantes que expõem Indoor **DEVEM** declarar `capabilities.indoor` no manifesto well-known (`GET /.well-known/opendelivery`), conforme a [especificação de Discovery](../reference/discovery.md). Indoor continua sendo uma **extensão de Orders no domínio**, mas sua declaração pública em Discovery é feita como objeto próprio.

Campos típicos da declaração Indoor no Discovery (detalhe normativo na [especificação Discovery](../reference/discovery.md)):

| Campo | Significado |
|---|---|
| `invoiceIssuer` | Quem emite o documento fiscal (`pos` / `app` / `platform`) |
| `invoiceIssueMoment` | Momento da emissão (`account_closing`, `item_addition`, `payment`) |
| `usesAccountId` | Se o participante rastreia sessões com `accountId` |

```json
"capabilities": {
 "indoor": {
 "version": "1.0.0",
 "supported": true,
 "endpoint": "https://api.example.com/od/v2",
 "invoiceIssuer": "pos",
 "invoiceIssueMoment": "account_closing",
 "usesAccountId": true
 }
}
```

Guia geral: [Discovery](discovery.md). Contrato: [especificação Discovery](../reference/discovery.md).

---

## Mapa: o que fazer → operação na especificação da API

Use esta tabela para ir do fluxo de negócio ao contrato HTTP. Todos os links abrem a [Especificação da API Indoor](../reference/indoor.md).

| Objetivo | Operação | Onde na spec |
|---|---|---|
| Abrir conta / adicionar itens | Evento `CREATED` + `GET /orders/{id}` com `fulfillment.orderType: INDOOR` | [Orders](../reference/orders.md) (pré-requisito) |
| Consultar conta (mesa/comanda) | `GET /accounts?operationMode&identifier` | `getAccount` |
| Consultar conta por ID | `GET /accounts/{accountId}` | `getAccountById` |
| Pré-fechar (lock) | `POST /accounts/pre-close` | `preCloseAccount` |
| Desbloquear | `POST /accounts/unlock` | `unlockAccount` |
| Fechar conta | `POST /accounts/close` | `closeAccount` |
| Cancelar item | `POST /accounts/items/{itemId}/cancel` | `cancelAccountItem` |
| Transferir itens/conta | `POST /accounts/transfers` | `transferAccountContent` |
| Lançar pagamento | `POST /accounts/payments` | `createPayment` |
| Listar pagamentos | `GET /accounts/payments` | `listAccountPayments` |
| Solicitar fiscal | `POST /accounts/fiscal` | `requestFiscalDocument` |
| Consultar documentos fiscais | `GET /accounts/fiscal` | `listAccountFiscalDocuments` |
| Receber eventos | Webhook `accountEvent` | `receiveAccountEvent` |

---

## Conceitos-chave

### A conta (Account)

A **conta** é o agrupador de todos os pedidos, itens, pagamentos e documentos fiscais de uma sessão de consumo. Cada conta é localizada por uma **chave operacional** — a combinação `operationMode` + `identifier`:

| `operationMode` | Significado | Exemplo de `identifier` |
|---|---|---|
| `TABLE` | Atendimento por mesa | `"5"` (mesa 5) |
| `TAB` | Atendimento por comanda | `"A-102"` |
| `COUNTER` | Consumo no balcão | `"3"` (posição 3) |

Além da chave operacional, a conta pode ter um `accountId` interno do PDV. A consulta primária é feita pela chave operacional (`GET /accounts?operationMode=TABLE&identifier=5`); quando o `accountId` já é conhecido, há também `GET /accounts/{accountId}`. A conta sempre traz um campo `lastEvent` com o **tipo** do último evento emitido (ex.: `ACCOUNT_ITEM_ADDED`) — útil para sincronização e depuração quando a entrega do webhook é incerta (ex.: após reconexão).

### Canais de origem (originChannel)

O `operationMode` define como a conta é **agrupada** — mas não diz por onde o pedido **entrou**. Essa informação é do `originChannel`, presente em cada pedido, e é aqui que fica explícito que o Indoor não pressupõe atendimento mediado por garçom:

| `originChannel.type` | Descrição |
|---|---|
| `TOTEM` | Autoatendimento em totem físico no estabelecimento. |
| `QR_CODE` | Cliente escaneia um QR Code na mesa/comanda e pede pelo próprio celular. |
| `CUSTOMER_TABLET` | Tablet entregue ao cliente para pedir diretamente, sem intermediário. |
| `WAITER_TABLET` | Tablet usado pelo garçom/atendente para lançar o pedido. |
| `FRONT_DESK` | Pedido lançado na frente de caixa. |
| `POS` | Pedido originado diretamente no sistema de ponto de venda. |
| `APP` | App de pedido do estabelecimento ou de terceiros. |
| `WHATSAPP` | Pedido recebido via WhatsApp. |
| `OTHER` | Qualquer outro canal não listado. |

`operationMode` e `originChannel` são independentes: uma mesma conta pode acumular pedidos de **canais diferentes** ao longo da sessão. Por exemplo, o cliente abre a conta pelo QR Code (`originChannel: QR_CODE`) e, depois, o garçom lança um item adicional pelo tablet (`originChannel: WAITER_TABLET`) — ambos os pedidos caem na mesma conta porque compartilham a chave operacional (`operationMode` + `identifier`). O canal é só um metadado do pedido, não afeta a identidade da conta.

### Objeto `fulfillment.indoor` no pedido

No pedido de Orders, o payload de Indoor fica em `order.fulfillment.indoor`.

Valores canônicos da V2 (identificadores técnicos) são sempre em inglês:

- `operationMode`: `TABLE`, `TAB`, `COUNTER`
- `consumptionType`: `DINE_IN`, `TAKEAWAY`
- `originChannel.type`: `TOTEM`, `QR_CODE`, `CUSTOMER_TABLET`, `WAITER_TABLET`, `FRONT_DESK`, `POS`, `APP`, `WHATSAPP`, `OTHER`

Mapeamento comum de labels legadas: `MESA -> TABLE`, `COMANDA -> TAB`, `BALCAO -> COUNTER`, `CONSUMIR_NO_LOCAL -> DINE_IN`, `LEVAR -> TAKEAWAY`.

| Campo | Tipo | Obrigatório | Descrição / enum |
|---|---|---|---|
| `operationMode` | `string` | Sim | Modo operacional da conta: `TABLE`, `TAB`, `COUNTER` |
| `identifier` | `string` | Sim | Identificador operacional (mesa/comanda/balcão) |
| `account.id` | `string` | Não | Id da conta quando já conhecido |
| `originChannel.type` | `string` | Sim | Canal de origem do pedido |
| `originChannel.id` | `string` | Não | Id específico de dispositivo/canal/origem |
| `originChannel.notes` | `string` | Não | Observação livre sobre o canal |
| `consumptionType` | `string` | Sim | Intenção de consumo: `DINE_IN`, `TAKEAWAY` |
| `fulfillment.type` | `string` | Condicional | Handoff local: `DISPATCH` ou `CALL` |
| `fulfillment.call.notifyOriginator` | `boolean` | Condicional | Notificar originador no fluxo de chamada |
| `fulfillment.call.type` | `string` | Condicional | Tipo de chamada: `TICKET_NUMBER`, `PAGER`, `CALL_NAME`, `WHATSAPP`, `OTHER` |
| `fulfillment.call.label` | `string` | Condicional | Valor exibido ao cliente (senha/nome/pager etc.) |
| `fulfillment.dispatch.id` | `string` | Condicional | Id do ponto de despacho |
| `fulfillment.dispatch.label` | `string` | Condicional | Nome amigável do ponto de despacho |
| `fulfillment.dispatch.sector` | `string` | Condicional | Setor/área operacional |
| `fulfillment.dispatch.seat.id` | `string` | Condicional | Identificador do assento/posição |
| `fulfillment.dispatch.seat.label` | `string` | Condicional | Nome amigável do assento/posição |
| `service.waiterCode` | `string` | Não | Código do atendente/garçom |
| `service.waiterName` | `string` | Não | Nome do atendente/garçom |
| `service.peopleCount` | `integer` | Não | Número de pessoas na sessão |
| `notifications.whatsAppId` | `string` | Não | Identificador de WhatsApp para notificações |
| `fiscal.shouldIssueDocument` | `boolean` | Condicional | Se deve emitir documento fiscal |
| `fiscal.documentStatus` | `string` | Não | Estado fiscal conhecido: `NOT_ISSUED`, `ISSUED`, `PENDING` |
| `fiscal.printDocument` | `boolean` | Não | Se deve imprimir documento |
| `fiscal.paymentNSURequiredForNFCE` | `boolean` | Não | Se NSU de pagamento é exigido para NFC-e |

### Como a conta nasce

A conta **não é criada por nenhum endpoint desta spec**. Ela nasce automaticamente no Software Service quando o protocolo de Orders processa um pedido com `fulfillment.orderType: INDOOR` (entrada via evento `CREATED` e snapshot em `GET /orders/{id}` — **sem `POST /orders`**) para uma chave operacional que ainda não tem conta aberta — seja esse pedido originado por um garçom, um totem ou um QR Code. A partir daí, novos pedidos INDOOR para a mesma chave **acumulam itens** na conta existente, independente do canal de origem de cada um.

### Status da conta

```mermaid
stateDiagram-v2
 direction LR
 [*] --> IN_USE: 1º pedido INDOOR
 IN_USE --> IN_PAYMENT: pré-fechamento
 IN_PAYMENT --> IN_USE: desbloqueio
 IN_PAYMENT --> CLOSED: fechamento
 CLOSED --> [*]
```

| Status | Significado |
|---|---|
| `IN_USE` | Conta aberta, aceitando novos itens. Pagamentos também podem ser registrados aqui. |
| `IN_PAYMENT` | Conta pré-fechada/bloqueada — não aceita novos itens, mas continua aceitando pagamentos, aguardando o fechamento. |
| `CLOSED` | Conta fechada definitivamente. Nenhuma operação adicional é aceita. |

### Pagamentos e fechamento

Este é o ponto que mais gera confusão em integrações Indoor, então vale destacar com cuidado:

**Pagamento não depende de pré-fechamento.** `POST /accounts/payments` pode ser chamado a qualquer momento — com a conta `IN_USE` ou já `IN_PAYMENT`. Não é preciso esperar o pré-fechamento para registrar um pagamento parcial: muitos estabelecimentos recebem pagamentos ao longo da sessão (ex.: o cliente paga uma rodada de bebidas no meio do consumo).

**Pré-fechamento é um lock, não um gatilho de pagamento.** `POST /accounts/pre-close` bloqueia novos itens, sinalizando que a conta está pronta para o checkout final. É o momento em que se espera o **último pagamento** — o saldo restante, se já houve pagamentos anteriores, ou o valor total, se nenhum pagamento foi feito até então.

**Fechamento é definitivo.** `POST /accounts/close` só deve ser chamado quando o total pago cobrir o valor da conta. Após o fechamento, **nenhuma operação adicional é aceita** — incluindo novos pagamentos.

| Operação | `IN_USE` | `IN_PAYMENT` |
|---|---|---|
| Adicionar itens (via Orders) | ✅ | ❌ |
| Cancelar item | ✅ | ❌ |
| Transferir itens | ✅ | ❌ |
| **Registrar pagamento** (`POST /accounts/payments`) | ✅ | ✅ |
| Pré-fechar (`pre-close`) | ✅ | — |
| Desbloquear (`unlock`) | — | ✅ |
| Fechar (`close`) | ❌ | ✅ |

Pagamento é, propositalmente, a única operação válida nos dois estados — é o que permite cobrar o cliente sem travar o resto da operação da conta.

### Eventos

A cada transição relevante, o Software Service **DEVE** notificar a Ordering Application via webhook. Não há polling para eventos Indoor: a entrega é **exclusivamente via webhook**, e a Ordering Application deve implementar um endpoint compatível com o contrato `accountEvent` da spec para recebê-los.

#### Matriz de eventos da conta {#matriz-de-eventos-da-conta}

<div class="od-matrix__legend">
 <span><span class="od-badge od-badge--must">MUST</span> emitir no fluxo core</span>
 <span><span class="od-badge od-badge--may">MAY</span> conforme cenário</span>
 <span>Status da conta após o evento (quando aplicável)</span>
</div>

<div class="od-matrix" markdown>

<div class="od-matrix__scroll" markdown>

| Evento | Gatilho | Obrigatoriedade | Status da conta | Observações |
|---|---|---|---|---|
| `ACCOUNT_OPENED` | Conta criada (pedido INDOOR) | <span class="od-badge od-badge--must">MUST</span> | `IN_USE` | Abertura da sessão de salão |
| `ACCOUNT_ITEM_ADDED` | Novo pedido INDOOR adiciona itens | <span class="od-badge od-badge--must">MUST</span> | `IN_USE` | Pedido é canal de itens |
| `ACCOUNT_ITEM_REMOVED` | Itens transferidos para outra conta | <span class="od-badge od-badge--may">MAY</span> | `IN_USE` | Transferência entre mesas/comandas |
| `ACCOUNT_ITEM_CANCELLED` | Item cancelado | <span class="od-badge od-badge--must">MUST</span> | `IN_USE` | Cancelamento de item, não da conta |
| `PAYMENT_CREATED` | Pagamento lançado | <span class="od-badge od-badge--must">MUST</span> | — | Válido em `IN_USE` e `IN_PAYMENT` |
| `PAYMENT_UPDATED` | Ajuste interno de um pagamento já criado | <span class="od-badge od-badge--may">MAY</span> | — | Conciliação; omitível se não houver update pós-create |
| `ACCOUNT_PRE_CLOSED` | Conta bloqueada para pagamento | <span class="od-badge od-badge--must">MUST</span> | `IN_PAYMENT` | Lock — sem novos itens |
| `ACCOUNT_UNLOCKED` | Bloqueio revertido | <span class="od-badge od-badge--may">MAY</span> | `IN_USE` | Reabre para novos itens |
| `FISCAL_ISSUED` | Documento fiscal emitido | <span class="od-badge od-badge--must">MUST</span> | — | Se fiscal solicitado; assíncrono; GET como fallback |
| `FISCAL_ERROR` | Falha na emissão fiscal | <span class="od-badge od-badge--must">MUST</span> | — | Se fiscal solicitado e falhar; conta pode fechar mesmo assim |
| `ACCOUNT_CLOSED` | Conta fechada definitivamente | <span class="od-badge od-badge--must">MUST</span> | `CLOSED` | Irreversível |

</div>
</div>

!!! tip "Pedidos Indoor vs conta"
    O ciclo de vida do **pedido** INDOOR (CREATED → CONFIRMED → …) está na [matriz Orders — perfil INDOOR](orders.md#perfil-indoor). A matriz acima é só da **conta** (Account).

!!! note "Payloads de webhook e exemplos JSON"
    Exemplos de cada `EventType` e do contrato `EventNotification` estão na especificação da API, operação [`receiveAccountEvent`](../reference/indoor.md) — não são duplicados aqui para evitar drift.

---

## Fora do MVP (V2.1+)

O comitê Salão/Indoor debateu e **deixou de fora** desta release candidate:

| Tema | Status |
|---|---|
| Reservas de mesa e fila de espera | Pós-V2 (possível V2.1) |
| Endpoint de “chamar garçom” | Avaliado; não normativo nesta RC |
| Histórico estruturado de transferências (`TransferHistoryEntry`) | Em debate; use `reason` no `TransferRequest` |
| Polling de eventos de conta (`GET /events`) | Comentado na spec; entrega é **webhook-only** |
| Timeout automático de lock / pré-close por origem | Em avaliação operacional |

Não espere esses comportamentos de uma implementação conforme V2.0.0-rc.

---

## Fluxos

Os fluxos abaixo mostram a sequência de chamadas entre a Ordering Application e o Software Service, e os eventos emitidos em cada passo.

### Fluxo normal

Ciclo completo de uma sessão de salão: abertura via pedido INDOOR, adição de itens, pré-fechamento, pagamento, emissão fiscal e fechamento.

```mermaid
sequenceDiagram
 participant OA as Ordering Application
 participant SS as Software Service

 Note over OA,SS: Abertura — pedido entra via Orders (sem POST /orders)
 OA->>SS: evento CREATED type=INDOOR (webhook ou polling)
 SS->>OA: GET /orders/{orderId}
 OA-->>SS: Order type=INDOOR
 SS-)OA: event: ACCOUNT_OPENED — status: IN_USE

 Note over OA,SS: Adição de itens — novo pedido INDOOR
 OA->>SS: evento CREATED (novo orderId)
 SS->>OA: GET /orders/{orderId}
 SS-)OA: event: ACCOUNT_ITEM_ADDED

 opt Pagamento antecipado (opcional, a qualquer momento em IN_USE)
 OA->>SS: POST /accounts/{id}/payments
 SS-->>OA: 200 OK
 SS-)OA: event: PAYMENT_CREATED
 end

 Note over OA,SS: Pré-fechamento — lock para checkout
 OA->>SS: POST /accounts/{id}/pre-close
 SS-->>OA: 202 Accepted
 SS-)OA: event: ACCOUNT_PRE_CLOSED — status: IN_PAYMENT

 Note over OA,SS: Quitação final
 OA->>SS: POST /accounts/{id}/payments
 SS-->>OA: 200 OK
 SS-)OA: event: PAYMENT_CREATED

 Note over OA,SS: Emissão fiscal
 OA->>SS: POST /accounts/{id}/fiscal
 SS-->>OA: 202 Accepted
 SS-)OA: event: FISCAL_ISSUED (assíncrono)

 Note over OA,SS: Fechamento
 OA->>SS: POST /accounts/{id}/close
 SS-->>OA: 202 Accepted
 SS-)OA: event: ACCOUNT_CLOSED — status: CLOSED
```

### Desbloqueio (unlock)

A Ordering Application pode reverter um pré-fechamento, devolvendo a conta ao estado `IN_USE` para continuar adicionando itens.

```mermaid
sequenceDiagram
 participant OA as Ordering Application
 participant SS as Software Service

 OA->>SS: POST /accounts/{id}/pre-close
 SS-->>OA: 202 Accepted
 SS-)OA: event: ACCOUNT_PRE_CLOSED — status: IN_PAYMENT

 Note over OA,SS: Operador decide adicionar mais itens
 OA->>SS: POST /accounts/{id}/unlock
 SS-->>OA: 202 Accepted
 SS-)OA: event: ACCOUNT_UNLOCKED — status: IN_USE

 OA->>SS: evento CREATED (novo pedido INDOOR)
 SS->>OA: GET /orders/{orderId}
 SS-)OA: event: ACCOUNT_ITEM_ADDED
```

### Pagamentos parciais

Uma conta pode receber múltiplos pagamentos ao longo de toda a sua vida útil, não apenas após o pré-fechamento — inclusive intercalados com a inclusão de novos itens, já que pagamento e itens não competem pelo mesmo lock. O exemplo abaixo mostra um pagamento parcial registrado ainda em `IN_USE` (ex.: o cliente paga uma rodada de bebidas no meio do consumo), seguido da inclusão de mais itens, e só então o pré-fechamento e a quitação final.

```mermaid
sequenceDiagram
 participant OA as Ordering Application
 participant SS as Software Service

 Note over OA,SS: Pagamento parcial — ex.: cartão de crédito, conta ainda em uso
 OA->>SS: POST /accounts/{id}/payments
 SS-->>OA: 200 OK
 SS-)OA: event: PAYMENT_CREATED (valor parcial)

 Note over OA,SS: Conta continua aberta — novos itens são adicionados normalmente
 OA->>SS: evento CREATED (novo pedido INDOOR)
 SS->>OA: GET /orders/{orderId}
 SS-)OA: event: ACCOUNT_ITEM_ADDED

 OA->>SS: POST /accounts/{id}/pre-close
 SS-->>OA: 202 Accepted
 SS-)OA: event: ACCOUNT_PRE_CLOSED — status: IN_PAYMENT

 Note over OA,SS: Quitação final — ex.: dinheiro (saldo restante)
 OA->>SS: POST /accounts/{id}/payments
 SS-->>OA: 200 OK
 SS-)OA: event: PAYMENT_CREATED (saldo quitado)

 OA->>SS: POST /accounts/{id}/close
 SS-->>OA: 202 Accepted
 SS-)OA: event: ACCOUNT_CLOSED — status: CLOSED
```

### Emissão fiscal

A emissão é **assíncrona** — o Software Service retorna `202 Accepted` e emite o evento quando o documento fica disponível. A conta pode ser fechada mesmo sem emissão bem-sucedida.

```mermaid
sequenceDiagram
 participant OA as Ordering Application
 participant SS as Software Service

 OA->>SS: POST /accounts/{id}/fiscal
 SS-->>OA: 202 Accepted

 alt Emissão bem-sucedida
 SS-)OA: event: FISCAL_ISSUED
 OA->>SS: GET /accounts/{id}/fiscal
 SS-->>OA: 200 OK (documento disponível)
 else Falha na emissão
 SS-)OA: event: FISCAL_ERROR
 Note over OA: Operador registra falha
 end

 Note over OA,SS: Conta pode ser fechada independente do resultado fiscal
 OA->>SS: POST /accounts/{id}/close
 SS-->>OA: 202 Accepted
 SS-)OA: event: ACCOUNT_CLOSED — status: CLOSED
```

### Cancelamento de item

Cancela um item específico dentro de uma conta `IN_USE`. A conta permanece aberta e os demais itens não são afetados.

```mermaid
sequenceDiagram
 participant OA as Ordering Application
 participant SS as Software Service

 Note over OA,SS: Item já adicionado à conta via pedido INDOOR
 OA->>SS: POST /accounts/items/{itemId}/cancel
 SS-->>OA: 200 OK
 SS-)OA: event: ACCOUNT_ITEM_CANCELLED

 Note over OA,SS: Conta permanece IN_USE — demais itens inalterados
```

### Transferência entre contas

Move itens de uma conta para outra — ex.: mesa muda de lugar, grupos se separam, ou um pedido de balcão é remanejado para uma comanda. Ambas as contas devem estar `IN_USE`.

```mermaid
sequenceDiagram
 participant OA as Ordering Application
 participant SS as Software Service

 Note over OA,SS: Conta A (origem) e Conta B (destino) estão IN_USE

 OA->>SS: POST /accounts/transfers
 Note over OA,SS: body: targetAccountId + lista de itens
 SS-->>OA: 200 OK
 SS-)OA: event: ACCOUNT_ITEM_REMOVED — Conta A (origem)
 SS-)OA: event: ACCOUNT_ITEM_ADDED — Conta B (destino)

 Note over OA,SS: Ambas as contas permanecem IN_USE
```

---

## Implementando o Software Service

Se você hospeda os endpoints e gerencia as contas, atente para:

**Abra a conta na recepção do primeiro pedido INDOOR.** Quando o protocolo de Orders processar um pedido `fulfillment.orderType: INDOOR` (evento `CREATED` + GET — sem `POST /orders`) para uma chave operacional sem conta ativa, crie a conta e emita `ACCOUNT_OPENED`. Pedidos seguintes para a mesma chave acumulam itens (`ACCOUNT_ITEM_ADDED`) em vez de abrir uma conta nova.

**Emita um evento para cada transição.** Toda mudança de estado relevante precisa gerar o evento correspondente, notificado via webhook (`accountEvent`). A Ordering Application depende exclusivamente desses eventos para se sincronizar — uma transição sem evento é uma transição invisível. Não há fallback de polling: se o webhook falhar, use o campo `lastEvent` da conta para reconciliar o estado.

**Trate o pré-fechamento como um bloqueio real — mas só para itens.** Uma conta `IN_PAYMENT` não deve aceitar novos itens. Se o operador precisar adicionar algo, exija o `unlock` explícito (`ACCOUNT_UNLOCKED`, volta a `IN_USE`). **Pagamento não entra nesse bloqueio**: `POST /accounts/{id}/payments` deve continuar sendo aceito tanto em `IN_USE` quanto em `IN_PAYMENT`, a qualquer momento — não exija pré-fechamento como condição para registrar um pagamento.

**Valide o pagamento antes de fechar, não antes de pagar.** Acumule os `PAYMENT_CREATED` ao longo de toda a vida da conta e só aceite `POST /accounts/{id}/close` quando o total quitado cobrir o valor da conta — salvo regras de negócio próprias (cortesia, desconto). Após o fechamento, rejeite qualquer operação adicional, incluindo novos pagamentos: `close` é o único marco realmente irreversível do ciclo de vida.

**Faça a emissão fiscal assíncrona.** Responda `202 Accepted` imediatamente e emita `FISCAL_ISSUED` ou `FISCAL_ERROR` quando o resultado estiver disponível. Não bloqueie o fechamento da conta esperando a SEFAZ.

**Mantenha os totais consistentes.** Cancelamentos, transferências e novos pedidos precisam refletir imediatamente em `totals`, já que a Ordering Application exibe esse valor ao cliente.

---

## Implementando a Ordering Application

Se você consome os endpoints e exibe a conta ao operador ou cliente, atente para:

**Localize a conta pela chave operacional.** Use `GET /accounts?operationMode=...&identifier=...` como forma primária de acesso. Só use `GET /accounts/{accountId}` quando já tiver o `accountId` retornado anteriormente.

**Receba eventos via webhook.** O Indoor não tem polling: implemente o endpoint de webhook (conforme o contrato `accountEvent` da spec) para receber `ACCOUNT_ITEM_ADDED`, `PAYMENT_CREATED`, `FISCAL_ISSUED` etc. em tempo real e atualizar a tela. Use o `lastEvent` da conta para reconciliar o estado caso suspeite de entrega perdida.

**Não espere o pré-fechamento para lançar um pagamento.** `POST /accounts/{id}/payments` funciona com a conta `IN_USE` ou `IN_PAYMENT` — use-o sempre que o cliente quiser pagar, mesmo no meio do consumo. Reserve o `pre-close` para o momento em que a conta deve parar de aceitar novos itens.

**Não assuma fechamento imediato após o pagamento.** Pagamento e fechamento são passos distintos. Lance os pagamentos com `POST /accounts/{id}/payments` e só então chame `POST /accounts/{id}/close` — tipicamente após o `pre-close`, quando o saldo restante (ou total, se nenhum pagamento anterior existiu) é quitado.

**Trate a emissão fiscal como assíncrona.** Após `202 Accepted`, aguarde o evento `FISCAL_ISSUED` (ou `FISCAL_ERROR`) — não espere o documento na resposta da requisição. Consulte `GET /accounts/{id}/fiscal` quando o evento chegar.

**Reflita cancelamentos e transferências na hora.** Ao receber `ACCOUNT_ITEM_CANCELLED` ou `ACCOUNT_ITEM_REMOVED`/`ACCOUNT_ITEM_ADDED`, atualize a conta exibida — o cliente não pode ver itens que já saíram da conta.

---

!!! tip "Checklist — Software Service"
    - Conta criada e `ACCOUNT_OPENED` emitido na recepção do 1º pedido INDOOR.
    - Todas as transições de estado emitem o evento correspondente.
    - Conta `IN_PAYMENT` rejeita novos itens até o `unlock`.
    - Pagamento (`POST /accounts/payments`) é aceito em `IN_USE` **e** `IN_PAYMENT`, sem depender de pré-fechamento.
    - Total quitado é validado antes de aceitar o fechamento.
    - Após `close`, toda operação adicional é rejeitada — incluindo novos pagamentos.
    - Emissão fiscal responde `202` e emite `FISCAL_ISSUED` / `FISCAL_ERROR` depois.
    - `totals` refletem cancelamentos e transferências imediatamente.

!!! tip "Checklist — Ordering Application"
    - Conta localizada pela chave operacional (`operationMode` + `identifier`).
    - Endpoint de webhook implementado e registrado para receber eventos (sem polling).
    - Pagamentos podem ser lançados a qualquer momento (`IN_USE` ou `IN_PAYMENT`), não só após o pré-fechamento.
    - Pagamento e fechamento tratados como passos separados.
    - Emissão fiscal tratada como assíncrona (aguarda o evento).
    - Cancelamentos e transferências refletidos na interface em tempo real.

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="../reference/indoor.md">Especificação de Indoor</a> — conta, pagamentos, fiscal</li>
    <li><a href="../reference/orders.md">Especificação de Orders</a> — pré-requisito</li>
    <li><a href="orders.md">Orders</a> — guia do domínio</li>
    <li><a href="discovery.md">Discovery</a></li>
  </ul>
</div>
