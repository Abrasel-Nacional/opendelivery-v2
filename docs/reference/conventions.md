# Regras gerais e convenções

!!! warning "Release Candidate (V2.0.0-rc)"
    Convenções da **V2.0.0-rc**, em validação com o ecossistema. Detalhes: [Evolução](../protocol/evolution.md) · [Changelog](../guide/changelog.md).

Esta página resume **convenções compartilhadas** da API REST/HTTP do Open Delivery V2.

**Fonte normativa:** cada especificação da API em [Referência da API](index.md). Em caso de divergência entre este resumo e a especificação da API, **prevalece a especificação da API**.

Para o modelo mental do domínio (papéis, fluxos, status vs eventos), use a tab **Protocolo**.

---

## Palavras-chave normativas

Nas especificações da API (em inglês), `MUST`, `MUST NOT`, `SHOULD` e `MAY` seguem a [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

Na documentação em português, equivalentes comuns: `DEVE`, `NÃO DEVE`, `DEVERIA`, `PODE`.

---

## Interoperabilidade

Comportamentos esperados em todas as capabilities (detalhados nos especificações da API):

1. Produtores incluem todos os campos obrigatórios do schema.
2. Consumidores validam campos obrigatórios.
3. Consumidores toleram campos adicionais desconhecidos (evolução aditiva).
4. Participantes não inferem transições de estado não suportadas.
5. Eventos recebidos mais de uma vez são tratados com **deduplicação** (por id de evento / fato), sem reprocessar efeito de negócio.

---

## Segurança (visão geral)

- Autenticação e escopos: [Autenticação](authentication.md) e [Discovery](discovery.md).
- Segredos não devem aparecer em logs ou traces.
- Webhooks exigem verificação de assinatura quando o contrato assim definir.

---

## Timestamps

Campos de data e hora usam **ISO 8601** com fuso explícito.

- Recomendado (UTC): `2026-07-01T14:30:00Z`
- Offset aceito: `2026-07-01T11:30:00-03:00`
- Datas sem hora não substituem timestamps

---

## Identificadores

Identificadores de entidades (`id`) são, em geral:

- Strings opacas (sem semântica derivável do valor)
- UUID v4 recomendado
- Únicos no escopo declarado
- Estáveis após a criação

Regras específicas de cada recurso estão na especificação da capability.

---

## Paginação

Listagens que retornam coleções costumam usar paginação. Padrão frequente:

| parâmetro | tipo | descrição |
|---|---|---|
| `page` | integer | Página (a partir de 1) |
| `pageSize` | integer | Itens por página |

Metadados de exemplo:

```json
{
 "pagination": {
 "page": 1,
 "pageSize": 20,
 "total": 150
 }
}
```

Parâmetros e defaults exatos: ver cada operação na especificação da API.

---

## Duplicidade de operações de ciclo de vida

Regra alinhada ao Comitê de Arquitetura (26/03/2026) e à intenção da Keeta: chamadas repetidas **não devem quebrar o fluxo** quando o estado alvo **já foi atingido**.

Na V1, a documentação sugeria `HTTP 422` para reprocessamento síncrono do mesmo fato e, no caminho assíncrono, reapresentar o evento no polling. A V2 é **async-first** (`202 Accepted`).

### Default universal (V2)

Para operações de progressão de pedido (e análogas) que retornam `202`:

| Situação | Resposta HTTP | Efeito de negócio |
|---|---|---|
| Transição **válida** ainda não aplicada | `202 Accepted` | Aceita processamento; resultado via evento / `GET` |
| Mesma operação **já aplicada** (ex.: `POST …/confirm` com pedido já `CONFIRMED`) | **`202 Accepted`** | **Sem nova transição**; o receptor **PODE** reapresentar o evento correspondente (webhook/polling) |
| Transição **inválida** (ex.: confirmar pedido `CANCELLED`) | `4xx` de erro (ex.: `409` / `422` conforme a especificação da API) | Nenhuma mudança de estado |

Implementadores **NÃO DEVEM** tratar a repetição de uma operação **já concluída com sucesso** como falha de negócio com `422`/`409` apenas por “já ter sido feita”. Esse era o anti-padrão da V1 que quebrava PDVs com confirmação dupla.

A **fonte de verdade** continua sendo o **status** consultável e os **eventos** — a resposta HTTP do `POST` não fecha lógica de negócio.

Detalhe normativo: [especificação Orders](orders.md) (e demais capabilities com o mesmo padrão async).

---

## Compatibilidade

- Campos obrigatórios existentes não são removidos em releases retrocompatíveis
- Extensões de enum devem ser aditivas; consumidores toleram valores desconhecidos quando possível
- Mudanças breaking usam versionamento (ver [Evolução](../protocol/evolution.md))

---

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="error-handling.md">Tratamento de Erros</a> — envelope e códigos HTTP</li>
    <li><a href="authentication.md">Autenticação</a> — OAuth, escopos e webhooks</li>
    <li><a href="discovery.md">Discovery</a> — manifesto well-known</li>
    <li><a href="index.md">Visão geral da API</a> — specs por capability</li>
  </ul>
</div>
