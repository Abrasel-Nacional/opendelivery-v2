# Menu / Cardápio

<p class="od-meta">
  <span class="od-badge od-badge--core">Módulo</span>
  <span class="od-badge od-badge--code">menu</span>
  <span class="od-badge">capability: merchant</span>
</p>

<div class="od-api-callout">
  <p>O cardápio é um <strong>módulo da capability Merchant</strong> — não uma extensão opcional. Mesmo contrato OpenAPI.</p>
  <a href="../reference/merchant/">Abrir referência OpenAPI →</a>
</div>

!!! note "Não é extensão formal"
    Diferente de [Indoor](indoor.md) ou [Loyalty](../extensions/loyalty.md), o Menu **não** se declara como `extension` no Discovery. Ele faz parte da capability `merchant`. A separação nesta documentação é só para **navegação e clareza**: identidade/serviços vs catálogo.

Esta página cobre a composição e o sincronismo do **catálogo**: menus, categorias, item-offers, option-groups e opções. Para Merchant ID, services e pause, veja a [visão geral de Merchant](merchant.md).

---

## Hierarquia do catálogo

O catálogo é composto por entidades independentes com relacionamentos explícitos. Cada entidade é gerenciada por **CRUD granular** — não há mais a operação monolítica de publicação do cardápio da V1.

```
Merchant
├── Service (DELIVERY / TAKEOUT / INDOOR)  →  menuId
└── Menu
    └── Category
        └── ItemOffer
            └── OptionGroup (recursivo)
                └── Option
```

Um estabelecimento pode ter **múltiplos menus** (ex.: almoço, janta, bebidas). Cada [Service](merchant.md#serviço-service) pode referenciar o menu ativo via `menuId`.

---

## Menu e Categoria

Um **Menu** agrupa Categorias. Uma **Categoria** agrupa ItemOffers.

Operações típicas (ver OpenAPI para o contrato completo):

- CRUD de menus, categorias e vínculos
- Snapshot hierárquico para bootstrap (abaixo)

---

## ItemOffer

Um **ItemOffer** é a oferta de um produto com preço e disponibilidade no contexto do catálogo.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string | SIM | Identificador único (UUID) |
| `name` | string | SIM | Nome exibido ao consumidor |
| `description` | string | NÃO | Texto descritivo |
| `unity_price` | object | SIM | Preço unitário com valor e moeda |
| `quantity_available` | integer | NÃO | Quantidade disponível no momento (operacional, não estoque) |
| `optionGroupIds` | array[string] | NÃO | Grupos de opções associados |

!!! info "`quantity_available` é operacional"
    Representa a quantidade disponível **agora** (ex.: prato do dia com 10 porções). **Não** é integração de estoque multi-canal. Quando omitido, considera-se disponibilidade ilimitada.

---

## OptionGroup (recursivo)

Grupo de opções selecionáveis (ex.: “Ponto da carne”, “Complementos”). OptionGroups são **recursivos** — uma opção pode carregar um sub-grupo.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string | SIM | Identificador único |
| `name` | string | SIM | Nome do grupo |
| `min` | integer | SIM | Mínimo de seleções (0 = opcional) |
| `max` | integer | SIM | Máximo de seleções |
| `options` | array[Option] | SIM | Lista de opções |

### Option

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string | SIM | Identificador único |
| `name` | string | SIM | Nome da opção |
| `option_price` | object | SIM | Preço incremental da opção |
| `optionGroupIds` | array[string] | NÃO | Sub-grupos (recursividade) |

!!! important "`option_price` é obrigatório na V2"
    Na V1 o preço da opção era opcional. Na V2, **todo `Option` DEVE ter `option_price`**. Sem custo adicional: `{ "value": 0, "currency": "BRL" }`. O campo `subtotal` foi removido — o total no pedido usa `unity_price` + soma dos `option_price`.

---

## Snapshot do cardápio

Para bootstrap ou reconciliação completa:

```
GET /merchants/{merchantId}/menus/{menuId}/snapshot
```

O snapshot retorna menu, categorias, item-offers, option-groups e options em uma estrutura hierárquica. **Recomendado** para onboarding e full sync.

Para atualizações incrementais, use os endpoints granulares de cada entidade (CRUD).

---

## Sincronismo (visão prática)

| Cenário | Abordagem |
|---|---|
| Carga inicial / reconciliação | Snapshot |
| Mudança de preço ou nome | PATCH da entidade (ItemOffer, Option…) |
| Novo item / categoria | POST na entidade correspondente |
| Menu completo substituído | PUT/snapshot conforme binding |

Quem é **fonte da verdade** do catálogo (PDV vs originador) deve ser declarado no [Discovery](discovery.md) e nas regras de negócio da integração — o protocolo não impõe um único dono universal.

---

## Regras normativas (catálogo)

**O Software Service DEVE:**

- Preservar integridade referencial entre menu, categorias, item-offers, option-groups e opções
- Retornar `202 Accepted` para mutações assíncronas
- Declarar `quantity_available` só quando houver limitação operacional real

**A Ordering Application DEVE:**

- Tratar `quantity_available` como dica operacional, não garantia de estoque
- Preferir snapshot no bootstrap e endpoints granulares para deltas

**Ambos DEVEM:**

- Usar `option_price: { value: 0, currency: "..." }` para opções sem custo
- Operar o catálogo sob a capability `merchant` (escopos de leitura/escrita de merchant/menu)

---

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo</div>
  <div class="od-next-step__links">
    <a href="merchant/">Visão geral Merchant</a>
    <a href="../reference/merchant/">OpenAPI Merchant</a>
    <a href="orders/">Capability Orders</a>
  </div>
</div>
