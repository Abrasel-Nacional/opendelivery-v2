# Open Delivery Protocol v2

Open Delivery is an open protocol that defines how independent systems exchange information in the food service and commerce ecosystem.

This repository contains the **Version 2** specification of the Open Delivery protocol, designed with a **protocol‑first**, modular, and long‑term approach.

Open Delivery is a specification.  
It defines **rules, concepts, and responsibilities**, not implementations.

---

## Purpose of This Specification

The purpose of the Open Delivery protocol is to enable interoperability between heterogeneous systems without requiring custom, one‑off integrations for each pair of participants.

The protocol establishes a shared language and set of expectations so that systems can integrate while remaining independently operated and governed.

---

## What Open Delivery Is

Open Delivery:

- Defines how systems communicate with each other
- Specifies concepts, entities, and responsibilities
- Is vendor‑neutral and implementation‑agnostic
- Enables point‑to‑point integrations
- Supports decentralized architectures

---

## What Open Delivery Is Not

Open Delivery does **not**:

- Provide infrastructure or hosting
- Define business rules or commercial agreements
- Act as a marketplace or platform
- Enforce a specific technology stack
- Replace internal system architectures

Each participant remains responsible for implementing, operating, and securing its own systems.

---

## Ecosystem Scope

The Open Delivery protocol is designed to support interoperability between systems such as:

- Ordering platforms
- Point of Sale (POS) systems
- CRM and loyalty platforms
- Logistics and delivery services
- Integration hubs and middleware

The protocol focuses on **communication between systems**, not on user interfaces or operational workflows.

---

## Design Approach

Open Delivery v2 is based on the following high‑level design approach:

- **Protocol‑first**, not API‑first
- Clear separation between protocol and transport
- Modular and domain‑oriented specifications
- Explicit versioning and evolution rules
- Backward compatibility as a design goal

These principles guide all decisions in this specification.

---

## Document Organization

This specification is organized as follows:

- **Overview** – High‑level description of the protocol and its actors
- **Principles** – Foundational design principles
- **Scope** – What is in scope and out of scope
- **Terminology** – Normative definitions of key terms
- **Domains** – Domain‑specific specifications (e.g., Orders, Menu, CRM)
- **Transport Bindings** – How the protocol can be exchanged over specific transports

Each section builds on the previous ones and should be read in order by first‑time readers.

---

## Status of This Document

This specification is under active development.

- Content may change as the protocol evolves
- Not all domains are fully specified
- Backward compatibility is not yet guaranteed

Feedback and discussion are expected and encouraged during this phase.

---

## Participation

Discussion, feedback, and proposals are handled through GitHub Issues.

👉 Open a new issue:  
https://github.com/Abrasel-Nacional/opendelivery-v2/issues/new

The project backlog and ongoing work are tracked in the official GitHub Project:

👉 https://github.com/orgs/Abrasel-Nacional/projects/5

---

## License

Open Delivery is licensed under the Apache License 2.0.
