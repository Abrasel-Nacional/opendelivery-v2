# Authentication

Authentication is not a capability domain.

It is a protocol-wide mechanism that governs how participants obtain and present credentials to access protected operations. Authentication applies uniformly across all ODP capabilities — Merchant, Orders, Logistics, and others.

## Supported Authentication Models

ODP v2 supports three OAuth2 authentication models. The protocol does not mandate a single model for all ecosystems. Each platform MUST declare which model(s) it supports, and this declaration MUST be made explicit in the Discovery endpoint and during onboarding.

| model | identifier | status |
|---|---|---|
| Client Credentials per Merchant | `client_credentials_merchant` | Supported — legacy compatibility |
| Client Credentials per Application | `client_credentials_application` | Supported — recommended for new integrations |
| Authorization Code | `authorization_code` | Supported — optional, advanced use cases |

## Common Requirements

Regardless of the authentication model selected, every implementation MUST follow these rules:

1. The selected authentication model MUST be declared in the Discovery endpoint.
2. The authentication model used in production MUST be aligned explicitly during onboarding.
3. Supported scopes MUST be declared and consistent with the protocol capabilities used.
4. Merchant authorization rules MUST be explicit and discoverable.
5. Message signing, when supported, MUST be declared independently from the OAuth2 flow.
6. Event and request payloads MUST preserve merchant identification whenever required by the integration model.
7. Authentication material MUST be protected in transit and at rest.

## Model 1 — Client Credentials per Merchant

A separate `client_id`/`client_secret` pair is issued for each merchant.

This is the model used in ODP v1. It is supported in v2 for compatibility and migration scenarios.

The **Ordering Application** or **Logistics Service** MUST provide one `client_id` and `client_secret` for each individual merchant it works with, even if those merchants use the same **Software Service**.

**Credential acquisition:** The merchant **Software Service** retrieves the `client_id` and `client_secret` from the **Ordering Application** or **Logistics Service** and uses them to obtain an access token via the [token endpoint](https://spec.opendelivery.io/v2/openapi.yaml#operation/postOAuthToken).

**Token usage:** The `accessToken` obtained must be included in the `Authorization` header of every protected request:

```
Authorization: Bearer <accessToken>
```

The `expiresIn` field indicates the lifetime of the access token in seconds. The token MUST be cached and reused across requests until expiration — it MUST NOT be regenerated per request.

!!! note
    Refresh Token is not supported in this model.

**Capability scope mapping in v1:**

| capability | responsible for credentials |
|---|---|
| Orders, Merchant | Ordering Application |
| Logistics | Logistics Service |

**When to use:**

- Legacy migrations from v1
- Ecosystems where credentials are provisioned per merchant
- Scenarios where changing the operational credential model would produce excessive migration cost

**Trade-offs:**

- Requires repeated credential provisioning for each merchant
- Higher operational overhead for software providers managing many merchants
- Weaker scalability for multi-merchant integrations

## Model 2 — Client Credentials per Application

A single `client_id`/`client_secret` pair is issued for the software or application. Merchant access is determined separately through authorization rules, outside the token itself.

This is the recommended model for new integrations in ODP v2.

**Recommended complementary capabilities when using this model:**

- An endpoint to list merchants authorized for the application (e.g., `GET /merchants`)
- Authorization and deauthorization notification mechanisms
- Optional filtering by merchant in asynchronous event retrieval flows

**Trade-offs:**

- Requires an explicit merchant authorization strategy separate from the credential
- Merchants MUST NOT be embedded in the access token itself

## Model 3 — Authorization Code

Authorization Code is an optional OAuth2 model intended for scenarios where a **merchant owner or administrator** must explicitly grant an external application access to their data.

In this flow, the authorization is not implicit in the credential — it requires an interactive step. The typical flow is:

1. A **Software Service** initiates an authorization request for a specific merchant.
2. The merchant is redirected to an authorization interface hosted by the platform.
3. The merchant authenticates and explicitly approves or denies access for that application.
4. Upon approval, the platform issues an authorization code that the application exchanges for an access token.
5. The resulting token is scoped to that merchant and that application.

This model provides stronger governance over which applications can access a merchant's data, making it suitable for ecosystems where merchant consent must be auditable and revocable.

It is not mandatory for all integrations. When supported, it MUST be declared in the Discovery. The detailed OAuth2 Authorization Code flow parameters are defined in the [REST transport binding](https://spec.opendelivery.io/v2/openapi.yaml#operation/postOAuthAuthorize).

## API Key

Some endpoints may require authentication via API Key instead of OAuth2. When used, the key MUST be passed in the request header (see [`ApiKeyAuth` security scheme](https://spec.opendelivery.io/v2/openapi.yaml#/components/securitySchemes/ApiKeyAuth)):

| header | type | description |
|---|---|---|
| `X-API-KEY` | string | API key issued by the endpoint host to its clients |

The creation and management of the API key is the responsibility of the endpoint host. Each client may hold its own key. Operations that require API Key authentication declare this explicitly in their operation definition.

## Webhook Authentication

Webhooks do not use OAuth2. They use a **message signing** mechanism to allow the receiver to verify the authenticity of the sender.

When an **Ordering Application** sends a webhook event to a **Software Service**, the request MUST carry signed identity information — including the identity of the application, the merchant involved, and a cryptographic signature of the payload derived from the shared `client_secret`.

The **Software Service** is responsible for verifying the signature on every received webhook to confirm the request originates from a known and authorized **Ordering Application**.

The specific headers, signing algorithm, and acknowledgement rules are defined in the [REST transport binding](https://spec.opendelivery.io/v2/openapi.yaml#operation/postWebhookEvent).

## Scopes

Scopes in ODP v2 are organized by capability domain. Every protected operation declares which scope it requires.

| scope | domain |
|---|---|
| `od.orders` | Orders |
| `od.menu` | Menu / Catalog |
| `od.logistics` | Logistics |
| `od.crm` | CRM and Loyalty |
| `od.all` | All capabilities (full access) |

!!! note
    In ODP v1, a single scope `od.all` was used for all endpoints. Domain-scoped tokens are a v2 introduction and allow more granular access control.

Implementations MUST declare the scopes they support in the Discovery.

## Message Signing

Message signing is a security capability independent of the OAuth2 authentication model. It can be applied to requests and responses in both directions.

- Message signing is **not mandatory** for REST transport outside of webhooks.
- Support for message signing MUST be declared in the Discovery.
- When declared, the signing mechanism and applicable operations MUST be specified explicitly.

## Discovery Declaration

Every ODP v2 implementation MUST expose a [Discovery endpoint](https://spec.opendelivery.io/v2/openapi.yaml#operation/getDiscovery) that declares its authentication configuration. The following fields are required for authentication declaration:

| field | type | required | description |
|---|---|---|---|
| `authentication.supportedModels` | array[string] | YES | List of supported authentication model identifiers |
| `authentication.defaultModel` | string | YES | Default model to use during onboarding |
| `authentication.scopes` | array[string] | YES | List of supported scopes |
| `authentication.messageSigning.supported` | boolean | YES | Whether message signing is supported |
| `authentication.messageSigning.required` | boolean | YES | Whether message signing is required |
| `authentication.merchantDiscovery.supported` | boolean | YES | Whether a merchant listing endpoint is available |

**Example Discovery authentication block:**

```yaml
authentication:
  supportedModels:
    - client_credentials_application
    - client_credentials_merchant
  defaultModel: client_credentials_application
  scopes:
    - od.orders
    - od.menu
    - od.logistics
    - od.crm
    - od.all
  messageSigning:
    supported: true
    required: false
  merchantDiscovery:
    supported: true
```

## Operation-Level Authentication Declaration

Each capability operation MUST explicitly document:

- Whether the operation is public or protected
- Which scope is required when the operation is protected
- Which participant is expected to present the credential

This declaration appears in the operation definition, with a reference to this section.

## Relationship to Capabilities

Authentication protects resources and operations exposed by capabilities such as Merchant, Orders, and Logistics. Some protocol operations (such as the Discovery endpoint itself) are public. Most productive interactions require authentication.

Authentication does not define business coordination logic. It is a prerequisite for capability access.
