# Fluxos de Interação

Esta seção define sequências de fluxo conceituais independentes de transporte.

## Fluxo de Publicação de Merchant

1. O Software Service publica o contexto do estabelecimento.
2. A Ordering Application consome as estruturas de serviço e catálogo.
3. Atualizações do contexto do estabelecimento são sinalizadas de forma assíncrona.
4. Os consumidores atualizam o escopo do estabelecimento afetado.

## Fluxo de Coordenação de Pedidos

1. A Ordering Application cria o pedido no **seu** sistema (não há `POST /orders` no protocolo).
2. Emite o evento **`CREATED`** (polling e/ou webhook).
3. O Software Service faz ACK (se polling) e busca o snapshot com **`GET /orders/{orderId}`**.
4. A progressão do ciclo de vida ocorre via operações assíncronas (`confirm`, `preparing`, …) no host da Ordering Application; o status autoritativo fica no GET.

## Fluxo de Cancelamento

O cancelamento no ODP v2 é uma operação direta e unilateral — não há handshake de solicitação/resposta.

1. Cancel do merchant: `POST /orders/{id}/requestCancellation` → se aceito: `CANCELLATION_REQUEST_ACCEPTED` **depois** `CANCELLED`; se recusado: `CANCELLATION_REQUEST_DENIED`. Cancel do originador: evento mandatório `CANCELLED`.
2. O status do pedido transita para `CANCELLED`.
3. Todos os participantes recebem o evento de cancelamento de forma assíncrona e convergem para o estado final.

!!! note "Diferença em relação à V1"
    Na V1, o cancelamento envolvia um handshake bilateral (solicitação → confirmação/rejeição). Na V2, o cancelamento é direto. O deny nunca foi implementado em escala na V1, tornando o handshake uma formalidade sem valor prático.

## Fluxo de Coordenação Logística

1. A coordenação de entrega é solicitada com o identificador do pedido como referência.
2. A Delivery Platform verifica disponibilidade e retorna cotação.
3. A entrega é criada; a Delivery Platform designa um entregador.
4. Fatos de coleta, trânsito e conclusão são emitidos progressivamente.
5. Problemas e fatos de cancelamento são emitidos quando aplicável.
6. Os participantes reconciliam condições de entrega e pedido.

## Fluxo de Customer

1. A Ordering Application ingere dados do cliente no host de Customer (em geral um Software CRM).
2. O host processa e deduplica o cliente por identificadores externos.
3. Pedidos vinculados ao cliente são ingeridos no contexto de relacionamento (mesmo shape de Orders).
4. O host emite eventos de relacionamento conforme necessário.
5. Módulos opcionais: Reviews e/ou Loyalty (podem ser adotados de forma independente).

## Fluxo de Loyalty (módulo de Customer)

1. A Ordering Application notifica o host de Loyalty sobre fatos de pedido relevantes.
2. O host registra pontos pendentes.
3. Após conclusão do pedido, pontos são creditados definitivamente.
4. O cliente pode resgatar pontos por recompensas e usar cupons no checkout.
5. Cancelamentos revertem pontos e cancelam cupons afetados.

## Regra de Padrão Assíncrono

- Polling e push são ambos padrões válidos, conforme declarado no Discovery e nos especificações da API.
- Consumidores devem implementar deduplicação de eventos por identificador.
- Consumidores não devem assumir garantias de ordenação de entrega de eventos, salvo indicação contrária no contrato.

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="orders.md">Orders</a></li>
    <li><a href="logistics.md">Logistics</a></li>
    <li><a href="../reference/orders.md">Especificação de Orders</a></li>
    <li><a href="../reference/index.md">Referência da API</a></li>
  </ul>
</div>
