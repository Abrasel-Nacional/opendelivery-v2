# Merchant

<p class="od-meta">
  <span class="od-badge od-badge--core">Capability</span>
  <span class="od-badge od-badge--code">merchant</span>
</p>

<div class="od-api-callout">
  <p>Identidade e serviços nesta página. Catálogo (menu, itens, opcionais) no módulo Menu.</p>
  <a href="menu/">Abrir módulo Menu / Cardápio →</a>
</div>

## Visão Geral

A capability **Merchant** define a identidade do estabelecimento, os contextos de serviço (delivery, retirada, salão) e o **catálogo** publicado no ecossistema. É a fonte de verdade para dados estáticos e operacionais relativos ao estabelecimento e ao que ele oferece.

Nesta documentação o domínio está organizado em duas páginas (mesma capability `merchant`):

| Página | Conteúdo |
|---|---|
| **Merchant** (esta) | Merchant ID, papéis, services, pause, discovery e autorização |
| **[Menu / Cardápio](menu.md)** | Hierarquia de catálogo, ItemOffer, opcionais, snapshot e sincronismo |

Esta capability cobre:

- Identidade e informações descritivas do estabelecimento
- Serviços operacionais (delivery, takeout, indoor) e seus horários
- Composição do catálogo: menus, categorias, item-offers, option-groups e opções → ver [Menu](menu.md)
- Disponibilidade operacional dos itens → ver [Menu](menu.md)
- Pausa e retomada de serviços

Esta capability **não** cobre:

- Ciclo de vida de pedidos (capability Orders)
- Coordenação de entrega (capability Logistics)
- Relacionamento com clientes e fidelidade (capability Customer)

!!! note "Menu não é extensão"
    Indoor e Loyalty são **extensões** opcionais de outras capabilities. O cardápio é **módulo integrante** de Merchant — declarado no Discovery como parte de `merchant`, não como `extension`.

---

## Papéis

| Papel | Responsabilidade |
|---|---|
| **Software Service** | Fonte de verdade do estabelecimento e, em muitos fluxos, do catálogo. Expõe interfaces de leitura e escrita. |
| **Ordering Application** | Consome dados de estabelecimento e catálogo para construir interfaces de pedido. Na V2 gera o `merchantId`. |
| **Delivery Platform** (opcional) | Consome contexto de serviço e disponibilidade para decisões logísticas. |

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
| `menuId` | string | NÃO | Referência ao [menu](menu.md) ativo para este serviço |

### Pausa de serviço

Para pausas operacionais (ex.: cozinha sobrecarregada, falta de entregadores):

```
POST /merchants/{merchantId}/services/{serviceType}/pause
```

A pausa produz resposta `202 Accepted`. O serviço permanece em `PAUSED` até ser reativado via `PATCH /merchants/{merchantId}/services/{serviceType}` com `status: OPEN`.

---

## Catálogo (Menu)

A hierarquia Menu → Category → ItemOffer → OptionGroup → Option, o snapshot e as regras de sincronismo estão em:

**[Módulo Menu / Cardápio →](menu.md)**

---

## Discovery

Participantes que expõem a capability Merchant DEVEM declarar `merchant` no documento well-known.

```json
"capabilities": {
  "merchant": {
    "baseUrl": "https://api.example.com",
    "operations": ["read", "write", "snapshot"]
  }
}
```

Não há chave de extension separada para menu — o catálogo entra nas operações/capabilities de `merchant`.

---

## Autorização

Todas as operações da capability Merchant exigem autenticação Bearer (OAuth 2.0).

Escopos mínimos recomendados:

| Escopo | Operações |
|---|---|
| `merchant.read` | Leitura de dados do estabelecimento e catálogo |
| `merchant.write` | Criação e atualização de entidades do catálogo |
| `merchant.events.write` | Emissão de eventos de mudança |

(Em alguns bindings/escopos legados o acesso ao catálogo também aparece como `od.menu` — ver [Autenticação](authentication.md) e o OpenAPI.)

---

## Regras normativas

**O Software Service DEVE:**

- Expor `merchantId` como identificador único e estável gerado pela Ordering Application
- Preservar integridade referencial do catálogo em todas as operações de atualização (detalhes em [Menu](menu.md))
- Retornar `202 Accepted` para mutações com efeito assíncrono

**A Ordering Application DEVE:**

- Gerar o `merchantId` antes do cadastro e mantê-lo estável
- Consultar o snapshot para bootstrap e usar endpoints granulares para deltas (ver [Menu](menu.md))

**Ambos DEVEM:**

- Declarar a capability `merchant` no discovery antes de iniciar operações

---

**Referência completa de campos e contratos REST:** [Referência da API — Merchant →](../reference/merchant.md)

---

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo</div>
  <div class="od-next-step__links">
    <a href="menu/">Módulo Menu / Cardápio</a>
    <a href="../reference/merchant/">Abrir referência OpenAPI</a>
    <a href="discovery/">Configurar Discovery</a>
  </div>
</div>
