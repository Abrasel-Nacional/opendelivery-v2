# Trilhas por papel

O Open Delivery não exige que você implemente tudo. Cada sistema assume um (ou mais) **papéis** no ecossistema e declara no [Discovery](../protocol/discovery.md) o que suporta.

Use esta página para montar um caminho de leitura e implementação alinhado ao seu produto.

---

## Mapa rápido

| Papel | Quem é | Capabilities típicas | Comece por |
|---|---|---|---|
| **Originador** | App de pedidos, marketplace, totem | Orders, Merchant (consumo), Auth, Discovery | [Trilha Originador](#originador) |
| **Software Service (PDV)** | Gestão do restaurante / POS | Merchant, Orders, Indoor, Auth, Discovery | [Trilha PDV](#pdv) |
| **Logística** | Operador de entrega, frota | Logistics (+ Orders contexto), Auth, Discovery | [Trilha Logística](#logistica) |
| **CRM / Loyalty** | CRM, fidelidade, reviews | Customer, Reviews, Loyalty, Auth, Discovery | [Trilha CRM](#crm) |

Um mesmo produto pode combinar papéis (ex.: marketplace com frota própria = Originador + Logística).

---

## Originador {#originador}

Você **cria pedidos** e, em muitos fluxos, é dono do **Merchant ID** e do cardápio exibido ao consumidor.

### O que implementar

1. [Discovery](../protocol/discovery.md) — manifesto well-known
2. [Autenticação](../protocol/authentication.md) — OAuth por aplicação
3. [Merchant](../protocol/merchant.md) + [Menu](../protocol/menu.md) — identidade, services e catálogo
4. [Orders](../protocol/orders.md) — criar pedidos, cancelar, consumir eventos/status
5. Opcional: [Logistics](../protocol/logistics.md), [Customer](../protocol/customer.md) (push de clientes), [Indoor](../protocol/indoor.md) (totem/QR)

### Leituras

| Tipo | Link |
|---|---|
| Guia | [Primeiros Passos](getting-started.md) |
| Protocolo | [Orders](../protocol/orders.md) · [Merchant](../protocol/merchant.md) · [Menu](../protocol/menu.md) |
| API | [Referência Orders](../reference/orders.md) · [Merchant](../reference/merchant.md) |
| Migração | [V1→V2](migration-v1-v2.md) |

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo — Originador</div>
  <div class="od-next-step__links">
    <a href="../protocol/discovery/">Publicar Discovery</a>
    <a href="../reference/orders/">OpenAPI Orders</a>
  </div>
</div>

---

## Software Service (PDV) {#pdv}

Você é a **fonte operacional** da loja: confirma pedidos, envia cardápio, é autoridade da **conta Indoor** e, em muitos casos, da emissão fiscal.

### O que implementar

1. [Discovery](../protocol/discovery.md) + [Auth](../protocol/authentication.md)
2. [Merchant](../protocol/merchant.md) + [Menu](../protocol/menu.md) — services, pause, CRUD/snapshot de catálogo
3. [Orders](../protocol/orders.md) — confirmação, preparo, eventos, cancelamento V2
4. [Indoor](../protocol/indoor.md) — se houver salão (Account, pagamentos, fiscal)
5. Webhooks de eventos (e/ou polling onde o manifesto declarar)

### Leituras

| Tipo | Link |
|---|---|
| Protocolo | [Merchant](../protocol/merchant.md) · [Menu](../protocol/menu.md) · [Orders](../protocol/orders.md) · [Indoor](../protocol/indoor.md) |
| API | [Merchant](../reference/merchant.md) · [Orders](../reference/orders.md) · [Indoor](../reference/indoor.md) |
| Matrizes | [Eventos por perfil (Orders)](../protocol/orders.md#matrizes-de-eventos-por-perfil) |

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo — PDV</div>
  <div class="od-next-step__links">
    <a href="../protocol/merchant/">Protocolo Merchant</a>
    <a href="../reference/merchant/">OpenAPI Merchant</a>
  </div>
</div>

---

## Logística {#logistica}

Você executa ou orquestra a **entrega** e emite eventos de tracking informativos (sem confundir com o status do pedido).

### O que implementar

1. [Discovery](../protocol/discovery.md) + [Auth](../protocol/authentication.md)
2. [Logistics](../protocol/logistics.md) — cotação, despacho, tracking, problemas
3. Integração com contexto de [Orders](../protocol/orders.md) (eventos logísticos vs status)

### Leituras

| Tipo | Link |
|---|---|
| Protocolo | [Logistics](../protocol/logistics.md) · [Orders — status × eventos](../protocol/orders.md#ciclo-de-vida-status) |
| API | [Logistics](../reference/logistics.md) |

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo — Logística</div>
  <div class="od-next-step__links">
    <a href="../protocol/logistics/">Protocolo Logistics</a>
    <a href="../reference/logistics/">OpenAPI Logistics</a>
  </div>
</div>

---

## CRM / Loyalty / Reviews {#crm}

Você cuida do **relacionamento**: cliente, leads, avaliações e programas de fidelidade. Não altera o ciclo operacional do pedido na cozinha.

### O que implementar

1. [Discovery](../protocol/discovery.md) + [Auth](../protocol/authentication.md) (escopo `od.crm`)
2. [Customer](../protocol/customer.md) — capability base (obrigatória para as extensões)
3. Extensões opcionais:
   - [Reviews](../extensions/reviews.md)
   - [Loyalty](../extensions/loyalty.md)

### Leituras

| Tipo | Link |
|---|---|
| Protocolo | [Customer](../protocol/customer.md) · [Reviews](../extensions/reviews.md) · [Loyalty](../extensions/loyalty.md) |
| API | [Customer & Fidelidade](../reference/customer.md) |

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo — CRM</div>
  <div class="od-next-step__links">
    <a href="../protocol/customer/">Protocolo Customer</a>
    <a href="../reference/customer/">OpenAPI Customer</a>
  </div>
</div>

---

## Indoor (quando o salão é o produto)

Se o seu produto é **totem, QR de mesa, tablet de garçom ou PDV de salão**, trate Indoor como trilha principal — mas lembre: é **extensão de Orders**.

| Papel no Indoor | Responsabilidade |
|---|---|
| **Software Service** | Hospeda Account, pagamentos, fiscal, eventos |
| **Ordering Application** | Envia pedidos INDOOR, consome webhooks, UI de conta |

→ [Protocolo Indoor](../protocol/indoor.md) · [OpenAPI Indoor](../reference/indoor.md) · [Matriz de eventos de conta](../protocol/indoor.md#matriz-de-eventos-da-conta)

---

## Checklist comum a todos os papéis

1. Publicar `GET /.well-known/opendelivery`
2. Obter token OAuth (preferência: por aplicação)
3. Listar merchants autorizados (`GET /merchants` quando aplicável)
4. Implementar só as capabilities declaradas no manifesto
5. Separar **status** (verdade no GET) de **eventos** (notificações)

Para o fluxo mínimo genérico, veja [Primeiros Passos](getting-started.md).
