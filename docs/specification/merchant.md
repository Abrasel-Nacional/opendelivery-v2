# Merchant Capability

- **Capability name:** `merchant`

## Overview

Merchant Capability defines merchant identity, operational services, and catalog structures used
across the ecosystem.

Every merchant record MUST include a stable identifier to support deterministic cross-system
reconciliation.

### Scope

Merchant Capability covers:

- Merchant registration and descriptive metadata
- Operational services context
- Catalog composition: menus, categories, items, offers, and options
- Availability references for catalog usage

Merchant Capability does not cover:

- Order lifecycle management
- Delivery execution orchestration
- CRM and loyalty workflows

## Participants

| Participant | Provider | Consumer |
|---|---|---|
| **Software Service** | Exposes merchant and catalog data and change feeds | Consumes reconciliation acknowledgements when applicable |
| **Ordering Application** | Exposes optional consumer callbacks when agreed | Consumes merchant/catalog snapshots and updates |
| **Logistics Service** | Exposes optional logistics constraints interface | Consumes merchant service and readiness context |

## Data Model

### Merchant

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Stable merchant identifier |
| `name` | string | YES | Merchant display name |
| `status` | string | YES | Operational status (`ONLINE`, `OFFLINE`, `SUSPENDED`) |
| `address` | object | YES | Physical location address |
| `contacts` | array[object] | NO | Contact channels |
| `categories` | array[string] | NO | Business category tags |
| `updatedAt` | string | NO | Last update timestamp (RFC 3339) |

### Menu

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Menu identifier |
| `merchantId` | string | YES | Owning merchant identifier |
| `name` | string | YES | Menu display name |
| `categories` | array[Category] | YES | Ordered list of item categories |
| `availability` | object | NO | Availability schedule reference |

### Category

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Category identifier |
| `name` | string | YES | Category display name |
| `items` | array[Item] | YES | Items in this category |

### Item

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Item identifier |
| `name` | string | YES | Item display name |
| `description` | string | NO | Item description |
| `price` | number | YES | Unit price in minor units (cents) |
| `imageUrl` | string | NO | Item image URI |
| `status` | string | YES | Availability status (`AVAILABLE`, `UNAVAILABLE`) |
| `optionGroups` | array[OptionGroup] | NO | Customization option groups |

### OptionGroup

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Option group identifier |
| `name` | string | YES | Option group display name |
| `min` | number | YES | Minimum selections required |
| `max` | number | YES | Maximum selections allowed |
| `options` | array[Option] | YES | Available options |

### Option

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | YES | Option identifier |
| `name` | string | YES | Option display name |
| `price` | number | YES | Additional price in minor units (cents) |
| `status` | string | YES | Availability status (`AVAILABLE`, `UNAVAILABLE`) |

## Operations

| Operation | Provider | Consumer | Description |
|---|---|---|---|
| `getMerchant` | Software Service | Ordering Application | Retrieve merchant metadata |
| `getMenu` | Software Service | Ordering Application | Retrieve full menu snapshot |
| `getMenuItem` | Software Service | Ordering Application | Retrieve a single item |
| `updateMerchantStatus` | Software Service | Ordering Application | Signal merchant operational status change |

For transport-specific details, see [REST Binding — Merchant](./merchant-rest.md).

## Example

```json
{
  "id": "merchant-001",
  "name": "Burger House",
  "status": "ONLINE",
  "address": {
    "street": "Av. Paulista, 1000",
    "city": "São Paulo",
    "state": "SP",
    "country": "BR",
    "postalCode": "01310-100"
  }
}
```
