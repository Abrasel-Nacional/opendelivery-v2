# REST Operations (v1)

Total paths: **30**

## `/v1/versions/orderingApp`

### `GET`
- OperationId: `getOrderingAppVersions`
- Summary: Get Current Ordering Application API Version
- Tags: `versionsEndpoint`
- Security: `none`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Successful returns Ordering Application API version. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/versions/merchant`

### `GET`
- OperationId: `getMerchantVersions`
- Summary: Get Current Merchant API Version
- Tags: `versionsEndpoint`
- Security: `none`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Successful returns Merchant API version. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/oauth/token`

### `POST`
- OperationId: `getToken`
- Summary: Get Access Token
- Tags: `authentication`
- Security: `none`
- Request Body: `$ref` `#/components/requestBodies/Token`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Successful returns token request. | `` |
| `401` |  | `#/components/responses/Unauthorized` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/merchant`

### `GET`
- OperationId: `getMerchant`
- Summary: Get information of a Merchant
- Tags: `merchantEndpoints`
- Security: `apiKey`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Successful returns Merchant information. | `` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/merchantStatus`

### `GET`
- OperationId: `getMerchantStatus`
- Summary: Check Merchant Update Processing Result
- Tags: `merchantUpdate`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `merchantId` | `query` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Returns the status and result of the last merchant update processing (GET /merchant or webhook). | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/merchantOnboarding`

### `PUT`
- OperationId: `putMerchantOnboarding`
- Summary: Register / Update Merchant endpoint info.
- Tags: `merchantStatus`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `merchantId` | `query` | `True` | `string` |

- Request Body Media Types: `application/json`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `201` | Resource has been created. | `` |
| `204` | Request has been processed. Return has no content. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/merchant/{id}/status`

### `GET`
- OperationId: `getMerchantAvailability`
- Summary: Get Merchant Status and Service Hours
- Tags: `merchantStatus`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `id` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Successfully returns Merchant status, services and sourceAppId. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/events:polling`

### `GET`
- OperationId: `pollingEvents`
- Summary: Get New Events
- Tags: `ordersPolling`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `x-polling-merchants` | `header` | `False` | `array` |
| `eventType` | `query` | `False` | `array` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Successful returns list of polled events . | `` |
| `204` | No content. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/events/acknowledgment`

### `POST`
- OperationId: `pollingAcknowledgment`
- Summary: Acknowledge Events
- Tags: `ordersPolling`
- Security: `OAuth2(od.all)`
- Request Body: `$ref` `#/components/requestBodies/AckEvents`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `404` |  | `#/components/responses/NotFound` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}`

### `GET`
- OperationId: `ordersDetails`
- Summary: Get Order Details
- Tags: `ordersDetails`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Order returning success. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/confirm`

### `POST`
- OperationId: `confirmOrder`
- Summary: Confirm
- Tags: `ordersStatus`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body Media Types: `application/json`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/preparing`

### `POST`
- OperationId: `orderPreparing`
- Summary: Preparing (Optional)
- Tags: `ordersStatus`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/readyForPickup`

### `POST`
- OperationId: `orderReady`
- Summary: Ready For Pickup
- Tags: `ordersStatus`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/pickedUp`

### `POST`
- OperationId: `orderPickedUp`
- Summary: Picked Up (Optional)
- Tags: `ordersStatus`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/dispatch`

### `POST`
- OperationId: `dispatchOrder`
- Summary: Dispatch
- Tags: `ordersStatus`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body Media Types: `application/json`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/delivered`

### `POST`
- OperationId: `orderDelivered`
- Summary: Delivered (Optional)
- Tags: `ordersStatus`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/validateCode`

### `POST`
- OperationId: `orderValidateDelivery`
- Summary: Validate Delivery Code
- Tags: `ordersTracking`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |
| `deliveryCode` | `query` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Confirmation Code is correct. You can proceed with the delivery. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/tracking`

### `POST`
- OperationId: `orderTracking`
- Summary: Send Delivery Updates
- Tags: `ordersTracking`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body Media Types: `application/json`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/details`

### `PATCH`
- OperationId: `patchOrderDetails`
- Summary: Update Order Details
- Tags: `ordersDetails`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body Media Types: `application/json`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Preparation time updated successfully. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/requestCancellation`

### `POST`
- OperationId: `requestCancellation`
- Summary: Request order cancellation
- Tags: `ordersCancellation`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body: `$ref` `#/components/requestBodies/CancelRequest`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` |  | `#/components/responses/Accepted` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntityOrderCancellation` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/acceptCancellation`

### `POST`
- OperationId: `cancellationAccepted`
- Summary: Accept order cancellation
- Tags: `ordersCancellation`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Status 200 available for compatibility reasons. Please use status 204 instead. | `` |
| `204` | Order cancellation has been confirmed. No response content. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/orders/{orderId}/denyCancellation`

### `POST`
- OperationId: `cancellationDenied`
- Summary: Deny order cancellation
- Tags: `ordersCancellation`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body: `$ref` `#/components/requestBodies/CancelDenied`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Status 200 available for compatibility reasons. Please use status 204 instead. | `` |
| `204` | Order cancellation has been denied. No response content. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/logistics/availability`

### `POST`
- OperationId: `logisticsAvailability`
- Summary: Check delivery availability and prices
- Tags: `logisticPrice`
- Security: `configured`
- Request Body Media Types: `application/json`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Successfully returns delivery availability and price. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/logistics/delivery`

### `POST`
- OperationId: `logisticsNewDelivery`
- Summary: Request new delivery
- Tags: `logisticOrder`
- Security: `OAuth2(od.all)`
- Request Body: `$ref` `#/components/requestBodies/DeliveryOrder`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` | Request has been accepted for processing. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/logistics/delivery/{orderId}`

### `GET`
- OperationId: `logisticDetails`
- Summary: Get delivery details
- Tags: `logisticDetails`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Successfully returns the delivery order details. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `404` |  | `#/components/responses/NotFound` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/logistics/readyForPickup/{orderId}`

### `POST`
- OperationId: `logisticsReadyForPickup`
- Summary: Inform Ready for Pickup
- Tags: `logisticOrder`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Order is ready for pickup. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/logistics/orderPicked/{orderId}`

### `POST`
- OperationId: `logisticsPicked`
- Summary: Inform Order Pickup
- Tags: `logisticOrder`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body Media Types: `application/json`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Order pickup has been confirmed. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/logistics/finishDelivery/{orderId}`

### `POST`
- OperationId: `logisticsFinish`
- Summary: Finish Delivery
- Tags: `logisticOrder`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body Media Types: `application/json`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | Delivery completion has been confirmed. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/logistics/handleProblem/{orderId}`

### `POST`
- OperationId: `logisticsProblem`
- Summary: Handle problem
- Tags: `logisticOrder`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body: `$ref` `#/components/requestBodies/DeliveryHandleProblem`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `200` | The problem has been addressed. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |


## `/v1/logistics/cancel/{orderId}`

### `POST`
- OperationId: `logisticsCancel`
- Summary: Cancel delivery
- Tags: `logisticOrder`
- Security: `OAuth2(od.all)`
- Parameters:

| Name | In | Required | Type |
|---|---|---|---|
| `orderId` | `path` | `True` | `string` |

- Request Body: `$ref` `#/components/requestBodies/DeliveryCancel`
- Responses:

| HTTP | Description | Ref |
|---|---|---|
| `202` | Cancel request has been accepted for processing. | `` |
| `400` |  | `#/components/responses/BadRequest` |
| `401` |  | `#/components/responses/Unauthorized` |
| `403` |  | `#/components/responses/AccessDenied` |
| `404` |  | `#/components/responses/NotFound` |
| `422` |  | `#/components/responses/UnprocessableEntity` |
| `503` |  | `#/components/responses/ServiceUnavailable` |

