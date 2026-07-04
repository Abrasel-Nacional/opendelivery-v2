# Tratamento de Erros

Esta seção define a semântica de erro independente de transporte do protocolo.

## Regras de Erro

1. Respostas de erro DEVEM ser legíveis por máquina.
2. A classificação de erros DEVE preservar significado semântico para automação.
3. Produtores NÃO DEVEM emitir fatos de resultado bem-sucedido quando o processamento falhou.
4. Falhas específicas de cancelamento DEVEM ser explicitamente distinguíveis.

## Campos de Erro

| campo | tipo | obrigatório | descrição |
|---|---|---|---|
| `error.code` | string | SIM | Código estável legível por máquina |
| `error.message` | string | SIM | Mensagem legível por humano |
| `error.details` | object | NÃO | Contexto estruturado adicional |
| `error.retryable` | boolean | NÃO | Indica se a retentativa é segura |
| `error.timestamp` | string | NÃO | Timestamp de emissão (ISO 8601 date-time) |

## Exemplo de Erro

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Identificador de pedido desconhecido para este escopo de estabelecimento",
    "retryable": false
  }
}
```

## Códigos HTTP

| status | quando usar |
|---|---|
| `400 Bad Request` | Payload malformado ou parâmetros inválidos |
| `401 Unauthorized` | Credenciais ausentes ou inválidas |
| `403 Forbidden` | Credenciais válidas mas escopo insuficiente |
| `404 Not Found` | Recurso não encontrado |
| `409 Conflict` | Conflito de estado ou versão |
| `422 Unprocessable Entity` | Transição de estado inválida ou violação de regra de negócio |
| `429 Too Many Requests` | Rate limit excedido |
| `500 Internal Server Error` | Falha interna inesperada do servidor |
| `202 Accepted` | Operação aceita para processamento assíncrono (não é erro) |

## Retentativas

Quando `error.retryable` for `true`, o consumidor PODE retentar a operação após um intervalo.

Implementações DEVERIAM usar backoff exponencial com jitter para retentativas:

- Primeira retentativa: após 1s
- Segunda retentativa: após 2s
- Terceira retentativa: após 4s
- Máximo recomendado: 3 retentativas

Operações idempotentes (com `X-Request-Id`) são seguras para retentativa. Operações não idempotentes NÃO DEVEM ser retentadas automaticamente.

## Erros de Transição de Estado

Quando um consumidor tenta uma transição de estado inválida (ex.: confirmar um pedido já cancelado), o produtor DEVE retornar `422 Unprocessable Entity` com um código de erro que identifique a transição inválida.

```json
{
  "error": {
    "code": "INVALID_STATE_TRANSITION",
    "message": "Não é possível confirmar um pedido no status CANCELLED",
    "retryable": false,
    "details": {
      "currentStatus": "CANCELLED",
      "attemptedTransition": "confirm"
    }
  }
}
```
