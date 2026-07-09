# Changelog

<div class="od-api-callout">
  <p>Histórico de versões. Continue a jornada ou abra o contrato técnico.</p>
  <a href="migration-v1-v2/">Guia de migração →</a>
</div>

Histórico de versões do Open Delivery Protocol.

---

## V2.0.0-rc — Julho 2026

Primeira versão Release Candidate do Open Delivery Protocol V2. Resultado de seis meses de trabalho
colaborativo em comitês técnicos com mais de dez empresas do ecossistema brasileiro de food tech.

### Breaking Changes

| Área | Mudança |
|---|---|
| **Autenticação** | Autenticação por aplicação — um único `client_id` para todas as lojas do software, em vez de um por loja |
| **Merchant ID** | Gerado pelo originador (não mais pelo PDV). O PDV usa `externalCode` para correlação interna |
| **Cardápio** | CRUD granular por entidade substitui o webhook monolítico `merchantUpdate` da V1 |
| **Cancelamento** | Handshake obrigatório (request/accept/deny) eliminado. Cancelamento direto e simplificado |
| **Evento `picked_up`** | Removido — era ambíguo entre takeout e coleta logística |
| **Service ID** | Serviços identificados por tipo (`DELIVERY`, `TAKEOUT`, `INDOOR`), sem ID separado |
| **`merchantType`** | Campo removido |
| **`subtotal` em opcionais** | Campo removido. Use `option_price` (obrigatório) e `unity_price` |

### Novos módulos

| Módulo | Descrição |
|---|---|
| **Customer / CRM** | Entidade de cliente, leads, avaliações — novo 4º ator no ecossistema |
| **Fidelidade** | Programas de pontos, cashback, cupons e catálogo de recompensas |
| **Indoor / Salão** | Operações de mesa, comanda e balcão com entidade Conta central |

### Melhorias e novidades

- **Escopos OAuth por domínio:** `od.orders` · `od.menu` · `od.logistics` · `od.crm` · `od.all`
- **Discovery Well-Known obrigatório:** endpoint `/.well-known/opendelivery` declarando todas as capabilities antes de qualquer integração
- **Separação status/evento:** campo `status` no GET do pedido; eventos são informativos, não definem estado
- **Authorization Code Flow:** suportado opcionalmente para casos de uso avançados
- **`quantity_available` no ItemOffer:** disponibilidade operacional (não controle de estoque)
- **Opcionais recursivos:** múltiplos níveis sem limite técnico via OptionGroups aninhados
- **Múltiplos services do mesmo tipo:** suportado (era limitação na V1)

### Indisponível no RC (previsto para V2.1)

- Reservas e fila de espera (Indoor)
- Detalhamento completo de LGPD / opt-in / opt-out (reunião pendente)
- Authorization Code Flow — fluxo completo em detalhamento

---

## V1.7.0

A V1 permanece ativa durante o período de transição. A especificação de referência está disponível em
[`/reference/v1/`](../reference/v2/authentication.openapi.yaml).

Para entender as diferenças e migrar, consulte o [Guia de Migração V1→V2](migration-v1-v2.md).
