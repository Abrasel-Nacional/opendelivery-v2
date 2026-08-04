# Menus

<p class="od-meta">
 <span class="od-badge od-badge--core">Capability</span>
 <span class="od-badge od-badge--code">merchant</span>
 <span class="od-badge">Merchant · catalog</span>
</p>

!!! note "API Spec"
    The implementable contract is in the **[Merchant API Spec](../reference/merchant.md)** — English only.

!!! note "Part of Merchant"
    **Menus** and **[Store data](merchant-store.md)** make up the `merchant` capability (see [overview](merchant.md)). They are not Discovery extensions.

This page covers the **catalog**: menus, categories, item-offers, option-groups, and options. Services and pause: [Store data](merchant-store.md).

---

## Breaking V1 → V2 (catalog)

!!! important "End of monolithic merchantUpdate"
    In V1, catalog updates used the **`merchantUpdate` / `menuUpdated`** webhook with a full payload. In V2 the normative path is **CRUD per entity** + **`GET …/snapshot`** for bootstrap.

| Field / model | V1 | V2 |
|---|---|---|
| Publication | Monolithic webhook | **CRUD + snapshot + PUT snapshot** |
| `optionPrice` | Optional | **Required** (0 if free) |
| Option `subtotal` | Present / confusing | **Removed** |
| `unityPrice` | Implicit | **Explicit** |
| `quantityAvailable` | — | **New** (operational) |
| Images in categories | No | **New** |
| Subcategories | No | **New** (category nesting) |

---

## Hierarchy

```
Merchant
├── Service (DELIVERY / TAKEOUT / INDOOR) → menuId
└── Menu
    └── Category
        ├── Subcategory (new — category nesting)
        └── ItemOffer
            └── OptionGroup (recursive)
                └── Option → OptionGroup…
```

A merchant may have **multiple menus**. Each [Service](merchant-store.md#serviço-service) may reference the active menu via `menuId`.

### Subcategories (new)

Categories can have subcategories (one level of nesting). Useful for structures like:
- Burgers > Classics, Specials
- Beverages > Hot, Cold

---

## Snapshot vs CRUD vs PUT

| Scenario | Approach | operationId |
|---|---|---|
| Initial load / full reconciliation | Full snapshot | `getMenuSnapshot` |
| Update entire catalog after major change | PUT full snapshot | `replaceMenuSnapshot` |
| List menus | Listing | `listMenus` |
| Price / name / availability | PATCH/PUT entity | `updateItemOffer`, … |
| New item / category / option | POST | `createItemOffer`, `createCategory`, `createOption` |
| Removal | DELETE (async `202`) | `deleteItemOffer`, … |

**New in V2**: Instead of the V1 pattern "update locally → notify via webhook → OA polling", use **PUT snapshot**:

```mermaid
sequenceDiagram
    participant SS as Software Service
    participant OA as Ordering Application

    Note over SS,OA: V2 — Push snapshot
    SS->>OA: PUT …/menus/{menuId}/snapshot
    OA-->>SS: 202 Accepted
    Note over OA: Process full catalog

    Note over SS,OA: Fallback — Pull snapshot
    OA->>SS: GET …/menus/{menuId}/snapshot
    SS-->>OA: 200 MenuSnapshot
    Note over OA: Bootstrap / error recovery
```

```
GET /merchants/{merchantId}/menus/{menuId}/snapshot
```

The snapshot returns the hierarchy (categories → item-offers → option-groups → options). It is the practical replacement for the V1 “full menu” **for bootstrap**, not a return of the monolithic webhook.

```mermaid
sequenceDiagram
 participant OA as Ordering Application
 participant SS as Software Service

 OA->>SS: GET …/menus/{menuId}/snapshot
 SS-->>OA: 200 MenuSnapshot
 Note over OA: local bootstrap
 OA->>SS: PATCH …/item-offers/{id} { unity_price }
 SS-->>OA: 202 Accepted
```

---

## ItemOffer and pricing

| Field | Required | Notes |
|---|---|---|
| `unityPrice` | YES | Base price in minor units |
| `quantityAvailable` | NO | **Operational** signal (e.g. 10 portions left). **Not** multi-channel stock. Omitted/`null` = no declared limit; `0` = unavailable |
| `status` | YES | `AVAILABLE` / `UNAVAILABLE` |
| `externalCode` | NO | POS internal code |
| `imageUrl` | NO | Item image URL (new in V2) |

---

## OptionGroup and Option (recursive)

OptionGroups may nest (e.g. size → doneness → sauce). Real-world depth is usually 2–3 levels.

!!! important "`optionPrice` required in V2"
    Every `Option` MUST have `optionPrice`. No extra cost: `0`. V1 option `subtotal` is removed — on the order, use `unityPrice` + sum of `optionPrice` (see [Orders](orders.md)).

---

## Operations map (catalog)

| Goal | operationId |
|---|---|
| List menus | `listMenus` |
| Snapshot (GET / PUT) | `getMenuSnapshot` · `replaceMenuSnapshot` |
| Categories | `listCategories` · `createCategory` · `replaceCategory` · `deleteCategory` |
| Subcategories | `listSubcategories` · `createSubcategory` · `replaceSubcategory` · `deleteSubcategory` |
| Item offers | `listItemOffers` · `createItemOffer` · `replaceItemOffer` · `updateItemOffer` · `deleteItemOffer` |
| Option groups | `listOptionGroups` · `createOptionGroup` · `replaceOptionGroup` · `deleteOptionGroup` |
| Options | `listOptions` · `createOption` · `replaceOption` · `deleteOption` |

---

## Sync model

Who is the **source of truth** for the catalog (POS vs originator) must be clear in Discovery and the commercial contract. The protocol:

- Does **not** reintroduce `merchantUpdate` as the V2 core path  
- Does **not** define a catalog-delta webhook in the MVP  
- Reconciliation: snapshot + CRUD  

Async mutations return **`202`**; synchronous creates may return **`201`** with a body.

---

## Checklists

!!! tip "Checklist — Ordering Application"
    - [ ] Bootstrap with snapshot  
    - [ ] Deltas via CRUD, not monolithic webhook  
    - [ ] Always expect `option_price`  
    - [ ] Treat `quantity_available` as a hint, not stock guarantee  

!!! tip "Checklist — Software Service"
    - [ ] Referential integrity menu → … → options  
    - [ ] `202` on async mutations  
    - [ ] No `merchantType` / no V1 option `subtotal`  

---

## Out of MVP

| Topic | Status |
|---|---|
| Catalog delta notification webhook | Not core-normative |
| Free-form custom fields | Out of MVP |
| Multi-channel stock control | Out of scope |

---

<div class="od-related">
  <p class="od-related__label">Related</p>
  <ul class="od-related__list">
    <li><a href="../reference/merchant.md">Merchant API Spec</a></li>
    <li><a href="merchant-store.md">Store data</a></li>
    <li><a href="merchant.md">Merchant overview</a></li>
    <li><a href="orders.md">Orders</a> — prices on the order</li>
  </ul>
</div>
