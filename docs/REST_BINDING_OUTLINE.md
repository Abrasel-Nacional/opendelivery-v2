# REST/HTTP Binding Outline

This document provides an outline of the REST/HTTP Transport Binding for Open Delivery v2.

The full binding specification (with complete schemas, examples, and implementation guidance) is under development.

---

## Overview

The REST/HTTP Binding translates Open Delivery Protocol concepts into standardized HTTP endpoints and JSON payloads.

**Status:** Outline in progress  
**Based on:** v1 API + v2 Protocol concepts  
**Versioning:** Will be independently versioned (e.g., REST/HTTP Binding v1.0)

---

## Payload Documentation Rule (REST)

All REST payloads in this binding should be documented using:

1. A field table with:
  - `name`
  - `required`
  - `description`
2. A JSON payload example

REST payloads must be derived from capability and extension documentation.

For indoor scenarios, REST payloads must follow the Indoor Extension draft rules.

---

## Binding Organization

### 1. Authentication & Security

**Software-Level Authentication (Normative)**

- Credentials are issued per integrating **software system**, not per merchant.
- Access MUST be scoped by functional domain (e.g., orders, menus, logistics).
- Authorization between software and merchant MUST be explicit, but the consent/authorization flow is implementation-specific.

**Token Endpoint**
```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id={clientId}
&client_secret={clientSecret}
&scope=orders menus logistics

← 200 OK
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "orders menus logistics"
}
```

**Security Headers** (All requests)
```
Authorization: Bearer {access_token}
X-API-Key: {apiKey}  // Alternative auth
X-Merchant-Id: {merchantId}
X-App-Id: {appId}
X-App-Signature: {hmac256(body, secret)}  // For webhooks
```

**Scopes by Domain (Example)**

- `orders` - Order creation, updates, and events
- `menus` - Merchant and menu data access
- `logistics` - Delivery and tracking operations

Endpoints SHOULD declare required scopes in the binding specification.

---

### 2. Merchant Endpoints

#### Retrieve Merchant Information
```
GET /v1/merchant/{merchantId}

← 200 OK
{
  "id": "merchant-123",
  "name": "Pizza Palace",
  "document": "12345678000100",
  "contact": {
    "phone": "+5511999999999",
    "email": "contact@pizzapalace.com",
    "website": "https://pizzapalace.com"
  },
  "services": [
    {
      "id": "service-1",
      "type": "DELIVERY",
      "area": {...},
      "hours": {...}
    }
  ],
  "menus": [...],
  "ttl": 3600
}
```

#### Retrieve Merchant Status
```
GET /v1/merchant/{merchantId}/status

← 200 OK
{
  "merchantId": "merchant-123",
  "status": "ACTIVE",  // ACTIVE, CLOSED, PAUSED, OFFLINE
  "lastUpdate": "2026-03-09T14:30:00Z",
  "capabilities": {
    "deliveryAvailable": true,
    "takeoutAvailable": true,
    "onPremiseAvailable": false,
    "loyaltyEnabled": true,
    "realTimeTracking": true
  }
}
```

#### Register/Update Merchant Endpoint
```
PUT /v1/merchantOnboarding

{
  "merchantId": "merchant-123",
  "baseUrl": "https://merchant-system.com",
  "webhookUrl": "https://merchant-system.com/webhooks/orders",
  "contact": {
    "name": "Integration Manager",
    "email": "integration@merchant.com"
  }
}

← 200 OK
{
  "status": "REGISTERED",
  "merchantId": "merchant-123",
  "orderingAppMerchantId": "app-merchant-456"
}
```

---

### 3. Order Endpoints

#### Create Order
```
POST /v1/orders

{
  "orderId": "order-abc-123",
  "merchant": {
    "id": "merchant-123",
    "name": "Pizza Palace"
  },
  "profile": "DELIVERY",  // DELIVERY, TAKEOUT, INDOOR
  "customer": {
    "id": "cust-456",
    "name": "John Doe",
    "phone": "+5511988888888",
    "documentNumber": "12345678900"
  },
  "items": [
    {
      "id": "item-1",
      "name": "Pizza Margherita",
      "quantity": 2,
      "unitPrice": {"value": 34.90, "currency": "BRL"},
      "totalPrice": {"value": 69.80, "currency": "BRL"},
      "options": [...]
    }
  ],
  "delivery": {
    "address": {
      "street": "Rua das Flores",
      "number": "123",
      "city": "São Paulo",
      "state": "SP",
      "neighborhood": "Moema",
      "postalCode": "04550-100",
      "coordinates": {
        "latitude": -23.5874,
        "longitude": -46.6761
      }
    },
    "expectedDeliveryTime": "2026-03-09T15:30:00Z",
    "additionalInfo": "Apartment 42, call when arriving"
  },
  "pricing": {
    "subtotal": {"value": 69.80, "currency": "BRL"},
    "deliveryFee": {"value": 8.90, "currency": "BRL"},
    "discount": {"value": 0, "currency": "BRL"},
    "total": {"value": 78.70, "currency": "BRL"}
  },
  "timing": "INSTANT",  // INSTANT or SCHEDULED
  "scheduledTime": "2026-03-09T15:30:00Z"
}

← 201 Created
{
  "orderId": "order-abc-123",
  "state": "CREATED",
  "createdAt": "2026-03-09T14:30:00Z"
}
```

#### Create INDOOR Order (Indoor Example)

Indoor draft field reference (inside `order.indoor`):

| name | type | required | description |
|---|---|---|---|
| `operationMode` | string | YES | Indoor operation mode (`MESA`, `COMANDA`, `BALCAO`) |
| `originChannel` | object | YES | Origin context of in-person interaction |
| `consumptionType` | string | NO | Consumption intent (`CONSUMIR_NO_LOCAL`, `LEVAR`) |
| `conta` | object | NO | Account linkage for open/incremental indoor flow |
| `tipoComanda` | string | NO | Tab token/type used by local operation |
| `localDeEntrega` | object | NO | On-premise delivery location context |
| `service` | object | NO | Staff/service metadata |
| `notifications` | object | NO | Notification metadata |
| `fiscal` | object | NO | Fiscal metadata under discussion |

```
POST /v1/orders

{
  "orderId": "order-indoor-001",
  "profile": "INDOOR",
  "merchant": {
    "id": "merchant-123",
    "name": "Pizza Palace"
  },
  "items": [
    {
      "id": "item-1",
      "name": "Pizza Margherita",
      "quantity": 1,
      "unitPrice": {"value": 42.90, "currency": "BRL"},
      "totalPrice": {"value": 42.90, "currency": "BRL"}
    }
  ],
  "indoor": {
    "operationMode": "MESA",
    "originChannel": {
      "type": "QR_CODE",
      "id": "qr-session-9182",
      "obs": "mesa 12"
    },
    "consumptionType": "CONSUMIR_NO_LOCAL",
    "conta": {
      "id": "conta-12-20260310",
      "label": "Mesa 12"
    },
    "tipoComanda": "QR_SESSION",
    "localDeEntrega": {
      "id": "table-12",
      "label": "Mesa 12",
      "sector": "SALAO_A",
      "seat": {
        "id": "seat-03",
        "label": "Lugar 3"
      }
    },
    "service": {
      "waiterCode": "W102",
      "waiterName": "Carla",
      "peopleCount": 4
    },
    "notifications": {
      "whatsAppId": "+5511999999999"
    },
    "fiscal": {
      "shouldIssueDocument": true,
      "issuer": "PDV",
      "documentStatus": "PENDENTE",
      "printDocument": false,
      "paymentNSURequiredForNFCE": true
    }
  },
  "pricing": {
    "subtotal": {"value": 42.90, "currency": "BRL"},
    "discount": {"value": 0, "currency": "BRL"},
    "total": {"value": 42.90, "currency": "BRL"}
  },
  "timing": "INSTANT"
}

← 201 Created
{
  "orderId": "order-indoor-001",
  "state": "CREATED",
  "profile": "INDOOR",
  "createdAt": "2026-03-10T13:10:00Z"
}
```

#### Get Order Details
```
GET /v1/orders/{orderId}

← 200 OK
{
  "orderId": "order-abc-123",
  "state": "CONFIRMED",
  "profile": "DELIVERY",
  "merchant": {...},
  "customer": {...},
  "items": [...],
  "delivery": {...},
  "pricing": {...},
  "createdAt": "2026-03-09T14:30:00Z",
  "confirmedAt": "2026-03-09T14:32:00Z"
}
```

#### Update Order Details
```
PATCH /v1/orders/{orderId}/details

{
  "customer": {
    "phone": "+5511987654321"  // Updated phone
  },
  "delivery": {
    "additionalInfo": "Updated instructions"
  }
}

← 200 OK
{
  "orderId": "order-abc-123",
  "state": "CREATED"  // Still in CREATED state
}
```

#### Confirm Order
```
POST /v1/orders/{orderId}/confirm

{
  "metadata": {
    "confirmationTime": "2026-03-09T14:32:00Z",
    "estimatedPrepTime": 25
  }
}

← 200 OK
{
  "orderId": "order-abc-123",
  "state": "CONFIRMED",
  "timestamp": "2026-03-09T14:32:00Z"
}

← 400 Bad Request (Order already confirmed)
{
  "error": "ORDER_ALREADY_CONFIRMED",
  "message": "This order has already been confirmed"
}
```

#### Mark Order Ready for Pickup
```
POST /v1/orders/{orderId}/readyForPickup

{
  "pickupArea": "COUNTER_A",  // Required for TAKEOUT profile
  "estimatedWaitTime": 5
}

← 200 OK
{
  "orderId": "order-abc-123",
  "state": "READY_FOR_PICKUP",
  "timestamp": "2026-03-09T14:45:00Z",
  "profile": "DELIVERY"
}
```

#### Dispatch Order
```
POST /v1/orders/{orderId}/dispatch

{
  "dispatchTime": "2026-03-09T14:50:00Z",
  "metadata": {}
}

← 200 OK
{
  "orderId": "order-abc-123",
  "state": "DISPATCHED",
  "timestamp": "2026-03-09T14:50:00Z"
}
```

#### Confirm Order Delivered
```
POST /v1/orders/{orderId}/delivered

{
  "deliveryTime": "2026-03-09T15:30:00Z"
}

← 200 OK
{
  "orderId": "order-abc-123",
  "state": "DELIVERED",
  "timestamp": "2026-03-09T15:30:00Z"
}
```

#### Request Cancellation
```
POST /v1/orders/{orderId}/requestCancellation

{
  "reason": "Restaurant out of items",
  "code": "UNAVAILABLE_ITEMS"  // From enum of cancellation reasons
}

← 202 Accepted
{
  "status": "CANCELLATION_REQUESTED"
}
```

#### Accept Cancellation
```
POST /v1/orders/{orderId}/acceptCancellation

← 200 OK
{
  "orderId": "order-abc-123",
  "state": "CANCELLED",
  "timestamp": "2026-03-09T14:35:00Z"
}
```

#### Deny Cancellation
```
POST /v1/orders/{orderId}/denyCancellation

{
  "reason": "Order already being prepared"
}

← 200 OK
{
  "orderId": "order-abc-123",
  "state": "CONFIRMED",  // Order continues
  "message": "Cancellation denied"
}
```

---

### 4. Event Polling

#### Poll for Events
```
GET /v1/events:polling
?limit=10&aggregateId=merchant-123

← 200 OK (Events available)
[
  {
    "id": "event-1",
    "type": "ORDER_CREATED",
    "aggregateId": "order-abc-123",
    "timestamp": "2026-03-09T14:30:00Z",
    "data": {
      "orderId": "order-abc-123",
      "merchantId": "merchant-123",
      "profile": "DELIVERY"
    }
  },
  {
    "id": "event-2",
    "type": "ORDER_READY_FOR_PICKUP",
    "aggregateId": "order-abc-123",
    "timestamp": "2026-03-09T14:45:00Z",
    "data": {}
  }
]

← 204 No Content (No events)
```

#### Acknowledge Events
```
POST /v1/events/acknowledgment

{
  "eventIds": ["event-1", "event-2"]
}

← 200 OK
{
  "acknowledged": 2
}
```

---

### 5. Logistics Endpoints

#### Check Delivery Availability
```
POST /v1/logistics/availability

{
  "merchantId": "merchant-123",
  "deliveryAddress": {
    "coordinates": {
      "latitude": -23.5874,
      "longitude": -46.6761
    }
  }
}

← 200 OK
{
  "available": true,
  "estimatedDeliveryTime": "2026-03-09T15:30:00Z",
  "pricing": {
    "deliveryFee": {"value": 8.90, "currency": "BRL"},
    "minOrderValue": {"value": 50.00, "currency": "BRL"}
  }
}

← 200 OK (Not available)
{
  "available": false,
  "reason": "Area outside service zone"
}
```

#### Create Delivery
```
POST /v1/logistics/delivery

{
  "orderId": "order-abc-123",
  "merchant": {
    "id": "merchant-123",
    "location": {
      "coordinates": {
        "latitude": -23.5874,
        "longitude": -46.6761
      }
    }
  },
  "customer": {
    "name": "John Doe",
    "phone": "+5511988888888"
  },
  "deliveryAddress": {
    "street": "Rua das Flores",
    "number": "123",
    "city": "São Paulo",
    "coordinates": {...}
  },
  "estimatedDeliveryTime": "2026-03-09T15:30:00Z"
}

← 201 Created
{
  "deliveryId": "delivery-xyz-789",
  "orderId": "order-abc-123",
  "state": "PENDING",
  "timestamp": "2026-03-09T14:50:00Z"
}

← 400 Bad Request (Area not served)
{
  "error": "DELIVERY_UNAVAILABLE",
  "message": "This address is outside service area"
}
```

#### Get Delivery Details
```
GET /v1/logistics/delivery/{orderId}

← 200 OK
{
  "deliveryId": "delivery-xyz-789",
  "orderId": "order-abc-123",
  "state": "IN_TRANSIT",
  "deliveryPerson": {
    "name": "Carlos",
    "phone": "+5511991234567"
  },
  "tracking": {
    "currentLocation": {
      "latitude": -23.5800,
      "longitude": -46.6700,
      "timestamp": "2026-03-09T15:15:00Z"
    },
    "estimatedArrival": "2026-03-09T15:25:00Z"
  },
  "events": [...]
}
```

#### Notify Ready for Pickup
```
POST /v1/logistics/readyForPickup/{orderId}

← 200 OK
{
  "deliveryId": "delivery-xyz-789",
  "status": "READY_TO_PICKUP"
}
```

#### Confirm Order Picked Up
```
POST /v1/logistics/orderPicked/{orderId}

{
  "timestamp": "2026-03-09T14:52:00Z"
}

← 200 OK
{
  "deliveryId": "delivery-xyz-789",
  "state": "PICKED_UP"
}
```

#### Confirm Delivery Completed
```
POST /v1/logistics/finishDelivery/{orderId}

{
  "deliveryTime": "2026-03-09T15:30:00Z",
  "confirmationCode": "ABC123"
}

← 200 OK
{
  "deliveryId": "delivery-xyz-789",
  "state": "DELIVERED"
}
```

#### Report Delivery Problem
```
POST /v1/logistics/handleProblem/{orderId}

{
  "problem": "Customer not found",
  "code": "CUSTOMER_UNAVAILABLE",
  "suggestedResolution": "REDELIVER_LATER"
}

← 200 OK
{
  "deliveryId": "delivery-xyz-789",
  "state": "PROBLEM_REPORTED",
  "nextAction": "AWAITING_MERCHANT_DECISION"
}
```

#### Cancel Delivery
```
POST /v1/logistics/cancel/{orderId}

{
  "reason": "Order cancelled by customer"
}

← 200 OK
{
  "deliveryId": "delivery-xyz-789",
  "state": "CANCELLED"
}
```

---

### 6. Webhook Endpoints (Receiver Implements)

#### Order Update Webhook
```
POST {yourBaseUrl}/v1/orderUpdate

Headers:
X-App-Id: ordering-app-123
X-App-MerchantId: merchant-123
X-App-Signature: {hmac256signature}

{
  "event": {
    "id": "event-123",
    "type": "ORDER_CONFIRMED",
    "timestamp": "2026-03-09T14:32:00Z",
    "orderId": "order-abc-123",
    "data": {
      "state": "CONFIRMED",
      "timestamp": "2026-03-09T14:32:00Z"
    }
  }
}

← 200 OK
(Empty body expected)
```

#### Delivery Update Webhook
```
POST {yourBaseUrl}/v1/deliveryUpdate

Headers:
X-App-Id: logistics-provider-456
X-App-Signature: {hmac256signature}

{
  "event": {
    "type": "DELIVERY_IN_TRANSIT",
    "timestamp": "2026-03-09T15:10:00Z",
    "orderId": "order-abc-123",
    "data": {
      "deliveryId": "delivery-xyz-789",
      "location": {...},
      "estimatedArrival": "2026-03-09T15:25:00Z"
    }
  }
}

← 200 OK
```

---

## Response Status Codes

```
2xx Success
  200 OK – Operation successful
  201 Created – Resource created
  202 Accepted – Request accepted for async processing
  204 No Content – Successful with no response body

4xx Client Error
  400 Bad Request – Invalid request data
  401 Unauthorized – Missing/invalid authentication
  403 Forbidden – Authenticated but not authorized
  404 Not Found – Resource not found
  409 Conflict – State conflict (e.g., order already confirmed)
  422 Unprocessable Entity – Request valid but semantically incorrect

5xx Server Error
  500 Internal Server Error
  503 Service Unavailable
```

---

## Error Response Format

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "orderId": "order-abc-123",
    "currentState": "CONFIRMED",
    "invalidTransition": "CONFIRMED -> CREATED"
  },
  "timestamp": "2026-03-09T14:35:00Z"
}
```

---

## Next Steps for Full Binding Specification

1. **Complete Endpoint Definitions**
   - All remaining endpoints detailed
   - All paths, methods, parameters documented

2. **JSON Schemas**
   - Request schema for each endpoint
   - Response schema for each endpoint
   - Event schemas for all event types
   - Error schema

3. **Implementation Guide**
   - Code examples (multiple languages)
   - Security best practices
   - Error handling strategies
   - Testing approaches

4. **OpenAPI Specification**
   - Machine-readable OpenAPI 3.0 spec
   - Swagger UI documentation
   - SDK generation support

5. **Examples & Test Cases**
   - Full order lifecycle example
   - Cancellation flow example
   - Error handling example
   - Webhook retry example

---
