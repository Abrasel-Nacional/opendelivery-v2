# Migration V1 -> V2

This guide explains how to migrate from V1 to V2 with a focus on implementation impact.
The structure below is capability-based so each squad can plan and deliver migration in slices.

See [Changelog](changelog.md) for release history.

!!! info "V1 remains active"
    V1 remains active during transition. New integrations should prioritize V2.

---

## Recommended migration flow

Recommended sequence:

1. Migrate **Authentication** (credential model and scopes).
2. Publish **Discovery** (mandatory integration manifest).
3. Migrate business capabilities in product-priority order (Merchant, Menu, Orders, Logistics, Customer, Indoor).
4. Run capability-by-capability certification with objective acceptance criteria.

---

## Authentication

### What changes from V1 to V2

- **Recommended change**: move to per-application credentials (single software `client_id`) for new integrations.
- **Legacy compatibility**: per-merchant credentials (`client_id` per store) remain supported for gradual migration.
- **Breaking**: scopes become domain-granular (`od.orders`, `od.menu`, `od.logistics`, `od.crm`, `od.all`).
- **Improvement**: optional `Authorization Code Flow` for delegated merchant authorization use cases.

### Code impact

- Prioritize app-level auth flow.
- Keep per-merchant fallback for partners still on legacy model.
- Update token request to include explicit scopes.
- Review token cache strategy to be per-application (not per store).

```diff
# V1
POST /oauth/token
- client_id=store_credential_123
- client_secret=store_secret_123

# V2
POST /oauth/token
+ client_id=application_credential
+ client_secret=application_secret
+ scope=od.orders od.menu
```

After token issuance, application-authorized merchants are resolved via:

```
GET /merchants
Authorization: Bearer {application_token}
```

### Legacy compatibility (important)

- The `by_merchant` model (one `client_id` per store) is still supported in V2 for transition.
- The recommended model for new integrations and gradual upgrades is `by_app`.
- If `authorization_code` is supported, it must also be declared in discovery.

### Discovery fields that must be populated

| Field | Type | Required | Migration use |
|---|---|---|---|
| `authentication.supportedGrantTypes` | array[string] | YES | Declare `client_credentials` and, when applicable, `authorization_code` |
| `authentication.clientIdGeneration` | array[string] | YES | Declare `by_app` (recommended) and/or `by_merchant` (legacy) |

### Migration steps

1. Introduce application-level credential storage.
2. Update OAuth client to always send `scope`.
3. Map internal actions to minimum required scopes.
4. Replace store discovery flow with `GET /merchants` under app token.
5. Validate compatibility fallback when partner still runs `by_merchant`.

### Acceptance criteria

- App gets tokens with correct scopes.
- App lists authorized merchants without store-specific credentials.
- Missing-scope calls fail with expected, observable errors.

### Common pitfalls

- Overusing `od.all` and losing least-privilege discipline.
- Keeping unnecessary per-merchant token caches.
- Forgetting token refresh in long-running async workers.

References: [Authentication Protocol](../protocol/authentication.md) · [Authentication API Spec](../reference/authentication.md)

---

## Discovery

### What changes from V1 to V2

- **Operational breaking change**: `GET /.well-known/opendelivery` becomes mandatory to start integration.
- **Improvement**: capabilities, versions, auth models, and event modes are declared in one manifest.

### Most critical discovery fields during migration

| Field | Type | Required | Why it matters |
|---|---|---|---|
| `openDelivery.supportedVersions` | array[string] | YES | Ensures version compatibility before activation |
| `authentication.supportedGrantTypes` | array[string] | YES | Defines allowed OAuth flows |
| `authentication.clientIdGeneration` | array[string] | YES | Shows whether partner is `by_app`, `by_merchant`, or both |
| `capabilities.orders.originator.supportedEvents` | array[string] | Conditional | Defines which order events are actually emitted |
| `capabilities.orders.originator.supportsWebhook` | boolean | Conditional | Defines push delivery availability |
| `capabilities.orders.originator.supportsPolling` | boolean | Conditional | Defines pull delivery availability |
| `capabilities.orders.receiver.supportedOperations` | array[string] | Conditional | Defines callable Orders operations |
| `capabilities.logistics.originator.supportedEvents` | array[string] | Conditional | Defines emitted logistics events |
| `capabilities.logistics.receiver.supportedOperations` | array[string] | Conditional | Defines accepted logistics operations |
| `capabilities.customer.maxBatchSize` | integer | Conditional | Controls sync batch size |
| `capabilities.customer.requestsPerSecond` | integer | Conditional | Controls safe rate limit |

### Code impact

- Add a bootstrap integration client driven by manifest data.
- Remove hardcoded capability/baseUrl config where manifest is available.
- Validate version compatibility before enabling business calls.

### Migration steps

1. Publish `/.well-known/opendelivery`.
2. Declare actually supported capabilities and `baseUrl`.
3. Declare auth model and event producer/consumer expectations.
4. Make consumer load and validate manifest during onboarding.
5. Block activation when manifest is missing or invalid.

### Acceptance criteria

- Integration activates only when discovery returns a valid contract.
- Discovery versions and capabilities match exposed API behavior.
- Bootstrap logs clearly show enabled/disabled capabilities.

### Common pitfalls

- Declaring a capability in discovery without implementing its endpoints.
- Environment drift (staging manifest differs from production).
- Treating discovery as optional and keeping manual onboarding.

References: [Discovery Protocol](../protocol/discovery.md) · [Discovery API Spec](../reference/discovery.md)

---

## Merchant

### Main changes

- **Breaking**: `merchantId` is generated by the originator.
- **Breaking**: `merchantType` removed.
- **Breaking**: service identifiers move to type-only (`DELIVERY`, `TAKEOUT`, `INDOOR`) without separate service id.

### What to adapt

- Update id ownership in registration and synchronization flows.
- Preserve internal POS mapping through `externalCode`.
- Update validators for type-based service model.

### Relevant discovery fields

| Field | Type | Use |
|---|---|---|
| `capabilities.merchant.supported` | boolean | Enables Merchant capability |
| `capabilities.merchant.supportsPartialUpdate` | boolean | Defines partial update vs full payload strategy |
| `capabilities.merchant.supportsFullGetByOriginator` | boolean | Defines whether full GET reconciliation is available |

References: [Merchant Protocol](../protocol/merchant.md) · [Merchant API Spec](../reference/merchant.md)

---

## Menu

### Main changes

- **Breaking**: end of monolithic `merchantUpdate` webhook.
- **Breaking**: granular CRUD by catalog entity.
- **Breaking**: option `subtotal` removed; `option_price` becomes required.
- **Improvement**: full snapshot support for reconciliation.

### What to adapt

- Split catalog update pipeline by entity (menu, category, itemOffer, optionGroup, option).
- Update price validations for `option_price` and `unity_price`.
- Add snapshot-based reconciliation when drift is detected.

References: [Menu Protocol](../protocol/menu.md)

---

## Orders

### Main changes

- **Breaking**: originator cancellation handshake removed; only mandatory `CANCELLED` remains.
- **Breaking**: `PICKED_UP` event removed.
- **Breaking**: `Order.type` leaves root and becomes `Order.fulfillment.orderType`.
- **Breaking**: `Order.delivery` / `Order.takeout` / `Order.indoor` move under `Order.fulfillment.*`.
- **Breaking**: item/option pricing fields move under `pricing` in `Order.items[*]` and `Order.items[*].options[*]`.
- **Breaking**: price format returns to the V1 model (`Price { value, currency }`) for item, option, discounts, fees, and totals.
- **Breaking**: `subtotalPrice` no longer exists for item and option pricing.
- **Consumer breaking change**: `Order.status` in `GET /orders/{id}` becomes source of truth.

### Essential migration rules

- Do not implement `POST /orders` for order entry.
- Treat events as notifications; reconcile lifecycle state via GET.
- Return `202` for already-applied duplicate lifecycle calls (no new transition).

### Discovery for Orders (critical migration point)

In V2, supported Orders events must be read from discovery before activating the flow.

| Field | Type | Use |
|---|---|---|
| `capabilities.orders.originator.supportedEvents` | array[string] | Lists events that will be emitted |
| `capabilities.orders.originator.unsupportedEvents` | array[string] | Lists events that should not be expected |
| `capabilities.orders.originator.supportsWebhook` | boolean | Defines push event delivery |
| `capabilities.orders.originator.supportsPolling` | boolean | Defines pull event delivery |
| `capabilities.orders.receiver.supportedOperations` | array[string] | Lists accepted Orders operations |
| `capabilities.orders.receiver.unsupportedOperations` | array[string] | Lists unavailable operations to avoid invalid calls |

```diff
# Before
{
  "id": "order-123",
- "type": "DELIVERY",
  "delivery": { "address": { "city": "Sao Paulo" } }
}

# After
{
  "id": "order-123",
  "fulfillment": {
+   "orderType": "DELIVERY",
    "delivery": { "address": { "city": "Sao Paulo" } }
  }
}
```

References: [Orders Protocol](../protocol/orders.md) · [Orders API Spec](../reference/orders.md) · [Conventions](../reference/conventions.md#duplicate-lifecycle-operations)

---

## Logistics

### Main changes

- **Normative improvement**: async-first semantics consolidated with `202 Accepted` on lifecycle mutations.
- **Improvement**: alignment with discovery-declared tracking mode (`push`/`pull`).

### What to adapt

- Ensure consumers do not treat `202` as terminal state.
- Adapt tracking orchestration to discovery mode.

### Relevant discovery fields

| Field | Type | Use |
|---|---|---|
| `capabilities.logistics.originator.supportedEvents` | array[string] | Defines emitted lifecycle events |
| `capabilities.logistics.originator.supportsWebhook` | boolean | Defines push delivery |
| `capabilities.logistics.originator.supportsPolling` | boolean | Defines pull delivery |
| `capabilities.logistics.receiver.supportedOperations` | array[string] | Defines accepted receiver operations |

References: [Logistics Protocol](../protocol/logistics.md) · [Logistics API Spec](../reference/logistics.md)

---

## Customer and Loyalty

### Main changes

- **New**: Customer capability for customer data, leads, and reviews.
- **New**: Loyalty module in the relationship domain.

### What to adapt

- Plan onboarding per capability (do not assume mandatory Orders dependency).
- Reuse Order data shape where relationship flows require order context.

### Relevant discovery fields

| Field | Type | Use |
|---|---|---|
| `capabilities.customer.supported` | boolean | Enables Customer capability |
| `capabilities.customer.supportsBatchGet` | boolean | Declares batch GET availability |
| `capabilities.customer.supportsBatchPost` | boolean | Declares batch POST availability |
| `capabilities.customer.maxBatchSize` | integer | Defines max items per batch |
| `capabilities.customer.maxGetPeriodDays` | integer | Defines max query window |
| `capabilities.customer.requestsPerSecond` | integer | Defines rate limit |

References: [Customer Protocol](../protocol/customer.md) · [Customer API Spec](../reference/customer.md) · [Loyalty Protocol](../protocol/loyalty.md)

---

## Indoor

### Main changes

- **New**: in-store capability (table, tab, counter) with central account model.
- **Important rule**: Indoor depends on Orders lifecycle.

### What to adapt

- Model account and payment flows without bypassing Orders lifecycle.
- Ensure consistency between order (`fulfillment.orderType: INDOOR`) and account state.

### Relevant discovery fields

| Field | Type | Use |
|---|---|---|
| `capabilities.indoor.supported` | boolean | Enables Indoor capability |
| `capabilities.indoor.invoiceIssuer` | string | Defines invoice issuer (`pos`, `app`, `platform`) |
| `capabilities.indoor.invoiceIssueMoment` | string | Defines invoice issuance moment |
| `capabilities.indoor.usesAccountId` | boolean | Defines whether account id is used |

References: [Indoor Protocol](../protocol/indoor.md) · [Indoor API Spec](../reference/indoor.md)

---

!!! abstract "Final capability checklist"
  | Capability | Checklist item |
  |---|---|
  | Authentication | Migrate to app-level credentials and proper scopes |
  | Authentication | Validate legacy auth compatibility (`by_merchant`) when needed |
  | Authentication | Declare Authorization Code in discovery when supported |
  | Discovery | Publish and validate discovery at onboarding |
  | Orders + Discovery | Validate supported Orders events and operations from discovery |
  | Merchant | Update to originator-owned `merchantId` and type-based services |
  | Menu | Migrate from `merchantUpdate` to granular CRUD |
  | Orders | Migrate to `fulfillment.orderType` and status-as-source-of-truth |
  | Logistics | Validate async-first `202` behavior |
  | Customer/Loyalty | Evaluate and plan according to product roadmap |
  | Indoor | Integrate with Orders lifecycle |

<div class="od-related">
  <p class="od-related__label">Related</p>
  <ul class="od-related__list">
    <li><a href="changelog.md">Changelog</a> - full version history</li>
    <li><a href="getting-started.md">Getting started</a> - minimum V2 path</li>
    <li><a href="../protocol/authentication.md">Authentication</a> · <a href="../protocol/discovery.md">Discovery</a></li>
    <li><a href="../reference/index.md">API reference</a></li>
  </ul>
</div>
