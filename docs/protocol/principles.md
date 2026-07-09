# Princípios de Design

<div class="od-api-callout">
  <p>Fundamentos do protocolo. Continue a jornada ou abra o contrato técnico.</p>
  <a href="../guide/getting-started/">Primeiros Passos →</a>
</div>

Esta seção define os princípios fundamentais que orientam o design, a governança e a evolução do Open Delivery Protocol v2.

Estes princípios são **normativos**.  
Todas as especificações, capabilities e extensões do protocolo DEVEM estar alinhadas a eles.

---

## Protocolo em Primeiro Lugar

O Open Delivery é projetado como um **protocolo**, não como uma API, plataforma ou produto.

A especificação define:
- Conceitos compartilhados
- Fatos observáveis
- Responsabilidades claras entre sistemas independentes

O protocolo NÃO:
- Dita fluxos de trabalho internos
- Prescreve detalhes de implementação
- Exige tecnologias ou fornecedores específicos

Mecanismos de transporte, APIs, padrões de mensageria e ferramental são **escolhas de implementação**, não parte do protocolo em si.

---

## Descentralização e Autonomia

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

## Separação Clara de Responsabilidades

O protocolo impõe uma separação estrita entre:

- **Regras do protocolo** — o que os sistemas devem acordar
- **Lógica de implementação** — como os sistemas se comportam internamente
- **Serviços do ecossistema** — ferramental e suporte à adoção

Esta separação garante:
- Estabilidade de longo prazo
- Múltiplos estilos de integração
- Liberdade de escolha arquitetural

---

## Independência de Capabilities

As capabilities do Open Delivery são **independentes** entre si.

Os participantes podem implementar qualquer capability ou combinação de capabilities:

- Uma plataforma pode implementar apenas **Merchant** — para publicar dados de catálogo
- Uma plataforma pode implementar apenas **Logistics** — para prover coordenação de entrega
- Uma plataforma pode implementar apenas **Orders** — para gerenciar o ciclo de vida de pedidos
- Uma plataforma pode implementar apenas **Customer** — para interoperabilidade de CRM e identidade
- Uma plataforma pode implementar **qualquer combinação** das anteriores

Nenhuma capability é pré-requisito para outra. Cada capability define suas próprias entidades de coordenação, ciclo de vida e obrigações.

**Dependências de extensão existem apenas onde explicitamente declaradas:**

- **Indoor** estende **Orders** — Indoor requer que Orders esteja implementada
- **Loyalty** estende **Customer** — Loyalty requer que Customer esteja implementada

Todas as demais combinações de capabilities são independentes por padrão.

---

## Eventos Representam Fatos, Não Etapas de Fluxo

Eventos representam **fatos que ocorreram**, não etapas de um fluxo de trabalho.

Um evento:
- É imutável
- Ocorre em um momento específico no tempo
- Comunica informações a outros sistemas

Eventos NÃO DEVEM:
- Codificar etapas internas de processo
- Espelhar máquinas de estado internas
- Descrever implicitamente como o trabalho é realizado

Apenas eventos relevantes para a **coordenação entre sistemas** são definidos pelo protocolo.

---

## Estados Representam a Condição Atual

Estados representam a **condição atual** de uma entidade.

- Estados podem mudar ao longo do tempo
- Estados descrevem o que é conhecido agora
- Estados são descritivos, não prescritivos

Consumidores DEVEM tratar o estado atual como a **fonte de verdade**, não a presença ou ausência de eventos opcionais.

---

## Eventos Normativos, Condicionais e Opcionais

O protocolo distingue entre:

- **Eventos normativos** — DEVEM ser emitidos em todos os contextos relevantes
- **Eventos condicionais** — DEVEM ser emitidos apenas em perfis específicos
- **Eventos opcionais** — PODEM ser emitidos para fornecer contexto adicional

Eventos opcionais:
- Nunca são exigidos para a correção do protocolo
- Não devem ser dependidos pelos consumidores
- Existem para enriquecer integrações, não para garantir comportamento

---

## Obrigações com Escopo por Perfil

As obrigações de eventos têm **escopo por perfil**, não são globais.

Um evento pode ser:
- Obrigatório em um perfil
- Opcional em outro
- Não aplicável em um terceiro

Isso evita super-especificação e preserva a flexibilidade do protocolo.

---

## Suporte Declarado em Vez de Flags por Pedido

O comportamento do protocolo NÃO DEVE ser controlado por flags dinâmicas por pedido.

Em vez disso:
- Os sistemas declaram explicitamente as capabilities, perfis e extensões suportadas
- O suporte declarado permanece estável entre pedidos
- Os pedidos contêm apenas dados de negócio e contexto

Isso garante comportamento previsível e separação limpa entre dados de negócio e declarações de suporte ao protocolo.

---

## Tolerância e Resiliência

O Open Delivery pressupõe sistemas distribuídos com falhas parciais.

Implementações DEVEM:
- Tolerar eventos opcionais ausentes
- Tratar eventos duplicados
- Aceitar entrega fora de ordem
- Evitar dependência de garantias de timing

O protocolo favorece **consistência eventual** em vez de sincronização estrita.

---

## Neutralidade de Transporte e Tecnologia

O protocolo é independente de:
- Protocolos de transporte
- Formatos de serialização
- Mecanismos de autenticação
- Modelos de implantação

Bindings de transporte PODEM ser definidos separadamente sem alterar o protocolo.

---

## Governança e Gestão

O Open Delivery é governado por um modelo formal de governança.

A governança existe para:
- Garantir transparência e isonomia
- Preservar a neutralidade do protocolo
- Coordenar sua evolução ao longo do tempo

A governança NÃO:
- Restringe a adoção
- Impõe condições comerciais
- Concede direitos exclusivos a qualquer participante

---

## Coordenação Institucional

A iniciativa Open Delivery é coordenada institucionalmente pela Abrasel.

Esta coordenação inclui:
- Gestão dos repositórios oficiais
- Publicação das especificações
- Atividades de comunicação e divulgação

A coordenação institucional NÃO:
- Altera a natureza aberta do protocolo
- Restringe o acesso à especificação
- Impõe participação ou registro obrigatórios

---

## Princípio do Minimalismo

O protocolo define a **superfície mínima necessária** para habilitar a interoperabilidade.

Qualquer coisa que:
- Seja puramente interna
- Seja específica de implementação
- Não seja necessária para a coordenação

DEVERIA permanecer fora do protocolo.

---

## Resumo

Estes princípios garantem que o Open Delivery v2 permaneça:
- Estável
- Neutro
- Extensível
- Adequado ao crescimento de longo prazo do ecossistema

Todas as seções futuras desta especificação DEVEM estar em conformidade com estes princípios.
