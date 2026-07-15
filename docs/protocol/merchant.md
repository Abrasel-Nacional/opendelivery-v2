# Merchant

<p class="od-meta">
 <span class="od-badge od-badge--core">Capability</span>
 <span class="od-badge od-badge--code">merchant</span>
</p>

!!! note "Especificação da API"
    O contrato implementável (endpoints, campos, erros e exemplos) está na **[especificação de Merchant](../reference/merchant.md)** — somente em inglês.

Esta página é a **visão geral** da capability: o que muda na V2, papéis e como a documentação se divide. Detalhe de loja e cardápio está nas páginas filhas.

---

## Para que serve

A capability **Merchant** define como o ecossistema troca o **estabelecimento** e o que ele oferece: identidade da loja, contextos de serviço (delivery, takeout, indoor) e **catálogo**.

É a fonte de verdade para dados estáticos e operacionais do merchant no Open Delivery — **sem** cobrir pedidos, logística ou CRM.

Merchant **não exige** Orders. Pode ser implementada sozinha (só loja/cardápio). O stack completo costuma combinar Merchant + Orders; **Indoor** exige Orders à parte.

---

## O que muda da V1 para a V2

!!! important "Breaking — leia antes de migrar"
    Este é o domínio com **mais mudanças** em relação à V1. Detalhe também no [guia de migração](../guide/migration-v1-v2.md).

| Tema | V1 | V2 |
|---|---|---|
| **Merchant ID** | Gerado pelo PDV | Gerado pela **Ordering Application**; PDV usa `externalCode` |
| **Cardápio** | Webhook monolítico `merchantUpdate` | **CRUD por entidade** + snapshot |
| **Service** | Identificado por id de serviço | Identificado por **tipo** (`DELIVERY` / `TAKEOUT` / `INDOOR`) |
| **`merchantType`** | Presente | **Removido** |
| **Preços de opção** | `option_price` opcional; `subtotal` confuso | **`option_price` obrigatório** (0 se grátis); sem `subtotal` |
| **`unity_price`** | Implícito | **Explícito** (unidades menores) |
| **Disponibilidade** | Não padronizada | **`quantity_available`** (sinal operacional) |
| **Pausa** | Ad-hoc | **`POST …/services/{type}/pause`** sem reescrever horários |

---

## Como a documentação se organiza

A capability `merchant` no Discovery é **uma só**. Na documentação ela se divide para leitura:

| Página | Conteúdo |
|---|---|
| **Merchant** (esta) | Conceito, V1→V2, papéis, discovery, mapa de ops |
| **[Dados da Loja](merchant-store.md)** | Merchant ID, identidade, `Service`, horários, área, pause |
| **[Menus](menu.md)** | Hierarquia, ItemOffer, opcionais, snapshot, sync |

```
Merchant (capability)
├── Dados da Loja → identidade + services
└── Menus → catálogo (CRUD + snapshot)
```

!!! note "Não são extensões do protocolo"
    **Dados da Loja** e **Menus** são módulos de documentação. A extensão formal **Indoor** se declara no Discovery junto de Orders; o cardápio **não** — faz parte de `merchant`.

---

## Papéis

| Papel | Responsabilidade |
|---|---|
| **Software Service** | Fonte operacional da loja e, em geral, **host** do catálogo e dos services. |
| **Ordering Application** | **Gera** o `merchantId`, consome loja/catálogo, monta a experiência de pedido. |
| **Delivery Platform** (opcional) | Consome disponibilidade / área de entrega quando necessário. |

Em integrações típicas, a Ordering Application é **cliente** e o Software Service é **servidor** dos endpoints desta capability.

---

## Mapa: objetivo → página → operação

| Objetivo | Página | Operação (spec) |
|---|---|---|
| Listar lojas do app | — | `listMerchants` |
| Ler / atualizar dados da loja | [Dados da Loja](merchant-store.md) | `getMerchant` · `updateMerchant` |
| Configurar service / pause | [Dados da Loja](merchant-store.md) | `getService` · `replaceService` · `updateService` · `pauseService` |
| Bootstrap do cardápio | [Menus](menu.md) | `getMenuSnapshot` |
| CRUD de item / opção | [Menus](menu.md) | `createItemOffer` · `createOption` · … |

Contrato completo: [especificação Merchant](../reference/merchant.md).

---

## Discovery

```json
"capabilities": {
  "merchant": {
    "endpoint": "https://api.example.com/od/v2",
    "supportedOperations": ["getMerchant", "getMenuSnapshot", "pauseService"]
  }
}
```

Loja e menus na **mesma** capability — sem chave de extensão para catálogo. Guia: [Discovery](discovery.md).

---

## Autorização

Bearer OAuth 2.0. Escopo preferido: `od.menu` (ou escopos equivalentes declarados no manifesto). Ver [Autenticação](authentication.md).

---

## O que não cobre

| Tema | Onde |
|---|---|
| Ciclo de vida de pedidos | [Orders](orders.md) |
| Conta de salão | [Indoor](indoor.md) (exige Orders) |
| Entrega | [Logistics](logistics.md) |
| Dados do cliente (Customer) | [Customer](customer.md) |

---

## Fora do MVP

| Tema | Status |
|---|---|
| Webhook de delta de cardápio (substituto fino do `merchantUpdate`) | Não normativo no core V2 — use snapshot + CRUD |
| Custom fields / key-value livres no merchant | Fora do MVP (comitê) |
| Estoque multi-canal | Fora de escopo; `quantity_available` é só sinal operacional |

---

<div class="od-related">
  <p class="od-related__label">Relacionado</p>
  <ul class="od-related__list">
    <li><a href="../reference/merchant.md">Especificação de Merchant</a></li>
    <li><a href="merchant-store.md">Dados da Loja</a></li>
    <li><a href="menu.md">Menus</a></li>
    <li><a href="../guide/migration-v1-v2.md">Migração V1→V2</a></li>
    <li><a href="discovery.md">Discovery</a></li>
  </ul>
</div>
