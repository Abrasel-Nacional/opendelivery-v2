# Princípios de Design

!!! warning "Release Candidate (V2.0.0-rc)"
    O protocolo V2 está em **Release Candidate**, em período de **validação com o ecossistema** (revisão por empresas e pilotos de implementação). A versão estável será publicada somente após essa fase. A V1 permanece ativa na transição. Detalhes: [Evolução](evolution.md) · [Changelog](../guide/changelog.md).

Esta seção descreve os **princípios de design** do Open Delivery Protocol v2: como o ecossistema se coordena e o que a documentação prioriza.

Eles orientam o conteúdo da tab **Protocolo** (conceitos, fluxos, papéis) e as **especificações da API** (contrato normativo REST/HTTP).
**Obrigações de implementação (campos, endpoints, MUST/MAY de API)** estão na [Referência da API](../reference/index.md) — a especificação da API é a fonte normativa do contrato.

---

## Interoperabilidade, não produto

O Open Delivery é um **protocolo de interoperabilidade** expresso como **especificação da API (REST/HTTP)**.

Ele define uma linguagem compartilhada para sistemas independentes de food service — não é uma plataforma, um runtime nem um produto SaaS.

A documentação se organiza em:

| Camada | Papel |
|---|---|
| **Guia** | Onboarding, papéis, migração, histórico |
| **Protocolo** | Domínio: conceitos, fluxos, responsabilidades (explicativo) |
| **Referência da API** | Especificação da API (normativa) — suficiente para implementar |

---

## Descentralização e autonomia

O Open Delivery pressupõe um **ecossistema descentralizado**.

- Não há runtime central
- Não há banco de dados compartilhado
- Não há intermediário obrigatório

Cada participante:

- Permanece autônomo
- Possui seu estado interno
- Aplica suas próprias regras de negócio

O protocolo existe para **coordenar sistemas**, não para controlá-los.

---

## Separação de responsabilidades na documentação

- **Protocolo (esta tab)** — *o que* os sistemas coordenam: entidades, ciclos de vida, papéis, fluxos
- **especificação da API (Referência da API)** — *como* isso se implementa em REST/HTTP: paths, schemas, erros, exemplos
- **Implementação** — arquitetura, UX e regras internas de cada participante

Isso evita duas fontes de verdade para campos e endpoints. Em dúvida de contrato, **prevalece a especificação da API**.

---

## Independência de capabilities

As capabilities do Open Delivery são **independentes** entre si.

Os participantes podem implementar qualquer capability ou combinação:

- Apenas **Merchant** — catálogo e dados de loja
- Apenas **Logistics** — coordenação de entrega
- Apenas **Orders** — ciclo de vida de pedidos
- Apenas **Customer** — CRM e identidade
- Qualquer combinação das anteriores

Nenhuma capability é pré-requisito para outra, salvo **extensões** explicitamente ligadas ao pai:

- **Indoor** estende **Orders**
- **Loyalty** (e **Reviews**) estendem **Customer**

---

## Eventos representam fatos, não etapas de workflow

Eventos representam **fatos que ocorreram**, não passos internos de processo.

Um evento:

- É imutável
- Ocorre em um momento específico
- Comunica informação a outros sistemas

Eventos não devem:

- Codificar etapas internas de processo
- Espelhar máquinas de estado internas
- Descrever como o trabalho é realizado por trás

Apenas fatos relevantes para a **coordenação entre sistemas** entram no protocolo.

---

## Estados representam a condição atual

Estados descrevem a **condição atual** de uma entidade.

- Podem mudar ao longo do tempo
- São descritivos, não prescritivos de workflow interno

Consumidores devem tratar o **estado consultável** (ex.: `GET` do recurso) como fonte de verdade para reconciliação, e eventos como notificações de fatos — detalhes por capability na especificação da API e nas páginas de Protocolo correspondentes.

---

## Obrigações com escopo por perfil

Obrigações de eventos e fluxos têm **escopo por perfil** (ex.: `DELIVERY`, `TAKEOUT`, `INDOOR`), não são necessariamente globais.

Um evento pode ser:

- Obrigatório em um perfil
- Opcional em outro
- Não aplicável em um terceiro

Isso evita super-especificação e preserva flexibilidade operacional.

---

## Suporte declarado, não flags por pedido

O comportamento esperado entre parceiros é declarado de forma estável (Discovery, onboarding), não por flags dinâmicas em cada pedido.

- Capabilities, perfis e extensões suportadas são **declarados**
- Pedidos carregam dados de negócio e contexto
- O manifesto well-known é o ponto de partida da integração

Ver [Discovery](discovery.md) e a [especificação de Discovery](../reference/discovery.md).

---

## Tolerância e resiliência

O Open Delivery pressupõe sistemas distribuídos com falhas parciais.

Implementações devem:

- Tolerar eventos opcionais ausentes
- Tratar eventos duplicados (deduplicação por id de evento)
- Aceitar entrega fora de ordem quando o contrato não garantir ordem
- Evitar dependência de timing rígido entre parceiros

Prefere-se **consistência eventual** a sincronização estrita.

Convenções HTTP compartilhadas: [Regras gerais](../reference/conventions.md) · [Erros](../reference/error-handling.md).

---

## Contrato único: especificação da API (REST/HTTP)

A forma padronizada de implementar o Open Delivery V2 é a **especificação da API** publicado na tab **Referência da API** (REST/HTTP + JSON).

Não há camada separada de “transport binding” nem expectativa de múltiplos bindings oficiais paralelos. Evolução do contrato ocorre nas especificações da API e na documentação associada.

---

## Governança e gestão

O Open Delivery é governado de forma aberta e transparente.

A governança existe para:

- Garantir transparência e isonomia
- Coordenar a evolução do protocolo
- Publicar releases e Release Candidates

A governança **não**:

- Restringe a adoção
- Impõe condições comerciais
- Concede direitos exclusivos a qualquer participante

Propostas e issues: [repositório GitHub](https://github.com/Abrasel-Nacional/opendelivery-v2).

---

## Coordenação institucional

A iniciativa é coordenada institucionalmente pela **Abrasel**.

Isso inclui repositórios oficiais, publicação da documentação e comunicação.
Não altera a natureza aberta do protocolo nem exige registro obrigatório para leitura da especificação.

---

## Minimalismo

O protocolo define a **superfície mínima** necessária à interoperabilidade.

O que for puramente interno, específico de implementação ou desnecessário à coordenação entre sistemas deve permanecer **fora** do contrato e desta documentação normativa de API.

---

## Resumo

O Open Delivery v2 prioriza:

- Interoperabilidade entre sistemas autônomos
- Capabilities independentes e extensões explícitas
- Estados consultáveis e eventos como fatos
- Um contrato implementável em **especificação da API (REST/HTTP)**
- Documentação em camadas claras: Guia · Protocolo · API

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="../reference/index.md">Referência da API</a> — contratos implementáveis</li>
    <li><a href="discovery.md">Discovery</a></li>
    <li><a href="flows.md">Fluxos</a></li>
    <li><a href="evolution.md">Evolução</a></li>
  </ul>
</div>
