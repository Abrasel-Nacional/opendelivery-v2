# Merchant / Cardápio

<p class="od-meta">
  <span class="od-badge od-badge--core">Capability</span>
  <span class="od-badge od-badge--code">merchant</span>
</p>

<div class="od-api-callout">
  <p>Regras e fluxos nesta página. Contrato HTTP na referência OpenAPI.</p>
  <a href="../reference/merchant/">Abrir referência OpenAPI →</a>
</div>

## Visão Geral

A capability **Merchant** define a identidade do estabelecimento, os contextos de serviço (delivery, retirada, salão) e as entidades de catálogo publicadas no ecossistema. É a fonte de verdade para todos os dados estáticos e operacionais relativos ao estabelecimento e ao que ele oferece.

Esta capability cobre:

- Identidade e informações descritivas do estabelecimento
- Serviços operacionais (delivery, takeout, indoor) e seus horários
- Composição do catálogo: menus, categorias, item-offers, option-groups e opções
- Disponibilidade operacional dos itens
- Pausa e retomada de serviços

Esta capability **não** cobre:

- Ciclo de vida de pedidos (capability Orders)
- Coordenação de entrega (capability Logistics)
- Relacionamento com clientes e fidelidade (capability Customer)

---

## Papéis

| Papel | Responsabilidade |
|---|---|
| **Software Service** | Fonte de verdade do estabelecimento e do catálogo. Expõe as interfaces de leitura e escrita do Merchant. |
| **Ordering Application** | Consome dados de estabelecimento e catálogo para construir interfaces de pedido. |
| **Delivery Platform** (opcional) | Consome contexto de serviço e disponibilidade do estabelecimento para decisões logísticas. |

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

## Entidades do catálogo

O catálogo é composto por entidades independentes com relacionamentos explícitos. Cada entidade é gerenciada por CRUD granular — não há mais uma operação monolítica de publicação do cardápio.

```
Merchant
└── Service (por tipo: delivery / takeout / indoor)
└── Menu
    └── Category
        └── ItemOffer
            └── OptionGroup (recursivo)
                └── Option
```

### Serviço (`Service`)

Cada estabelecimento pode ter múltiplos serviços. Um serviço é identificado pelo seu **tipo** — não há Service ID separado.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | string (enum) | SIM | `DELIVERY`, `TAKEOUT` ou `INDOOR` |
| `status` | string (enum) | SIM | `OPEN`, `CLOSED` ou `PAUSED` |
| `operatingHours` | array[object] | SIM | Horários de funcionamento por dia da semana |
| `deliveryArea` | object | NÃO | Raio ou polígono de cobertura (somente `DELIVERY`) |
| `menuId` | string | NÃO | Referência ao menu ativo para este serviço |

#### Pausa de serviço

Para pausas operacionais (ex.: cozinha sobrecarregada, falta de entregadores), use:

```
POST /merchants/{merchantId}/services/{serviceType}/pause
```

A pausa é uma transição de estado que produz resposta `202 Accepted`. O serviço permanece em `PAUSED` até ser reativado via `PATCH /merchants/{merchantId}/services/{serviceType}` com `status: OPEN`.

### Menu e Categoria

Um Menu agrupa Categorias. Uma Categoria agrupa ItemOffers. Um estabelecimento pode ter múltiplos Menus (ex.: cardápio do almoço, cardápio da janta, cardápio de bebidas).

### ItemOffer

Um **ItemOffer** é a oferta de um produto com preço e disponibilidade.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string | SIM | Identificador único (UUID) |
| `name` | string | SIM | Nome exibido ao consumidor |
| `description` | string | NÃO | Texto descritivo |
| `unity_price` | object | SIM | Preço unitário com valor e moeda |
| `quantity_available` | integer | NÃO | Quantidade disponível no momento (operacional, não estoque) |
| `optionGroupIds` | array[string] | NÃO | Grupos de opções associados |

!!! info "`quantity_available` é operacional"
    Este campo representa a quantidade disponível **agora** (por exemplo, um prato do dia com 10 porções restantes). Não é um controle de estoque — o sistema de gestão de estoque não é responsabilidade do protocolo. Quando não informado, considera-se disponibilidade ilimitada.

### OptionGroup (recursivo)

Um grupo de opções contém opções selecionáveis pelo cliente (ex.: "Ponto da carne", "Complementos"). OptionGroups são **recursivos** — uma opção pode conter um sub-grupo de opções.

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
    Na V1, o preço da opção era opcional. Na V2, **todo `Option` DEVE ter `option_price`**. Se a opção não tem custo adicional, declare `{ "value": 0, "currency": "BRL" }`. O campo `subtotal` foi removido — o total de um pedido com opções é calculado a partir de `unity_price` + soma dos `option_price`.

---

## Snapshot do cardápio

Para obter o cardápio completo de um estabelecimento em uma única chamada (bootstrap inicial ou sincronização completa), use:

```
GET /merchants/{merchantId}/menus/{menuId}/snapshot
```

O snapshot retorna menu, categorias, item-offers, option-groups e options em uma estrutura hierárquica única. Esta é a operação recomendada para onboarding e reconciliação.

Para atualizações incrementais, use os endpoints granulares de cada entidade.

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

---

## Autorização

Todas as operações da capability Merchant exigem autenticação Bearer (OAuth 2.0).

Escopos mínimos recomendados:

| Escopo | Operações |
|---|---|
| `merchant.read` | Leitura de dados do estabelecimento e catálogo |
| `merchant.write` | Criação e atualização de entidades do catálogo |
| `merchant.events.write` | Emissão de eventos de mudança |

---

## Regras normativas

**O Software Service DEVE:**

- Expor `merchantId` como identificador único e estável gerado pela Ordering Application
- Preservar integridade referencial entre menu, categorias, item-offers, option-groups e opções em todas as operações de atualização
- Retornar `202 Accepted` para todas as mutações (PATCH, PUT, DELETE com efeito assíncrono)
- Declarar `quantity_available` apenas quando há limitação operacional real

**A Ordering Application DEVE:**

- Gerar o `merchantId` antes do cadastro e mantê-lo estável
- Tratar `quantity_available` como uma dica operacional, não como garantia de estoque
- Consultar o snapshot para bootstrap e usar endpoints granulares para deltas

**Ambos DEVEM:**

- Declarar a capability `merchant` no discovery antes de iniciar operações
- Usar `option_price: { value: 0, currency: "..." }` explicitamente para opções sem custo adicional

---

**Referência completa de campos e contratos REST:** [Referência da API — Merchant →](../reference/merchant.md)

---

<div class="od-next-step">
  <div class="od-next-step__label">Próximo passo</div>
  <div class="od-next-step__links">
    <a href="../reference/merchant/">Abrir referência OpenAPI</a>
    <a href="discovery/">Configurar Discovery</a>
  </div>
</div>
