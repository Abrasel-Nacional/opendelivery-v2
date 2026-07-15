# Authentication

<p class="od-meta">
 <span class="od-badge od-badge--code">authentication</span>
</p>

!!! note "API Spec"
    The implementable contract (endpoints, fields, errors, and examples) is in the **[Authentication API Spec](../reference/authentication.md)** — English only.

Authentication is not a capability domain.

It is a cross-cutting protocol mechanism for how participants obtain and present credentials for protected operations. It applies uniformly to all ODP capabilities — Merchant, Orders, Logistics, and others.

## Supported authentication models

ODP v2 supports three OAuth 2.0 models. The protocol does not mandate a single model for every ecosystem. Each platform **MUST** declare which model(s) it supports in Discovery and during onboarding.

| Model | Identifier | Status |
|---|---|---|
| Client credentials by merchant | `client_credentials` + merchant-scoped credentials | Supported — legacy compatibility |
| Client credentials by application | `client_credentials` + `by_app` | Supported — **recommended for new integrations** |
| Authorization code | `authorization_code` | Supported — optional, advanced use cases |

!!! tip "V1 -> V2 migration"
  For new integrations, prefer `by_app`.
  The `by_merchant` model remains supported as legacy compatibility during transition.
  If `authorization_code` is supported, it MUST be declared in Discovery.

## Common requirements

Regardless of model, every implementation **MUST**:

1. Declare the selected authentication model in Discovery.
2. Align the production model explicitly during onboarding.
3. Declare scopes consistent with the protocol capabilities used.
4. Make merchant authorization rules explicit and discoverable.
5. Declare message signing independently of the OAuth 2.0 flow when supported.
6. Preserve merchant identification in event/request payloads when required by the integration model.
7. Protect authentication material in transit and at rest.

## Model 1 — Client credentials by merchant

One `client_id` / `client_secret` pair **per store**. Matches V1 patterns. Useful for migration; new integrations SHOULD prefer by-application.

## Model 2 — Client credentials by application (recommended)

One `client_id` for the whole software. Authorized merchants are listed via:

```
GET /merchants
Authorization: Bearer {token}
```

**Do not** embed the merchant list in the OAuth token payload (breaks OAuth2 / gateway assumptions).

Example token request:

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id={client_id}
&client_secret={client_secret}
&scope=od.orders od.menu
```

### Scopes

| Scope | Access |
|---|---|
| `od.orders` | Order lifecycle |
| `od.menu` | Menu / merchant data |
| `od.logistics` | Logistics |
| `od.crm` | Customer, loyalty, reviews |
| `od.all` | All domains (compatibility) |

## Model 3 — Authorization code

Optional flow for interactive / delegated authorization. When supported, Discovery **MUST** declare it. Full operational detail may evolve in later releases.

## Message signing (optional)

Bidirectional request/response signing may be offered as a security feature. It is **not** mandatory. When offered, declare it in Discovery and document verification expectations.

## Relationship to Discovery

Authentication configuration **MUST** be discoverable via the well-known manifest so partners do not rely only on bilateral email/setup docs.

See [Discovery](discovery.md) and the [Authentication API Spec](../reference/authentication.md) (English).

---

<div class="od-related">
  <p class="od-related__label">Related</p>
  <ul class="od-related__list">
    <li><a href="../reference/authentication.md">Authentication API Spec</a> — OAuth, tokens, webhooks</li>
    <li><a href="discovery.md">Discovery</a> — grant models and scopes</li>
    <li><a href="../reference/discovery.md">Discovery API Spec</a></li>
    <li><a href="../reference/conventions.md">General rules</a></li>
  </ul>
</div>
