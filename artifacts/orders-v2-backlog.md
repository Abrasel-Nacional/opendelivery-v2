# Orders V2 — backlog (registrado, a fazer)

Lista de ajustes pendentes na capability Orders. Não implementar até o time retomar.

| # | Item | Notas |
|---|------|--------|
| 1 | Padronizar a tabela de Eventos / Status | Alinhar guia + API Spec (matrizes por perfil, MUST/MAY, status projetado) |
| 2 | Arrumar o fluxo do cancelamento | **Feito:** SS handshake mantido + `CANCELLATION_REQUEST_ACCEPTED` → depois `CANCELLED`; OA só mandatório; sem accept/deny HTTP do originador |
| 3 | Arrumar descrição de campos | Schemas OpenAPI e textos do guia |
| 4 | Atualizar o payload do pedido para a V2 | **Feito (2026-07-14):** ver detalhamento completo no changelog (`docs/guide/changelog.md` / `.en.md`, seção "Payload do pedido"). Pontos de decisão futura abaixo. |
| 5 | Tracking | Eventos/ops de tracking vs Logistics; o que fica em Orders |
| 6 | Remover o Conclude | Remover status/evento/op `conclude` se for a decisão |
| 7 | Bater com a V1 | Diff normativo V1↔V2 (ops, eventos, hosting, polling/webhook) |

**Arquivos principais:** `docs/reference/v2/orders.openapi.yaml`, `docs/protocol/orders.md` (+ `.en.md`), migration/changelog se breaking.

**Registrado em:** sessão de revisão Orders / ReDoc (2026-07-13).

## Pontos de decisão futura (payload)

Registrados na revisão do item #4 (2026-07-14). Não implementar sem decisão do usuário/comitê.

| # | Ponto | Contexto | Atas relacionadas |
|---|---|---|---|
| A | `OrderItem.originalPrice` / `OrderItemOption.optionsPrice` — confirmar remoção definitiva | Já estão fora do schema v2 atual; ata só pediu "investigar uso real", nunca fechou a remoção formalmente | 26/03, 09/04 |
| B | `Order.preparationStartDateTime` | Apontado como campo com alto índice de erro nos sistemas; usuário vai verificar antes de qualquer mudança | 26/03 |
| C | Formato de preço (`Price{value,currency}` vs. inteiro em minor units) | Preocupação registrada em ata sobre "quebra do padrão value+currency"; **não mexer** por instrução explícita do usuário (2026-07-14) até haver decisão de comitê | 08/06 |
