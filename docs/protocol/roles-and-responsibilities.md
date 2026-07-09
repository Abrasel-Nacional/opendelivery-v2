# Papéis e Responsabilidades

<div class="od-api-callout">
  <p>Papéis no ecossistema. Continue a jornada ou abra o contrato técnico.</p>
  <a href="../guide/by-role/">Trilhas por papel →</a>
</div>

## Papéis de Interação Entre Capabilities

Para padronizar a documentação de capabilities, cada operação usa estes papéis transversais:

- `Provider`: participante que expõe a interface da operação (endpoint, ferramenta ou canal de eventos).
- `Consumer`: participante que invoca, assina ou consome essa interface.

Orientação normativa:

- Toda operação DEVE declarar um Provider e um Consumer.
- Um participante PODE atuar como Provider em uma operação e Consumer em outra.
- A classificação Provider/Consumer é específica por operação e NÃO DEVE ser tratada como identidade global do sistema.

---

## Ordering Application

**Quem é:** Aplicativo de pedido do consumidor final, marketplace, PDV de autoatendimento, totem.

**Responsabilidades:**

- Consumir contexto de estabelecimento (catálogo, horários, disponibilidade).
- Criar pedidos e acompanhar o ciclo de vida.
- Consumir eventos de pedido e entrega.
- Acionar ações de ciclo de vida quando aplicável.
- Publicar endpoint de Discovery declarando suas capabilities.

**Capabilities típicas:**

| Capability | Papel |
|---|---|
| Merchant | Consumer |
| Orders | Consumer / Provider (callbacks) |
| Logistics | Consumer |
| Customer | Provider (ingesta dados) |

---

## Software Service (PDV)

**Quem é:** Sistema de gestão do restaurante, PDV, sistema de retaguarda.

**Responsabilidades:**

- Publicar contexto do estabelecimento (cardápio, horários, serviços).
- Receber e processar pedidos.
- Emitir fatos de progressão do ciclo de vida do pedido.
- Coordenar com participantes de logística quando necessário.
- Gerenciar conta e comandas em operações Indoor.

**Capabilities típicas:**

| Capability | Papel |
|---|---|
| Merchant | Provider |
| Orders | Provider |
| Indoor | Provider |
| Logistics | Consumer |

---

## Logistics Service (Delivery Platform)

**Quem é:** Operador de entrega, frota própria, agregador logístico.

**Responsabilidades:**

- Verificar disponibilidade e fornecer cotação de entrega.
- Aceitar ou recusar solicitações de coordenação de entrega.
- Emitir fatos de progresso de entrega e incidentes.
- Fornecer contexto de status e disponibilidade de entrega.

**Capabilities típicas:**

| Capability | Papel |
|---|---|
| Logistics | Provider |

!!! note "Independência"
    O Logistics Service pode operar sem que a capability Orders esteja implementada por nenhum dos outros participantes. O `orderId` é apenas um identificador de correlação acordado entre as partes.

---

## CRM Software Service

**Quem é:** Plataforma de CRM, automação de marketing, sistema de fidelidade.

**Responsabilidades:**

- Receber e deduplicar dados de clientes.
- Receber pedidos vinculados a clientes para análise e fidelidade.
- Gerenciar programas de fidelidade, pontos, resgates e cupons.
- Emitir eventos de ciclo de vida do cliente.

**Capabilities típicas:**

| Capability | Papel |
|---|---|
| Customer | Provider |
| Loyalty | Provider |

---

## Modelo Hub / Intermediário

Um hub PODE atuar como Ordering Application em um lado da integração e como Software Service em outro.

Implementações DEVEM preservar o comportamento específico do papel para cada papel que assumem.

**Exemplo:** Um marketplace que gerencia múltiplos restaurantes atua como Ordering Application para o consumidor final e como intermediário para o Software Service de cada restaurante.
