# Protocol Evolution

This page records protocol-level revision highlights for v1.

## Scope

- Focus on v1 protocol semantics.
- Ignore v2 concepts in this documentation cycle.
- Keep this documentation transport-agnostic.

## Current Baseline (v1.7.0)

Highlights reflected in the current baseline:

- Order fee vocabulary includes `MIN_ORDER_FEE`.
- Merchant status signaling is explicitly part of the merchant domain.
- Merchant onboarding context includes `orderingAppMerchantId` semantics.

## Evolution Rule

Changes MUST be documented as protocol behavior updates first.

Transport mappings MAY be defined later as separate profiles, preserving the same domain semantics.
