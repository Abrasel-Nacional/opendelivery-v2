# Merchant Capability

## 1. Overview

Merchant Capability defines merchant identity, service context, and catalog publication structures used by the ecosystem.

Every merchant record MUST include a stable identifier to support deterministic cross-system reconciliation.

## 2. Scope and Extensions

Merchant Capability covers:

- Merchant registration and descriptive metadata
- Operational services context
- Catalog composition entities (menus, categories, items, offers, options)
- Availability references for catalog usage

Merchant Capability does not cover:

- Order lifecycle management
- Delivery execution orchestration
- CRM/loyalty relationship workflows

Current extension set: no Merchant extensions are defined in this version.

## 3. Players

- `SOFTWARE_SERVICE`: source of truth for merchant and catalog publication
- `ORDERING_APPLICATION`: consumes merchant/catlog data for ordering interfaces
- `DELIVERY_PLATFORM` (optional): consumes service and readiness context for delivery features

Consumers MUST treat merchant data as authoritative only for declared merchant scope.

### Provider/Consumer Mapping

| participant | typical role as Provider | typical role as Consumer |
|---|---|---|
| `SOFTWARE_SERVICE` | Exposes merchant/catalog data and change feeds | Consumes reconciliation acknowledgements when used |
| `ORDERING_APPLICATION` | Exposes optional consumer callbacks when agreed | Consumes merchant/catalog snapshots and updates |
| `DELIVERY_PLATFORM` | Exposes optional logistics constraints interface | Consumes merchant service/readiness context |

## 4. Interaction Between Players

Typical interaction pattern:

1. Source participant publishes merchant snapshot or delta.
2. Consumer participants ingest and validate structure and references.
3. Updates are propagated as asynchronous change signals.

Update signaling MUST identify changed entity types to allow partial refresh strategies.

## 5. Flows (Statuses and Events)

Merchant catalog exchange is snapshot/delta oriented.

Flow expectations:

- Initial bootstrap of merchant and catalog entities
- Incremental update notifications for changed entities
- Consumer-side reconciliation preserving referential integrity

Implementations MUST preserve referential integrity between menus, categories, items, offers, and options through all update flows.

## 6. Discovery / Well-Known Configuration

Participants exposing merchant data MUST declare capability name `merchant` in discovery.

Discovery declaration SHOULD include:

- Supported operation mode (push/pull/hybrid)
- Merchant endpoint base URL for transport binding
- Snapshot and/or incremental update support

## 7. Authorization

Merchant exchange operations require authenticated access.

Implementations MUST enforce scope-based authorization as defined in [Authentication and Authorization](authentication.md).

Recommended minimum scope families:

- `merchant.read`
- `merchant.write`
- `merchant.events.write`

## 8. Operations

Reference operations include merchant publication, merchant query, and change notification workflows. Concrete endpoint contracts are defined in REST API Binding pages.

### Merchant Object Fields

| name | type | required | description |
|---|---|---|---|
| `merchant.id` | string | YES | Merchant unique identifier |
| `merchant.basicInfo` | object | YES | Registration and descriptive metadata |
| `merchant.services` | array[object] | YES | Service operation contexts |
| `merchant.menus` | array[object] | YES | Menu entities |
| `merchant.categories` | array[object] | YES | Category entities |
| `merchant.items` | array[object] | YES | Item entities |
| `merchant.itemOffers` | array[object] | YES | Offer entities |
| `merchant.optionGroups` | array[object] | YES | Option group entities |
| `merchant.options` | array[object] | YES | Option entities |
| `merchant.availabilities` | array[object] | YES | Availability entities |

### Merchant Object Example

```json
{
  "merchant": {
    "id": "merchant-123",
    "basicInfo": {},
    "services": [],
    "menus": [],
    "categories": [],
    "items": [],
    "itemOffers": [],
    "optionGroups": [],
    "options": [],
    "availabilities": []
  }
}
```
