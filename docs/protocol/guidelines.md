# Regras Gerais

Esta seção define as regras transversais do protocolo, aplicáveis a todas as capabilities.

## Palavras-chave Normativas

As palavras `DEVE` (`MUST`), `NÃO DEVE` (`MUST NOT`), `DEVERIA` (`SHOULD`) e `PODE` (`MAY`) são normativas, conforme definido na RFC 2119.

Na documentação técnica em inglês, os termos originais em maiúsculas (`MUST`, `MUST NOT`, `SHOULD`, `MAY`) são mantidos por convenção internacional de especificações.

## Regras de Interoperabilidade

1. Produtores DEVEM incluir todos os campos obrigatórios.
2. Consumidores DEVEM validar os campos obrigatórios.
3. Consumidores DEVERIAM tolerar campos adicionais desconhecidos.
4. Participantes NÃO DEVEM inferir transições de estado não suportadas.
5. Participantes DEVEM processar eventos de forma idempotente.

## Padrão de Documentação de Payload

Cada descrição de payload do protocolo DEVE incluir:

1. Tabela de campos com `nome`, `tipo`, `obrigatório` e `descrição`.
2. Exemplo de payload.

Exemplos são formatos ilustrativos do protocolo, não contratos de transporte.

## Padrão de Documentação de Operação

Cada operação documentada DEVE declarar:

1. Se autenticação é necessária.
2. Qual escopo ou permissão é exigido quando a autenticação se aplica.
3. Referência à seção de Autenticação.

Isso permite que implementadores entendam os requisitos de acesso diretamente da definição da operação, sem precisar inferir a partir de exemplos de transporte.

## Regras de Segurança

- O contexto de autenticação DEVE ter escopo por estabelecimento.
- Segredos NÃO DEVEM ser expostos em logs ou traces.
- A validação de confiança de callbacks DEVE ser aplicada para entrega assíncrona.

## Regras de Compatibilidade

- Campos obrigatórios existentes NÃO DEVEM ser removidos em atualizações retrocompatíveis.
- Extensões de enum DEVERIAM ser aditivas.
- Mudanças de comportamento que quebram compatibilidade DEVEM ser sinalizadas por versão.

## Timestamps

Todos os campos de data e hora DEVEM usar o formato ISO 8601 com timezone explícito.

- Formato recomendado: `2026-07-01T14:30:00Z` (UTC)
- Formatos com offset também são aceitos: `2026-07-01T11:30:00-03:00`
- Datas sem hora NÃO DEVEM ser usadas em campos de timestamp

## Identificadores

Identificadores de entidades (`id`) DEVEM ser:

- Strings opacas (sem significado semântico derivável)
- UUID v4 recomendado
- Únicos dentro do escopo declarado
- Estáveis — uma vez criados, NÃO DEVEM ser alterados

## Paginação

Endpoints de listagem que retornam coleções DEVERIAM suportar paginação.

| parâmetro | tipo | descrição |
|---|---|---|
| `page` | integer | Número da página (começando em 1) |
| `pageSize` | integer | Itens por página (padrão e máximo definidos por implementação) |

A resposta DEVERIA incluir metadados de paginação:

```json
{
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 150
  }
}
```

## Idempotência

Operações de mutação DEVERIAM suportar idempotência via header `X-Request-Id`.

- O produtor DEVE processar uma requisição com o mesmo `X-Request-Id` apenas uma vez
- Requisições repetidas com o mesmo `X-Request-Id` DEVEM retornar o mesmo resultado
- O `X-Request-Id` DEVE ser gerado pelo consumidor e ser único por operação
