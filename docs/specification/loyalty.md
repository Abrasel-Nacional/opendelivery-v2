# Loyalty Extension

!!! info "Extension"
    Loyalty extends the [Customer Capability](./customer.md). It MUST NOT be used independently.

- **Capability name:** `loyalty`
- **Extends:** `customer`

## Overview

Loyalty Extension standardizes transport for loyalty account visibility, reward catalog,
redemptions, customer coupons, and loyalty transaction history.

It does not standardize internal program policy (accrual logic, tier policy, expiration rules,
or campaign strategy), only the interoperability contract.

## Schema Baseline (Aligned with Committee OpenAPI)

| Schema | Type | Required | Description |
|---|---|---|---|
| `Loyalty` | object | NO | Loyalty account summary by customer/program |
| `LoyaltyTransaction` | object | NO | Loyalty movement (`earn`, `burn`, `expire`, `adjust`) |
| `Reward` | object | NO | Redeemable reward catalog item |
| `RedemptionRequest` | object | NO | Request payload for reward redemption |
| `RedemptionResult` | object | NO | Result payload for reward redemption |
| `Coupon` | object | NO | Coupon entity reused by loyalty and campaigns |

### Loyalty Schema Highlights

| Field | Type | Required | Description |
|---|---|---|---|
| `Loyalty.customerId` | string | NO | Customer reference |
| `Loyalty.programId` | string | NO | Loyalty program reference |
| `Loyalty.summary.pointsAvailable` | integer | NO | Available points balance |
| `Loyalty.summary.pointsPending` | integer | NO | Pending points |
| `Loyalty.summary.pointsExpiringSoon` | integer | NO | Points close to expiration |
| `LoyaltyTransaction.type` | string | NO | `earn`, `burn`, `expire`, `adjust` |
| `Reward.accountType` | string | NO | `points` or `cashback` |
| `Coupon.status` | string | NO | Coupon lifecycle state |

## Operations

| Operation | Provider | Consumer | Description |
|---|---|---|---|
| `listCustomerLoyaltyAccounts` | Origin Platform | CRM Software Service | List customer loyalty accounts |
| `getCustomerLoyaltyAccount` | Origin Platform | CRM Software Service | Retrieve specific loyalty account |
| `listCustomerLoyaltyTransactions` | Origin Platform | CRM Software Service | Retrieve loyalty transaction history |
| `listLoyaltyRewards` | Origin Platform | CRM Software Service | Retrieve rewards catalog |
| `createCustomerLoyaltyRedemption` | CRM Software Service | Origin Platform | Request reward redemption |
| `listCustomerCoupons` | Origin Platform | CRM Software Service | Retrieve customer coupons |
| `getCustomerCoupon` | Origin Platform | CRM Software Service | Retrieve single customer coupon |

For transport-specific details, see [REST Binding - Loyalty](./loyalty-rest.md).
