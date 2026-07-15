# Conceitos Fundamentais

O Open Delivery Protocol (ODP) é um padrão aberto projetado para melhorar a comunicação e a interoperabilidade em ecossistemas de delivery de alimentos e food service.

Sistemas diferentes geralmente operam com modelos, payloads e regras operacionais desconexos. O ODP fornece uma linguagem compartilhada para que esses sistemas coordenem dados de estabelecimentos, ciclos de vida de pedidos, relacionamentos com clientes e rastreamento de entregas — sem integrações bilaterais customizadas para cada parceiro.

Esta página explica o ODP em nível conceitual.

| Camada | O que encontrar |
|---|---|
| **Guia** | Onboarding, papéis, migração |
| **Protocolo** | Domínio, fluxos e responsabilidades |
| **Referência da API** | Especificação da API normativa (REST/HTTP) |

## Arquitetura de Alto Nível

O ODP é um protocolo de coordenação entre participantes independentes.

Não há host central exigido. Cada participante opera sua própria infraestrutura e integra-se via o **especificação da API** do Open Delivery (REST/HTTP), após Discovery e autenticação.

Em alto nível, o protocolo coordena quatro fluxos de informação:

- **Contexto de Merchant** — identidade, serviços operacionais, catálogo
- **Contexto de Pedidos** — estados, eventos, cancelamento
- **Contexto de Customer** — dados do cliente, fidelidade, fatos de relacionamento
- **Contexto de Logistics** — cotação, despacho, rastreamento, problemas

## Papéis e Participantes

O ODP define quatro papéis primários de participante:

- **Ordering Application** — Interface voltada ao consumidor final onde os usuários navegam por cardápios e fazem pedidos. Consome informações de estabelecimento e coordena interações de pedidos.
- **Software Service** — Sistema do lado do estabelecimento que publica dados do merchant e processa o ciclo de vida de pedidos.
- **Logistics Service** — Plataforma de entrega que recebe solicitações de entrega, retorna cotações e envia atualizações de rastreamento e problemas.
- **Software CRM** — Backends de relacionamento com o cliente, automação de marketing, fidelidade e cupons que usam a capability **Customer**.

Uma única empresa pode desempenhar múltiplos papéis dependendo do contexto de integração.

## Capabilities

Capabilities são as áreas funcionais primárias do protocolo. Elas representam os principais problemas de coordenação que o ODP resolve.

| Capability | Descrição |
|---|---|
| **Merchant** | Estabelecimento: **Dados da Loja** + **Menus** |
| **Orders** | Ciclo de vida de pedidos, gerenciamento de estado e coordenação |
| **Customer** | Dados do cliente, leads, eventos, reviews e loyalty (módulos da mesma capability) |
| **Logistics** | Coordenação de entrega, rastreamento e tratamento de problemas |

Capabilities são **independentes** entre si. Uma plataforma pode implementar qualquer capability ou combinação sem precisar das demais. Não existe capability obrigatória nem capability central da qual outras dependam.

O nome da capability de dados do cliente é **sempre Customer** — não “CRM”. Software CRM é a classe de produto que implementa ou consome Customer.

### Módulos de documentação (não são extensions)

Alguns domínios grandes são fatiados em páginas de protocolo para legibilidade, **sem** mudar o Discovery:

| Página | Capability | Descrição |
|---|---|---|
| **Visão geral** | Merchant | Conceito e mapa do domínio |
| **Dados da Loja** | Merchant | Merchant ID, services, horários, pause |
| **Menus** | Merchant | Hierarquia de catálogo, snapshot e sincronismo |
| **Visão geral** | Customer | Conceito, papéis, núcleo de dados do cliente |
| **Reviews** | Customer | Avaliações — módulo; MAY ser implementado sozinho |
| **Loyalty** | Customer | Fidelidade e cupons — módulo; MAY ser implementado sozinho |

Reviews e Loyalty **não** são extensões Discovery: são módulos de Customer, declarados via `supportedOperations` sob `customer`.

## Extensões

Extensões são módulos **opcionais** que aumentam uma capability base sem redefiní-la. Uma extensão é sempre declarada junto com sua capability pai.

| Extensão | Capability pai | Descrição |
|---|---|---|
| **Indoor** | Orders | Agregação de conta em salão, pedidos incrementais, pagamentos parciais |

## Especificação da API

A forma padronizada de implementar o ODP V2 é o conjunto de **especificações da API** na tab [Referência da API](../reference/index.md) — REST/HTTP com JSON.

Não há camada separada de “transport binding”. Guia e Protocolo explicam o domínio; a especificação da API define o contrato implementável.

Convenções transversais (datas, paginação, erros): [Regras gerais](../reference/conventions.md) · [Tratamento de erros](../reference/error-handling.md).

## Discovery

Antes de qualquer operação de capability, os participantes publicam um documento de discovery legível por máquina em um endpoint well-known:

```
GET /.well-known/opendelivery
```

Este documento declara a identidade do participante, as capabilities suportadas e como autenticar/integrar. Nenhuma integração deve prosseguir sem Discovery disponível.

Consulte [Protocolo — Discovery](../protocol/discovery.md) e a [especificação de Discovery](../reference/discovery.md).

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="../guide/getting-started.md">Primeiros Passos</a> — começar a integrar</li>
    <li><a href="../guide/by-role.md">Trilhas por papel</a> — o que implementar por tipo de produto</li>
    <li><a href="../protocol/principles.md">Princípios</a> · <a href="../overview.md">Visão geral do protocolo</a></li>
    <li><a href="../reference/index.md">Referência da API</a> — contrato implementável</li>
  </ul>
</div>
