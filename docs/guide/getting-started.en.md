# Getting started

Open Delivery is an **open protocol**, not a product. It defines how independent food-tech systems — ordering apps, restaurant management systems, logistics operators, and CRM platforms — interoperate without custom bilateral integrations.

This guide covers the minimum you need to start an integration.

<div class="od-api-callout">
  <p>Prefer a path by product type? Use role-based paths.</p>
  <a href="by-role/">Open role paths →</a>
</div>

---

## 1. Understand your role in the ecosystem

The protocol defines four roles. A system may play more than one.

| Role | Who | What they do |
|---|---|---|
| **Originator** | Ordering app, marketplace, kiosk | Creates the order; receives lifecycle updates |
| **Software Service (POS)** | Restaurant management system | Accepts orders; manages menu, account, fiscal |
| **Logistics** | Delivery operator, own fleet | Executes delivery; emits tracking events |
| **CRM** | Loyalty / customer data platform | Consumes order and customer data; manages loyalty programs |

Identify which role(s) your system plays. That determines which capabilities you need.

Detailed guide: **[Paths by role](by-role.md)**.

---

## 2. Authenticate

Open Delivery V2 uses **OAuth 2.0** with application-level authentication: a single `client_id` for every store your system integrates.

Three models are supported:

| Model | Identifier | Recommendation |
|---|---|---|
| Client credentials by application | `client_credentials` + `by_app` | **Recommended for new integrations** |
| Client credentials by store | `client_credentials` + `by_merchant` | V1 compatibility |
| Authorization code | `authorization_code` | Advanced use cases |

Request an access token:

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id={your_client_id}
&client_secret={your_client_secret}
&scope=od.orders od.menu
```

Include the token as `Authorization: Bearer {token}` on every request.

!!! note "Available scopes"
    `od.orders` · `od.menu` · `od.logistics` · `od.crm` · `od.all`

See [Authentication](../protocol/authentication.md) and the [Authentication API reference](../reference/authentication.md).

---

## 3. Declare capabilities via Discovery

Every integration **MUST** publish a Discovery endpoint in the Well-Known pattern:

```
GET /.well-known/opendelivery
```

This endpoint declares which capabilities you implement, which protocol versions you support, and how partners authenticate. **No integration can proceed without Discovery.**

Minimal response example:

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
    "orders": { "endpoint": "https://api.yourcompany.com/v2" }
  }
}
```

See [Discovery](../protocol/discovery.md) and the [Discovery API reference](../reference/discovery.md).

---

## 4. Choose which capability to implement first

Depending on your role:

=== "Originator"
    1. **Discovery** — publish your Well-Known endpoint
    2. **Orders** — create orders and consume lifecycle events
    3. **Merchant** — read menus and store status

=== "Software Service (POS)"
    1. **Discovery** — publish your Well-Known endpoint
    2. **Merchant** — expose menu, hours, and pause
    3. **Orders** — accept and process incoming orders
    4. **Indoor** — if you support dine-in / tab / kiosk

=== "Logistics"
    1. **Discovery** — publish your Well-Known endpoint
    2. **Logistics** — receive delivery requests and emit tracking events

=== "CRM"
    1. **Discovery** — publish your Well-Known endpoint
    2. **Customer** — manage customer data
    3. **Loyalty** — manage loyalty programs and redemptions

---

## 5. References

| Document | Description |
|---|---|
| [Concepts](../documentation/core-concepts.md) | Architecture, entities, interaction model |
| [Roles and responsibilities](../protocol/roles-and-responsibilities.md) | Obligations of each role |
| [Authentication](../protocol/authentication.md) | OAuth 2.0 models and scopes |
| [Discovery](../protocol/discovery.md) | Well-Known endpoint and manifest structure |
| [Guidelines](../protocol/guidelines.md) | Dates, pagination, idempotency |
| [Error handling](../protocol/error-handling.md) | Standard error format and HTTP codes |
| [Migration V1→V2](migration-v1-v2.md) | Breaking changes and migration guide |
| [API reference](../reference/index.md) | Interactive OpenAPI specs |
