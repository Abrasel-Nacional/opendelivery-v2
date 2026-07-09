# Migração V1 → V2

<div class="od-api-callout">
  <p>Migração V1→V2. Continue a jornada ou abra o contrato técnico.</p>
  <a href="../protocol/discovery/">Discovery V2 →</a>
</div>

Este guia descreve as mudanças entre o Open Delivery Protocol V1 e V2, focando nos breaking changes
que exigem adaptação de código. Consulte o [Changelog](changelog.md) para a lista completa de novidades.

!!! info "V1 continua ativa"
    A V1 permanece ativa durante o período de transição. Não há prazo de descontinuação definido ainda.
    Novas integrações devem usar V2.

---

## 1. Autenticação — por aplicação em vez de por loja

**V1:** Um par `client_id` / `client_secret` por loja. Cada novo merchant exigia novas credenciais.

**V2:** Um único `client_id` por aplicação, independente de quantas lojas ela integra.

```diff
# V1 — token por loja
POST /oauth/token
- client_id=credencial_da_loja_123
- client_secret=segredo_da_loja_123

# V2 — token por aplicação
POST /oauth/token
+ client_id=credencial_da_aplicacao
+ client_secret=segredo_da_aplicacao
+ scope=od.orders od.menu
```

A lista de lojas autorizadas para a aplicação é obtida via:

```
GET /merchants
Authorization: Bearer {token_da_aplicacao}
```

**Compatibilidade V1:** O modelo `by_merchant` (um `client_id` por loja) ainda é suportado na V2 para
facilitar a migração gradual. Declare `clientIdGeneration: [by_merchant]` no Discovery.

---

## 2. Escopos OAuth

**V1:** Escopo único `OD.ALL` (ou sem escopo explícito).

**V2:** Escopos granulares por domínio.

| Escopo | Acesso |
|---|---|
| `od.orders` | Ciclo de vida de pedidos |
| `od.menu` | Cardápio e dados do merchant |
| `od.logistics` | Operações de logística |
| `od.crm` | Customer, fidelidade e reviews |
| `od.all` | Todos os domínios (compatibilidade V1) |

---

## 3. Merchant ID — gerado pelo originador

**V1:** O PDV gerava o `merchantId` e o comunicava ao originador.

**V2:** O originador gera o `merchantId`. O PDV mantém seu próprio identificador interno e
usa o campo `externalCode` para correlacionar os dois sistemas.

```diff
# V1 — PDV define o ID
{
-  "merchant": { "id": "id_gerado_pelo_pdv" }
}

# V2 — originador define o ID; PDV tem seu próprio código
{
+  "merchant": {
+    "id": "id_gerado_pelo_originador",
+    "externalCode": "codigo_interno_do_pdv"
+  }
}
```

---

## 4. Cardápio — CRUD granular substituiu webhook monolítico

**V1:** Toda atualização de cardápio era enviada via webhook `merchantUpdate` com o payload completo.

**V2:** Cada entidade tem seu próprio endpoint CRUD. Não existe mais o `merchantUpdate` monolítico.

| Entidade | Endpoints V2 |
|---|---|
| Merchant (basic info) | `GET /merchants/{id}` · `PATCH /merchants/{id}` |
| Services | `GET/PUT/PATCH /merchants/{id}/services/{type}` |
| Menus | `GET /merchants/{id}/menus` |
| Categorias | `GET/POST/PUT/DELETE /merchants/{id}/menus/{menuId}/categories` |
| ItemOffers | `GET/POST/PUT/DELETE /merchants/{id}/menus/{menuId}/item-offers` |
| OptionGroups | `GET/POST/PUT/DELETE .../item-offers/{id}/option-groups` |
| Options | `GET/POST/PUT/DELETE .../option-groups/{id}/options` |
| Snapshot completo | `GET /merchants/{id}/menus/{menuId}/snapshot` |
| Pausa de serviço | `POST /merchants/{id}/services/{type}/pause` |

### Campos alterados no cardápio

| Campo | V1 | V2 |
|---|---|---|
| `merchantType` | Existia | **Removido** |
| `subtotal` em opcionais | Existia | **Removido** — use `option_price` |
| `option_price` | Opcional | **Obrigatório** |
| `unity_price` | Implícito | **Explícito** |
| `quantity_available` | Não existia | **Novo** — disponibilidade operacional do item |
| Service ID | Identificado por ID | **Identificado apenas por tipo** (`DELIVERY`, `TAKEOUT`, `INDOOR`) |

---

## 5. Pedidos — cancelamento e eventos

### Cancelamento simplificado

**V1:** Handshake de três etapas: `requestCancellation` → `acceptCancellation` / `denyCancellation`.

**V2:** Cancelamento direto, sem handshake obrigatório.

```diff
# V1
POST /v1/orders/{id}/requestCancellation
POST /v1/orders/{id}/acceptCancellation   # ou denyCancellation

# V2
POST /orders/{id}/cancel
```

O handshake foi eliminado porque, na prática da V1, o deny nunca era implementado em escala.

### Evento `picked_up` removido

O evento `picked_up` era ambíguo (usado tanto para takeout quanto para coleta logística) e foi removido.
Use os eventos de logística para rastreamento de coleta.

### Separação status / evento

**V1:** Eventos e status eram frequentemente confundidos.

**V2:** Regra clara:
- `status` no `GET /orders/{id}` → estado atual do pedido (fonte de verdade)
- Eventos (webhooks) → informativos; não redefinem o estado

Nunca infira o status de um pedido apenas pelos eventos recebidos. Sempre consulte o GET para reconciliação.

---

## 6. Discovery Well-Known — agora obrigatório

**V1:** Discovery era opcional e pouco utilizado.

**V2:** `GET /.well-known/opendelivery` é **obrigatório** antes de qualquer integração.

Sem o endpoint de Discovery publicado e acessível, a integração não pode ser estabelecida.

---

## 7. Módulos novos — não existiam na V1

### Customer / CRM

Entidade de cliente com identificação flexível (tipo + valor: CPF, e-mail, telefone).
Reviews com escalas abertas (estrelas, NPS, like/dislike). Leads com estrutura mínima.

### Fidelidade

Programa de fidelidade como entidade principal. Pontos, cashback, cupons e catálogo de recompensas.
Múltiplos programas por loja, rede ou franquia.

### Indoor / Salão

Conta como entidade central que agrega pedidos, pagamentos e fiscal. Modos: mesa, comanda, balcão.
Suporte a pagamento parcial, transferência de itens e fechamento com emissão fiscal assíncrona.

---

## Checklist de migração

- [ ] Atualizar mecanismo de autenticação para `by_app` (ou declarar `by_merchant` para compatibilidade)
- [ ] Adicionar escopos ao token request
- [ ] Publicar endpoint `/.well-known/opendelivery` com capabilities corretas
- [ ] Atualizar geração de `merchantId` (originador passa a gerar)
- [ ] Substituir `merchantUpdate` pelo CRUD granular de cardápio
- [ ] Remover lógica de `requestCancellation` / `acceptCancellation` / `denyCancellation`
- [ ] Remover emissão e consumo do evento `picked_up`
- [ ] Atualizar campos do cardápio: remover `subtotal`, tornar `option_price` obrigatório
- [ ] Remover `merchantType` dos payloads
