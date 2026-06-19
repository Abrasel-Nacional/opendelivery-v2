# Interaction Flows

This section defines conceptual flow sequences independent of transport.

## Merchant Publication Flow

1. Software Service publishes merchant context.
2. Ordering Application consumes service and catalog structures.
3. Merchant context updates are signaled asynchronously.
4. Consumers refresh affected merchant scope.

## Order Coordination Flow

1. Ordering Application receives an order fact signal.
2. Ordering Application resolves full order context.
3. Software Service emits lifecycle progression facts.
4. Consumers acknowledge processing in the chosen asynchronous pattern.

## Cancellation Flow

1. A participant emits cancellation request fact.
2. Counterparty emits resolution fact (`accepted` or `denied`).
3. All participants converge to consistent final order condition.

## Logistics Coordination Flow

1. Delivery coordination is requested for an order context.
2. Logistics emits pickup, transit, and completion facts.
3. Problems and cancellation facts are emitted when applicable.
4. Participants reconcile delivery and order conditions.

## Asynchronous Pattern Rule

- Polling and push are both valid patterns.
- Transport mapping MUST preserve ordering/tolerance semantics defined by the protocol.
