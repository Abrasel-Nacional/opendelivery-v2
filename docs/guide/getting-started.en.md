# Getting started

!!! warning "Release Candidate (V2.0.0-rc)"
    This documentation is a **Release Candidate**. It was consolidated in technical committees and is now in an **ecosystem validation** period: company review and **implementation pilots**.

    During this phase the specification may still change based on feedback. A **stable release** will be published only after validation completes. **V1 remains active** and is the production reference during the transition.

    Send feedback via the [GitHub repository](https://github.com/Abrasel-Nacional/opendelivery-v2/issues). Details in the [changelog](changelog.md).

Open Delivery is an **open protocol**, not a product. It defines how independent food-tech systems — ordering apps, restaurant management systems, logistics operators, and CRM platforms — interoperate without custom bilateral integrations.

This guide covers the minimum you need to start an integration.

---

## 1. Understand your role in the ecosystem

The protocol defines four roles. A system may play more than one.

| Role | Who | What they do |
|---|---|---|
| **Originator** | Ordering app, marketplace, kiosk | Creates the order; receives lifecycle updates |
| **Software Service (POS)** | Restaurant management system | Accepts orders; manages menu, account, fiscal |
| **Logistics** | Delivery operator, own fleet | Executes delivery; emits tracking events |
| **CRM software** | Customer data / loyalty platform | Consumes the **Customer** capability (and Reviews/Loyalty modules); does not drive kitchen order lifecycle |

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

=== "CRM software"
 1. **Discovery** — publish your Well-Known endpoint
 2. **Customer** — customer-data capability (Reviews and/or Loyalty modules as needed)
 3. **Loyalty** (module) — programs and redemptions, if applicable

---

<div class="od-related">
  <p class="od-related__label">Related</p>
  <ul class="od-related__list">
    <li><a href="by-role.md">Paths by role</a> — what to implement by product type</li>
    <li><a href="../documentation/core-concepts.md">Concepts</a> — architecture and entities</li>
    <li><a href="../protocol/discovery.md">Discovery</a> · <a href="../protocol/authentication.md">Authentication</a></li>
    <li><a href="../reference/conventions.md">General rules</a> · <a href="../reference/error-handling.md">Error handling</a></li>
    <li><a href="migration-v1-v2.md">Migration V1→V2</a> · <a href="../reference/index.md">API reference</a></li>
  </ul>
</div>
