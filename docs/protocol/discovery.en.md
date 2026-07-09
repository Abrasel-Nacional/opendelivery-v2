# Discovery

<p class="od-meta">
  <span class="od-badge od-badge--core">Infraestrutura</span>
  <span class="od-badge od-badge--code">discovery</span>
  <span class="od-badge od-badge--must">Obrigatório</span>
</p>

<div class="od-api-callout">
  <p>First step of any V2 integration. HTTP contract is OpenAPI <strong>in English only</strong>.</p>
  <a href="../reference/discovery/">Open OpenAPI reference →</a>
</div>

Before any capability operation can happen, each participant publishes a public, machine-readable document that tells the other side exactly what it supports. That document is the **discovery manifest**, served at a well-known URL.

This page explains what discovery is for, how each side of the integration uses it, and how to read and publish a manifest. Normative rules and the full field reference are in the [Discovery API spec](../reference/discovery.md).

---

## The problem discovery solves

In V1, there was no standard way to know what a counterpart supported before calling it. Integrators found out through trial and error: they called an endpoint, got a `404` or an unexpected error, and then went back to their counterpart asking what was actually implemented. This was slow, expensive, and led to divergent implementations where each pair of participants had their own set of informal bilateral agreements.

Discovery eliminates that. Instead of discovering capabilities indirectly through failed calls, each participant declares its capabilities upfront in a single, always-available document.

---

## How it works

The manifest is served over a standard HTTP `GET` at a URL that always ends with `/.well-known/opendelivery`:

```
GET https://dominio.com/.well-known/opendelivery
```

The endpoint is always public — no authentication required. The response is a JSON document that describes everything a counterpart needs to know before sending a single capability request: which capabilities are active, what operations are supported, which events are emitted, how to deliver messages (webhook or polling), and what operational limits to respect.

The two parties can sit at opposite ends of this exchange:

- **The publisher** is the participant who implements and serves the manifest.
- **The consumer** is the counterpart who reads the manifest before starting the integration.

In practice, both sides are usually publishers and consumers — each side has its own manifest, and each reads the other's before coordinating.

---

## The integration flow

Discovery is always step zero. The sequence looks like this:

```
Consumer                                 Publisher
   |                                         |
   |  GET /.well-known/opendelivery          |
   |---------------------------------------->|
   |                                         |
   |  200 OK  { manifest }                   |
   |<----------------------------------------|
   |                                         |
   |  [reads capabilities, limits, events]   |
   |  [configures integration accordingly]   |
   |                                         |
   |  POST /orders   (or webhook, etc.)      |
   |---------------------------------------->|
```

The consumer reads the manifest once (or periodically to detect changes) and uses it to decide how to behave. Only after reading the manifest does it begin capability operations.

The full discovery URL is exchanged out-of-band — through registration, configuration, or manual setup — before the integration starts. The manifest itself is not the place to learn the URL; the URL is shared through your onboarding process.

---

## What the manifest contains

The manifest is a single JSON object with five top-level sections. Here is a quick tour of each one, using the full example from the spec as reference.

### Identity and protocol version

```json
{
  "appId": "550e8400-e29b-41d4-a716-446655440000",
  "openDelivery": {
    "currentVersion": "2.0",
    "supportedVersions": ["2.0"]
  },
  "discovery": {
    "version": "1.0.0"
  }
}
```

`appId` is the stable identifier for the participant application, issued during onboarding. The consumer uses it to correlate the manifest with the credentials it already has.

`openDelivery.supportedVersions` tells the consumer which protocol versions this participant can interoperate with. If there is no version overlap, the integration cannot proceed.

`discovery.version` identifies which version of the discovery format this manifest follows.

---

### Authentication

```json
{
  "authentication": {
    "supportedGrantTypes": ["client_credentials", "authorization_code"],
    "clientIdGeneration": ["by_app", "by_merchant"]
  }
}
```

This section tells the consumer which OAuth 2.0 grant types to use and how credentials are issued:

- `client_credentials` — the standard application-level flow.
- `authorization_code` — used when a merchant must explicitly grant consent. Only implement this if it is declared here.
- `by_app` — one credential pair covers all merchants (recommended for V2).
- `by_merchant` — separate credentials per merchant (V1 legacy, still supported for migration).

The consumer looks at this section and configures its authentication client accordingly before making any protected capability call.

---

### Capabilities

Capabilities are the core of the manifest. Each capability key (`orders`, `merchant`, `customer`, `logistics`, `indoor`) is present only if the participant actively supports it. Omitting a key means the capability is not supported — no need to guess.

#### Orders and Logistics — originator and receiver

Orders and Logistics have two sub-roles that can exist independently:

```json
{
  "capabilities": {
    "orders": {
      "version": "1.0.0",
      "supported": true,
      "originator": {
        "supported": true,
        "supportedEvents": ["ORDER_CREATED", "ORDER_CONFIRMED", "ORDER_CANCELLED", "ORDER_COMPLETED"],
        "unsupportedEvents": ["ORDER_DISPATCHED"],
        "supportsWebhook": true,
        "supportsPolling": false
      },
      "receiver": {
        "supported": true,
        "supportedOperations": ["createOrder", "confirmOrder", "cancelOrder", "updateOrderStatus"],
        "unsupportedOperations": ["dispatchOrder"],
        "supportsWebhook": true,
        "supportsPolling": true
      }
    }
  }
}
```

**Originator** means this participant emits order events. The consumer knows exactly which events will arrive (`supportedEvents`) and which will never arrive (`unsupportedEvents`). This eliminates the classic ambiguity of "does this partner send `ORDER_DISPATCHED` or not?" — it is declared explicitly.

**Receiver** means this participant accepts incoming order operations. The consumer knows which operations it can call and which it should not attempt.

`supportsWebhook` and `supportsPolling` tell the consumer how to deliver or retrieve messages. If only `supportsWebhook: true` and `supportsPolling: false`, the consumer must push events; it cannot poll for them.

The same structure applies to Logistics.

---

#### Merchant — synchronization flags

```json
{
  "capabilities": {
    "merchant": {
      "version": "1.0.0",
      "supported": true,
      "supportsPartialUpdate": true,
      "supportsFullGetByOriginator": true
    }
  }
}
```

`supportsPartialUpdate` tells the consumer whether it can send patch-style updates or must always send the full merchant payload. `supportsFullGetByOriginator` tells whether the originator side exposes a GET endpoint for the consumer to fetch the current state — useful for reconciliation and initial loads.

---

#### Indoor — fiscal and table configuration

```json
{
  "capabilities": {
    "indoor": {
      "version": "1.0.0",
      "supported": true,
      "invoiceIssuer": "pos",
      "invoiceIssueMoment": "account_closing",
      "usesAccountId": true
    }
  }
}
```

Indoor (table service) has operational characteristics that vary significantly between implementations. The manifest declares who issues the fiscal invoice (`pos`, `app`, or `platform`), when it is issued, and whether the integration uses an `accountId` to track open table sessions. Without this, consumers would have to negotiate these details bilaterally for every deployment.

---

#### Customer — operational limits

```json
{
  "capabilities": {
    "customer": {
      "version": "1.0.0",
      "supported": true,
      "supportsBatchGet": true,
      "supportsBatchPost": true,
      "maxBatchSize": 100,
      "maxGetPeriodDays": 30,
      "requestsPerSecond": 10,
      "maxPayloadSizeKb": 1024,
      "acceptedGetPeriodicity": "daily"
    }
  }
}
```

The Customer capability declares the operational limits the consumer must respect. This is where the manifest acts as a live configuration document: instead of hunting through separate documentation to find rate limits and batch sizes, the consumer reads them here and adapts its behavior automatically.

- `maxBatchSize` — never send more items than this in a single POST.
- `maxGetPeriodDays` — never query a date range wider than this.
- `requestsPerSecond` — throttle accordingly.
- `acceptedGetPeriodicity` — how often the consumer should poll (e.g., `daily` means once per day is enough and more frequent polling is discouraged).

---

## The publisher's perspective

If you are implementing the manifest endpoint, here is what to keep in mind:

**Declare what you actually support, not what you aspire to support.** A consumer reading `supportedEvents: [ORDER_CREATED, ORDER_CONFIRMED]` will build its integration around those two events. If `ORDER_CONFIRMED` never actually arrives, the consumer's flow breaks.

**Be explicit about what you do not support.** Use `unsupportedEvents` and `unsupportedOperations` to declare gaps clearly. An empty list `[]` is a valid value and means "all standard items in this category are supported."

**Keep the manifest up to date.** If your implementation changes — you add polling support, raise a batch limit, or start emitting a new event — update the manifest. Consumers may re-read it periodically to detect changes.

**Serve it fast and reliably.** The manifest is read before the integration starts. A slow or intermittent discovery endpoint can block an entire onboarding.

---

## The consumer's perspective

If you are reading a counterpart's manifest before connecting, here is how to use it:

**Read the manifest before any capability call.** Do not assume what the counterpart supports. Read the manifest first, then configure your integration accordingly.

**Check protocol version compatibility.** If `openDelivery.supportedVersions` does not include your version, coordinate with the counterpart before proceeding.

**Adapt to the declared delivery mode.** If the manifest says `supportsWebhook: true, supportsPolling: false` for a capability, set up your webhook receiver — do not build a polling loop.

**Respect operational limits.** The `customer` capability's limits (`maxBatchSize`, `requestsPerSecond`, `maxGetPeriodDays`) are declarations, not suggestions. Exceeding them will result in errors or throttling.

**Handle missing capabilities gracefully.** If a capability key is absent from the manifest, treat it as unsupported and do not call it. Log it clearly so the integration owner understands what is and is not available.

**Re-read periodically.** Manifests change rarely, but they do change. Re-reading the manifest on startup and periodically in production lets you detect changes (new capabilities, updated limits, added events) without manual reconfiguration.

---

!!! tip "Quick checklist for publishers"
    - The endpoint URL ends with `/.well-known/opendelivery`.
    - The endpoint is public — no authentication required.
    - The endpoint uses HTTPS.
    - Only capabilities you actively support are listed.
    - `unsupportedEvents` and `unsupportedOperations` are populated explicitly.
    - Operational limits (batch sizes, rate limits, query windows) are accurate.
    - The full URL has been shared with your counterpart out-of-band.

!!! tip "Quick checklist for consumers"
    - Read the manifest before the first capability call.
    - Verify protocol version compatibility.
    - Configure delivery mode (webhook vs. polling) from `supportsWebhook` / `supportsPolling`.
    - Apply operational limits from the `customer` (or other) capability section.
    - Treat absent capability keys as unsupported.
    - Plan to re-read the manifest periodically.

---

**Full field reference and normative rules:** [Discovery API →](../reference/discovery.md)

---

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo</div>
  <div class="od-next-step__links">
    <a href="../reference/discovery/">Abrir referência OpenAPI</a>
    <a href="authentication/">Autenticação</a>
    <a href="../guide/getting-started/">Primeiros Passos</a>
  </div>
</div>
