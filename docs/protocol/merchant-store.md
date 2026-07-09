# Dados da Loja

<p class="od-meta">
  <span class="od-badge od-badge--code">merchant</span>
  <span class="od-badge">Merchant · identidade e services</span>
</p>

<div class="od-api-callout">
  <p>Merchant ID, Basic Info e Service. O catálogo fica em <strong>Menus</strong>.</p>
  <a href="menu/">Ir para Menus →</a>
</div>

Esta página cobre os **dados da loja** dentro da capability [Merchant](merchant.md):

- Identidade e informações descritivas do estabelecimento
- Serviços operacionais (`Service`: delivery, takeout, indoor)
- Horários, área de entrega e pausa operacional

O **cardápio** (itens, categorias, opcionais) está em [Menus](menu.md).

---

## Merchant ID — gerado pelo originador

!!! important "Quebra de comportamento em relação à V1"
    Na V1, o `merchantId` era gerado pelo Software Service (POS). Na V2, o `merchantId` é **gerado pela Ordering Application** no momento do cadastro do estabelecimento.

    Isso inverte quem tem a chave de referência: a plataforma de pedidos escolhe o ID e o POS o registra. Os dois lados DEVEM usar exatamente o mesmo identificador em todas as operações subsequentes.

Essa decisão foi tomada para:

- Eliminar a dependência de um round-trip de cadastro antes de enviar pedidos
- Permitir que a Ordering Application referencie o merchant de forma determinista desde a criação
- Simplificar reconciliações em cenários multi-plataforma

O `merchantId` DEVE ser único por Ordering Application. O formato DEVE ser uma string opaca (UUID v4 recomendado).

---

## Serviço (`Service`) {#serviço-service}

Cada estabelecimento pode ter múltiplos serviços. Um serviço é identificado pelo seu **tipo** — não há Service ID separado.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | string (enum) | SIM | `DELIVERY`, `TAKEOUT` ou `INDOOR` |
| `status` | string (enum) | SIM | `OPEN`, `CLOSED` ou `PAUSED` |
| `operatingHours` | array[object] | SIM | Horários de funcionamento por dia da semana |
| `deliveryArea` | object | NÃO | Raio ou polígono de cobertura (somente `DELIVERY`) |
| `menuId` | string | NÃO | Referência ao menu ativo deste serviço — ver [Menus](menu.md) |

### Pausa de serviço

Para pausas operacionais (ex.: cozinha sobrecarregada, falta de entregadores):

```
POST /merchants/{merchantId}/services/{serviceType}/pause
```

A pausa produz resposta `202 Accepted`. O serviço permanece em `PAUSED` até ser reativado via `PATCH /merchants/{merchantId}/services/{serviceType}` com `status: OPEN`.

---

## Relação com Menus

Cada service pode apontar para um menu via `menuId`. A hierarquia de catálogo, snapshot e sincronismo estão em:

**[Menus →](menu.md)**

---

## Regras normativas (loja)

**O Software Service DEVE:**

- Expor `merchantId` como identificador único e estável gerado pela Ordering Application
- Respeitar os estados de service (`OPEN`, `CLOSED`, `PAUSED`) de forma consistente

**A Ordering Application DEVE:**

- Gerar o `merchantId` antes do cadastro e mantê-lo estável

**Ambos DEVEM:**

- Declarar a capability `merchant` no [Discovery](discovery.md) antes de iniciar operações

---

**Contrato REST completo:** [Referência da API — Merchant →](../reference/merchant.md)

---

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo</div>
  <div class="od-next-step__links">
    <a href="merchant/">Visão geral Merchant</a>
    <a href="menu/">Menus</a>
    <a href="../reference/merchant/">OpenAPI Merchant</a>
  </div>
</div>
