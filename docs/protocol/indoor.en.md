# Indoor / Table Service

<p class="od-meta">
  <span class="od-badge od-badge--ext">Extension</span>
  <span class="od-badge od-badge--code">indoor</span>
  <span class="od-badge">parent: Orders</span>
  <span class="od-badge od-badge--new">New in V2</span>
</p>

<div class="od-api-callout">
  <p><strong>Helper guide</strong> — concepts, roles, and flows. The full normative contract (fields, endpoints, errors, and JSON examples) lives in the OpenAPI; an experienced implementer can integrate from the spec alone.</p>
  <a href="../reference/indoor/">Implement with Indoor OpenAPI →</a>
</div>

The **Indoor** capability standardizes on-premise consumption — table, tab, and counter — covering both waiter-mediated service and **full self-service** via totem, QR Code, or tablet. It covers the full dining session: grouping orders into an **account**, registering payments (including partial ones), issuing fiscal documents, and closing the account — kept in sync between the restaurant management system and the ordering application.

This page is a **reading guide**: what the capability is, the concepts you need, interaction flows, and per-role checklists. **Fields, schemas, error codes, and payload examples** live in the [Indoor OpenAPI](../reference/indoor.md) (ReDoc) — the normative, self-contained source.

| Layer | What it contains | When to use it |
|---|---|---|
| **This guide** | Business view, roles, Mermaid flows, checklists | You are learning the domain or building the integration for the first time |
| **[Indoor OpenAPI](../reference/indoor.md)** | Endpoints, fields, MUST/MAY, errors, JSON examples | You are coding or validating the HTTP contract |

!!! note "Language"
    OpenAPI contracts are **always English**. Protocol guides are bilingual (this EN page + the PT default).

---

## What it is for

In traditional delivery, an order is born and ends as an isolated unit: created, prepared, delivered, closed. On the floor the reality is different. An account opens — at a table, on a tab, or at a self-service counter — and receives **several orders over time**, possibly from different channels (waiter tablet, customer QR Code, totem). Items are cancelled or transferred to another account, the total is split, paid in parts, and only then is the account closed with fiscal issuance.

Without a standard, every POS–floor-app integration had to bilaterally negotiate how to represent that accumulation: where the total lives, how to cancel an item without cancelling the whole order, when to issue the invoice, how to handle partial payment. Indoor removes that negotiation by defining the **account** as the central entity and a fixed set of operations and events on it.

---

## Prerequisite: Orders protocol

!!! warning "Indoor is an Orders extension, not a standalone capability"
    Both parties **MUST** implement the **Orders** protocol before Indoor. The **dining account is opened from an order**: when Orders processes a `orderType: INDOOR` order for an operational key with no open account, the Software Service creates the account. Later INDOOR orders on the same key only accumulate items.

    Order **lifecycle and order-event** details live only in Orders — they are not redefined here. Implementations without active Orders **MUST NOT** use this capability.

    - Guide: [Orders](orders.md)
    - Contract: [Orders OpenAPI](../reference/orders.md)

The order is the **channel that brings items in**; the account is the **operational aggregator** of those orders for payment, close, and fiscal integration.

---

## The two sides of the integration

| Role | Responsibility |
|---|---|
| **Software Service** | Restaurant management system. **Hosts and implements** all endpoints in this spec and **emits** account lifecycle events. |
| **Ordering Application** | Ordering surface (totem, waiter tablet, customer app, front desk). **Consumes** endpoints and **receives** events via webhook to stay in sync. |

In every operation of this capability the Software Service is the server and the Ordering Application is the client.

---

## Discovery

Participants that expose Indoor **MUST** declare the extension in the well-known manifest (`GET /.well-known/opendelivery`), under the parent **Orders** capability (or as defined by the Discovery binding of the implementation).

Typical Indoor declaration fields in Discovery (normative detail in [Discovery OpenAPI](../reference/discovery.md)):

| Field | Meaning |
|---|---|
| `invoiceIssuer` | Who issues the fiscal document (`pos` / `app` / `platform`) |
| `invoiceIssueMoment` | When it is issued (`account_closing`, `item_addition`, `payment`) |
| `usesAccountId` | Whether the participant tracks sessions with `accountId` |

```json
"capabilities": {
  "orders": {
    "endpoint": "https://api.example.com/od/v2"
  },
  "indoor": {
    "endpoint": "https://api.example.com/od/v2",
    "invoiceIssuer": "pos",
    "invoiceIssueMoment": "account_closing",
    "usesAccountId": true
  }
}
```

General guide: [Discovery](discovery.md). Contract: [Discovery OpenAPI](../reference/discovery.md).

---

## Map: goal → OpenAPI operation

Use this table to go from business flow to HTTP contract. All links open the [Indoor OpenAPI reference](../reference/indoor.md).

| Goal | Operation | Spec |
|---|---|---|
| Open account / add items | `POST /orders` with `orderType: INDOOR` | [Orders](../reference/orders.md) (prerequisite) |
| Query account (table/tab) | `GET /accounts?operationMode&identifier` | `getAccount` |
| Query account by ID | `GET /accounts/{accountId}` | `getAccountById` |
| Pre-close (lock) | `POST /accounts/pre-close` | `preCloseAccount` |
| Unlock | `POST /accounts/unlock` | `unlockAccount` |
| Close account | `POST /accounts/close` | `closeAccount` |
| Cancel item | `POST /accounts/items/{itemId}/cancel` | `cancelAccountItem` |
| Transfer items/account | `POST /accounts/transfers` | `transferAccountContent` |
| Post payment | `POST /accounts/payments` | `createPayment` |
| List payments | `GET /accounts/payments` | `listAccountPayments` |
| Request fiscal | `POST /accounts/fiscal` | `requestFiscalDocument` |
| List fiscal documents | `GET /accounts/fiscal` | `listAccountFiscalDocuments` |
| Receive events | Webhook `accountEvent` | `receiveAccountEvent` |

---

## Key concepts

### The account (Account)

The **account** aggregates all orders, items, payments, and fiscal documents of a consumption session. Each account is located by an **operational key** — the pair `operationMode` + `identifier`:

| `operationMode` | Meaning | Example `identifier` |
|---|---|---|
| `TABLE` | Table service | `"5"` (table 5) |
| `TAB` | Tab service | `"A-102"` |
| `COUNTER` | Counter consumption | `"3"` (position 3) |

Besides the operational key, the account may have an internal POS `accountId`. Primary lookup uses the operational key (`GET /accounts?operationMode=TABLE&identifier=5`); when `accountId` is already known, use `GET /accounts/{accountId}`. The account always carries `lastEvent` with the **type** of the last emitted event (e.g. `ACCOUNT_ITEM_ADDED`) — useful for sync and debugging when webhook delivery is uncertain (e.g. after reconnection).

### Origin channels (originChannel)

`operationMode` defines how the account is **grouped** — not where the order **entered**. That is `originChannel`, present on each order, and this is where Indoor makes clear it does not assume waiter-mediated service only:

| `originChannel.type` | Description |
|---|---|
| `TOTEM` | Self-service on a physical totem in the venue. |
| `QR_CODE` | Customer scans a QR Code on the table/tab and orders on their phone. |
| `CUSTOMER_TABLET` | Tablet handed to the customer to order directly. |
| `WAITER_TABLET` | Tablet used by the waiter/attendant to place the order. |
| `FRONT_DESK` | Order placed at the front desk. |
| `POS` | Order originated directly on the POS. |
| `APP` | Venue or third-party ordering app. |
| `WHATSAPP` | Order received via WhatsApp. |
| `OTHER` | Any other unlisted channel. |

`operationMode` and `originChannel` are independent: the same account may accumulate orders from **different channels** during the session. For example, the customer opens the account via QR Code (`originChannel: QR_CODE`) and later the waiter posts an extra item on a tablet (`originChannel: WAITER_TABLET`) — both land on the same account because they share the operational key. The channel is order metadata only; it does not define account identity.

### How the account is born

The account is **not created by any endpoint in this spec**. It is created automatically in the Software Service when Orders processes an order with `orderType: INDOOR` for an operational key that has no open account — whether that order comes from a waiter, a totem, or a QR Code. From then on, new INDOOR orders for the same key **accumulate items** on the existing account, regardless of each order’s origin channel.

### Account status

```mermaid
stateDiagram-v2
    direction LR
    [*] --> IN_USE : 1st INDOOR order
    IN_USE --> IN_PAYMENT : pre-close
    IN_PAYMENT --> IN_USE : unlock
    IN_PAYMENT --> CLOSED : close
    CLOSED --> [*]
```

| Status | Meaning |
|---|---|
| `IN_USE` | Account open, accepting new items. Payments may also be posted here. |
| `IN_PAYMENT` | Account pre-closed/locked — no new items, but still accepts payments, awaiting close. |
| `CLOSED` | Account permanently closed. No further operations are accepted. |

### Payments and closing

This is the area that most often confuses Indoor integrations, so it is worth highlighting carefully:

**Payment does not depend on pre-close.** `POST /accounts/payments` may be called at any time — while the account is `IN_USE` or already `IN_PAYMENT`. You do not need to wait for pre-close to register a partial payment: many venues take payments throughout the session (e.g. the customer pays a round of drinks mid-meal).

**Pre-close is a lock, not a payment trigger.** `POST /accounts/pre-close` blocks new items, signalling the account is ready for final checkout. That is when the **last payment** is expected — remaining balance if earlier payments exist, or the full amount if none yet.

**Close is final.** `POST /accounts/close` should only be called when paid total covers the account amount. After close, **no further operations are accepted** — including new payments.

| Operation | `IN_USE` | `IN_PAYMENT` |
|---|---|---|
| Add items (via Orders) | ✅ | ❌ |
| Cancel item | ✅ | ❌ |
| Transfer items | ✅ | ❌ |
| **Post payment** (`POST /accounts/payments`) | ✅ | ✅ |
| Pre-close (`pre-close`) | ✅ | — |
| Unlock (`unlock`) | — | ✅ |
| Close (`close`) | ❌ | ✅ |

Payment is deliberately the only operation valid in both states — it allows charging the customer without locking the rest of account operations.

### Events

On every relevant transition, the Software Service **MUST** notify the Ordering Application via webhook. There is no polling for Indoor events: delivery is **webhook-only**, and the Ordering Application must implement an endpoint compatible with the `accountEvent` contract in the spec.

#### Account event matrix {#matriz-de-eventos-da-conta}

<div class="od-matrix__legend">
  <span><span class="od-badge od-badge--must">MUST</span> emit in the core flow</span>
  <span><span class="od-badge od-badge--may">MAY</span> depending on scenario</span>
  <span>Account status after the event (when applicable)</span>
</div>

<div class="od-matrix" markdown>

<div class="od-matrix__scroll" markdown>

| Event | Trigger | Obligation | Account status | Notes |
|---|---|---|---|---|
| `ACCOUNT_OPENED` | Account created (INDOOR order) | <span class="od-badge od-badge--must">MUST</span> | `IN_USE` | Dining session opened |
| `ACCOUNT_ITEM_ADDED` | New INDOOR order adds items | <span class="od-badge od-badge--must">MUST</span> | `IN_USE` | Order is the item channel |
| `ACCOUNT_ITEM_REMOVED` | Items transferred to another account | <span class="od-badge od-badge--may">MAY</span> | `IN_USE` | Transfer between tables/tabs |
| `ACCOUNT_ITEM_CANCELLED` | Item cancelled | <span class="od-badge od-badge--must">MUST</span> | `IN_USE` | Item cancel, not account cancel |
| `PAYMENT_CREATED` | Payment posted | <span class="od-badge od-badge--must">MUST</span> | — | Valid in `IN_USE` and `IN_PAYMENT` |
| `PAYMENT_UPDATED` | Internal adjustment of an existing payment | <span class="od-badge od-badge--may">MAY</span> | — | Reconciliation; omit if no post-create update |
| `ACCOUNT_PRE_CLOSED` | Account locked for payment | <span class="od-badge od-badge--must">MUST</span> | `IN_PAYMENT` | Lock — no new items |
| `ACCOUNT_UNLOCKED` | Lock reversed | <span class="od-badge od-badge--may">MAY</span> | `IN_USE` | Reopens for new items |
| `FISCAL_ISSUED` | Fiscal document issued | <span class="od-badge od-badge--must">MUST</span> | — | If fiscal requested; async; GET as fallback |
| `FISCAL_ERROR` | Fiscal issuance failed | <span class="od-badge od-badge--must">MUST</span> | — | If fiscal requested and failed; account may still close |
| `ACCOUNT_CLOSED` | Account closed permanently | <span class="od-badge od-badge--must">MUST</span> | `CLOSED` | Irreversible |

</div>
</div>

!!! tip "Indoor orders vs account"
    The **order** lifecycle for INDOOR (CREATED → CONFIRMED → …) is in the [Orders matrix — INDOOR profile](orders.md#perfil-indoor). The matrix above is only the **account**.

!!! note "Webhook payloads and JSON examples"
    Examples for each `EventType` and the `EventNotification` contract are in the OpenAPI, operation [`receiveAccountEvent`](../reference/indoor.md) — not duplicated here to avoid drift.

---

## Out of MVP (V2.1+)

The Indoor committee discussed and **left out** of this release candidate:

| Topic | Status |
|---|---|
| Table reservations and waitlists | Post-V2 (possible V2.1) |
| “Call waiter” endpoint | Evaluated; not normative in this RC |
| Structured transfer history (`TransferHistoryEntry`) | Under discussion; use `reason` on `TransferRequest` |
| Account event polling (`GET /events`) | Commented in the spec; delivery is **webhook-only** |
| Automatic lock / pre-close timeout by origin | Under operational evaluation |

Do not expect these behaviours from a V2.0.0-rc-compliant implementation.

---

## Flows

The flows below show the call sequence between Ordering Application and Software Service, and the events emitted at each step.

### Happy path

Full dining session: open via INDOOR order, add items, pre-close, payment, fiscal issuance, and close.

```mermaid
sequenceDiagram
    participant OA as Ordering Application
    participant SS as Software Service

    Note over OA,SS: Open
    OA->>SS: POST /orders (orderType: INDOOR)
    SS-->>OA: 201 Created
    SS-)OA: event: ACCOUNT_OPENED — status: IN_USE

    Note over OA,SS: Add items
    OA->>SS: POST /orders (new INDOOR order)
    SS-->>OA: 201 Created
    SS-)OA: event: ACCOUNT_ITEM_ADDED

    opt Early payment (optional, any time in IN_USE)
        OA->>SS: POST /accounts/{id}/payments
        SS-->>OA: 200 OK
        SS-)OA: event: PAYMENT_CREATED
    end

    Note over OA,SS: Pre-close — lock for checkout
    OA->>SS: POST /accounts/{id}/pre-close
    SS-->>OA: 202 Accepted
    SS-)OA: event: ACCOUNT_PRE_CLOSED — status: IN_PAYMENT

    Note over OA,SS: Final settlement
    OA->>SS: POST /accounts/{id}/payments
    SS-->>OA: 200 OK
    SS-)OA: event: PAYMENT_CREATED

    Note over OA,SS: Fiscal issuance
    OA->>SS: POST /accounts/{id}/fiscal
    SS-->>OA: 202 Accepted
    SS-)OA: event: FISCAL_ISSUED (async)

    Note over OA,SS: Close
    OA->>SS: POST /accounts/{id}/close
    SS-->>OA: 202 Accepted
    SS-)OA: event: ACCOUNT_CLOSED — status: CLOSED
```

### Unlock

The Ordering Application may reverse a pre-close, returning the account to `IN_USE` to keep adding items.

```mermaid
sequenceDiagram
    participant OA as Ordering Application
    participant SS as Software Service

    OA->>SS: POST /accounts/{id}/pre-close
    SS-->>OA: 202 Accepted
    SS-)OA: event: ACCOUNT_PRE_CLOSED — status: IN_PAYMENT

    Note over OA,SS: Operator decides to add more items
    OA->>SS: POST /accounts/{id}/unlock
    SS-->>OA: 202 Accepted
    SS-)OA: event: ACCOUNT_UNLOCKED — status: IN_USE

    OA->>SS: POST /orders (new INDOOR order)
    SS-->>OA: 201 Created
    SS-)OA: event: ACCOUNT_ITEM_ADDED
```

### Partial payments

An account may receive multiple payments over its lifetime, not only after pre-close — including interleaved with new items, since payment and items do not compete for the same lock. The example below shows a partial payment while still `IN_USE` (e.g. customer pays a round of drinks mid-session), then more items, then pre-close and final settlement.

```mermaid
sequenceDiagram
    participant OA as Ordering Application
    participant SS as Software Service

    Note over OA,SS: Partial payment — e.g. card, account still in use
    OA->>SS: POST /accounts/{id}/payments
    SS-->>OA: 200 OK
    SS-)OA: event: PAYMENT_CREATED (partial amount)

    Note over OA,SS: Account stays open — new items added normally
    OA->>SS: POST /orders (new INDOOR order)
    SS-->>OA: 201 Created
    SS-)OA: event: ACCOUNT_ITEM_ADDED

    OA->>SS: POST /accounts/{id}/pre-close
    SS-->>OA: 202 Accepted
    SS-)OA: event: ACCOUNT_PRE_CLOSED — status: IN_PAYMENT

    Note over OA,SS: Final settlement — e.g. cash (remaining balance)
    OA->>SS: POST /accounts/{id}/payments
    SS-->>OA: 200 OK
    SS-)OA: event: PAYMENT_CREATED (balance settled)

    OA->>SS: POST /accounts/{id}/close
    SS-->>OA: 202 Accepted
    SS-)OA: event: ACCOUNT_CLOSED — status: CLOSED
```

### Fiscal issuance

Issuance is **asynchronous** — the Software Service returns `202 Accepted` and emits the event when the document is available. The account may be closed even without successful issuance.

```mermaid
sequenceDiagram
    participant OA as Ordering Application
    participant SS as Software Service

    OA->>SS: POST /accounts/{id}/fiscal
    SS-->>OA: 202 Accepted

    alt Successful issuance
        SS-)OA: event: FISCAL_ISSUED
        OA->>SS: GET /accounts/{id}/fiscal
        SS-->>OA: 200 OK (document available)
    else Issuance failure
        SS-)OA: event: FISCAL_ERROR
        Note over OA: Operator records the failure
    end

    Note over OA,SS: Account may close regardless of fiscal outcome
    OA->>SS: POST /accounts/{id}/close
    SS-->>OA: 202 Accepted
    SS-)OA: event: ACCOUNT_CLOSED — status: CLOSED
```

### Item cancellation

Cancels a specific item on an `IN_USE` account. The account stays open; other items are unaffected.

```mermaid
sequenceDiagram
    participant OA as Ordering Application
    participant SS as Software Service

    Note over OA,SS: Item already on the account via INDOOR order
    OA->>SS: POST /accounts/items/{itemId}/cancel
    SS-->>OA: 200 OK
    SS-)OA: event: ACCOUNT_ITEM_CANCELLED

    Note over OA,SS: Account remains IN_USE — other items unchanged
```

### Transfer between accounts

Moves items from one account to another — e.g. table change, groups splitting, or a counter order reassigned to a tab. Both accounts must be `IN_USE`.

```mermaid
sequenceDiagram
    participant OA as Ordering Application
    participant SS as Software Service

    Note over OA,SS: Account A (source) and Account B (target) are IN_USE

    OA->>SS: POST /accounts/transfers
    Note over OA,SS: body: targetAccountId + item list
    SS-->>OA: 200 OK
    SS-)OA: event: ACCOUNT_ITEM_REMOVED — Account A (source)
    SS-)OA: event: ACCOUNT_ITEM_ADDED — Account B (target)

    Note over OA,SS: Both accounts remain IN_USE
```

---

## Implementing the Software Service

If you host the endpoints and manage accounts, pay attention to:

**Open the account on the first INDOOR order.** When Orders processes an `orderType: INDOOR` order for an operational key with no active account, create the account and emit `ACCOUNT_OPENED`. Later orders for the same key accumulate items (`ACCOUNT_ITEM_ADDED`) instead of opening a new account.

**Emit an event for every transition.** Every relevant state change must produce the corresponding event, delivered via webhook (`accountEvent`). The Ordering Application relies exclusively on these events to sync — a transition without an event is an invisible transition. There is no polling fallback: if the webhook fails, use the account’s `lastEvent` field to reconcile state.

**Treat pre-close as a real lock — but only for items.** An `IN_PAYMENT` account must not accept new items. If the operator needs to add something, require an explicit `unlock` (`ACCOUNT_UNLOCKED`, back to `IN_USE`). **Payment is not part of that lock**: `POST /accounts/{id}/payments` must remain accepted in both `IN_USE` and `IN_PAYMENT` at any time — do not require pre-close before posting a payment.

**Validate payment before close, not before pay.** Accumulate `PAYMENT_CREATED` over the whole account life and only accept `POST /accounts/{id}/close` when paid total covers the account amount — unless your own business rules (courtesy, discount). After close, reject any further operation, including new payments: `close` is the only truly irreversible milestone.

**Make fiscal issuance asynchronous.** Respond `202 Accepted` immediately and emit `FISCAL_ISSUED` or `FISCAL_ERROR` when the result is available. Do not block account close waiting on SEFAZ.

**Keep totals consistent.** Cancellations, transfers, and new orders must reflect immediately in `totals`, because the Ordering Application shows that value to the customer.

---

## Implementing the Ordering Application

If you consume the endpoints and display the account to operator or customer, pay attention to:

**Locate the account by operational key.** Use `GET /accounts?operationMode=...&identifier=...` as the primary access path. Only use `GET /accounts/{accountId}` when you already have an `accountId` from a previous response.

**Receive events via webhook.** Indoor has no polling: implement the webhook endpoint (per the `accountEvent` contract in the spec) to receive `ACCOUNT_ITEM_ADDED`, `PAYMENT_CREATED`, `FISCAL_ISSUED`, etc. in real time and update the UI. Use account `lastEvent` to reconcile if you suspect a missed delivery.

**Do not wait for pre-close to post a payment.** `POST /accounts/{id}/payments` works with the account `IN_USE` or `IN_PAYMENT` — use it whenever the customer wants to pay, even mid-session. Reserve `pre-close` for when the account must stop accepting new items.

**Do not assume immediate close after payment.** Payment and close are distinct steps. Post payments with `POST /accounts/{id}/payments` and only then call `POST /accounts/{id}/close` — typically after `pre-close`, when the remaining balance (or full total if no prior payments) is settled.

**Treat fiscal issuance as asynchronous.** After `202 Accepted`, wait for `FISCAL_ISSUED` (or `FISCAL_ERROR`) — do not expect the document in the request response. Call `GET /accounts/{id}/fiscal` when the event arrives.

**Reflect cancellations and transfers immediately.** On `ACCOUNT_ITEM_CANCELLED` or `ACCOUNT_ITEM_REMOVED`/`ACCOUNT_ITEM_ADDED`, update the displayed account — the customer must not see items that already left the account.

---

!!! tip "Checklist — Software Service"
    - Account created and `ACCOUNT_OPENED` emitted on first INDOOR order.
    - Every state transition emits the corresponding event.
    - `IN_PAYMENT` account rejects new items until `unlock`.
    - Payment (`POST /accounts/payments`) accepted in `IN_USE` **and** `IN_PAYMENT`, without requiring pre-close.
    - Paid total validated before accepting close.
    - After `close`, every further operation is rejected — including new payments.
    - Fiscal issuance responds `202` and later emits `FISCAL_ISSUED` / `FISCAL_ERROR`.
    - `totals` reflect cancellations and transfers immediately.

!!! tip "Checklist — Ordering Application"
    - Account located by operational key (`operationMode` + `identifier`).
    - Webhook endpoint implemented and registered for events (no polling).
    - Payments may be posted at any time (`IN_USE` or `IN_PAYMENT`), not only after pre-close.
    - Payment and close treated as separate steps.
    - Fiscal issuance treated as asynchronous (wait for the event).
    - Cancellations and transfers reflected in the UI in real time.

---

**Normative contract (fields, endpoints, errors, examples):** [Indoor OpenAPI →](../reference/indoor.md)

---

<div class="od-next-step">
  <div class="od-next-step__label">Next step</div>
  <div class="od-next-step__links">
    <a href="../reference/indoor/">Implement with Indoor OpenAPI</a>
    <a href="orders/">Orders protocol (prerequisite)</a>
    <a href="../reference/orders/">Orders OpenAPI</a>
    <a href="discovery/">Discovery</a>
  </div>
</div>
