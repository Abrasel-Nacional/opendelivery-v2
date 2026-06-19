# Error Model

This section defines transport-neutral error semantics.

## Error Rules

1. Error responses MUST be machine-readable.
2. Error classification MUST preserve semantic meaning for automation.
3. Producers MUST NOT emit successful outcome facts when processing failed.
4. Cancellation-specific failures MUST be explicitly distinguishable.

## Error Fields

| name | type | required | description |
|---|---|---|---|
| `error.code` | string | YES | Stable machine-readable code |
| `error.message` | string | YES | Human-readable message |
| `error.details` | object | NO | Additional structured context |
| `error.retryable` | boolean | NO | Indicates whether retry is safe |
| `error.timestamp` | string | NO | Emission timestamp (ISO 8601 date-time) |

## Error Example

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Order identifier is unknown for this merchant scope",
    "retryable": false
  }
}
```
