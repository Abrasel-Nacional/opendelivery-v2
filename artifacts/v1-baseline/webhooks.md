# Webhooks (v1)

Total webhook paths: **4**

## `/v1/menuUpdated`

### `POST`
- OperationId: `menuUpdated`
- Summary: New Merchant Update Notification
- Tags: `merchantUpdate`

| HTTP | Description | Ref |
|---|---|---|
| `200` | Status 200 available for compatibility reasons. Please use status 204 instead. | `` |
| `204` | Data was received successfully. No response content. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/newEvent`

### `POST`
- OperationId: `newEvent`
- Summary: New Order Event Notification
- Tags: `ordersWebhook`

| Header/Param | In | Required |
|---|---|---|
| `X-App-Id` | `header` | `True` |
| `X-App-MerchantId` | `header` | `True` |
| `X-App-Signature` | `header` | `True` |


| HTTP | Description | Ref |
|---|---|---|
| `200` | Status 200 available for compatibility reasons. Please use status 204 instead. | `` |
| `204` | Data was received successfully. No response content. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/newLogisticEvent`

### `POST`
- OperationId: `newLogisticEvent`
- Summary: Tracking Event Webhook
- Tags: `logisticsWebhook`

| Header/Param | In | Required |
|---|---|---|
| `X-App-Id` | `header` | `True` |
| `X-App-MerchantId` | `header` | `True` |
| `X-App-Signature` | `header` | `True` |


| HTTP | Description | Ref |
|---|---|---|
| `204` | Data was received successfully. No response content. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/confirmationCode`

### `POST`
- OperationId: `logistictsDeliveryCode`
- Summary: Delivery Code Webhook
- Tags: `logisticsWebhook`

| Header/Param | In | Required |
|---|---|---|
| `X-App-Id` | `header` | `True` |
| `X-App-MerchantId` | `header` | `True` |
| `X-App-Signature` | `header` | `True` |


| HTTP | Description | Ref |
|---|---|---|
| `200` | Confirmation Code is correct. You can proceed with the delivery. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `503` |  | `#/components/responses/ServiceUnavailable` |

