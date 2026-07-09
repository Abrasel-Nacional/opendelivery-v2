# Merchant

<p class="od-meta">
  <span class="od-badge od-badge--code">merchant</span>
</p>

<div class="od-api-callout">
  <p>Conceito da capability. Detalhes de loja e catálogo nas páginas filhas.</p>
  <a href="../reference/merchant/">Abrir referência OpenAPI →</a>
</div>

## O que é

A capability **Merchant** define como o ecossistema troca informações sobre o **estabelecimento** e o que ele oferece: identidade da loja, contextos de serviço (delivery, takeout, indoor) e **catálogo**.

É a fonte de verdade para dados estáticos e operacionais do merchant no Open Delivery — sem cobrir pedidos, logística ou CRM.

## Como a documentação se organiza

A capability `merchant` no Discovery é **uma só**. Na documentação ela se divide em páginas para facilitar a leitura:

| Página | Conteúdo |
|---|---|
| **Merchant** (esta) | Conceito, papéis, mapa do domínio, discovery e autorização |
| **[Dados da Loja](merchant-store.md)** | Merchant ID, identidade, `Service`, horários, área, pause |
| **[Menus](menu.md)** | Hierarquia de cardápio, ItemOffer, opcionais, snapshot, sincronismo |

```
Merchant (capability)
├── Dados da Loja     → identidade + services
└── Menus             → catálogo (CRUD + snapshot)
```

!!! note "Não são extensões do protocolo"
    **Dados da Loja** e **Menus** são módulos de documentação. Extensões formais (ex.: Indoor, Loyalty) se declaram no Discovery; o cardápio **não** — ele faz parte de `merchant`.

## Papéis

| Papel | Responsabilidade |
|---|---|
| **Software Service** | Fonte de verdade do estabelecimento e, em muitos fluxos, do catálogo. Expõe interfaces de leitura e escrita. |
| **Ordering Application** | Consome loja e catálogo para montar a experiência de pedido. Na V2 **gera** o `merchantId`. |
| **Delivery Platform** (opcional) | Consome contexto de serviço e disponibilidade para decisões logísticas. |

## O que a capability cobre

- Identidade e dados descritivos da loja → [Dados da Loja](merchant-store.md)
- Serviços (`DELIVERY` / `TAKEOUT` / `INDOOR`), horários e pause → [Dados da Loja](merchant-store.md)
- Catálogo: menus, categorias, item-offers, option-groups, opções → [Menus](menu.md)
- Snapshot e sincronismo incremental do cardápio → [Menus](menu.md)

## O que não cobre

- Ciclo de vida de pedidos → [Orders](orders.md)
- Coordenação de entrega → [Logistics](logistics.md)
- Cliente, reviews e fidelidade → [Customer](customer.md)

## Discovery

Participantes que expõem Merchant DEVEM declarar `merchant` no well-known:

```json
"capabilities": {
  "merchant": {
    "baseUrl": "https://api.example.com",
    "operations": ["read", "write", "snapshot"]
  }
}
```

Loja e menus entram na **mesma** capability — sem chave `extension` para catálogo.

## Autorização

Operações Merchant exigem Bearer (OAuth 2.0). Escopos mínimos recomendados:

| Escopo | Operações |
|---|---|
| `merchant.read` | Leitura de loja e catálogo |
| `merchant.write` | Criação e atualização |
| `merchant.events.write` | Emissão de eventos de mudança |

(Em alguns bindings legados o catálogo também aparece como `od.menu` — ver [Autenticação](authentication.md).)

## Por onde seguir

1. Entenda [Dados da Loja](merchant-store.md) (ID + services)  
2. Implemente [Menus](menu.md) (catálogo e sync)  
3. Consulte o [OpenAPI Merchant](../reference/merchant.md)

---

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo</div>
  <div class="od-next-step__links">
    <a href="merchant-store/">Dados da Loja</a>
    <a href="menu/">Menus</a>
    <a href="../reference/merchant/">OpenAPI Merchant</a>
  </div>
</div>
