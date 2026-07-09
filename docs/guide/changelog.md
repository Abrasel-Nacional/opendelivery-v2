# Changelog

Histórico de versões do Open Delivery Protocol.

<div class="od-version-banner">
  <span class="od-version-banner__ver">V2.0.0-rc</span>
  <span class="od-version-banner__meta">Release Candidate · Julho 2026 · V1 permanece ativa na transição</span>
</div>

## O que mudou na V2

<div class="od-whats-new">
  <p class="od-whats-new__intro">
    Resumo visual das mudanças principais. Detalhes de migração no
    <a href="migration-v1-v2/">guia V1→V2</a>.
  </p>

  <div class="od-whats-new__grid">

    <a class="od-wn-card" href="../protocol/authentication/">
      <span class="od-wn-card__tag od-wn-card__tag--break">Breaking</span>
      <span class="od-wn-card__title">Auth por aplicação</span>
      <p>Um <code>client_id</code> por software, não por loja. Lista de merchants via <code>GET /merchants</code>.</p>
    </a>

    <a class="od-wn-card" href="../protocol/merchant-store/">
      <span class="od-wn-card__tag od-wn-card__tag--break">Breaking</span>
      <span class="od-wn-card__title">Merchant ID do originador</span>
      <p>ID gerado pela Ordering Application; PDV correlaciona com <code>externalCode</code>.</p>
    </a>

    <a class="od-wn-card" href="../protocol/menu/">
      <span class="od-wn-card__tag od-wn-card__tag--break">Breaking</span>
      <span class="od-wn-card__title">Cardápio com CRUD</span>
      <p>Fim do webhook monolítico <code>merchantUpdate</code>. Snapshot + endpoints por entidade.</p>
    </a>

    <a class="od-wn-card" href="../protocol/orders/">
      <span class="od-wn-card__tag od-wn-card__tag--break">Breaking</span>
      <span class="od-wn-card__title">Cancelamento simplificado</span>
      <p>Sem handshake request/accept/deny. Cancelamento direto com motivo.</p>
    </a>

    <a class="od-wn-card" href="../protocol/customer/">
      <span class="od-wn-card__tag od-wn-card__tag--new">Novo</span>
      <span class="od-wn-card__title">Customer / CRM</span>
      <p>Cliente, leads e eventos de relacionamento — novo domínio na V2.</p>
    </a>

    <a class="od-wn-card" href="../extensions/loyalty/">
      <span class="od-wn-card__tag od-wn-card__tag--new">Novo</span>
      <span class="od-wn-card__title">Fidelidade</span>
      <p>Pontos, cashback, cupons e catálogo de recompensas.</p>
    </a>

    <a class="od-wn-card" href="../protocol/indoor/">
      <span class="od-wn-card__tag od-wn-card__tag--new">Novo</span>
      <span class="od-wn-card__title">Indoor / Salão</span>
      <p>Conta de mesa/comanda/balcão, pagamentos e fiscal assíncrono.</p>
    </a>

    <a class="od-wn-card" href="../protocol/discovery/">
      <span class="od-wn-card__tag od-wn-card__tag--improve">Melhoria</span>
      <span class="od-wn-card__title">Discovery obrigatório</span>
      <p>Well-known declara capabilities, versões e modos de integração.</p>
    </a>

    <a class="od-wn-card" href="../protocol/orders/#ciclo-de-vida-status">
      <span class="od-wn-card__tag od-wn-card__tag--improve">Melhoria</span>
      <span class="od-wn-card__title">Status ≠ eventos</span>
      <p>Status consultável no GET; eventos são notificações (podem ser informativos).</p>
    </a>

  </div>
</div>

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

A V1 permanece ativa durante o período de transição.

Para entender as diferenças e migrar, consulte o [Guia de Migração V1→V2](migration-v1-v2.md).
