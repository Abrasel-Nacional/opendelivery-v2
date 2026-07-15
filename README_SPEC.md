# Open Delivery v2 – Documentation map

Open Delivery V2 is an interoperability protocol with a single implementable contract: **API Spec (REST/HTTP)**.

Documentation layers:

| Layer | Role |
|-------|------|
| **Guide** | Onboarding, migration, roles |
| **Protocol** | Domain narrative (concepts, flows) — not field-level norm |
| **API reference** | Normative API Spec |

There is **no transport-binding layer**. Canonical layout: [STRUCTURE.md](STRUCTURE.md) · [AGENTS.md](AGENTS.md).

---

## 📋 Published site (start here)

### Guide
- [docs/index.md](docs/index.md) – Landing
- [docs/guide/getting-started.md](docs/guide/getting-started.md) – Getting started
- [docs/overview.md](docs/overview.md) – High-level overview
- [docs/documentation/core-concepts.md](docs/documentation/core-concepts.md) – Core concepts
- [docs/guide/migration-v1-v2.md](docs/guide/migration-v1-v2.md) – V1→V2 migration
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) – Implementer notes (v1→v2)

### Protocol
- [docs/protocol/principles.md](docs/protocol/principles.md) – Design principles
- [docs/protocol/orders.md](docs/protocol/orders.md) – Orders domain
- [docs/protocol/merchant.md](docs/protocol/merchant.md) – Merchant domain
- [docs/protocol/logistics.md](docs/protocol/logistics.md) – Logistics domain
- Capability pages under `docs/protocol/` (Customer modules: reviews, loyalty; Indoor under protocol as Orders extension)

### API reference (normative)
- [docs/reference/index.md](docs/reference/index.md) – API overview
- [docs/reference/conventions.md](docs/reference/conventions.md) – Shared conventions
- [docs/reference/error-handling.md](docs/reference/error-handling.md) – Error model
- API Spec YAML: `docs/reference/v2/*.openapi.yaml` (API reference shells in `docs/reference/*.md`)

### Legacy (not published)
- `docs/transport-bindings/**` – legacy REST notes; excluded from the site

---

## 🎯 Quick start by role

### Merchant / POS
1. [Principles](docs/protocol/principles.md)
2. [Orders](docs/protocol/orders.md) + [Orders API Spec](docs/reference/orders.md)
3. [Merchant](docs/protocol/merchant.md) + [Merchant API Spec](docs/reference/merchant.md)

### Ordering application
1. [Getting started](docs/guide/getting-started.md)
2. [Orders](docs/protocol/orders.md) + API Spec
3. [Discovery](docs/protocol/discovery.md) + [Auth](docs/protocol/authentication.md)

### Logistics
1. [Logistics](docs/protocol/logistics.md) + API Spec
2. [Orders](docs/protocol/orders.md) (DELIVERY profile)

### Coming from v1
1. [Migration V1→V2](docs/guide/migration-v1-v2.md)
2. [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
3. capability API Spec under `docs/reference/`

The migration path is based on reading the v2 spec as the authoritative target and using migration documents only to understand differences from the legacy v1 model.

---

## Key concepts (short)

- **Capabilities:** Merchant, Orders, Logistics, Customer (+ Indoor, Reviews, Loyalty extensions)
- **Actors:** Ordering Application, Software Service (POS), Logistics, CRM
- **Contract:** API Spec REST/HTTP under `docs/reference/v2/`
- **Status:** V2.0.0-rc — ecosystem validation (see changelog)

## Reading path

1. [Landing](docs/index.md) → [Getting started](docs/guide/getting-started.md)
2. [Principles](docs/protocol/principles.md) → capability Protocol pages
3. API Spec for the capability you implement

Coming from v1: [Migration](docs/guide/migration-v1-v2.md) · [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)

## Contributing

- Prefer issues on the [GitHub repository](https://github.com/Abrasel-Nacional/opendelivery-v2)
- Follow [AGENTS.md](AGENTS.md) language rules and [STRUCTURE.md](STRUCTURE.md) capability checklist
- Do not reintroduce transport-binding language

**Version:** 2.0.0-rc · **Status:** Release Candidate

