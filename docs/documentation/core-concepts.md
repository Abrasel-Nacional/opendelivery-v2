# Conceitos Fundamentais

O Open Delivery Protocol (ODP) é um padrão aberto projetado para melhorar a comunicação e a interoperabilidade em ecossistemas de delivery de alimentos e varejo.

Sistemas diferentes geralmente operam com modelos, payloads e regras operacionais desconexos. O ODP fornece uma linguagem compartilhada para que esses sistemas coordenem dados de estabelecimentos, ciclos de vida de pedidos, relacionamentos com clientes e rastreamento de entregas — sem integrações bilaterais customizadas para cada parceiro.

Esta página explica o ODP em nível conceitual. O comportamento normativo é descrito na seção [Protocolo](../protocol/authentication.md).

## Arquitetura de Alto Nível

O ODP é um protocolo de coordenação entre participantes independentes.

Não há host central exigido pelo protocolo. Cada participante opera sua própria infraestrutura e troca informações do protocolo por meio de bindings de transporte acordados.

Em alto nível, o protocolo coordena quatro fluxos de informação:

- **Contexto de Merchant** — identidade, serviços operacionais, catálogo
- **Contexto de Pedidos** — eventos, estados, resultados de cancelamento
- **Contexto de Customer** — CRM, fatos relacionados à fidelidade, análise centrada no cliente
- **Contexto de Logistics** — cotação, despacho, rastreamento, tratamento de problemas

## Papéis e Participantes

O ODP define quatro papéis primários de participante:

- **Ordering Application** — Interface voltada ao consumidor final onde os usuários navegam por cardápios e fazem pedidos. Consome informações de estabelecimento e coordena interações de pedidos.
- **Software Service** — Sistema do lado do estabelecimento que publica dados do merchant e processa atualizações do ciclo de vida de pedidos.
- **Logistics Service** — Plataforma de entrega que recebe solicitações de entrega, retorna cotações e envia atualizações de rastreamento e problemas.
- **CRM Software Service** — Backends de CRM, automação de marketing, fidelidade e cupons.

Uma única empresa pode desempenhar múltiplos papéis dependendo do contexto de integração.

## Capabilities

Capabilities são as áreas funcionais primárias do protocolo. Elas representam os principais problemas de coordenação que o ODP resolve.

| Capability | Descrição |
|---|---|
| **Merchant** | Identidade do estabelecimento, catálogo, serviços e contexto operacional |
| **Orders** | Ciclo de vida de pedidos, gerenciamento de estado e coordenação |
| **Customer** | CRM, leads, eventos de cliente e visões de pedidos centradas no cliente |
| **Loyalty** | Identidade de fidelidade, acúmulo, resgate e validação de cupons |
| **Logistics** | Coordenação de entrega, rastreamento e tratamento de problemas |
| **Indoor** | Operações de pedidos em salão — serviço de mesa, balcão, comanda |

Capabilities são **independentes** entre si. Uma plataforma pode implementar qualquer capability ou combinação sem precisar das demais. Não existe capability obrigatória nem capability central da qual outras dependam.

## Extensões

Extensões são módulos opcionais do protocolo que aumentam uma capability base sem redefiní-la. Uma extensão é sempre declarada junto com sua capability pai e NÃO DEVE ser usada de forma independente.

| Extensão | Capability Pai | Descrição |
|---|---|---|
| **Indoor** | Orders | Agregação de conta em salão, pedidos incrementais, pagamentos parciais |
| **Loyalty** | Customer | Conta de fidelidade, acúmulo, resgate e validação de cupons/vouchers |

## Bindings de Transporte

Bindings de transporte definem a camada de comunicação usada para trocar mensagens ODP entre participantes. O ODP especifica atualmente um binding de transporte:

- **REST/HTTP** — Endpoints HTTP RESTful com payloads JSON

Bindings de transporte são definidos separadamente da semântica de capability. A mesma semântica de capability se aplica independentemente do transporte.

## Discovery

Antes de qualquer operação de capability, os participantes DEVEM publicar um documento de discovery legível por máquina em um endpoint well-known:

```
GET /.well-known/opendelivery
```

Este documento declara a identidade do participante, as capabilities suportadas e os endpoints de transporte disponíveis para cada capability. Nenhuma integração pode prosseguir sem que o Discovery esteja disponível.

Consulte [Protocolo — Discovery](../protocol/discovery.md) para as regras normativas.
