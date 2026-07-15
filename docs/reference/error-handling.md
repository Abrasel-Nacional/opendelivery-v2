# Tratamento de Erros

Esta página descreve o **modelo de erro HTTP** compartilhado pelas especificações da API do Open Delivery V2.

**Fonte normativa:** respostas e schemas de erro em cada [especificação da API](index.md). Este resumo orienta implementadores; em divergência, **prevalece a especificação da API**.

---

## Princípios

1. Respostas de erro são legíveis por máquina (`code` estável).
2. A classificação preserva significado para automação (retry, UX, auditoria).
3. Produtores não emitem sucesso de negócio quando o processamento falhou.
4. Falhas de cancelamento e de transição de estado são distinguíveis por código.

---

## Envelope de erro (padrão)

| campo | tipo | obrigatório | descrição |
|---|---|---|---|
| `error.code` | string | SIM | Código estável legível por máquina |
| `error.message` | string | SIM | Mensagem legível por humano |
| `error.details` | object | NÃO | Contexto estruturado adicional |
| `error.retryable` | boolean | NÃO | Indica se retentar é seguro |
| `error.timestamp` | string | NÃO | Instantâneo ISO 8601 |

### Exemplo

```json
{
 "error": {
 "code": "ORDER_NOT_FOUND",
 "message": "Unknown order identifier for this merchant scope",
 "retryable": false
 }
}
```

---

## Códigos HTTP (uso típico)

| status | quando usar |
|---|---|
| `400 Bad Request` | Payload malformado ou parâmetros inválidos |
| `401 Unauthorized` | Credenciais ausentes ou inválidas |
| `403 Forbidden` | Credenciais válidas, escopo insuficiente |
| `404 Not Found` | Recurso não encontrado |
| `409 Conflict` | Conflito de estado ou versão |
| `422 Unprocessable Entity` | Transição inválida ou regra de negócio |
| `429 Too Many Requests` | Rate limit |
| `500 Internal Server Error` | Falha interna inesperada |
| `202 Accepted` | Aceito para processamento assíncrono (**não é erro**) |

Muitas mutações do ODP V2 são **async-first** (`202`). Confirme o resultado via evento ou `GET`, conforme a capability.

---

## Retentativas

Quando `error.retryable` for `true`, o cliente pode retentar após um intervalo.

Recomendação: backoff exponencial com jitter (ex.: 1s → 2s → 4s; no máximo ~3 tentativas).

- Em mutações async (`202`), a **repetição da mesma operação já aplicada** (ex.: segundo `confirm` com pedido já `CONFIRMED`) **não é erro** — ver [duplicidade de ciclo de vida](conventions.md#duplicidade-de-operacoes-de-ciclo-de-vida).
- Não confunda isso com transição **inválida** (estado incompatível), que sim retorna `4xx`.

---

## Erros de transição de estado

Use erro **somente** quando a transição é **impossível** no estado atual (ex.: confirmar pedido já `CANCELLED`). Pedido **já no estado alvo** da operação **não** é erro — retorne `202` (ver convenções).

Exemplo de transição inválida:

```json
{
 "error": {
 "code": "INVALID_STATE_TRANSITION",
 "message": "Cannot confirm an order in CANCELLED status",
 "retryable": false,
 "details": {
 "currentStatus": "CANCELLED",
 "attemptedTransition": "confirm"
 }
 }
}
```

Códigos e status HTTP exatos: especificação da capability.

---

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="conventions.md">Convenções gerais</a> — datas, paginação, duplicidade de ciclo de vida</li>
    <li><a href="authentication.md">Autenticação</a> — OAuth, escopos e assinatura de webhooks</li>
    <li><a href="../protocol/principles.md">Princípios do protocolo</a> — domínio e modelo mental</li>
  </ul>
</div>
