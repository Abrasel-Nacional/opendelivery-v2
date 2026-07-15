# Papéis e Responsabilidades

## Papéis de Interação Entre Capabilities

Para padronizar a documentação de capabilities, cada operação usa estes papéis transversais:

- `Provider`: participante que expõe a interface da operação (endpoint, ferramenta ou canal de eventos).
- `Consumer`: participante que invoca, assina ou consome essa interface.

Orientação de documentação:

- Toda operação documentada declara um Provider e um Consumer.
- Um participante pode atuar como Provider em uma operação e Consumer em outra.
- A classificação Provider/Consumer é específica por operação e não é identidade global do sistema.

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

## Software CRM (host de Customer)

**Quem é:** Plataforma de CRM, automação de marketing ou sistema de fidelidade que usa a capability **Customer**.

**Responsabilidades:**

- Receber e deduplicar dados do cliente.
- Receber pedidos no contexto de relacionamento (sem alterar o ciclo operacional de Orders).
- Opcionalmente hospedar módulos Reviews e/ou Loyalty.
- Emitir eventos de relacionamento e de fidelidade quando for a autoridade.

**Capabilities típicas:**

| Capability | Papel |
|---|---|
| Customer (núcleo + módulos Reviews/Loyalty conforme suporte) | Provider |

---

## Modelo Hub / Intermediário

Um hub PODE atuar como Ordering Application em um lado da integração e como Software Service em outro.

Implementações DEVEM preservar o comportamento específico do papel para cada papel que assumem.

**Exemplo:** Um marketplace que gerencia múltiplos restaurantes atua como Ordering Application para o consumidor final e como intermediário para o Software Service de cada restaurante.

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="../guide/by-role.md">Trilhas por papel</a> — checklist por produto</li>
    <li><a href="../guide/getting-started.md">Primeiros Passos</a></li>
    <li><a href="principles.md">Princípios</a></li>
    <li><a href="../reference/index.md">Referência da API</a></li>
  </ul>
</div>
