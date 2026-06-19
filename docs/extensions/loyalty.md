# Loyalty Extension (Customer)

!!! warning "Work in Progress"
    This extension is currently under committee review. The content on this page is a placeholder and will be expanded once normative decisions are finalized.

## 1. Overview

Loyalty Extension expands Customer Capability with interoperability for loyalty identity, accrual, redemption, and coupon/voucher validation contexts.

## 2. Scope and Extensions

This extension covers:

- Loyalty account identification and balance inquiry
- Point or credit accumulation linked to orders
- Redemption of rewards at checkout
- Coupon and voucher validation and application

This extension does not cover:

- Program configuration or tier management (platform-internal)
- Financial settlement of redeemed rewards (out of scope)
- Marketing campaign orchestration

Loyalty is an extension of Customer Capability and MUST follow Customer capability boundaries.

Current sub-extensions: none.

## 3. Players

- `ORDERING_APPLICATION`
- `CRM_SOFTWARE_SERVICE`
- `LOYALTY_SOFTWARE_SERVICE` (when loyalty is a dedicated system)

### Provider/Consumer Mapping

| participant | typical role as Provider | typical role as Consumer |
|---|---|---|
| `LOYALTY_SOFTWARE_SERVICE` | Exposes balance, accrual, redemption, and coupon validation interfaces | Consumes order context for accrual/reversal |
| `CRM_SOFTWARE_SERVICE` | Exposes customer relationship context for loyalty enrichment | Consumes loyalty outcomes for customer intelligence |
| `ORDERING_APPLICATION` | Exposes optional callback channels when agreed | Consumes loyalty validation and redemption outcomes |

## 4. Interaction Between Players

Typical interaction model:

1. Ordering side identifies the loyalty account in a compliant way.
2. Loyalty service validates eligibility, balances, and redemption constraints.
3. Order confirmation triggers accrual and/or redemption registration.
4. Customer profile may be enriched in CRM with loyalty outcomes.

Integrations SHOULD support both synchronous validation and asynchronous confirmation events for accrual/reversal.

## 5. Flows (Statuses and Events)

Illustrative loyalty states:

- `ENROLLED`
- `ACTIVE`
- `SUSPENDED`

Illustrative loyalty events:

- `loyalty.account_linked`
- `loyalty.points_accrued`
- `loyalty.points_redeemed`
- `loyalty.redemption_reversed`

Reward and coupon events MUST be traceable to customer and order references when applicable.

## 6. Discovery / Well-Known Configuration

Participants supporting loyalty behavior SHOULD declare loyalty extension support under Customer capability metadata in discovery.

Declaration SHOULD include:

- Supported operation groups (balance, accrual, redemption, coupon validation)
- Supported channels and timing mode (real-time/deferred)
- Event support for accrual/redemption outcomes

## 7. Authorization

Loyalty operations require authenticated calls and scope enforcement.

Recommended minimum scope families:

- `customer.loyalty.read`
- `customer.loyalty.write`
- `customer.coupon.validate`

## 8. Operations

Illustrative operation set (subject to committee finalization):

- `getLoyaltyBalance`
- `registerLoyaltyAccrual`
- `redeemLoyaltyReward`
- `validateCoupon`

## Pending Topics

The following topics are open for committee decision:

- Loyalty account linking model (CPF-based vs. platform token)
- Real-time vs. deferred point accumulation
- Multi-program support per customer
- Coupon validation timing (pre-checkout vs. order confirmation)

## Out of Scope

- Loyalty program administration interfaces
- Partner-specific reward catalogs
