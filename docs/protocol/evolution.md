# Evolução do Protocolo

Esta seção descreve como o Open Delivery Protocol evolui ao longo do tempo e as regras que governam a introdução de mudanças.

## Ciclo de Vida de Versões

O ODP usa versionamento semântico com um ciclo de Release Candidate (RC) antes de cada release estável.

| Fase | Descrição |
|---|---|
| **Draft** | Proposta em discussão nos grupos de trabalho — não implementar |
| **Release Candidate (RC)** | Especificação estável para implementação piloto; mudanças ainda possíveis com base em feedback |
| **Stable** | Release final — retrocompatibilidade garantida dentro da major version |
| **Deprecated** | Versão antiga ainda suportada por período de migração, mas sem novos desenvolvimentos |

## Versão Atual

| Versão | Status | Disponível desde |
|---|---|---|
| `2.0.0-rc` | Release Candidate | Julho 2026 |
| `1.7.0` | Stable (referência V1) | — |

## Regras de Evolução

### Mudanças retrocompatíveis (minor/patch)

Podem ser introduzidas sem incremento de major version:

- Adição de novos campos opcionais em payloads existentes
- Adição de novos valores em enums (consumidores DEVERIAM tolerar valores desconhecidos)
- Adição de novos endpoints ou operações
- Adição de novos eventos opcionais
- Correções de ambiguidade que não alteram comportamento implementado

### Mudanças que quebram compatibilidade (major)

Requerem incremento de major version e período de migração:

- Remoção de campos obrigatórios
- Alteração de semântica de campos existentes
- Remoção de endpoints ou operações
- Mudança de comportamento normativo de eventos obrigatórios

### Regra geral

Mudanças DEVEM ser documentadas como atualizações de comportamento do protocolo primeiro. Mapeamentos de transporte PODEM ser definidos depois como perfis separados, preservando a mesma semântica de domínio.

## Coexistência V1 e V2

A V1 **não será descontinuada abruptamente**. O período de migração gradual permite que implementações existentes migrem sem interrupção de serviço.

Durante o período de coexistência:

- Implementações PODEM declarar suporte a múltiplas versões no Discovery
- O campo `supportedVersions` no documento well-known lista todas as versões ativas
- Parceiros de integração negociam bilateralmente qual versão usar com base no Discovery mútuo

## Governança da Evolução

Propostas de mudança passam pelo comitê técnico do Open Delivery antes de serem incorporadas à especificação. O comitê se reúne semanalmente e é aberto a todos os aderentes do protocolo.

Para propor mudanças: abra uma issue no [repositório oficial](https://github.com/Abrasel-Nacional/opendelivery-v2).
