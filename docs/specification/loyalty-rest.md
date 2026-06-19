# Loyalty - REST Binding

This document specifies the HTTP/REST binding for the [Loyalty Extension](./loyalty.md).

## Protocol Fundamentals

### Discovery

Participants advertise Loyalty REST availability through discovery metadata,
including extension name, transport (`rest`), and endpoint base URL.

### Authentication

All endpoints require `bearerAuth` (HTTP Bearer JWT).

### Content Type

- Request content type: `application/json`
- Response content type: `application/json`

### Base URL

Example base URL from committee draft:

`https://api.opendelivery.io/v2`

## Operations

| Operation | Method | Path | Entity | Description |
|---|---|---|---|---|
| [List Customer Loyalty Accounts](#list-customer-loyalty-accounts) | GET | `/customers/{customerId}/loyalty/accounts` | Account | Retrieve loyalty accounts for a customer |
| [Get Customer Loyalty Account](#get-customer-loyalty-account) | GET | `/customers/{customerId}/loyalty/accounts/{accountId}` | Account | Retrieve a specific loyalty account details |
| [List Customer Loyalty Transactions](#list-customer-loyalty-transactions) | GET | `/customers/{customerId}/loyalty/transactions` | Transaction | Retrieve loyalty transaction history |
| [List Loyalty Rewards](#list-loyalty-rewards) | GET | `/loyalty/rewards` | Reward | Retrieve available rewards catalog |
| [Create Customer Loyalty Redemption](#create-customer-loyalty-redemption) | POST | `/customers/{customerId}/loyalty/redemptions` | Redemption | Redeem a reward for a customer |
| [List Customer Coupons](#list-customer-coupons) | GET | `/customers/{customerId}/coupons` | Coupon | Retrieve coupons for a customer |
| [Get Customer Coupon](#get-customer-coupon) | GET | `/customers/{customerId}/coupons/{couponId}` | Coupon | Retrieve a specific coupon details |

### List Customer Loyalty Accounts

Method and path: `GET /customers/{customerId}/loyalty/accounts`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `customerId` | string | Yes | Customer identifier |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | Loyalty | Yes | Loyalty account summary |

#### Example

=== "Request"
    ```http
    GET /customers/cust-001/loyalty/accounts HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    {
      "customerId": "cust-001",
      "merchantId": "merchant-01",
      "programId": "program-default",
      "summary": {
        "pointsAvailable": 1250,
        "pointsPending": 120,
        "pointsExpiringSoon": 50
      }
    }
    ```

### Get Customer Loyalty Account

Method and path: `GET /customers/{customerId}/loyalty/accounts/{accountId}`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `customerId` | string | Yes | Customer identifier |
| `accountId` | string | Yes | Loyalty account identifier |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | Loyalty | Yes | Loyalty account payload |

#### Example

=== "Request"
    ```http
    GET /customers/cust-001/loyalty/accounts/acc-001 HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    {
      "customerId": "cust-001",
      "merchantId": "merchant-01",
      "programId": "program-default",
      "tier": {
        "code": "gold",
        "name": "Gold"
      },
      "summary": {
        "pointsAvailable": 1250,
        "pointsPending": 120,
        "pointsExpiringSoon": 50
      }
    }
    ```

### List Customer Loyalty Transactions

Method and path: `GET /customers/{customerId}/loyalty/transactions`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `customerId` | string | Yes | Customer identifier |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[LoyaltyTransaction] | Yes | Loyalty transaction list |

#### Example

=== "Request"
    ```http
    GET /customers/cust-001/loyalty/transactions HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    [
      {
        "id": "txn-001",
        "accountId": "acc-001",
        "type": "earn",
        "amount": 100,
        "relatedOrderId": "ord-001",
        "occurredAt": "2026-06-01T12:00:00Z"
      }
    ]
    ```

### List Loyalty Rewards

Method and path: `GET /loyalty/rewards`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| query params | object | No | Optional implementation-specific filters |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Reward] | Yes | Rewards catalog |

#### Example

=== "Request"
    ```http
    GET /loyalty/rewards HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    [
      {
        "id": "reward-001",
        "name": "R$10 Off",
        "cost": 1000,
        "accountType": "points",
        "available": true
      }
    ]
    ```

### Create Customer Loyalty Redemption

Method and path: `POST /customers/{customerId}/loyalty/redemptions`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `customerId` | string | Yes | Customer identifier |
| body | RedemptionRequest | Yes | Redemption request payload |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | RedemptionResult | Yes | Redemption result payload |
| status | integer | Yes | `201` on success |

#### Example

=== "Request"
    ```http
    POST /customers/cust-001/loyalty/redemptions HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Content-Type: application/json

    {
      "rewardId": "reward-001",
      "quantity": 1
    }
    ```

=== "Response (201)"
    ```json
    {
      "redemptionId": "red-001",
      "transactionId": "txn-009",
      "coupon": {
        "id": "coupon-001",
        "code": "SAVE10",
        "type": "discount",
        "value": 10,
        "currency": "BRL",
        "status": "available",
        "source": "loyalty",
        "customerId": "cust-001"
      }
    }
    ```

### List Customer Coupons

Method and path: `GET /customers/{customerId}/coupons`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `customerId` | string | Yes | Customer identifier |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Coupon] | Yes | Coupon list |

#### Example

=== "Request"
    ```http
    GET /customers/cust-001/coupons HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    [
      {
        "id": "coupon-001",
        "code": "SAVE10",
        "type": "discount",
        "value": 10,
        "currency": "BRL",
        "status": "available",
        "source": "loyalty",
        "customerId": "cust-001"
      }
    ]
    ```

### Get Customer Coupon

Method and path: `GET /customers/{customerId}/coupons/{couponId}`

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `customerId` | string | Yes | Customer identifier |
| `couponId` | string | Yes | Coupon identifier |

#### Output Schema

| Field | Type | Required | Description |
|---|---|---|---|
| body | Coupon | Yes | Coupon payload |

#### Example

=== "Request"
    ```http
    GET /customers/cust-001/coupons/coupon-001 HTTP/1.1
    Host: api.opendelivery.io
    Authorization: Bearer {token}
    Accept: application/json
    ```

=== "Response (200)"
    ```json
    {
      "id": "coupon-001",
      "code": "SAVE10",
      "type": "discount",
      "value": 10,
      "currency": "BRL",
      "status": "available",
      "source": "loyalty",
      "customerId": "cust-001"
    }
    ```

## Error Handling

UCP-style two-layer interpretation applies: transport-level failures use HTTP status,
while business semantics are expressed by endpoint responses and payloads.

### Transport Errors

| HTTP | Description |
|---|---|
| `400` | Bad request (defined in committee OpenAPI) |
| `401` | Unauthorized (auth policy) |
| `403` | Forbidden (authz policy) |
| `404` | Not found (resource path/ID resolution) |
| `500` | Internal server error |

### Business Outcomes

Business outcomes are represented by endpoint-specific success responses (`200`, `201`)
and response payloads (`Loyalty`, `LoyaltyTransaction`, `Reward`, `RedemptionResult`, `Coupon`).

## Entities

### Loyalty Response

| Field | Type | Required | Description |
|---|---|---|---|
| body | Loyalty | Yes | Loyalty account summary response |

### Loyalty Transactions Response

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[LoyaltyTransaction] | Yes | Loyalty transaction collection |

### Rewards Response

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Reward] | Yes | Reward collection |

### Coupons Response

| Field | Type | Required | Description |
|---|---|---|---|
| body | array[Coupon] | Yes | Coupon collection |

### Error Response (`BadRequest`)

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string | No | Machine-readable error code |
| `message` | string | No | Human-readable error message |

## Conformance

A conforming Loyalty REST implementation MUST:

1. Implement all advertised Loyalty operations in discovery metadata.
2. Enforce Bearer authentication on all operations.
3. Accept and return JSON payloads as defined by Loyalty schemas.
4. Preserve path-scoped customer semantics for account, transaction, redemption, and coupon operations.
5. Return status codes consistent with this binding and committee OpenAPI.
