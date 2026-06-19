# Open Delivery v2 – Complete Specification Structure

A protocol-first redesign of Open Delivery, enabling interoperable food service systems.

The specification should be read as the new canonical documentation for Open Delivery v2, starting from the behavior already established in v1 and evolving through explicit changes, additions, and migration guidance.

---

## 📋 Documentation Index

### Foundation (Read First)
- [README.md](../README.md) – Project overview and status
- [docs/index.md](index.md) – Specification introduction
- [docs/overview.md](overview.md) – High-level protocol description
- [docs/principles.md](principles.md) – ⭐ Normative design principles
- [docs/scope.md](scope.md) – In/out of scope
- [docs/terminology.md](terminology.md) – Normative definitions

### Core Protocol Capabilities (Read by Role)
- **Orders Capability** [docs/domains/orders/](domains/orders/index.md) – ⭐ PRIMARY
  - Order lifecycle, states, events, profiles, cancellation
  - **Read this first** if implementing any participant

- **Merchant Capability** [docs/domains/merchant/](domains/merchant/index.md)
  - Merchant overview, menu modeling, synchronization, and open questions
  - **Read this** to understand merchant data model

- **Logistics Capability** [docs/domains/logistics/](domains/logistics/index.md)
  - Delivery lifecycle, tracking, availability, problem handling
  - **Read this** if handling `DELIVERY` profile orders

### Extensions
- **Indoor Extension** – extends Orders for on-premise order context
- **Loyalty Extension** – planned extension of CRM for rewards coordination

### Transport & Implementation
- [docs/QUICK_REFERENCE.md](QUICK_REFERENCE.md) – ⭐ **START HERE if asking "how do I map protocol to endpoints?"**
- [docs/PROTOCOL_VS_BINDING.md](PROTOCOL_VS_BINDING.md) – How protocol and bindings relate (detailed explanation)
- [docs/REST_BINDING_OUTLINE.md](REST_BINDING_OUTLINE.md) – REST/HTTP binding with all endpoints and examples
- [docs/transport-bindings.md](transport-bindings.md) – Transport binding patterns and design
- [IMPLEMENTATION_GUIDE.md](../IMPLEMENTATION_GUIDE.md) – v1→v2 transition guide
- [STRUCTURE.md](../STRUCTURE.md) – Visual specification structure
- [docs/domains/ENDPOINT_MAPPING.md](domains/ENDPOINT_MAPPING.md) – v1 endpoints → v2 concepts

---

## 🎯 Quick Start by Role

### I'm a Merchant System Developer
1. Read: [Principles](principles.md) (especially "Protocol-First")
2. Read: [Orders Capability](domains/orders/index.md) – Understand your responsibilities
3. Read: [Merchant Capability](domains/merchant/index.md) – Understand merchant data
4. Consult: [REST/HTTP Binding](transport-bindings.md) (when choosing REST)
5. Reference: [Endpoint Mapping](domains/ENDPOINT_MAPPING.md) – Map v1 to v2

### I'm an Ordering Application Developer
1. Read: [Principles](principles.md)
2. Read: [Orders Capability](domains/orders/index.md) – Learn order lifecycle
3. Read: [Merchant Capability](domains/merchant/index.md) – Learn to query merchant data
4. Understand: [Order Profiles](domains/orders/index.md#order-profiles) – DELIVERY, PICKUP, ON_PREMISE
5. Consult: [REST/HTTP Binding](transport-bindings.md)

### I'm a Logistics Provider Developer
1. Read: [Principles](principles.md)
2. Read: [Logistics Capability](domains/logistics/index.md) – Core responsibility
3. Read: [Orders Capability](domains/orders/index.md) – Understand DELIVERY profile
4. Understand: Delivery lifecycle and events
5. Consult: [REST/HTTP Binding](transport-bindings.md)

### I'm an Architect Designing Integration
1. Read: [Overview](overview.md) + [Principles](principles.md)
2. Read: [Protocol Capabilities Overview](domains/index.md) – Understand modular structure
3. Review: All three capabilities (Orders, Merchant, Logistics)
4. Study: [Transport Bindings](transport-bindings.md) – Choose implementation approach
5. Consider: [STRUCTURE.md](../STRUCTURE.md) – Dependency and versioning strategy

### I'm Coming from v1
1. **Essential**: [IMPLEMENTATION_GUIDE.md](../IMPLEMENTATION_GUIDE.md)
2. **Reference**: [Endpoint Mapping](domains/ENDPOINT_MAPPING.md)
3. Then follow your role above

The migration path is based on reading the v2 spec as the authoritative target and using migration documents only to understand differences from the legacy v1 model.

---

## 🔑 Key Concepts at a Glance

### Core Protocol Constructs

**Orders Capability** (PRIMARY)
- ⭐ Central coordination entity
- Order → CONFIRMED → PREPARING → READY → DISPATCHED → DELIVERED
- Three profiles: DELIVERY, PICKUP, ON_PREMISE
- Events: Normative, Conditional, Optional (profile-scoped)
- Cancellation as coordinated process

**Merchant Capability**
- Merchant as the principal entity, with Services and Menus as sub-entities
- Service types: DELIVERY, TAKEOUT, INDOOR
- Menu modeling trade-offs and synchronization concerns
- Open questions remain explicit while the committee converges

**Logistics Capability**
- Delivery lifecycle parallel to order (for DELIVERY profile)
- States: PENDING → ACCEPTED → PICKED_UP → IN_TRANSIT → DELIVERED
- Tracking, availability, pricing, problem handling
- Coordinates with Orders Capability

**Extensions**
- Indoor Extension augments Orders for on-premise execution
- Loyalty Extension augments CRM for rewards coordination

### The Three Actors

**Originator**
- Creates order, provides customer context
- Receives order updates, manages customer communication

**Merchant System**
- Receives order, accepts/rejects, fulfills
- Emits order status updates
- Selects delivery partner (if delivery order)

**Logistics Provider**
- Receives delivery assignment
- Executes delivery, provides tracking
- Handles delivery exceptions

### Transport Agnosticism

- Protocol ≠ HTTP, ≠ JSON, ≠ OAuth2
- Multiple bindings possible: REST, Events, gRPC, GraphQL, Custom
- Implementation details, not protocol spec

---

## 📚 Reading Patterns

### Deep Dive (Implementer)
Start with [Principles](principles.md) → [Terminology](terminology.md) → Your Capability → [Implementation Guide](../IMPLEMENTATION_GUIDE.md)

### High Level (Architect)
[Overview](overview.md) → [Principles](principles.md) → [Protocol Capabilities Overview](domains/index.md) → [Transport Bindings](transport-bindings.md)

### Migration from v1
[Endpoint Mapping](domains/ENDPOINT_MAPPING.md) → [Implementation Guide](../IMPLEMENTATION_GUIDE.md) → Your Service Spec

### Specific Concept
[Terminology](terminology.md) → Relevant Capability → [Endpoint Mapping](domains/ENDPOINT_MAPPING.md)

---

## 🗂️ File Structure

```
opendelivery-v2/
├── README.md                               # Project intro
├── STRUCTURE.md                            # Visual overview (this repo)
├── IMPLEMENTATION_GUIDE.md                 # v1→v2 transition
├── docs/
│   ├── index.md                           # Spec introduction
│   ├── overview.md                        # High-level description
│   ├── principles.md                      # Design principles ⭐ NORMATIVE
│   ├── scope.md                           # In/out of scope
│   ├── terminology.md                     # Key definitions
│   ├── transport-bindings.md              # How to carry protocol
   └── domains/
│       ├── index.md                       # Protocol capabilities overview
│       ├── orders/
│       │   └── index.md                   # Orders Capability ⭐ PRIMARY
│       ├── merchant/
│       │   ├── index.md                   # Merchant Capability overview
│       │   ├── entities/
│       │   │   ├── index.md               # Entities overview
│       │   │   ├── merchant-basic-info.md # Merchant identity and ownership context
│       │   │   ├── services.md            # Service contexts and constraints
│       │   │   ├── items.md               # Item entity baseline
│       │   │   ├── relationship.md        # Relationship
│       │   │   └── menus/
│       │   │       └── index.md           # Menu + categories/offers/options/availability sections
│       │   └── synchronization.md         # Synchronization alternatives
│       ├── logistics/
│       │   └── index.md                   # Logistics Capability
│       ├── crm/                           # Planned
│       ├── loyalty/                       # Planned
│       └── ENDPOINT_MAPPING.md            # v1→v2 reference
└── .github/
  └── copilot-instructions.md            # Capability-specific guidance
```

---

## 🔄 Workflow: v1 API → v2 Protocol

```
Your v1 REST Endpoints:

GET /v1/merchant
  ↓ Maps to → Merchant Capability (Information Exchange)

POST /v1/orders/{id}/confirm
  ↓ Maps to → Orders Capability (State: CONFIRMED event)

POST /v1/logistics/delivery
  ↓ Maps to → Logistics Capability (Delivery creation)

+

Transport Binding (REST/HTTP):
  └─ How above concepts are carried in HTTP request/response

= v2 Compliance
```

---

## ✅ Specification Status

- **Foundation** ✅ Introduced + Terminology
- **Orders Capability** ✅ Complete with all profiles
- **Merchant Capability** 🔄 In active refinement
- **Logistics Capability** ✅ Complete
- **REST/HTTP Binding** 🔄 In development
- **Event Stream Binding** 📋 Proposed for v2.1
- **CRM Service** 📋 Planned for v2.1
- **Loyalty Service** 📋 Planned for v2.1
- **gRPC Binding** 📋 Planned for v2.2
- **GraphQL Binding** 📋 Planned for v2.2

---

## 🚀Next Steps

### For Specification Development
- [ ] REST/HTTP Transport Binding (detailed)
- [ ] CRM Capability specification
- [ ] Loyalty Extension specification
- [ ] Event Stream Transport Binding
- [ ] Security/authentication details

### For Implementation
- [ ] Sandbox with v2 support
- [ ] Reference implementations (minimal)
- [ ] Testing tools and validators
- [ ] Migration guides for v1 platforms

### For Community
- [ ] Community feedback on protocol capabilities
- [ ] Use case validation
- [ ] Real-world implementation feedback
- [ ] Binding proposals

---

## 📖 How to Use This Documentation

**For Reading (Linear → Understanding)**
1. Start at [README](../README.md)
2. Then [Overview](overview.md) and [Principles](principles.md)
3. Then [Terminology](terminology.md)
4. Then your relevant capability

**For Reference (Non-linear → Looking up)**
- Need a term? → [Terminology](terminology.md)
- Want to understand endpoint? → [Endpoint Mapping](domains/ENDPOINT_MAPPING.md)
- Need transport details? → [Transport Bindings](transport-bindings.md)
- Coming from v1? → [Implementation Guide](../IMPLEMENTATION_GUIDE.md)

**For Governance**
- Is it normative? → [Principles](principles.md)
- Scope details? → [Scope](scope.md)
- Capability versioning? → [Protocol Capabilities Overview](domains/index.md)

---

## 🤝 Contributing

This specification is under active development. Contributions welcome!

- Questions? Open an issue
- Feedback? Discussions section
- Proposals? Create a detailed proposal

Key guidelines:
- All changes must align with [Principles](principles.md)
- Backward compatibility is a goal
- Transport neutrality required
- Clear normative vs. informative

---

## 📜 License

(See LICENSE file in repository)

---

**Version:** 2.0 (In Development)  
**Last Updated:** March 2026  
**Status:** Active Development

🔗 **Links**
- GitHub: https://github.com/Abrasel-Nacional/opendelivery-v2
- Discussions: (repository discussions)
- Issues: (repository issues)

