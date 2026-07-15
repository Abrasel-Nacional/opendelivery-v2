# Open Delivery Protocol – Version 2

This repository hosts the **next generation of the Open Delivery protocol**.

Open Delivery v2 is a protocol‑first redesign focused on long‑term interoperability, modularity, and clear governance for the food service and commerce ecosystem.

This work is **under active development**.

The intent is for v2 to become the **official Open Delivery documentation** from a defined effective date, while v1 remains active for a transition period and is later deprecated.

---

## 📌 What is Open Delivery?

Open Delivery is an open protocol that standardizes how independent systems exchange information in the food service ecosystem, including:

- Ordering platforms
- Point of Sale (POS) systems
- CRM and loyalty platforms
- Logistics and delivery services
- Integration hubs and middleware

Open Delivery defines **how systems communicate**, not how they are implemented.

It is **not a product**, **not a hosted API**, and **not a marketplace**.

---

## Why a Version 2?

Open Delivery v2 was created to evolve the protocol beyond the original API‑centric approach, addressing lessons learned from real‑world adoption.

Key goals of v2 include:

- Protocol‑first design (not API‑first)
- Clear separation between protocol and transport
- Modular capabilities, extensions, and bindings
- Explicit versioning and governance rules
- Long‑term extensibility and backward compatibility

This repository represents a **new protocol generation**, not a patch or minor revision.

At the same time, v2 is being written from the functional baseline already established in v1. In practice, the v2 specification starts by preserving existing behavior and then evolves through approved changes and new capabilities.

---

## 🚧 Project Status

Open Delivery v2 is currently:

- Under active design and specification
- Subject to changes and refinements
- Not yet considered stable for production use

Discussions, proposals, and early drafts are expected as part of this phase.

---

## 📚 Specification Documentation

The complete specification is organized into modular protocol capabilities:

**→ Start here:** [**Specification Index and Guide**](README_SPEC.md)

### Quick Links
- **Foundation:** [Principles](docs/principles.md) · [Terminology](docs/terminology.md) · [Overview](docs/overview.md)
- **Primary Capability:** [Orders](docs/domains/orders/index.md)
- **Supporting Capabilities:** [Merchant](docs/domains/merchant/index.md) · [Logistics](docs/domains/logistics/index.md)
- **For v1 Users:** [Implementation Guide](IMPLEMENTATION_GUIDE.md) · [Endpoint Mapping](docs/domains/ENDPOINT_MAPPING.md)

The v2 documentation is the target source of truth. Migration material is intended to explain deltas from v1, not to embed a full public copy of the legacy reference.

---

## 🧱 Structure and Scope

Open Delivery v2 is organized around independent protocol capabilities and extensions, such as:

- Orders
- Merchant
- Logistics
- Customer (including Reviews and Loyalty modules — not separate extensions)
- Indoor Extension (of Orders)
- Core protocol and security

Each capability is designed to be:

- Independently implementable
- Versioned explicitly
- Loosely coupled to other capabilities

The implementable contract is published as **API Spec** (REST/HTTP) under the API reference. Guide and Protocol pages explain the domain; API Spec is the normative source for integration.

---

## 🤝 Contributions and Collaboration

Contributions are welcome and encouraged.

At this stage, participation happens primarily through **GitHub Issues**, which are used for:

- Architectural discussions
- Capability modeling feedback
- Questions and clarifications
- Specification proposals

👉 **Open a new issue:**
https://github.com/Abrasel-Nacional/opendelivery-v2/issues/new

The project backlog and ongoing work can be followed through the official GitHub Project:

👉 **Open Delivery – Project Board:**
https://github.com/orgs/Abrasel-Nacional/projects/5

Contribution guidelines will be refined as the protocol stabilizes.

---

## 📄 License

Open Delivery is licensed under the Apache 2.0 License.
