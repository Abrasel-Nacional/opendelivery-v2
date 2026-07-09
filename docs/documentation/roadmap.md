# Roadmap

<div class="od-api-callout">
  <p>Roadmap do protocolo. Continue a jornada ou abra o contrato técnico.</p>
  <a href="../guide/changelog/">Changelog →</a>
</div>

This page outlines areas under active development and future planned work for the Open Delivery Protocol.

!!! note "Work in progress"
    This roadmap reflects current committee priorities. Items may be added, deferred, or reprioritized as decisions are finalized.

## Active Work

### Orders Capability
- State machine formalization and normative transition guards
- Cancellation flow improvements and rejection reason vocabulary
- Idempotency rules consolidation

### Merchant Capability
- Catalog schema normalization and required field alignment
- Menu availability and scheduling model

### Indoor Extension
- Account lifecycle formal state machine
- Partial payment model normalization
- Indoor event vocabulary

### Customer Capability
- Review ingestion model (under committee review)
- Customer event classification

### Loyalty Extension
- Full normative content (under committee review)

## Planned

- **Logistics Capability** — Delivery quote, dispatch, and tracking normalization
- **Webhooks and event contracts** — Normative webhook payload shapes per capability
- **Error taxonomy** — Consolidated error code vocabulary per capability
- **Versioning policy** — Date-based versioning rules and compatibility declarations

## Out of Scope

The following topics are explicitly outside the current ODP scope:

- Reservation and waiting-list workflows
- Table occupancy and seating mapping
- Campaign orchestration internals
- Financial settlement of loyalty rewards
- Country-specific fiscal modules
