# Roadmap

This page outlines areas under active development and future planned work for the Open Delivery Protocol.

!!! note "Work in progress"
    This roadmap reflects current committee priorities. Items may be added, deferred, or reprioritized as decisions are finalized.

## Active Work

### Orders Capability
- Status vs events, polling/webhook, and V1→V2 narrative formalized in guide + API Spec (RC)
- Lifecycle duplicate-call behavior (default: `202` when already in target state)
- Remaining: final deprecation decision on `DISPATCHED`; cancellation reason vocabulary polish

### Merchant Capability
- Store + catalog docs and API Spec aligned to Orders-quality structure (RC)
- Remaining: catalog delta notifications (out of MVP); optional multi-level optionals polish

### Indoor Extension
- Account lifecycle formal state machine
- Partial payment model normalization
- Indoor event vocabulary

### Customer capability
- Review ingestion model (under committee review)
- Customer event classification
- Loyalty module normative content (under committee review)

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

<div class="od-related">
  <p class="od-related__label">Related</p>
  <ul class="od-related__list">
    <li><a href="../guide/changelog.md">Changelog</a> — what is already in the RC</li>
    <li><a href="../guide/migration-v1-v2.md">Migration V1→V2</a></li>
    <li><a href="../reference/index.md">API reference</a></li>
  </ul>
</div>
