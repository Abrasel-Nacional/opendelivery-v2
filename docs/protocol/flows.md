# Fluxos de Interação

Esta seção define sequências de fluxo conceituais independentes de transporte.

## Fluxo de Publicação de Merchant

1. O Software Service publica o contexto do estabelecimento.
2. A Ordering Application consome as estruturas de serviço e catálogo.
3. Atualizações do contexto do estabelecimento são sinalizadas de forma assíncrona.
4. Os consumidores atualizam o escopo do estabelecimento afetado.

## Fluxo de Coordenação de Pedidos

1. A Ordering Application recebe um sinal de criação de pedido.
2. A Ordering Application envia o pedido completo ao Software Service.
3. O Software Service emite fatos de progressão do ciclo de vida.
4. Os consumidores processam as atualizações no padrão assíncrono escolhido.

## Fluxo de Cancelamento

O cancelamento no ODP v2 é uma operação direta e unilateral — não há handshake de solicitação/resposta.

1. Um participante executa o cancelamento: `POST /orders/{id}/cancel` com motivo e código.
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

## Fluxo de Customer / CRM

1. A Ordering Application ingesta dados de cliente no CRM Software Service.
2. O CRM Software Service processa e deduplica o cliente por identificadores externos.
3. Pedidos vinculados ao cliente são ingeridos para análise e fidelidade.
4. O CRM Software Service emite eventos de ciclo de vida do cliente conforme necessário.

## Fluxo de Fidelidade

1. A Ordering Application notifica o Loyalty Software Service sobre criação de pedido.
2. O Loyalty Software Service registra pontos pendentes.
3. Após entrega confirmada, pontos são creditados definitivamente.
4. O cliente pode resgatar pontos por recompensas e usar cupons no checkout.
5. Cancelamentos revertem pontos e cancelam cupons afetados.

## Regra de Padrão Assíncrono

- Polling e push são ambos padrões válidos.
- O binding de transporte DEVE preservar a semântica de ordenação/tolerância definida pelo protocolo.
- Consumidores DEVEM implementar deduplicação de eventos por identificador.
- Consumidores NÃO DEVEM assumir garantias de ordenação de entrega de eventos.
